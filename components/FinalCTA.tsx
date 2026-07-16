import { PRODUCT } from "@/lib/product";
import { CheckoutButton } from "./CheckoutButton";
import { Reveal } from "./motion";

export function FinalCTA() {
  return (
    <section className="relative overflow-hidden border-t border-border bg-white py-20 sm:py-24">
      <div className="dot-grid-dark pointer-events-none absolute inset-0 opacity-60 [mask-image:radial-gradient(ellipse_at_center,black_10%,transparent_70%)]" />
      <div className="relative mx-auto max-w-3xl px-5 text-center sm:px-8">
        <Reveal>
          <h2 className="font-display text-3xl font-semibold leading-tight text-navy-dark sm:text-4xl">
            Tomorrow morning: open Notion,
            <br className="hidden sm:block" /> see one task, do it.
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg text-ink-mid">
            That&apos;s the whole promise. No streaks to maintain, no dashboard
            to feed — just the next physical action, visible.
          </p>
          <div className="mt-8 flex flex-col items-center gap-3">
            <CheckoutButton size="lg" />
            <p className="text-sm text-ink-lt">
              ${PRODUCT.price} · instant download · 14-day guarantee
            </p>
          </div>
          <p className="mx-auto mt-10 max-w-md text-sm italic leading-relaxed text-ink-lt">
            P.S. — If you&apos;re reading this section bottom-to-top after
            skimming everything else: hi, the guide is written for exactly how
            you just read this page.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
