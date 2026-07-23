"use client";

import { useState } from "react";
import { PRODUCT, SUMMER_DEAL } from "@/lib/product";
import { trackEvent } from "./Track";
import { MagneticButton } from "./MagneticButton";

type Props = {
  size?: "md" | "lg";
  className?: string;
  label?: string;
};

export function CheckoutButton({
  size = "md",
  className = "",
  label = SUMMER_DEAL.active
    ? `Claim summer deal — $${PRODUCT.price}`
    : "Get instant access",
}: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sizeClasses =
    size === "lg"
      ? "px-8 py-4 text-base"
      : "px-6 py-3 text-sm";

  async function handleCheckout() {
    setLoading(true);
    setError(null);
    trackEvent("checkout_click");
    try {
      const ref = new URLSearchParams(window.location.search).get("ref");
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(ref ? { affiliateRef: ref } : {}),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Checkout failed");
      }
      if (data.url) {
        window.location.href = data.url;
        return;
      }
      throw new Error("No checkout URL returned");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setLoading(false);
    }
  }

  return (
    <div className={className}>
      <MagneticButton>
        <button
          type="button"
          onClick={handleCheckout}
          disabled={loading}
          className={`btn-glow inline-flex items-center gap-2 rounded-full bg-coral font-semibold text-white shadow-md transition hover:bg-[#e55a3a] disabled:cursor-not-allowed disabled:opacity-70 ${sizeClasses}`}
        >
          {loading ? (
            <>
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
              Redirecting…
            </>
          ) : (
            label
          )}
        </button>
      </MagneticButton>
      {error ? (
        <p className="mt-2 text-sm text-rose">{error}</p>
      ) : null}
    </div>
  );
}