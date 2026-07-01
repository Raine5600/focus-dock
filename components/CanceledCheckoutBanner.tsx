"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { PRODUCT } from "@/lib/product";

export function CanceledCheckoutBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("canceled") === "1") {
      setVisible(true);
    }
  }, []);

  if (!visible) return null;

  function dismiss() {
    setVisible(false);
    const url = new URL(window.location.href);
    url.searchParams.delete("canceled");
    window.history.replaceState({}, "", url.pathname + url.search + url.hash);
  }

  return (
    <div
      role="status"
      className="border-b border-amber/30 bg-cream-dk px-5 py-3 text-sm text-navy-dark sm:px-8"
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p>
          Checkout canceled — your summer deal is still active.{" "}
          <Link href="#pricing" className="font-semibold text-coral hover:underline">
            Claim ${PRODUCT.price} access
          </Link>{" "}
          when you&apos;re ready.
        </p>
        <button
          type="button"
          onClick={dismiss}
          className="shrink-0 self-end rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide text-ink-mid transition hover:bg-white/60 sm:self-center"
          aria-label="Dismiss checkout recovery message"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}