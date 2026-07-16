import { list, put } from "@vercel/blob";

/** Cookie that persists affiliate attribution across the session. */
export const AFFILIATE_COOKIE = "fd_ref";
/** Last-touch attribution window: 30 days. */
export const AFFILIATE_COOKIE_MAX_AGE = 60 * 60 * 24 * 30;
/** Commission owed to affiliates per sale. */
export const COMMISSION_RATE = 0.4;

export type Affiliate = {
  code: string;
  name: string;
  notes?: string;
};

/**
 * Registered affiliate codes. Add a row per partner — the link is
 * https://<domain>/a/<code>. Unknown codes still track (they show as
 * "unregistered" in admin) so a typo never loses a sale.
 */
export const AFFILIATES: Affiliate[] = [
  { code: "launch", name: "Launch promos", notes: "Your own posts/newsletter" },
  { code: "partner-01", name: "Unassigned slot 1" },
  { code: "partner-02", name: "Unassigned slot 2" },
  { code: "partner-03", name: "Unassigned slot 3" },
  { code: "partner-04", name: "Unassigned slot 4" },
  { code: "partner-05", name: "Unassigned slot 5" },
];

/** Lowercase slug, strip anything unexpected, cap length. */
export function normalizeRef(raw: string | null | undefined): string | null {
  if (!raw) return null;
  const code = raw
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, "")
    .slice(0, 40);
  return code.length > 0 ? code : null;
}

export function getAffiliate(code: string): Affiliate | undefined {
  return AFFILIATES.find((a) => a.code === code);
}

export function affiliateLink(code: string, baseUrl: string): string {
  return `${baseUrl.replace(/\/$/, "")}/a/${code}`;
}

/** Fire-and-forget click log (one small blob per click). */
export async function logAffiliateClick(code: string): Promise<void> {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return;
  try {
    await put(
      `affiliate-clicks/${code}/click.json`,
      JSON.stringify({ code, at: new Date().toISOString() }),
      {
        access: "private",
        contentType: "application/json",
        addRandomSuffix: true,
      }
    );
  } catch (err) {
    console.error("[affiliate] click log failed:", err);
  }
}

/** Click counts per affiliate code, from blob pathnames (no downloads needed). */
export async function getAffiliateClicks(): Promise<Record<string, number>> {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return {};
  const counts: Record<string, number> = {};
  try {
    let cursor: string | undefined;
    do {
      const page = await list({ prefix: "affiliate-clicks/", cursor });
      for (const blob of page.blobs) {
        const code = blob.pathname.split("/")[1];
        if (code) counts[code] = (counts[code] ?? 0) + 1;
      }
      cursor = page.cursor ?? undefined;
    } while (cursor);
  } catch (err) {
    console.error("[affiliate] click list failed:", err);
  }
  return counts;
}
