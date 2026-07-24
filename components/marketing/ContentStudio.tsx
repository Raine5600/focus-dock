"use client";

import { useState } from "react";

type Angle = "social_proof" | "adhd_empathy" | "affiliate" | "testimonial" | "urgency";

type GeneratedContent = {
  reddit: { title: string; body: string };
  twitter: string;
  bluesky: string;
  email: { subject: string; body: string };
};

type Props = {
  totalSales: number;
  totalRevenue: number;
  subscriberCount: number;
  onUseInBroadcast?: (subject: string, body: string) => void;
  onPostToBluesky?: (text: string) => void;
};

const ANGLES: { id: Angle; label: string; description: string }[] = [
  { id: "social_proof", label: "Social Proof", description: "Sales numbers + results" },
  { id: "adhd_empathy", label: "ADHD Empathy", description: "Lead with the feeling" },
  { id: "affiliate", label: "Affiliate Pitch", description: "40% commission, recruit partners" },
  { id: "testimonial", label: "Testimonial", description: "Customer transformation story" },
  { id: "urgency", label: "Sale Urgency", description: "$27 deal, limited time" },
];

function CopyButton({ text, label = "Copy" }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={async () => {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1800);
      }}
      className="rounded-lg border border-border px-3 py-1.5 text-xs font-semibold text-ink-mid transition hover:bg-cream-dk hover:text-navy-dark"
    >
      {copied ? "✓ Copied" : label}
    </button>
  );
}

function CharCount({ text, limit }: { text: string; limit: number }) {
  const len = [...text].length;
  const over = len > limit;
  return (
    <span className={`ml-auto text-xs tabular-nums ${over ? "font-bold text-coral" : "text-ink-lt"}`}>
      {len}/{limit}
    </span>
  );
}

