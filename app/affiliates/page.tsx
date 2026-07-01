import Link from "next/link";
import { AffiliateApplicationForm } from "@/components/AffiliateApplicationForm";
import { Footer } from "@/components/Footer";
import { SiteChrome } from "@/components/SiteChrome";
import { JsonLd } from "@/components/JsonLd";
import { BRAND, PACKAGE_ITEMS, PRODUCT, SUMMER_DEAL } from "@/lib/product";
import { affiliatesJsonLd, affiliatesMetadata } from "@/lib/seo";
import { getContactEmail } from "@/lib/site";

const COMMISSION_RATE = 0.4;
const COMMISSION_PER_SALE = PRODUCT.price * COMMISSION_RATE;

const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Apply",
    description:
      "Fill out the short form below with your name, email, and where you create. We review every application within a few business days.",
  },
  {
    step: "02",
    title: "Get your link",
    description:
      "Approved partners receive a unique referral link and simple talking points to share with your audience.",
  },
  {
    step: "03",
    title: "Share with your audience",
    description:
      "Recommend Focus Dock to ADHD/Notion audiences who've template-hopped their way into a graveyard — honest recovery, not hype.",
  },
  {
    step: "04",
    title: "Earn on every sale",
    description:
      "You earn 40% commission on each purchase made through your link. We handle checkout, delivery, and support.",
  },
] as const;

const CREATOR_TYPES = [
  "ADHD & neurodivergent creators",
  "Notion / productivity YouTubers",
  "Executive dysfunction coaches",
  "Newsletter writers & podcast hosts",
] as const;

export const metadata = affiliatesMetadata();

