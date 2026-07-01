"use client";

import { useEffect, useState } from "react";
import { getDealBadgeText } from "@/lib/deal";

export function DealBadge() {
  const [badgeText, setBadgeText] = useState(() => getDealBadgeText());

  useEffect(() => {
    const tick = () => setBadgeText(getDealBadgeText());
    tick();
    const id = setInterval(tick, 60_000);
    return () => clearInterval(id);
  }, []);

  return (
    <p className="inline-flex rounded-full bg-coral px-4 py-1.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm">
      ⚡ {badgeText}
    </p>
  );
}