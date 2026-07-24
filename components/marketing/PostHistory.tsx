"use client";

import { useEffect, useState } from "react";
import type { MarketingLogEntry, MarketingChannel } from "@/lib/marketing";

const CHANNEL_STYLES: Record<MarketingChannel, { label: string; className: string }> = {
  email: { label: "Email", className: "bg-navy-dark text-white" },
  bluesky: { label: "Bluesky", className: "bg-[#0085FF] text-white" },
  twitter: { label: "X", className: "bg-black text-white" },
  reddit: { label: "Reddit", className: "bg-[#FF4500] text-white" },
};

export function PostHistory() {
  const [entries, setEntries] = useState<MarketingLogEntry[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try {
      const res = await fetch("/api/admin/marketing/log");
      const data = await res.json();
      setEntries(data.entries ?? []);
    } catch {
      setEntries([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-sm text-ink-lt">
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-border border-t-ink-lt" />
        Loading history…
      </div>
    );
  }

  if (entries.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-border p-10 text-center">
        <p className="text-sm font-semibold text-ink-lt">No activity yet</p>
        <p className="mt-1 text-xs text-ink-lt">Your sent emails, posts, and Reddit submissions appear here.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <p className="text-xs text-ink-lt">{entries.length} entries</p>
        <button onClick={load} className="text-xs font-medium text-coral hover:underline">
          Refresh
        </button>
      </div>
      <div className="overflow-hidden rounded-2xl border border-border bg-white">
        <table className="w-full text-left text-sm">
          <thead className="bg-navy-dark text-white">
            <tr>
              <th className="px-4 py-3 font-semibold">Date</th>
              <th className="px-4 py-3 font-semibold">Channel</th>
              <th className="px-4 py-3 font-semibold">Preview</th>
              <th className="px-4 py-3 text-right font-semibold">Recipients</th>
              <th className="px-4 py-3 font-semibold">Link</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry, i) => {
              const style = CHANNEL_STYLES[entry.channel];
              return (
                <tr key={entry.id} className={i % 2 === 0 ? "bg-white" : "bg-cream"}>
                  <td className="px-4 py-3 text-xs text-ink-lt whitespace-nowrap">
                    {new Date(entry.sentAt).toLocaleString()}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`rounded-full px-2.5 py-0.5 text-[11px] font-bold ${style.className}`}>
                      {style.label}
                    </span>
                    {entry.notes && (
                      <span className="ml-1.5 text-[11px] text-ink-lt">{entry.notes}</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-ink-mid max-w-xs truncate">
                    {entry.preview}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums text-ink-mid">
                    {entry.recipientCount ?? "—"}
                  </td>
                  <td className="px-4 py-3">
                    {entry.postUrl ? (
                      <a
                        href={entry.postUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-coral hover:underline"
                      >
                        View →
                      </a>
                    ) : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
