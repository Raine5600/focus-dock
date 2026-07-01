import Link from "next/link";
import { Footer } from "@/components/Footer";
import { SiteChrome } from "@/components/SiteChrome";
import { BRAND } from "@/lib/product";
import { buildPageMetadata } from "@/lib/seo";
import { getContactEmail } from "@/lib/site";

export const metadata = buildPageMetadata({
  title: `Privacy Policy — ${BRAND.name}`,
  description: `How ${BRAND.name} collects, uses, and protects your information.`,
  path: "/privacy",
});

export default function PrivacyPage() {
  const supportEmail = getContactEmail("support");

  return (
    <>
      <SiteChrome />
      <main className="min-h-[60vh] bg-cream py-16">
        <div className="mx-auto max-w-3xl px-5 sm:px-8">
          <h1 className="font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            Privacy Policy
          </h1>
          <p className="mt-4 text-sm text-ink-lt">Last updated: July 1, 2026</p>

          <div className="mt-10 space-y-8 text-ink-mid leading-relaxed">
            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                What we collect
              </h2>
              <p className="mt-3">
                When you purchase {BRAND.name}, we receive your email address and
                payment details through Stripe. We do not store full card numbers on
                our servers. If you apply to our affiliate program, we collect the
                information you submit in the application form.
              </p>
            </section>

            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                How we use it
              </h2>
              <p className="mt-3">
                We use your email to deliver your purchase, send receipts, and
                respond to support requests. Affiliate referral codes passed via{" "}
                <code className="rounded bg-white px-1.5 py-0.5 text-sm">?ref=</code>{" "}
                are stored with checkout metadata to attribute sales to partners.
              </p>
            </section>

            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                Third parties
              </h2>
              <p className="mt-3">
                Payments are processed by Stripe. Hosting and file delivery may use
                Vercel and related infrastructure. These providers process data
                according to their own privacy policies.
              </p>
            </section>

            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                Your choices
              </h2>
              <p className="mt-3">
                You can request access to or deletion of purchase-related data by
                emailing{" "}
                <a
                  href={`mailto:${supportEmail}`}
                  className="font-medium text-coral hover:underline"
                >
                  {supportEmail}
                </a>
                . We do not sell your personal information.
              </p>
            </section>
          </div>

          <p className="mt-12 text-sm text-ink-lt">
            <Link href="/" className="font-medium text-coral hover:underline">
              ← Back to home
            </Link>
          </p>
        </div>
      </main>
      <Footer />
    </>
  );
}