import { list, put } from "@vercel/blob";
import type { Analytics } from "./analytics";
import { fetchBlobJson } from "./blob";
import type { TrafficStats } from "./traffic";
import { formatAmount } from "./purchases";
import { pct } from "./analytics";

export type Insight = {
  text: string;
  generatedAt: string;
  source: "claude" | "rules";
};

const CACHE_PATH = "insights/summary.json";
const CACHE_TTL_MS = 6 * 60 * 60 * 1000; // regenerate at most every 6h

function statsDigest(t: TrafficStats, a: Analytics): string {
  return JSON.stringify([
    t.pageviews,
    t.visitors,
    t.checkoutClicks,
    a.totalSales,
    a.totalClicks,
  ]);
}

/** Deterministic fallback summary — used when no ANTHROPIC_API_KEY is set. */
function ruleBasedSummary(t: TrafficStats, a: Analytics): string {
  if (t.visitors === 0) {
    return (
      "No visitor data yet — the tracker starts collecting the moment this deploy goes live. " +
      "Once people visit, this summary will describe where they come from, what they read, and how often they reach checkout."
    );
  }
  const parts: string[] = [];
  parts.push(
    `Over the last ${t.days} days the site had ${t.visitors} visitor${t.visitors === 1 ? "" : "s"} and ${t.pageviews} pageviews` +
      (t.pagesPerVisitor
        ? ` — about ${t.pagesPerVisitor.toFixed(1)} pages per visit.`
        : ".")
  );
  if (t.topSources.length > 0) {
    const [src, n] = t.topSources[0];
    parts.push(
      `The biggest traffic source is ${src} (${n} visitor${n === 1 ? "" : "s"}).`
    );
  }
  if (t.checkoutClicks > 0) {
    parts.push(
      `${t.checkoutClicks} checkout click${t.checkoutClicks === 1 ? "" : "s"} so far (${pct(t.checkoutCtr)} of visitors), leading to ${a.totalSales} completed sale${a.totalSales === 1 ? "" : "s"}.`
    );
  } else {
    parts.push("No visitor has clicked checkout yet.");
  }
  const { mobile, desktop } = t.deviceSplit;
  if (mobile + desktop > 0) {
    parts.push(
      `${Math.round((mobile / (mobile + desktop)) * 100)}% of views are on mobile.`
    );
  }
  return parts.join(" ");
}

async function readCache(): Promise<(Insight & { digest?: string }) | null> {
  try {
    const { blobs } = await list({ prefix: CACHE_PATH });
    const hit = blobs.find((b) => b.pathname === CACHE_PATH);
    if (!hit) return null;
    return await fetchBlobJson<Insight & { digest?: string }>(hit.url);
  } catch {
    return null;
  }
}

async function claudeSummary(
  t: TrafficStats,
  a: Analytics
): Promise<string | null> {
  const { default: Anthropic } = await import("@anthropic-ai/sdk");
  const client = new Anthropic();

  const data = {
    windowDays: t.days,
    visitors: t.visitors,
    pageviews: t.pageviews,
    pagesPerVisitor: t.pagesPerVisitor,
    checkoutClicks: t.checkoutClicks,
    checkoutClickRate: t.checkoutCtr,
    topPages: t.topPages,
    topSources: t.topSources,
    topCountries: t.topCountries,
    deviceSplit: t.deviceSplit,
    dailyTraffic: t.daily,
    sales: {
      total: a.totalSales,
      revenue: formatAmount(a.totalRevenue, "usd"),
      viaAffiliates: a.affiliateSales,
      affiliateClicks: a.totalClicks,
      byAffiliate: a.affiliates.map((r) => ({
        code: r.code,
        clicks: r.clicks,
        sales: r.sales,
      })),
    },
  };

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 600,
    system:
      "You are the analytics assistant for Focus Dock, a one-product site selling a $27 ADHD Notion guide PDF. " +
      "Given traffic and sales stats, write a plain-English summary for the founder: what visitors typically do on the site, " +
      "where they come from, how behavior converts toward checkout, and the single most actionable observation. " +
      "4-6 sentences, no headings, no bullet lists, no flattery, no hedging boilerplate. " +
      "If the numbers are small, say so plainly and avoid over-interpreting.",
    messages: [
      {
        role: "user",
        content: `Stats for the last ${t.days} days:\n${JSON.stringify(data, null, 2)}`,
      },
    ],
  });

  const text = response.content
    .filter((b): b is Extract<typeof b, { type: "text" }> => b.type === "text")
    .map((b) => b.text)
    .join("")
    .trim();
  return text.length > 0 ? text : null;
}

/**
 * Visitor-behavior summary for the dashboard. Uses Claude when
 * ANTHROPIC_API_KEY is configured (cached 6h in Blob), otherwise a
 * deterministic rule-based summary.
 */
export async function getInsight(
  t: TrafficStats,
  a: Analytics
): Promise<Insight> {
  const digest = statsDigest(t, a);

  if (!process.env.ANTHROPIC_API_KEY) {
    return {
      text: ruleBasedSummary(t, a),
      generatedAt: new Date().toISOString(),
      source: "rules",
    };
  }

  const cached = process.env.BLOB_READ_WRITE_TOKEN ? await readCache() : null;
  if (
    cached &&
    cached.digest === digest &&
    Date.now() - new Date(cached.generatedAt).getTime() < CACHE_TTL_MS
  ) {
    return cached;
  }

  try {
    const text = await claudeSummary(t, a);
    if (!text) throw new Error("empty summary");
    const insight: Insight = {
      text,
      generatedAt: new Date().toISOString(),
      source: "claude",
    };
    if (process.env.BLOB_READ_WRITE_TOKEN) {
      await put(CACHE_PATH, JSON.stringify({ ...insight, digest }), {
        access: "private",
        contentType: "application/json",
        addRandomSuffix: false,
        allowOverwrite: true,
      });
    }
    return insight;
  } catch (err) {
    console.error("[insights] Claude summary failed:", err);
    if (cached) return cached; // stale beats broken
    return {
      text: ruleBasedSummary(t, a),
      generatedAt: new Date().toISOString(),
      source: "rules",
    };
  }
}
