import { list, put } from "@vercel/blob";
import { fetchBlobJson } from "./blob";

/** Dev traffic goes to a separate prefix so local testing never pollutes prod stats. */
const PREFIX =
  process.env.NODE_ENV === "production" ? "traffic" : "traffic-dev";

export type TrafficEvent = {
  ts: string; // ISO
  sid: string; // random session id (no PII)
  ev: "pv" | "checkout_click";
  path: string;
  src: string; // derived source: direct | google | reddit | ... | affiliate:<code>
  country: string;
  device: "mobile" | "desktop";
};

export type TrafficStats = {
  days: number;
  pageviews: number;
  visitors: number;
  pagesPerVisitor: number | null;
  checkoutClicks: number;
  checkoutCtr: number | null; // clicks / visitors
  topPages: [string, number][];
  topSources: [string, number][];
  topCountries: [string, number][];
  deviceSplit: { mobile: number; desktop: number };
  daily: { date: string; label: string; pageviews: number; visitors: number }[];
  sampled: boolean; // true if we hit the read cap
};

const DAY_MS = 24 * 60 * 60 * 1000;
const MAX_EVENTS = 4000; // read cap per dashboard load

/** Derive a coarse traffic source from referrer + landing params. */
export function deriveSource(
  referrer: string | null,
  utmSource: string | null,
  affiliateRef: string | null
): string {
  if (affiliateRef) return `affiliate:${affiliateRef}`;
  if (utmSource) return utmSource.toLowerCase().slice(0, 40);
  if (!referrer) return "direct";
  try {
    const host = new URL(referrer).hostname.replace(/^www\./, "");
    if (!host) return "direct";
    if (host.includes("google.")) return "google";
    if (host.includes("bing.")) return "bing";
    if (host.includes("reddit.")) return "reddit";
    if (host === "t.co" || host.includes("twitter") || host === "x.com")
      return "x-twitter";
    if (host.includes("youtube.") || host === "youtu.be") return "youtube";
    if (host.includes("instagram.")) return "instagram";
    if (host.includes("tiktok.")) return "tiktok";
    if (host.includes("facebook.") || host === "fb.me") return "facebook";
    if (host.includes("linkedin.")) return "linkedin";
    return host.slice(0, 40);
  } catch {
    return "direct";
  }
}

export async function logTrafficEvent(event: TrafficEvent): Promise<void> {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return;
  const day = event.ts.slice(0, 10);
  try {
    await put(`${PREFIX}/${day}/e.json`, JSON.stringify(event), {
      access: "private",
      contentType: "application/json",
      addRandomSuffix: true,
    });
  } catch (err) {
    console.error("[traffic] log failed:", err);
  }
}

async function listDay(day: string): Promise<string[]> {
  const urls: string[] = [];
  let cursor: string | undefined;
  do {
    const page = await list({ prefix: `${PREFIX}/${day}/`, cursor });
    for (const blob of page.blobs) urls.push(blob.url);
    cursor = page.cursor ?? undefined;
  } while (cursor && urls.length < MAX_EVENTS);
  return urls;
}

export async function getTrafficStats(
  days = 14,
  now = Date.now()
): Promise<TrafficStats> {
  const empty: TrafficStats = {
    days,
    pageviews: 0,
    visitors: 0,
    pagesPerVisitor: null,
    checkoutClicks: 0,
    checkoutCtr: null,
    topPages: [],
    topSources: [],
    topCountries: [],
    deviceSplit: { mobile: 0, desktop: 0 },
    daily: [],
    sampled: false,
  };
  if (!process.env.BLOB_READ_WRITE_TOKEN) return empty;

  const dayKeys: string[] = [];
  for (let i = days - 1; i >= 0; i--) {
    dayKeys.push(new Date(now - i * DAY_MS).toISOString().slice(0, 10));
  }

  let urls: string[] = [];
  try {
    const perDay = await Promise.all(dayKeys.map(listDay));
    urls = perDay.flat();
  } catch (err) {
    console.error("[traffic] list failed:", err);
    return empty;
  }

  const sampled = urls.length > MAX_EVENTS;
  const events: TrafficEvent[] = (
    await Promise.all(
      urls.slice(0, MAX_EVENTS).map((url) => fetchBlobJson<TrafficEvent>(url))
    )
  ).filter((e): e is TrafficEvent => e !== null);

  const sids = new Set<string>();
  const pages = new Map<string, number>();
  const sources = new Map<string, Set<string>>(); // source -> unique sids
  const countries = new Map<string, number>();
  const device = { mobile: 0, desktop: 0 };
  const daily = new Map<
    string,
    { pageviews: number; sids: Set<string> }
  >(dayKeys.map((d) => [d, { pageviews: 0, sids: new Set() }]));
  let pageviews = 0;
  let checkoutClicks = 0;

  for (const e of events) {
    if (e.ev === "checkout_click") {
      checkoutClicks++;
      continue;
    }
    pageviews++;
    sids.add(e.sid);
    pages.set(e.path, (pages.get(e.path) ?? 0) + 1);
    if (!sources.has(e.src)) sources.set(e.src, new Set());
    sources.get(e.src)!.add(e.sid);
    if (e.country) countries.set(e.country, (countries.get(e.country) ?? 0) + 1);
    device[e.device === "mobile" ? "mobile" : "desktop"]++;
    const d = daily.get(e.ts.slice(0, 10));
    if (d) {
      d.pageviews++;
      d.sids.add(e.sid);
    }
  }

  const top = (m: Map<string, number>, n: number): [string, number][] =>
    [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, n);

  return {
    days,
    pageviews,
    visitors: sids.size,
    pagesPerVisitor: sids.size > 0 ? pageviews / sids.size : null,
    checkoutClicks,
    checkoutCtr: sids.size > 0 ? checkoutClicks / sids.size : null,
    topPages: top(pages, 6),
    topSources: [...sources.entries()]
      .map(([src, set]): [string, number] => [src, set.size])
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6),
    topCountries: top(countries, 6),
    deviceSplit: device,
    daily: dayKeys.map((date) => ({
      date,
      label: new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        timeZone: "UTC",
      }),
      pageviews: daily.get(date)?.pageviews ?? 0,
      visitors: daily.get(date)?.sids.size ?? 0,
    })),
    sampled,
  };
}
