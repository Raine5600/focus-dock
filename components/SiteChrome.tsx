import { DealBanner } from "@/components/DealBanner";
import { Header } from "@/components/Header";
import { ScrollProgress } from "@/components/ScrollProgress";

export function SiteChrome() {
  return (
    <>
      <ScrollProgress />
      <div className="sticky top-0 z-50">
        <DealBanner />
        <Header />
      </div>
    </>
  );
}