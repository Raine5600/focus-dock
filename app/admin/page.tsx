import type { Metadata } from "next";
import Link from "next/link";
import { AdminLogin } from "@/components/AdminLogin";
import {
  formatAmount,
  getPurchases,
  type PurchaseRecord,
} from "@/lib/purchases";
import {
  AFFILIATES,
  COMMISSION_RATE,
  affiliateLink,
  getAffiliate,
  getAffiliateClicks,
} from "@/lib/affiliates";
import { getAppUrl } from "@/lib/stripe";
import { isAdminAuthenticated, isAdminConfigured } from "@/lib/admin";
import { buildPageMetadata } from "@/lib/seo";

type AffiliateRow = {
  code: string;
  name: string;
  link: string;
  clicks: number;
  sales: number;
  revenue: number;
  commission: number;
  registered: boolean;
};

function buildAffiliateRows(
  purchases: PurchaseRecord[],
  clicks: Record<string, number>
): AffiliateRow[] {
  const codes = new Set<string>([
    ...AFFILIATES.map((a) => a.code),
    ...Object.keys(clicks),
    ...purchases
      .map((p) => p.affiliateRef)
      .filter((r): r is string => Boolean(r)),
  ]);

  const base = getAppUrl();
  return [...codes]
    .map((code) => {
      const sold = purchases.filter((p) => p.affiliateRef === code);
      const revenue = sold.reduce((sum, p) => sum + p.amount, 0);
      const affiliate = getAffiliate(code);
      return {
        code,
        name: affiliate?.name ?? "Unregistered code",
        link: affiliateLink(code, base),
        clicks: clicks[code] ?? 0,
        sales: sold.length,
        revenue,
        commission: Math.round(revenue * COMMISSION_RATE),
        registered: Boolean(affiliate),
      };
    })
    .sort((a, b) => b.revenue - a.revenue || b.clicks - a.clicks);
}

export const dynamic = "force-dynamic";

export const metadata: Metadata = buildPageMetadata({
  title: "Admin",
  description: "Focus Dock purchase log.",
  path: "/admin",
  noIndex: true,
});

