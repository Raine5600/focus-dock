import { getDealTimeLeft, getUrgentDealLabel } from "@/lib/deal";
import { PACKAGE_ITEMS, PRODUCT, SUMMER_DEAL } from "@/lib/product";
import { CheckoutButton } from "./CheckoutButton";

export function Pricing() {
  const timeLeft = getDealTimeLeft();
  const urgency = timeLeft ? getUrgentDealLabel(timeLeft) : "Limited time";

  return (
    <section id="pricing" className="bg-navy-dark py-20 text-white">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-sage-lt">
            Simple pricing
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold sm:text-4xl">
            One purchase. Lifetime access.
          </h2>
          <p className="mt-4 text-lg text-moon-lt">
            No subscription. No upsells required. Download instantly and keep
            the files forever.
          </p>
        </div>

        <div className="mx-auto mt-12 max-w-lg">
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur-sm">
            <div className="border-b border-white/10 bg-gradient-to-r from-amber/80 to-sage/60 px-8 py-4 text-center">
              <p className="text-sm font-bold uppercase tracking-wider text-white">
                ⚡ {urgency} — {SUMMER_DEAL.label}
              </p>
            </div>
            <div className="px-8 py-10 text-center">
              <p className="font-display text-xl font-semibold">{PRODUCT.fullName}</p>
              <div className="mt-6 flex items-end justify-center gap-3">
                <span className="text-2xl text-moon line-through">
                  ${PRODUCT.compareAt}
                </span>
                <span className="font-display text-6xl font-semibold">
                  ${PRODUCT.price}
                </span>
              </div>
              <p className="mt-2 text-sm text-moon-lt">
                Summer price ends Aug 31 · One-time payment · Instant download
              </p>

              <div className="mt-8">
                <CheckoutButton size="lg" className="w-full justify-center" />
              </div>

              <ul className="mt-8 space-y-3 text-left text-sm text-moon-lt">
                {PACKAGE_ITEMS.map((item) => (
                  <li key={item.num} className="flex items-start gap-3">
                    <span className="mt-0.5 text-sage">✓</span>
                    <span>
                      <strong className="text-white">{item.title}</strong> —{" "}
                      {item.description.split(".")[0]}.
                    </span>
                  </li>
                ))}
                <li className="flex items-start gap-3">
                  <span className="mt-0.5 text-sage">✓</span>
                  <span>
                    <strong className="text-white">14-day money-back guarantee</strong>
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}