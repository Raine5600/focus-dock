"use client";

import { useState } from "react";

export function CopyEmailList({ emails }: { emails: string[] }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(emails.join("\n"));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <section className="rounded-2xl border border-border bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="font-display text-lg font-semibold text-navy-dark">
            Subscriber emails
          </h2>
          <p className="mt-0.5 text-sm text-ink-lt">
            {emails.length} address{emails.length === 1 ? "" : "es"} — Brain Dump formula opt-ins
          </p>
        </div>
        <button
          onClick={handleCopy}
          disabled={emails.length === 0}
          className="rounded-full bg-navy-dark px-5 py-2 text-sm font-semibold text-white transition hover:bg-navy disabled:opacity-40"
        >
          {copied ? "Copied!" : "Copy all"}
        </button>
      </div>

      {emails.length === 0 ? (
        <p className="text-sm text-ink-mid">No subscribers yet.</p>
      ) : (
        <textarea
          readOnly
          value={emails.join("\n")}
          rows={Math.min(emails.length, 8)}
          className="w-full rounded-xl border border-border bg-cream px-4 py-3 font-mono text-xs text-ink-mid outline-none resize-none"
        />
      )}
    </section>
  );
}
