import { getDealTimeLeft, getUrgentDealLabel } from "@/lib/deal";
import { PACKAGE_ITEMS, PRODUCT, SUMMER_DEAL } from "@/lib/product";
import { CheckoutButton } from "./CheckoutButton";
import { Reveal } from "./motion";

const AFTER_CHECKOUT = [
  { step: "1", label: "Pay securely", detail: "Stripe checkout — card or wallet" },
  { step: "2", label: "Download instantly", detail: "PDF + formulas file, yours forever" },
  { step: "3", label: "Build tonight", detail: "One sitting. One real task done." },
];

export function Pricing() {
  const timeLeft = getDealTimeLeft();
  const urgency = timeLeft ? getUrgentDealLabel(timeLeft) : "Limited time";

  return (
    <section id="pricing" className="relative overflow-hidden bg-navy-dark py-20 text-white sm:py-24">
      <div className="aurora aurora-a -right-40 -top-24 h-96 w-96 bg-coral/15" />
      <div className="aurora aurora-b -left-32 bottom-0 h-80 w-80 bg-mint/15" />

      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-mint">
            Simple pricing
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold sm:text-4xl">
            One price. One payment. No tiers to compare.
          </h2>
          <p className="mt-4 text-lg text-white/70">
            Decision fatigue is the enemy — so there&apos;s exactly one option.
            Less than the last template you abandoned.
          </p>
        </Reveal>

        <Reveal delay={0.1} className="mx-auto mt-12 max-w-lg">
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur-sm">
            <div className="border-b border-white/10 bg-gradient-to-r from-coral/90 to-coral/60 px-8 py-4 text-center">
              <p className="text-sm font-bold uppercase tracking-wider text-white">
                {SUMMER_DEAL.label} · {urgency}
              </p>
            </div>
            <div className="px-8 py-10 text-center">
              <p className="font-display text-xl font-semibold">{PRODUCT.fullName}</p>
              <div className="mt-6 flex items-end justify-center gap-3">
                <span className="text-2xl text-white/40 line-through">
                  ${PRODUCT.compareAt}
                </span>
                <span className="font-display text-6xl font-semibold">
                  ${PRODUCT.price}
                </span>
              </div>
              <p className="mt-2 text-sm text-white/60">
                Summer sale pricing — one-time payment, yours forever.
              </p>

              <div className="mt-8">
                <CheckoutButton size="lg" className="w-full justify-center" />
              </div>
              <p className="mt-3 text-xs text-white/50">
                Secure checkout via Stripe · Instant download · 14-day refund
              </p>

              <ul className="mt-8 space-y-3 text-left text-sm text-white/70">
                {PACKAGE_ITEMS.map((item) => (
                  <li key={item.num} className="flex items-start gap-3">
                    <span className="mt-0.5 text-mint">✓</span>
                    <span>
                      <strong className="text-white">{item.title}</strong> —{" "}
                      {item.description.split(".")[0]}.
                    </span>
                  </li>
                ))}
                <li className="flex items-start gap-3">
                  <span className="mt-0.5 text-mint">✓</span>
                  <span>
                    <strong className="text-white">
                      14-day money-back guarantee
                    </strong>{" "}
                    — no questions asked
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </Reveal>

        <Reveal delay={0.15}>
          <div className="mx-auto mt-10 grid max-w-3xl gap-4 sm:grid-cols-3">
            {AFTER_CHECKOUT.map((item) => (
              <div
                key={item.step}
                className="rounded-2xl border border-white/10 bg-white/5 p-5 text-center"
              >
                <span className="mx-auto flex h-8 w-8 items-center justify-center rounded-full bg-mint font-display text-sm font-bold text-navy-dark">
                  {item.step}
                </span>
                <p className="mt-3 font-semibold text-white">{item.label}</p>
                <p className="mt-1 text-sm text-white/60">{item.detail}</p>
              </div>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
