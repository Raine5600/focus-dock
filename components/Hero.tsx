import { BRAND, PRODUCT } from "@/lib/product";
import { CheckoutButton } from "./CheckoutButton";
import { DealBadge } from "./DealBadge";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-navy-dark text-white">
      <div
        className="pointer-events-none absolute inset-0 opacity-50"
        style={{
          backgroundImage:
            "radial-gradient(circle at 20% 20%, #3dd6c3 0%, transparent 45%), radial-gradient(circle at 80% 10%, #ff6b4a 0%, transparent 35%)",
        }}
      />
      <div className="pointer-events-none absolute right-8 top-16 text-mint/30 text-6xl">
        ⚡
      </div>
      <div className="pointer-events-none absolute left-12 top-32 text-coral/20 text-4xl">
        🧠
      </div>

      <div className="relative mx-auto grid max-w-6xl gap-12 px-5 py-16 sm:px-8 lg:grid-cols-2 lg:items-center lg:py-24">
        <div>
          <div className="mb-4 flex flex-wrap items-center gap-2">
            <DealBadge />
            <p className="inline-flex rounded-full bg-mint/20 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-mint">
              Not a template
            </p>
          </div>
          <h1 className="font-display text-4xl font-semibold leading-[1.1] sm:text-5xl lg:text-[3.25rem]">
            Your Notion graveyard ends here
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-mint-lt">
            {BRAND.tagline} The {PRODUCT.name} is a step-by-step recovery protocol
            that installs a minimal 3-database system — built for ADHD brains
            stuck in one too many Saturday setup spirals.
          </p>
          <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">
            <CheckoutButton size="lg" />
            <p className="text-sm text-mint-lt">
              <span className="font-semibold text-white">${PRODUCT.price}</span>{" "}
              <span className="text-ink-lt line-through">${PRODUCT.compareAt}</span>{" "}
              · Instant PDF · 14-day guarantee
            </p>
          </div>
          <ul className="mt-10 grid gap-3 text-sm text-mint-lt sm:grid-cols-2">
            {[
              "Step-by-step install protocol",
              "What to delete from old setup",
              "Daily workflow",
              "Task sequences + formulas",
              "Sunday reset",
              "Emergency overwhelm card",
            ].map((item) => (
              <li key={item} className="flex items-center gap-2">
                <span className="text-mint">✓</span>
                {item}
              </li>
            ))}
          </ul>
        </div>

        <div className="relative mx-auto w-full max-w-md lg:max-w-none">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-sm">
            <div className="space-y-4">
              <div className="rounded-2xl bg-navy p-5 border-l-4 border-coral">
                <p className="text-xs font-bold uppercase tracking-wider text-coral">
                  Do this next
                </p>
                <p className="mt-2 font-display text-xl font-semibold">
                  Put 3 dishes in the sink
                </p>
                <p className="mt-1 text-sm text-mint-lt">
                  Sequence 2 of 6 · Clean kitchen · 1–3 parallel tasks max
                </p>
              </div>
              <div className="rounded-2xl bg-white/10 p-4">
                <p className="text-xs font-bold uppercase tracking-wider text-mint">
                  Brain dump
                </p>
                <p className="mt-2 text-sm text-white/80">
                  Call dentist · email boss · buy milk
                </p>
              </div>
              <div className="flex gap-2">
                <span className="rounded-full bg-mint/20 px-3 py-1 text-xs text-mint">
                  3 databases
                </span>
                <span className="rounded-full bg-yellow/20 px-3 py-1 text-xs text-yellow">
                  0 streaks
                </span>
                <span className="rounded-full bg-coral/20 px-3 py-1 text-xs text-coral">
                  0 guilt
                </span>
              </div>
            </div>
          </div>
          <div className="absolute -bottom-4 -left-4 rounded-2xl bg-white px-5 py-4 shadow-xl sm:-left-8">
            <p className="text-xs font-semibold uppercase tracking-wide text-coral">
              Summer sale
            </p>
            <p className="font-display text-2xl font-semibold text-navy-dark">
              <span className="text-ink-lt line-through">${PRODUCT.compareAt}</span>{" "}
              ${PRODUCT.price}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}