import { PACKAGE_ITEMS } from "@/lib/product";

const accentMap: Record<string, string> = {
  navy: "bg-navy text-white",
  coral: "bg-coral text-white",
  mint: "bg-mint text-navy-dark",
  amber: "bg-yellow text-navy-dark",
};

export function WhatsIncluded() {
  return (
    <section id="included" className="py-20">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-start">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-mint">
              29-page guide
            </p>
            <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
              Everything in one PDF
            </h2>
            <p className="mt-4 text-lg text-ink-mid">
              High-contrast, ADHD-friendly layout. No blank space, no fluff.
              Copy-paste Notion formulas. Read on your phone or print the
              emergency card for your monitor.
            </p>
            <div className="mt-8 rounded-2xl border-2 border-coral bg-coral-lt p-6">
              <p className="font-display text-lg font-semibold text-navy-dark">
                The 3-Database Recovery Protocol
              </p>
              <ul className="mt-4 space-y-2 text-sm text-ink-mid">
                <li>
                  <strong className="text-navy">Brain Dump</strong> — 2-second
                  capture, no tags
                </li>
                <li>
                  <strong className="text-navy">Today</strong> — one sequence
                  step visible; keep 1–3 parallel tasks max
                </li>
                <li>
                  <strong className="text-navy">Projects</strong> — parking lot,
                  Sunday only
                </li>
              </ul>
              <div className="mt-4 rounded-xl border border-navy/15 bg-white/80 p-4">
                <p className="text-sm font-semibold text-navy-dark">
                  Deletion protocol included
                </p>
                <p className="mt-1 text-sm leading-relaxed text-ink-mid">
                  Step one isn&apos;t adding — it&apos;s ripping out habit
                  trackers, streak counters, mood logs, and guilt dashboards
                  before you build the 3-database system.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            {PACKAGE_ITEMS.map((item) => (
              <article
                key={item.num}
                className="flex gap-4 rounded-2xl border border-border bg-white p-5 shadow-sm transition hover:border-mint/40"
              >
                <span
                  className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-sm font-bold ${accentMap[item.accent]}`}
                >
                  {item.num}
                </span>
                <div>
                  <h3 className="font-display text-lg font-semibold text-navy-dark">
                    {item.title}
                  </h3>
                  <p className="mt-1 text-sm leading-relaxed text-ink-mid">
                    {item.description}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}