export function ContentStudio({ totalSales, totalRevenue, subscriberCount, onUseInBroadcast, onPostToBluesky }: Props) {
  const [angle, setAngle] = useState<Angle>("adhd_empathy");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [content, setContent] = useState<GeneratedContent | null>(null);
  const [editedContent, setEditedContent] = useState<GeneratedContent | null>(null);
  const [postingBsky, setPostingBsky] = useState(false);
  const [bskyResult, setBskyResult] = useState<{ url: string } | null>(null);

  const active = editedContent ?? content;

  async function generate() {
    setLoading(true);
    setError(null);
    setBskyResult(null);
    try {
      const res = await fetch("/api/admin/marketing/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ angle, context: { totalSales, totalRevenue, subscriberCount } }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Generation failed");
      setContent(data);
      setEditedContent(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  function updateField(path: string[], value: string) {
    const base = editedContent ?? content;
    if (!base) return;
    const updated = JSON.parse(JSON.stringify(base)) as GeneratedContent;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let obj: any = updated;
    for (let i = 0; i < path.length - 1; i++) obj = obj[path[i]];
    obj[path[path.length - 1]] = value;
    setEditedContent(updated);
  }

  async function postBluesky() {
    if (!active?.bluesky) return;
    setPostingBsky(true);
    try {
      const res = await fetch("/api/admin/marketing/bluesky", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: active.bluesky }),
      });
      const data = await res.json();
      if (data.error === "not_configured") {
        onPostToBluesky?.(active.bluesky);
        return;
      }
      if (!res.ok) throw new Error(data.error ?? "Post failed");
      setBskyResult({ url: data.url });
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed to post");
    } finally {
      setPostingBsky(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Context strip */}
      <div className="flex flex-wrap gap-2">
        {[
          { label: "Sales", value: totalSales },
          { label: "Revenue", value: `$${(totalRevenue / 100).toFixed(0)}` },
          { label: "Subscribers", value: subscriberCount },
        ].map(({ label, value }) => (
          <span key={label} className="rounded-full bg-navy-dark px-3 py-1 text-xs font-semibold text-white">
            {value} {label}
          </span>
        ))}
      </div>

      {/* Angle selector */}
      <div>
        <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-ink-lt">Content angle</p>
        <div className="flex flex-wrap gap-2">
          {ANGLES.map((a) => (
            <button
              key={a.id}
              onClick={() => setAngle(a.id)}
              title={a.description}
              className={`rounded-full px-4 py-1.5 text-sm font-semibold transition ${
                angle === a.id
                  ? "bg-coral text-white"
                  : "border border-border bg-white text-ink-mid hover:border-coral/50 hover:text-navy-dark"
              }`}
            >
              {a.label}
            </button>
          ))}
        </div>
      </div>

      {/* Generate button */}
      <button
        onClick={generate}
        disabled={loading}
        className="flex items-center gap-2 rounded-xl bg-navy-dark px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-navy disabled:opacity-60"
      >
        {loading ? (
          <>
            <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
            Generating drafts…
          </>
        ) : (
          <>✦ Generate Drafts</>
        )}
      </button>

      {error && (
        <p className="rounded-xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">
          {error}
        </p>
      )}

      {/* Draft cards */}
      {active && (
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Reddit */}
          <div className="rounded-2xl border border-border bg-cream p-4 space-y-3">
            <div className="flex items-center gap-2">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-[#FF4500] text-[10px] font-bold text-white">r</span>
              <span className="text-sm font-semibold text-navy-dark">Reddit</span>
              <span className="ml-auto text-[11px] text-ink-lt">manual post</span>
            </div>
            <div className="space-y-1.5">
              <p className="text-xs font-semibold text-ink-lt">Title</p>
              <textarea
                className="w-full resize-none rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:border-coral focus:outline-none"
                rows={2}
                value={active.reddit.title}
                onChange={(e) => updateField(["reddit", "title"], e.target.value)}
              />
              <div className="flex gap-2">
                <CopyButton text={active.reddit.title} label="Copy title" />
              </div>
            </div>
            <div className="space-y-1.5">
              <p className="text-xs font-semibold text-ink-lt">Body</p>
              <textarea
                className="w-full resize-none rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:border-coral focus:outline-none"
                rows={7}
                value={active.reddit.body}
                onChange={(e) => updateField(["reddit", "body"], e.target.value)}
              />
              <div className="flex gap-2">
                <CopyButton text={active.reddit.body} label="Copy body" />
                <CopyButton text={`${active.reddit.title}\n\n${active.reddit.body}`} label="Copy all" />
              </div>
            </div>
          </div>

          {/* Bluesky */}
          <div className="rounded-2xl border border-border bg-cream p-4 space-y-3">
            <div className="flex items-center gap-2">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-[#0085FF] text-[10px] font-bold text-white">B</span>
              <span className="text-sm font-semibold text-navy-dark">Bluesky</span>
              <CharCount text={active.bluesky} limit={300} />
            </div>
            <textarea
              className="w-full resize-none rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:border-coral focus:outline-none"
              rows={5}
              value={active.bluesky}
              onChange={(e) => updateField(["bluesky"], e.target.value)}
            />
            <div className="flex flex-wrap gap-2">
              <CopyButton text={active.bluesky} />
              {bskyResult ? (
                <a
                  href={bskyResult.url}
                  target="_blank"
                  rel="noreferrer"
                  className="rounded-lg bg-[#0085FF] px-3 py-1.5 text-xs font-semibold text-white hover:opacity-90"
                >
                  ✓ View post →
                </a>
              ) : (
                <button
                  onClick={postBluesky}
                  disabled={postingBsky}
                  className="rounded-lg bg-[#0085FF] px-3 py-1.5 text-xs font-semibold text-white transition hover:opacity-90 disabled:opacity-60"
                >
                  {postingBsky ? "Posting…" : "Post to Bluesky"}
                </button>
              )}
            </div>
          </div>

          {/* X/Twitter */}
          <div className="rounded-2xl border border-border bg-cream p-4 space-y-3">
            <div className="flex items-center gap-2">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-black text-[10px] font-bold text-white">𝕏</span>
              <span className="text-sm font-semibold text-navy-dark">X / Twitter</span>
              <CharCount text={active.twitter} limit={280} />
            </div>
            <textarea
              className="w-full resize-none rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:border-coral focus:outline-none"
              rows={5}
              value={active.twitter}
              onChange={(e) => updateField(["twitter"], e.target.value)}
            />
            <CopyButton text={active.twitter} />
          </div>

          {/* Email */}
          <div className="rounded-2xl border border-border bg-cream p-4 space-y-3">
            <div className="flex items-center gap-2">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-navy text-[10px] font-bold text-white">@</span>
              <span className="text-sm font-semibold text-navy-dark">Email broadcast</span>
            </div>
            <div className="space-y-1.5">
              <p className="text-xs font-semibold text-ink-lt">Subject</p>
              <input
                type="text"
                className="w-full rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:border-coral focus:outline-none"
                value={active.email.subject}
                onChange={(e) => updateField(["email", "subject"], e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <p className="text-xs font-semibold text-ink-lt">Body</p>
              <textarea
                className="w-full resize-none rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:border-coral focus:outline-none"
                rows={6}
                value={active.email.body}
                onChange={(e) => updateField(["email", "body"], e.target.value)}
              />
            </div>
            <div className="flex flex-wrap gap-2">
              <CopyButton text={active.email.body} />
              <button
                onClick={() => onUseInBroadcast?.(active!.email.subject, active!.email.body)}
                className="rounded-lg border border-coral/40 bg-coral/10 px-3 py-1.5 text-xs font-semibold text-coral transition hover:bg-coral/20"
              >
                Use in Broadcast →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