export default async function AdminPage() {
  if (!isAdminConfigured()) {
    return (
      <div className="mx-auto max-w-lg px-5 py-20 text-center">
        <h1 className="font-display text-2xl font-semibold text-navy-dark">
          Admin not configured
        </h1>
        <p className="mt-3 text-ink-mid">
          Set <code className="rounded bg-cream-dk px-1.5 py-0.5">ADMIN_PASSWORD</code>{" "}
          in your environment variables to view purchase logs.
        </p>
      </div>
    );
  }

  const authed = await isAdminAuthenticated();
  if (!authed) {
    return (
      <div className="min-h-screen bg-cream px-5 py-20">
        <AdminLogin />
      </div>
    );
  }

  const purchases = await getPurchases();
  const clicks = await getAffiliateClicks();
  const affiliateRows = buildAffiliateRows(purchases, clicks);
  const usingBlob = Boolean(process.env.BLOB_READ_WRITE_TOKEN);

  return (
    <div className="min-h-screen bg-cream">
      <header className="border-b border-border bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
          <div>
            <h1 className="font-display text-xl font-semibold text-navy-dark">
              Purchase log
            </h1>
            <p className="text-sm text-ink-lt">
              {purchases.length} recorded sale{purchases.length === 1 ? "" : "s"}
              {usingBlob ? " · stored via webhook" : " · from Stripe API"}
            </p>
          </div>
          <Link href="/" className="text-sm font-medium text-sage hover:underline">
            ← Back to site
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-5 py-8 sm:px-8">
        {!usingBlob ? (
          <p className="mb-6 rounded-xl border border-amber/30 bg-[#fdf6e3] px-4 py-3 text-sm text-ink-mid">
            Add <strong>BLOB_READ_WRITE_TOKEN</strong> in Vercel Storage for
            persistent webhook logs. Until then, this page reads from Stripe
            directly.
          </p>
        ) : null}

        <section className="mb-10">
          <h2 className="font-display text-lg font-semibold text-navy-dark">
            Affiliate links
          </h2>
          <p className="mt-1 text-sm text-ink-lt">
            Give a partner their link below. Clicks set a 30-day cookie;
            purchases attribute automatically. Commission rate:{" "}
            {Math.round(COMMISSION_RATE * 100)}%. Edit codes in{" "}
            <code className="rounded bg-cream-dk px-1.5 py-0.5">
              lib/affiliates.ts
            </code>
            .
          </p>
          <div className="mt-4 overflow-x-auto rounded-2xl border border-border bg-white shadow-sm">
            <table className="w-full text-left text-sm">
              <thead className="bg-navy-dark text-white">
                <tr>
                  <th className="px-4 py-3 font-semibold">Partner</th>
                  <th className="px-4 py-3 font-semibold">Link</th>
                  <th className="px-4 py-3 text-right font-semibold">Clicks</th>
                  <th className="px-4 py-3 text-right font-semibold">Sales</th>
                  <th className="px-4 py-3 text-right font-semibold">Revenue</th>
                  <th className="px-4 py-3 text-right font-semibold">
                    Commission owed
                  </th>
                </tr>
              </thead>
              <tbody>
                {affiliateRows.map((row, i) => (
                  <tr
                    key={row.code}
                    className={i % 2 === 0 ? "bg-white" : "bg-cream"}
                  >
                    <td className="px-4 py-3">
                      <span className="font-medium text-ink">{row.name}</span>
                      {!row.registered ? (
                        <span className="ml-2 rounded-full bg-yellow/30 px-2 py-0.5 text-xs font-semibold text-ink-mid">
                          unregistered
                        </span>
                      ) : null}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-ink-mid">
                      {row.link}
                    </td>
                    <td className="px-4 py-3 text-right text-ink-mid">
                      {row.clicks}
                    </td>
                    <td className="px-4 py-3 text-right text-ink-mid">
                      {row.sales}
                    </td>
                    <td className="px-4 py-3 text-right font-semibold text-navy-dark">
                      {formatAmount(row.revenue, "usd")}
                    </td>
                    <td className="px-4 py-3 text-right font-semibold text-coral">
                      {formatAmount(row.commission, "usd")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {purchases.length === 0 ? (
          <div className="rounded-2xl border border-border bg-white p-10 text-center">
            <p className="text-ink-mid">No purchases logged yet.</p>
            <p className="mt-2 text-sm text-ink-lt">
              Sales appear here after Stripe sends a{" "}
              <code className="rounded bg-cream px-1">checkout.session.completed</code>{" "}
              webhook event.
            </p>
          </div>
        ) : (
          <div className="overflow-hidden rounded-2xl border border-border bg-white shadow-sm">
            <table className="w-full text-left text-sm">
              <thead className="bg-navy-dark text-white">
                <tr>
                  <th className="px-4 py-3 font-semibold">Date</th>
                  <th className="px-4 py-3 font-semibold">Customer</th>
                  <th className="px-4 py-3 font-semibold">Email</th>
                  <th className="px-4 py-3 font-semibold">Amount</th>
                  <th className="px-4 py-3 font-semibold">Ref</th>
                  <th className="hidden px-4 py-3 font-semibold md:table-cell">
                    Session
                  </th>
                </tr>
              </thead>
              <tbody>
                {purchases.map((purchase: PurchaseRecord, i) => (
                  <tr
                    key={purchase.id}
                    className={i % 2 === 0 ? "bg-white" : "bg-cream"}
                  >
                    <td className="px-4 py-3 text-ink-mid">
                      {new Date(purchase.purchasedAt).toLocaleString()}
                    </td>
                    <td className="px-4 py-3 text-ink">
                      {purchase.customerName ?? "—"}
                    </td>
                    <td className="px-4 py-3 text-ink">
                      {purchase.email ?? "—"}
                    </td>
                    <td className="px-4 py-3 font-semibold text-navy-dark">
                      {formatAmount(purchase.amount, purchase.currency)}
                    </td>
                    <td className="px-4 py-3 text-ink-mid">
                      {purchase.affiliateRef ?? "—"}
                    </td>
                    <td className="hidden px-4 py-3 font-mono text-xs text-ink-lt md:table-cell">
                      {purchase.id}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}