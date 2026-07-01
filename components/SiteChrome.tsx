import { DealBanner } from "@/components/DealBanner";
import { Header } from "@/components/Header";

export function SiteChrome() {
  return (
    <div className="sticky top-0 z-50">
      <DealBanner />
      <Header />
    </div>
  );
}