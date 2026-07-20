import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { AdminLogin } from "@/components/AdminLogin";
import { RevenueChart } from "@/components/RevenueChart";
import { affiliateLink, getAffiliateClicks } from "@/lib/affiliates";
import { buildAnalytics, pct } from "@/lib/analytics";
import { getInsight } from "@/lib/insights";
import { getTrafficStats } from "@/lib/traffic";
import { getAppUrl } from "@/lib/stripe";
import {
  formatAmount,
  getPurchases,
  type PurchaseRecord,
} from "@/lib/purchases";
import { isAdminAuthenticated, isAdminConfigured } from "@/lib/admin";
import { buildPageMetadata } from "@/lib/seo";

export const dynamic = "force-dynamic";

export const metadata: Metadata = buildPageMetadata({
  title: "Dashboard",
  description: "Focus Dock sales and affiliate analytics.",
  path: "/admin",
  noIndex: true,
});

function StatTile({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <div className="rounded-2xl border border-border bg-white p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-wider text-ink-lt">
        {label}
      </p>
      <p className="mt-2 font-display text-3xl font-semibold text-navy-dark">
        {value}
      </p>
      {hint ? <p className="mt-1 text-xs text-ink-lt">{hint}</p> : null}
    </div>
  );
}

export default async function AdminPage() {
  if (!isAdminConfigured()) {
    return (
      <div className="mx-auto max-w-lg px-5 py-20 text-center">
        <h1 className="font-display text-2xl font-semibold text-navy-dark">
          Admin not configured
        </h1>
        <p className="mt-3 text-ink-mid">
          Set <code className="rounded bg-cream-dk px-1.5 py-0.5">ADMIN_PASSWORD</code>{" "}
          in your environment variables to view the dashboard.
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

  const [purchases, clicks, traffic] = await Promise.all([
    getPurchases(),
    getAffiliateClicks(),
    getTrafficStats(14),
  ]);
  const a = buildAnalytics(purchases, clicks);
  const insight = await getInsight(traffic, a);
  const base = getAppUrl();

  return (
    <div className="min-h-screen bg-cream">
      <header className="border-b border-border bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
          <div className="flex items-center gap-3">
            <Image
              src="/images/logo-mark.png"
              alt=""
              width={36}
              height={36}
              className="h-9 w-9"
            />
            <div>
              <h1 className="font-display text-xl font-semibold text-navy-dark">
                Dashboard
              </h1>
              <p className="text-sm text-ink-lt">
                {a.totalSales} sale{a.totalSales === 1 ? "" : "s"} ·{" "}
                {formatAmount(a.totalRevenue, "usd")} all-time
              </p>
            </div>
          </div>
          <Link href="/" className="text-sm font-medium text-sage hover:underline">
            ← Back to site
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-8 px-5 py-8 sm:px-8">
        {/* AI visitor summary */}
        <section className="rounded-2xl border border-border bg-white p-6 shadow-sm">
          <div className="flex items-baseline justify-between">
            <h2 className="font-display text-lg font-semibold text-navy-dark">
              Visitor behavior
            </h2>
            <p className="text-xs text-ink-lt">
              {insight.source === "claude"
                ? `Written by Claude · ${new Date(insight.generatedAt).toLocaleString()}`
                : "Auto summary — add ANTHROPIC_API_KEY in Vercel for Claude-written insights"}
            </p>
          </div>
          <p className="mt-3 leading-relaxed text-ink">{insight.text}</p>
        </section>

        {/* Traffic tiles */}
        <section className="grid grid-cols-2 gap-4 lg:grid-cols-4">
          <StatTile
            label="Visitors"
            value={String(traffic.visitors)}
            hint={`Last ${traffic.days} days`}
          />
          <StatTile
            label="Pageviews"
            value={String(traffic.pageviews)}
            hint={
              traffic.pagesPerVisitor
                ? `${traffic.pagesPerVisitor.toFixed(1)} pages per visit`
                : "—"
            }
          />
          <StatTile
            label="Checkout clicks"
            value={String(traffic.checkoutClicks)}
            hint={`${pct(traffic.checkoutCtr)} of visitors`}
          />
          <StatTile
            label="Devices"
            value={
              traffic.deviceSplit.mobile + traffic.deviceSplit.desktop > 0
                ? `${Math.round(
                    (traffic.deviceSplit.mobile /
                      (traffic.deviceSplit.mobile + traffic.deviceSplit.desktop)) *
                      100
                  )}% mobile`
                : "—"
            }
            hint={`${traffic.deviceSplit.mobile} mobile · ${traffic.deviceSplit.desktop} desktop`}
          />
        </section>

        {/* Where visitors go / come from */}
        <section className="grid gap-4 lg:grid-cols-3">
          {(
            [
              ["Top pages", traffic.topPages],
              ["Traffic sources", traffic.topSources],
              ["Countries", traffic.topCountries],
            ] as [string, [string, number][]][]
          ).map(([title, rows]) => (
            <div
              key={title}
              className="rounded-2xl border border-border bg-white p-5 shadow-sm"
            >
              <h3 className="font-display text-base font-semibold text-navy-dark">
                {title}
              </h3>
              {rows.length === 0 ? (
                <p className="mt-3 text-sm text-ink-lt">No data yet.</p>
              ) : (
                <ul className="mt-3 space-y-2 text-sm">
                  {rows.map(([label, n]) => (
                    <li key={label} className="flex items-center justify-between gap-3">
                      <span className="truncate text-ink-mid">{label}</span>
                      <span className="tabular-nums font-semibold text-navy-dark">
                        {n}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </section>

        {/* Stat tiles */}
        <section className="grid grid-cols-2 gap-4 lg:grid-cols-4">
          <StatTile
            label="Revenue"
            value={formatAmount(a.totalRevenue, "usd")}
            hint="All-time, paid orders"
          />
          <StatTile
            label="Sales"
            value={String(a.totalSales)}
            hint={`${a.affiliateSales} via affiliates · ${a.organicSales} direct`}
          />
          <StatTile
            label="Affiliate clicks"
            value={String(a.totalClicks)}
            hint="Tracked link visits, all-time"
          />
          <StatTile
            label="Click → sale"
            value={pct(a.conversion)}
            hint="Across all affiliate links"
          />
        </section>

        {/* Revenue chart */}
        <section className="rounded-2xl border border-border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-baseline justify-between">
            <h2 className="font-display text-lg font-semibold text-navy-dark">
              Daily revenue
            </h2>
            <p className="text-sm text-ink-lt">Last 14 days</p>
          </div>
          <RevenueChart daily={a.daily} />
        </section>

        {/* Affiliate performance */}
        <section className="overflow-hidden rounded-2xl border border-border bg-white shadow-sm">
          <div className="px-6 pb-2 pt-5">
            <div className="flex items-baseline justify-between">
              <h2 className="font-display text-lg font-semibold text-navy-dark">
                Affiliates
              </h2>
              <p className="text-sm text-ink-lt">40% commission</p>
            </div>
            <p className="mt-1 text-sm text-ink-lt">
              Clicks set a 30-day cookie; purchases attribute automatically.
              Add codes in{" "}
              <code className="rounded bg-cream-dk px-1.5 py-0.5">
                lib/affiliates.ts
              </code>
              .
            </p>
          </div>
          <div className="mt-3 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-navy-dark text-white">
                <tr>
                  <th className="px-4 py-3 font-semibold">Affiliate</th>
                  <th className="px-4 py-3 font-semibold">Link</th>
                  <th className="px-4 py-3 text-right font-semibold">Clicks</th>
                  <th className="px-4 py-3 text-right font-semibold">Sales</th>
                  <th className="px-4 py-3 text-right font-semibold">Conv.</th>
                  <th className="px-4 py-3 text-right font-semibold">Revenue</th>
                  <th className="px-4 py-3 text-right font-semibold">Owed (40%)</th>
                </tr>
              </thead>
              <tbody>
                {a.affiliates.map((row, i) => (
                  <tr
                    key={row.code}
                    className={i % 2 === 0 ? "bg-white" : "bg-cream"}
                  >
                    <td className="px-4 py-3">
                      <span className="font-semibold text-ink">{row.name}</span>
                      {!row.registered ? (
                        <span className="ml-2 rounded-full bg-yellow/25 px-2 py-0.5 text-[0.65rem] font-bold uppercase tracking-wide text-[#8a6d00]">
                          unregistered
                        </span>
                      ) : null}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-ink-mid">
                      {affiliateLink(row.code, base)}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-ink-mid">
                      {row.clicks}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-ink-mid">
                      {row.sales}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-ink-mid">
                      {pct(row.conversion)}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums font-semibold text-navy-dark">
                      {formatAmount(row.revenue, "usd")}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums font-semibold text-[#1f7a6d]">
                      {formatAmount(row.commission, "usd")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Recent purchases */}
        <section className="overflow-hidden rounded-2xl border border-border bg-white shadow-sm">
          <div className="flex items-baseline justify-between px-6 pb-2 pt-5">
            <h2 className="font-display text-lg font-semibold text-navy-dark">
              Recent purchases
            </h2>
            <p className="text-sm text-ink-lt">{purchases.length} recorded</p>
          </div>
          {purchases.length === 0 ? (
            <p className="px-6 pb-6 pt-2 text-sm text-ink-mid">
              No purchases yet. Sales appear here the moment a checkout
              completes — webhook or not.
            </p>
          ) : (
            <div className="mt-3 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-navy-dark text-white">
                  <tr>
                    <th className="px-4 py-3 font-semibold">Date</th>
                    <th className="px-4 py-3 font-semibold">Customer</th>
                    <th className="px-4 py-3 font-semibold">Email</th>
                    <th className="px-4 py-3 font-semibold">Affiliate</th>
                    <th className="px-4 py-3 text-right font-semibold">Amount</th>
                    <th className="hidden px-4 py-3 font-semibold md:table-cell">
                      Session
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {purchases.slice(0, 50).map((p: PurchaseRecord, i) => (
                    <tr
                      key={p.id}
                      className={i % 2 === 0 ? "bg-white" : "bg-cream"}
                    >
                      <td className="px-4 py-3 text-ink-mid">
                        {new Date(p.purchasedAt).toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-ink">
                        {p.customerName ?? "—"}
                      </td>
                      <td className="px-4 py-3 text-ink">{p.email ?? "—"}</td>
                      <td className="px-4 py-3 text-ink-mid">
                        {p.affiliateRef ?? "direct"}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums font-semibold text-navy-dark">
                        {formatAmount(p.amount, p.currency)}
                      </td>
                      <td className="hidden px-4 py-3 font-mono text-xs text-ink-lt md:table-cell">
                        {p.id}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
