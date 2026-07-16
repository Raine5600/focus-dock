import { PACKAGE_ITEMS, PRODUCT } from "@/lib/product";
import { Reveal, Stagger, StaggerItem } from "./motion";

const ACCENTS: Record<string, string> = {
  navy: "bg-navy text-white",
  coral: "bg-coral text-white",
  mint: "bg-mint text-navy-dark",
  amber: "bg-yellow text-navy-dark",
};

export function WhatsIncluded() {
  return (
    <section className="bg-cream py-20 sm:py-24" id="included">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            What&apos;s included
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            Everything you need. Nothing you&apos;ll abandon.
          </h2>
          <p className="mt-4 text-lg text-ink-mid">
            One {PRODUCT.pages}-page PDF + a copy-paste formulas file. Built to
            be used, not admired.
          </p>
        </Reveal>

        <Stagger className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PACKAGE_ITEMS.map((item, i) => (
            <StaggerItem
              key={item.num}
              className={i === 0 ? "sm:col-span-2 lg:col-span-1" : undefined}
            >
              <article className="h-full rounded-2xl border border-border bg-white p-6 shadow-sm transition-shadow hover:shadow-md">
                <span
                  className={`inline-flex h-9 w-9 items-center justify-center rounded-xl font-display text-sm font-bold ${ACCENTS[item.accent] ?? ACCENTS.navy}`}
                >
                  {item.num}
                </span>
                <h3 className="mt-4 font-display text-xl font-semibold text-navy-dark">
                  {item.title}
                </h3>
                <p className="mt-2 leading-relaxed text-ink-mid">
                  {item.description}
                </p>
              </article>
            </StaggerItem>
          ))}

          <StaggerItem>
            <article className="flex h-full flex-col justify-center rounded-2xl bg-navy-dark p-6 text-white">
              <p className="font-display text-xl font-semibold">
                Plus: the 5-minute win
              </p>
              <p className="mt-2 leading-relaxed text-white/70">
                Section 2 has you finish one real task before you build
                anything — proof the protocol works before Notion is even open.
              </p>
            </article>
          </StaggerItem>
        </Stagger>
      </div>
    </section>
  );
}
