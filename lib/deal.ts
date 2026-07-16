import { PRODUCT, SUMMER_DEAL } from "@/lib/product";

export type DealTimeLeft = {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  totalMs: number;
};

/** End of the current rolling cycle — always in the future. */
export function getDealEndMs(now = Date.now()): number {
  const anchor = new Date(SUMMER_DEAL.cycleAnchor).getTime();
  const cycleMs = SUMMER_DEAL.cycleDays * 24 * 60 * 60 * 1000;
  const elapsed = Math.max(0, now - anchor);
  return anchor + (Math.floor(elapsed / cycleMs) + 1) * cycleMs;
}

export function getDealTimeLeft(now = Date.now()): DealTimeLeft | null {
  if (!SUMMER_DEAL.active) return null;

  const totalMs = getDealEndMs(now) - now;

  return {
    totalMs,
    days: Math.floor(totalMs / (1000 * 60 * 60 * 24)),
    hours: Math.floor((totalMs / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((totalMs / (1000 * 60)) % 60),
    seconds: Math.floor((totalMs / 1000) % 60),
  };
}

/** Short label for badges and banners — e.g. "6 days left", "Ends tonight" */
export function getUrgentDealLabel(timeLeft: DealTimeLeft): string {
  if (timeLeft.days === 0 && timeLeft.hours < 6) {
    return "Ends tonight";
  }
  if (timeLeft.days === 0) {
    return "Last day — ends at midnight";
  }
  if (timeLeft.days === 1) {
    return "1 day left";
  }
  return `${timeLeft.days} days left`;
}

export function getDealBadgeText(now = Date.now()): string {
  const timeLeft = getDealTimeLeft(now);
  if (!timeLeft) return "Summer deal ended";
  return `${getUrgentDealLabel(timeLeft)} — $${PRODUCT.price}`;
}