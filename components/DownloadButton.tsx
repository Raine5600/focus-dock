"use client";

import { useState } from "react";
import { PRODUCT } from "@/lib/product";

type Props = {
  sessionId: string;
  file?: "pdf" | "formulas";
  label?: string;
  variant?: "primary" | "secondary";
};

export function DownloadButton({
  sessionId,
  file = "pdf",
  label,
  variant = "primary",
}: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleDownload() {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ session_id: sessionId });
      if (file === "formulas") {
        params.set("file", "formulas");
      }
      const res = await fetch(`/api/download?${params.toString()}`);
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "Download failed");
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = file === "formulas" ? PRODUCT.formulasFileName : PRODUCT.fileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Download failed");
    } finally {
      setLoading(false);
    }
  }

  const buttonLabel =
    label ??
    (file === "formulas" ? "Download Formulas (.txt)" : `Download ${PRODUCT.fileLabel}`);
  const buttonClass =
    variant === "secondary"
      ? "inline-flex w-full items-center justify-center gap-2 rounded-full border border-border bg-white px-8 py-4 text-base font-semibold text-navy-dark shadow-sm transition hover:bg-cream disabled:opacity-70 sm:w-auto"
      : "inline-flex w-full items-center justify-center gap-2 rounded-full bg-coral px-8 py-4 text-base font-semibold text-white shadow-md transition hover:bg-[#e55a3a] disabled:opacity-70 sm:w-auto";

  return (
    <div>
      <button
        type="button"
        onClick={handleDownload}
        disabled={loading}
        className={buttonClass}
      >
        {loading ? "Preparing download…" : buttonLabel}
      </button>
      {error ? <p className="mt-3 text-sm text-rose">{error}</p> : null}
    </div>
  );
}