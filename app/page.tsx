import { CanceledCheckoutBanner } from "@/components/CanceledCheckoutBanner";
import { SiteChrome } from "@/components/SiteChrome";
import { Hero } from "@/components/Hero";
import { Problem } from "@/components/Problem";
import { WhatsIncluded } from "@/components/WhatsIncluded";
import { Pricing } from "@/components/Pricing";
import { FAQ } from "@/components/FAQ";
import { Footer } from "@/components/Footer";
import { JsonLd } from "@/components/JsonLd";
import { productJsonLd } from "@/lib/seo";

export default function HomePage() {
  return (
    <>
      <JsonLd data={productJsonLd()} />
      <SiteChrome />
      <CanceledCheckoutBanner />
      <main>
        <Hero />
        <Problem />
        <WhatsIncluded />
        <Pricing />
        <FAQ />
      </main>
      <Footer />
    </>
  );
}