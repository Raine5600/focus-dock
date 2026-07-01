import Link from "next/link";
import { Footer } from "@/components/Footer";
import { SiteChrome } from "@/components/SiteChrome";
import { BRAND } from "@/lib/product";
import { buildPageMetadata } from "@/lib/seo";
import { getContactEmail } from "@/lib/site";

export const metadata = buildPageMetadata({
  title: `Refund Policy — ${BRAND.name}`,
  description: `14-day refund policy for ${BRAND.name} purchases.`,
  path: "/refund",
});

export default function RefundPage() {
  const supportEmail = getContactEmail("support");

  return (
    <>
      <SiteChrome />
      <main className="min-h-[60vh] bg-cream py-16">
        <div className="mx-auto max-w-3xl px-5 sm:px-8">
          <h1 className="font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            Refund Policy
          </h1>
          <p className="mt-4 text-sm text-ink-lt">Last updated: July 1, 2026</p>

          <div className="mt-10 space-y-8 text-ink-mid leading-relaxed">
            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                14-day guarantee
              </h2>
              <p className="mt-3">
                If the {BRAND.name} ADHD Notion Recovery Guide isn&apos;t helpful
                for you, email us within 14 days of purchase for a full refund. No
                hoops, no guilt — same energy as the system itself.
              </p>
            </section>

            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                How to request a refund
              </h2>
              <p className="mt-3">
                Send your order email or Stripe receipt to{" "}
                <a
                  href={`mailto:${supportEmail}`}
                  className="font-medium text-coral hover:underline"
                >
                  {supportEmail}
                </a>{" "}
                with the subject line &quot;Refund request.&quot; We typically
                process refunds within 3–5 business days.
              </p>
            </section>

            <section>
              <h2 className="font-display text-xl font-semibold text-navy-dark">
                What happens after
              </h2>
              <p className="mt-3">
                Once refunded, your download link may be revoked. You may keep a
                personal copy only if permitted by applicable law; otherwise please
                delete the PDF.
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