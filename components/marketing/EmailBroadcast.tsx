"use client";

import { useState } from "react";

type Props = {
  subscriberCount: number;
  initialSubject?: string;
  initialBody?: string;
};

type BroadcastResult = {
  sent: number;
  failed: number;
  total: number;
  id: string | null;
};

export function EmailBroadcast({ subscriberCount, initialSubject = "", initialBody = "" }: Props) {
  const [subject, setSubject] = useState(initialSubject);
  const [body, setBody] = useState(initialBody);
  const [preview, setPreview] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState<BroadcastResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const canSend = subject.trim().length > 0 && body.trim().length > 0 && subscriberCount > 0;

  async function send() {
    setSending(true);
    setConfirming(false);
    setError(null);
    try {
      const res = await fetch("/api/admin/marketing/broadcast", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, body }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Broadcast failed");
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setSending(false);
    }
  }

  if (result) {
    return (
      <div className="space-y-4">
        <div className="rounded-2xl border border-mint/40 bg-mint/10 p-5">
          <p className="font-semibold text-navy-dark">
            ✓ Broadcast sent
          </p>
          <p className="mt-1 text-sm text-ink-mid">
            {result.sent} delivered · {result.failed} failed · {result.total} total subscribers
          </p>
        </div>
        <button
          onClick={() => { setResult(null); setSubject(""); setBody(""); }}
          className="text-sm font-medium text-coral hover:underline"
        >
          Send another broadcast
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex items-center gap-3">
        <div className="rounded-full bg-navy-dark px-3 py-1 text-xs font-semibold text-white">
          {subscriberCount} subscriber{subscriberCount === 1 ? "" : "s"}
        </div>
        {subscriberCount === 0 && (
          <span className="text-xs text-ink-lt">No subscribers yet — collect emails via the lead magnet form.</span>
        )}
      </div>

      <div className="space-y-1.5">
        <label className="text-xs font-semibold uppercase tracking-wider text-ink-lt">
          Subject line
        </label>
        <input
          type="text"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="e.g. The Notion habit that actually stuck"
          className="w-full rounded-xl border border-border bg-white px-4 py-2.5 text-sm text-ink focus:border-coral focus:outline-none"
        />
        <p className="text-right text-xs tabular-nums text-ink-lt">{subject.length} chars</p>
      </div>

      <div className="space-y-1.5">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold uppercase tracking-wider text-ink-lt">
            Body
          </label>
          <button
            onClick={() => setPreview(!preview)}
            className="text-xs font-medium text-coral hover:underline"
          >
            {preview ? "← Edit" : "Preview →"}
          </button>
        </div>

        {preview ? (
          <div className="min-h-[180px] rounded-xl border border-border bg-white p-5">
            <p className="mb-3 text-sm font-semibold text-navy-dark">{subject || "(no subject)"}</p>
            <div className="whitespace-pre-wrap text-sm leading-relaxed text-ink-mid">{body}</div>
            <hr className="my-4 border-border" />
            <p className="text-xs text-ink-lt">
              Focus Dock · getfocusdock.com<br />
              Reply STOP to unsubscribe.
            </p>
          </div>
        ) : (
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={10}
            placeholder="Write your email body here. Plain text. Be conversational."
            className="w-full resize-none rounded-xl border border-border bg-white px-4 py-3 text-sm leading-relaxed text-ink focus:border-coral focus:outline-none"
          />
        )}
      </div>

      {error && (
        <p className="rounded-xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">
          {error}
        </p>
      )}

      {!confirming ? (
        <button
          onClick={() => setConfirming(true)}
          disabled={!canSend || sending}
          className="rounded-xl bg-coral px-5 py-2.5 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-40"
        >
          Send to {subscriberCount} subscriber{subscriberCount === 1 ? "" : "s"} →
        </button>
      ) : (
        <div className="rounded-xl border border-coral/40 bg-coral/10 p-4 space-y-3">
          <p className="text-sm font-semibold text-navy-dark">
            Send to {subscriberCount} subscribers? This cannot be undone.
          </p>
          <div className="flex gap-3">
            <button
              onClick={send}
              disabled={sending}
              className="rounded-xl bg-coral px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-60"
            >
              {sending ? "Sending…" : "Confirm Send"}
            </button>
            <button
              onClick={() => setConfirming(false)}
              className="rounded-xl border border-border bg-white px-4 py-2 text-sm font-semibold text-ink-mid hover:bg-cream-dk"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
