import { CanceledCheckoutBanner } from "@/components/CanceledCheckoutBanner";
import { SiteChrome } from "@/components/SiteChrome";
import { Hero } from "@/components/Hero";
import { Problem } from "@/components/Problem";
import { Mechanism } from "@/components/Mechanism";
import { LookInside } from "@/components/LookInside";
import { WhatsIncluded } from "@/components/WhatsIncluded";
import { WhoItsFor } from "@/components/WhoItsFor";
import { FounderNote } from "@/components/FounderNote";
import { Guarantee } from "@/components/Guarantee";
import { Pricing } from "@/components/Pricing";
import { FAQ } from "@/components/FAQ";
import { FinalCTA } from "@/components/FinalCTA";
import { Footer } from "@/components/Footer";
import { JsonLd } from "@/components/JsonLd";
import { MotionProvider } from "@/components/motion";
import { productJsonLd } from "@/lib/seo";
import { Testimonials } from "@/components/Testimonials";
import { EmailCapture } from "@/components/EmailCapture";

export default function HomePage() {
  return (
    <MotionProvider>
      <JsonLd data={productJsonLd()} />
      <SiteChrome />
      <CanceledCheckoutBanner />
      <main>
        <Hero />
        <Problem />
        <Mechanism />
        <LookInside />
        <WhatsIncluded />
        <WhoItsFor />
        <Testimonials />
        <FounderNote />
        <Guarantee />
        <Pricing />
        <EmailCapture />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
    </MotionProvider>
  );
}