export default function AffiliatesPage() {
  const helloEmail = getContactEmail("hello");

  return (
    <>
      <JsonLd data={affiliatesJsonLd()} />
      <SiteChrome />
      <main>
        {/* Hero */}
        <section className="relative overflow-hidden bg-navy-dark py-16 text-white sm:py-24">
          <div
            className="pointer-events-none absolute inset-0 opacity-40"
            style={{
              backgroundImage:
                "radial-gradient(circle at 20% 20%, #7b9ec4 0%, transparent 45%), radial-gradient(circle at 80% 10%, #5b8a72 0%, transparent 35%)",
            }}
          />
          <div className="relative mx-auto max-w-4xl px-5 text-center sm:px-8">
            <p className="inline-flex rounded-full bg-sage/20 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-sage-lt">
              Affiliate program
            </p>
            <h1 className="mt-6 font-display text-4xl font-semibold leading-[1.1] sm:text-5xl">
              Help ADHD brains escape Notion hell — earn on every sale
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-moon-lt">
              Partner with {BRAND.name} and earn{" "}
              <strong className="text-white">
                {Math.round(COMMISSION_RATE * 100)}% commission
              </strong>{" "}
              when your audience buys the {PRODUCT.name}.
            </p>
            <p className="mt-6 text-sm text-moon-lt">
              <span className="font-semibold text-white">
                ${COMMISSION_PER_SALE.toFixed(2)}
              </span>{" "}
              per sale at the current ${PRODUCT.price} price
            </p>
          </div>
        </section>

        {/* Commission */}
        <section className="py-20">
          <div className="mx-auto max-w-6xl px-5 sm:px-8">
            <div className="mx-auto max-w-3xl text-center">
              <p className="text-sm font-semibold uppercase tracking-wider text-sage">
                Commission details
              </p>
              <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
                Generous payouts, simple math
              </h2>
            </div>

            <div className="mx-auto mt-12 grid max-w-4xl gap-6 sm:grid-cols-3">
              <div className="rounded-2xl border border-border bg-white p-6 text-center shadow-sm">
                <p className="text-sm font-semibold uppercase tracking-wide text-sage">
                  Commission rate
                </p>
                <p className="mt-3 font-display text-4xl font-semibold text-navy-dark">
                  {Math.round(COMMISSION_RATE * 100)}%
                </p>
                <p className="mt-2 text-sm text-ink-mid">On every referred sale</p>
              </div>
              <div className="rounded-2xl border border-border bg-white p-6 text-center shadow-sm">
                <p className="text-sm font-semibold uppercase tracking-wide text-sage">
                  You earn
                </p>
                <p className="mt-3 font-display text-4xl font-semibold text-navy-dark">
                  ${COMMISSION_PER_SALE.toFixed(2)}
                </p>
                <p className="mt-2 text-sm text-ink-mid">
                  Per sale at ${PRODUCT.price} (summer deal)
                </p>
              </div>
              <div className="rounded-2xl border border-border bg-white p-6 text-center shadow-sm">
                <p className="text-sm font-semibold uppercase tracking-wide text-sage">
                  Product price
                </p>
                <p className="mt-3 font-display text-4xl font-semibold text-navy-dark">
                  <span className="text-ink-lt line-through text-2xl">
                    ${PRODUCT.compareAt}
                  </span>{" "}
                  ${PRODUCT.price}
                </p>
                <p className="mt-2 text-sm text-ink-mid">
                  {SUMMER_DEAL.badge} · normally ${PRODUCT.compareAt}
                </p>
              </div>
            </div>

            <p className="mx-auto mt-8 max-w-2xl text-center text-sm text-ink-lt">
              Instant digital delivery means high conversion and zero shipping
              headaches. Commission is calculated on the purchase price at time
              of sale.
            </p>
          </div>
        </section>

        {/* Who it's for */}
        <section className="bg-cream-dk/50 py-20">
          <div className="mx-auto max-w-6xl px-5 sm:px-8">
            <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
              <div>
                <p className="text-sm font-semibold uppercase tracking-wider text-sage">
                  Who it&apos;s for
                </p>
                <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
                  ADHD & Notion creators who get it
                </h2>
                <p className="mt-4 text-lg text-ink-mid">
                  If your audience has abandoned a Notion template or three,
                  this is a natural fit. We partner with creators who talk
                  honestly about executive dysfunction — not productivity
                  performance theater.
                </p>
              </div>
              <ul className="space-y-4">
                {CREATOR_TYPES.map((type) => (
                  <li
                    key={type}
                    className="flex items-start gap-3 rounded-2xl border border-border bg-white p-5 shadow-sm"
                  >
                    <span className="mt-0.5 text-sage">✓</span>
                    <span className="text-ink-mid">{type}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* Product */}
        <section className="py-20">
          <div className="mx-auto max-w-6xl px-5 sm:px-8">
            <div className="mx-auto max-w-3xl text-center">
              <p className="text-sm font-semibold uppercase tracking-wider text-sage">
                What you&apos;re promoting
              </p>
              <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
                The {PRODUCT.name}
              </h2>
              <p className="mt-4 text-lg text-ink-mid">{PRODUCT.description}</p>
            </div>

            <div className="mx-auto mt-12 grid max-w-4xl gap-4">
              {PACKAGE_ITEMS.map((item) => (
                <article
                  key={item.num}
                  className="flex gap-4 rounded-2xl border border-border bg-white p-5 shadow-sm"
                >
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sage text-sm font-bold text-white">
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
        </section>

        {/* How it works */}
        <section className="bg-navy-dark py-20 text-white">
          <div className="mx-auto max-w-6xl px-5 sm:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <p className="text-sm font-semibold uppercase tracking-wider text-sage-lt">
                How it works
              </p>
              <h2 className="mt-3 font-display text-3xl font-semibold sm:text-4xl">
                Four steps to start earning
              </h2>
            </div>

            <div className="mx-auto mt-12 grid max-w-4xl gap-6 sm:grid-cols-2">
              {HOW_IT_WORKS.map((item) => (
                <article
                  key={item.step}
                  className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm"
                >
                  <span className="font-display text-2xl font-semibold text-sage-lt">
                    {item.step}
                  </span>
                  <h3 className="mt-3 font-display text-xl font-semibold">
                    {item.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-moon-lt">
                    {item.description}
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* Application form */}
        <section className="py-20" id="apply">
          <div className="mx-auto max-w-xl px-5 sm:px-8">
            <div className="text-center">
              <h2 className="font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
                Apply to partner
              </h2>
              <p className="mt-4 text-lg text-ink-mid">
                Submit the form and we&apos;ll send your application straight to{" "}
                <span className="font-medium text-navy-dark">{helloEmail}</span>.
                We typically reply within a few business days.
              </p>
            </div>

            <div className="mt-10 rounded-2xl border border-border bg-white p-6 shadow-sm sm:p-8">
              <AffiliateApplicationForm />
            </div>

            <p className="mt-8 text-center text-sm text-ink-lt">
              <Link href="/" className="font-medium text-sage hover:underline">
                ← Back to {BRAND.name}
              </Link>
            </p>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}