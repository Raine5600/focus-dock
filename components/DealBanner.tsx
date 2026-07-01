"use client";

import { useEffect, useState } from "react";
import { getDealEndMs, getDealTimeLeft, getUrgentDealLabel, type DealTimeLeft } from "@/lib/deal";
import { PRODUCT, SUMMER_DEAL } from "@/lib/product";

function pad(n: number) {
  return String(n).padStart(2, "0");
}

export function DealBanner() {
  const endMs = getDealEndMs();
  const [timeLeft, setTimeLeft] = useState<DealTimeLeft | null>(() =>
    SUMMER_DEAL.active ? getDealTimeLeft() : null
  );

  useEffect(() => {
    if (!SUMMER_DEAL.active) return;
    const tick = () => setTimeLeft(getDealTimeLeft());
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [endMs]);

  if (!SUMMER_DEAL.active || !timeLeft) return null;

  const savings = PRODUCT.compareAt - PRODUCT.price;
  const urgentLabel = getUrgentDealLabel(timeLeft);
  const isFinalHours = timeLeft.days === 0;

  return (
    <div
      className={`relative overflow-hidden text-white ${
        isFinalHours
          ? "bg-gradient-to-r from-[#8b2e2e] via-[#b83a3a] to-[#c45c2a]"
          : "bg-gradient-to-r from-[#9a3b12] via-amber to-[#c45c2a]"
      }`}
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-25"
        style={{
          backgroundImage:
            "radial-gradient(circle at 15% 50%, white 0%, transparent 35%), radial-gradient(circle at 85% 50%, white 0%, transparent 30%)",
        }}
      />

      <div className="relative mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-5 py-3 sm:flex-row sm:px-8">
        <div className="flex flex-col items-center gap-2 text-center sm:flex-row sm:items-center sm:gap-4 sm:text-left">
          <span className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-bold uppercase tracking-wider ring-1 ring-white/25 backdrop-blur-sm">
            <span
              className="h-2 w-2 shrink-0 rounded-full bg-white animate-pulse"
              aria-hidden
            />
            {urgentLabel}
          </span>
          <p className="text-sm font-medium leading-snug sm:text-[0.95rem]">
            <span className="font-bold uppercase tracking-wide">
              {SUMMER_DEAL.headline}
            </span>
            <span className="text-white/95">
              {" "}
              — <span className="font-semibold">${PRODUCT.price} today</span>
              <span className="text-white/80"> (save ${savings})</span>
            </span>
          </p>
        </div>

        <div className="flex items-center gap-2.5 sm:gap-3">
          <div
            className="flex items-center gap-2 rounded-xl bg-black/25 px-3 py-1.5 font-mono text-sm tabular-nums ring-1 ring-white/15 backdrop-blur-sm"
            aria-live="polite"
            aria-label={`Deal ${urgentLabel}. ${timeLeft.hours} hours, ${timeLeft.minutes} minutes, ${timeLeft.seconds} seconds remaining`}
          >
            <span className="text-[0.65rem] font-sans font-bold uppercase tracking-wide text-white/90">
              {timeLeft.days > 0 ? `${timeLeft.days}d` : "Today"}
            </span>
            <span className="font-bold">
              {pad(timeLeft.hours)}:{pad(timeLeft.minutes)}:{pad(timeLeft.seconds)}
            </span>
          </div>
          <a
            href="#pricing"
            className="rounded-full bg-white px-4 py-1.5 text-sm font-bold text-[#8b2e2e] shadow-sm transition hover:bg-moon-lt"
          >
            Claim now
          </a>
        </div>
      </div>
    </div>
  );
}