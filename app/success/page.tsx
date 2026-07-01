import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { buildPageMetadata } from "@/lib/seo";
import { DownloadButton } from "@/components/DownloadButton";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { PACKAGE_ITEMS, PRODUCT } from "@/lib/product";
import { getContactEmail } from "@/lib/site";
import { getStripe } from "@/lib/stripe";

export const dynamic = "force-dynamic";

export const metadata: Metadata = buildPageMetadata({
  title: "Download Your ADHD Notion Recovery Guide",
  description: "Your Focus Dock purchase is complete. Download your PDF guide instantly.",
  path: "/success",
  noIndex: true,
});

type Props = {
  searchParams: Promise<{ session_id?: string }>;
};

export default async function SuccessPage({ searchParams }: Props) {
  const { session_id: sessionId } = await searchParams;

  if (!sessionId) {
    redirect("/");
  }

  let customerEmail: string | null = null;
  let paid = false;

  try {
    const stripe = getStripe();
    const session = await stripe.checkout.sessions.retrieve(sessionId);
    paid = session.payment_status === "paid";
    customerEmail = session.customer_details?.email ?? null;
    const affiliateRef = session.metadata?.affiliate_ref;
    if (affiliateRef) {
      console.log(
        "[affiliate]",
        JSON.stringify({ sessionId, affiliateRef })
      );
    }
  } catch {
    redirect("/");
  }

  if (!paid) {
    redirect("/");
  }

  return (
    <>
      <Header />
      <main className="min-h-[70vh] bg-cream py-16">
        <div className="mx-auto max-w-2xl px-5 text-center sm:px-8">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-mint-lt text-3xl text-mint">
            ✓
          </div>
          <h1 className="mt-6 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            You&apos;re in — time to build, not tweak
          </h1>
          <p className="mt-4 text-lg text-ink-mid">
            Thank you for purchasing the {PRODUCT.fullName}. Your download is
            ready below.
          </p>
          {customerEmail ? (
            <p className="mt-2 text-sm text-ink-lt">
              Receipt sent to <strong className="text-ink">{customerEmail}</strong>
            </p>
          ) : null}

          <div className="mt-10 rounded-3xl border border-border bg-white p-8 shadow-sm">
            <div className="flex flex-col items-center gap-4">
              <DownloadButton sessionId={sessionId} />
              <DownloadButton
                sessionId={sessionId}
                file="formulas"
                variant="secondary"
              />
            </div>
            <p className="mt-4 text-sm text-ink-lt">
              Save both files to your device. You can re-download from this page
              anytime using the same link — we also email this URL after
              checkout when email delivery is configured.
            </p>
          </div>

          <div className="mt-10 rounded-2xl border border-border bg-white p-6 text-left shadow-sm">
            <h2 className="font-display text-lg font-semibold text-navy-dark">
              What&apos;s in your download
            </h2>
            <ul className="mt-4 space-y-3 text-sm text-ink-mid">
              {PACKAGE_ITEMS.map((item) => (
                <li key={item.num} className="flex gap-3">
                  <span className="font-semibold text-coral">{item.num}</span>
                  <span>
                    <strong className="text-ink">{item.title}</strong> —{" "}
                    {item.description}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <p className="mt-8 text-sm text-ink-lt">
            Need help?{" "}
            <a
              href={`mailto:${getContactEmail("support")}`}
              className="font-medium text-coral hover:underline"
            >
              Email support
            </a>{" "}
            ·{" "}
            <Link href="/" className="font-medium text-coral hover:underline">
              Back to home
            </Link>
          </p>
        </div>
      </main>
      <Footer />
    </>
  );
}