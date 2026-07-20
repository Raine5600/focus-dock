import { AFFILIATES, COMMISSION_RATE, getAffiliate } from "./affiliates";
import type { PurchaseRecord } from "./purchases";

export type AffiliateRow = {
  code: string;
  name: string;
  registered: boolean;
  clicks: number;
  sales: number;
  revenue: number; // cents
  commission: number; // cents owed at COMMISSION_RATE
  conversion: number | null; // sales / clicks, null when no clicks
};

export type DailyPoint = {
  date: string; // YYYY-MM-DD
  label: string; // "Jul 19"
  revenue: number; // cents
  sales: number;
};

export type Analytics = {
  totalRevenue: number;
  totalSales: number;
  totalClicks: number;
  affiliateSales: number;
  organicSales: number;
  conversion: number | null;
  affiliates: AffiliateRow[];
  daily: DailyPoint[];
};

const DAY_MS = 24 * 60 * 60 * 1000;

export function buildAnalytics(
  purchases: PurchaseRecord[],
  clicks: Record<string, number>,
  days = 14,
  now = Date.now()
): Analytics {
  const paid = purchases.filter((p) => p.paymentStatus === "paid");

  const byCode = new Map<string, { sales: number; revenue: number }>();
  for (const p of paid) {
    if (!p.affiliateRef) continue;
    const cur = byCode.get(p.affiliateRef) ?? { sales: 0, revenue: 0 };
    cur.sales += 1;
    cur.revenue += p.amount;
    byCode.set(p.affiliateRef, cur);
  }

  // Every registered affiliate appears (even at zero); unregistered codes
  // that produced clicks or sales appear flagged so a typo never hides money.
  const codes = new Set<string>([
    ...AFFILIATES.map((a) => a.code),
    ...Object.keys(clicks),
    ...byCode.keys(),
  ]);

  const affiliates: AffiliateRow[] = [...codes]
    .map((code) => {
      const reg = getAffiliate(code);
      const perf = byCode.get(code) ?? { sales: 0, revenue: 0 };
      const clickCount = clicks[code] ?? 0;
      return {
        code,
        name: reg?.name ?? code,
        registered: Boolean(reg),
        clicks: clickCount,
        sales: perf.sales,
        revenue: perf.revenue,
        commission: Math.round(perf.revenue * COMMISSION_RATE),
        conversion: clickCount > 0 ? perf.sales / clickCount : null,
      };
    })
    .sort((a, b) => b.revenue - a.revenue || b.clicks - a.clicks);

  const daily: DailyPoint[] = [];
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(now - i * DAY_MS);
    const key = d.toISOString().slice(0, 10);
    daily.push({
      date: key,
      label: d.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
      revenue: 0,
      sales: 0,
    });
  }
  const dayIndex = new Map(daily.map((p, i) => [p.date, i]));
  for (const p of paid) {
    const idx = dayIndex.get(p.purchasedAt.slice(0, 10));
    if (idx !== undefined) {
      daily[idx].revenue += p.amount;
      daily[idx].sales += 1;
    }
  }

  const totalRevenue = paid.reduce((s, p) => s + p.amount, 0);
  const affiliateSales = [...byCode.values()].reduce((s, v) => s + v.sales, 0);
  const totalClicks = Object.values(clicks).reduce((s, n) => s + n, 0);

  return {
    totalRevenue,
    totalSales: paid.length,
    totalClicks,
    affiliateSales,
    organicSales: paid.length - affiliateSales,
    conversion: totalClicks > 0 ? affiliateSales / totalClicks : null,
    affiliates,
    daily,
  };
}

export function pct(n: number | null): string {
  if (n === null) return "—";
  return `${(n * 100).toFixed(1)}%`;
}
