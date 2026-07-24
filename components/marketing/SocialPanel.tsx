"use client";

import { useEffect, useState } from "react";

type BlueskyConfig = { configured: boolean; handle: string | null };
type TwitterConfig = { configured: boolean };

const REDDIT_SUBREDDITS = [
  { id: "ADHD", url: "https://reddit.com/r/ADHD/submit", rules: "No links in body · Personal experience framing" },
  { id: "Notion", url: "https://reddit.com/r/Notion/submit", rules: "Links OK · 'What worked for me' framing" },
  { id: "productivity", url: "https://reddit.com/r/productivity/submit", rules: "Links OK · Practical system post" },
  { id: "neurodivergent", url: "https://reddit.com/r/neurodivergent/submit", rules: "No links · Vulnerable, personal framing" },
];

function StatusDot({ ok }: { ok: boolean }) {
  return (
    <span className={`inline-block h-2 w-2 rounded-full ${ok ? "bg-mint" : "bg-ink-lt"}`} />
  );
}

function SetupInstructions({ platform }: { platform: "bluesky" | "twitter" }) {
  const steps =
    platform === "bluesky"
      ? [
          "Create a Bluesky account at bsky.app (free)",
          "Go to Settings → App Passwords → Add App Password",
          'Name it "Focus Dock", copy the generated password',
          "Add to Vercel env vars: BLUESKY_HANDLE and BLUESKY_APP_PASSWORD",
          "Redeploy (or the next deploy picks it up automatically)",
        ]
      : [
          "Go to developer.twitter.com and create a project + app",
          "Under 'User authentication settings', enable OAuth 1.0a with Read & Write",
          "Generate Access Token & Secret under 'Keys and Tokens'",
          "Add 4 env vars to Vercel: X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET",
          "Note: Free tier allows 1,500 posts/month — more than enough",
        ];

  return (
    <ol className="mt-3 space-y-2">
      {steps.map((step, i) => (
        <li key={i} className="flex gap-3 text-sm text-ink-mid">
          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-navy-dark text-[10px] font-bold text-white">
            {i + 1}
          </span>
          {step}
        </li>
      ))}
    </ol>
  );
}

function BlueskyCard({ initialText = "" }: { initialText?: string }) {
  const [config, setConfig] = useState<BlueskyConfig | null>(null);
  const [text, setText] = useState(initialText);
  const [posting, setPosting] = useState(false);
  const [result, setResult] = useState<{ url: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showSetup, setShowSetup] = useState(false);

  useEffect(() => {
    fetch("/api/admin/marketing/bluesky")
      .then((r) => r.json())
      .then(setConfig)
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (initialText) setText(initialText);
  }, [initialText]);

  const charCount = [...text].length;
  const overLimit = charCount > 300;

  async function post() {
    setPosting(true);
    setError(null);
    try {
      const res = await fetch("/api/admin/marketing/bluesky", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Post failed");
      setResult({ url: data.url });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Post failed");
    } finally {
      setPosting(false);
    }
  }

  return (
    <div className="rounded-2xl border border-border bg-white p-5 space-y-4">
      <div className="flex items-center gap-2.5">
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#0085FF] text-sm font-bold text-white">B</span>
        <div>
          <p className="text-sm font-semibold text-navy-dark">Bluesky</p>
          {config && (
            <div className="flex items-center gap-1.5 text-xs text-ink-lt">
              <StatusDot ok={config.configured} />
              {config.configured ? `Connected as @${config.handle}` : "Not configured"}
            </div>
          )}
        </div>
        {!config?.configured && (
          <button
            onClick={() => setShowSetup(!showSetup)}
            className="ml-auto text-xs font-medium text-coral hover:underline"
          >
            Setup guide
          </button>
        )}
      </div>

      {showSetup && !config?.configured && (
        <div className="rounded-xl bg-cream p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-ink-lt">How to connect Bluesky</p>
          <SetupInstructions platform="bluesky" />
        </div>
      )}

      {config?.configured && (
        <>
          <div className="space-y-1.5">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={5}
              placeholder="Write your Bluesky post…"
              className="w-full resize-none rounded-xl border border-border bg-cream px-4 py-3 text-sm text-ink focus:border-[#0085FF] focus:outline-none"
            />
            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-lt">Links in text auto-detect as clickable</span>
              <span className={`text-xs tabular-nums ${overLimit ? "font-bold text-coral" : "text-ink-lt"}`}>
                {charCount}/300
              </span>
            </div>
          </div>

          {error && <p className="text-sm text-coral">{error}</p>}

          {result ? (
            <a
              href={result.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 rounded-xl bg-[#0085FF] px-4 py-2 text-sm font-semibold text-white hover:opacity-90"
            >
              ✓ Posted — View on Bluesky →
            </a>
          ) : (
            <button
              onClick={post}
              disabled={posting || overLimit || !text.trim()}
              className="rounded-xl bg-[#0085FF] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-50"
            >
              {posting ? "Posting…" : "Post to Bluesky"}
            </button>
          )}
        </>
      )}
    </div>
  );
}

function TwitterCard({ initialText = "" }: { initialText?: string }) {
  const [config, setConfig] = useState<TwitterConfig | null>(null);
  const [text, setText] = useState(initialText);
  const [posting, setPosting] = useState(false);
  const [result, setResult] = useState<{ url: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showSetup, setShowSetup] = useState(false);

  useEffect(() => {
    fetch("/api/admin/marketing/twitter")
      .then((r) => r.json())
      .then(setConfig)
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (initialText) setText(initialText);
  }, [initialText]);

  const charCount = [...text].length;
  const overLimit = charCount > 280;

  async function post() {
    setPosting(true);
    setError(null);
    try {
      const res = await fetch("/api/admin/marketing/twitter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Post failed");
      setResult({ url: data.url });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Post failed");
    } finally {
      setPosting(false);
    }
  }

  return (
    <div className="rounded-2xl border border-border bg-white p-5 space-y-4">
      <div className="flex items-center gap-2.5">
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-black text-sm font-bold text-white">𝕏</span>
        <div>
          <p className="text-sm font-semibold text-navy-dark">X / Twitter</p>
          {config && (
            <div className="flex items-center gap-1.5 text-xs text-ink-lt">
              <StatusDot ok={config.configured} />
              {config.configured ? "Connected" : "Not configured"}
            </div>
          )}
        </div>
        <button
          onClick={() => setShowSetup(!showSetup)}
          className="ml-auto text-xs font-medium text-coral hover:underline"
        >
          {showSetup ? "Hide" : config?.configured ? "Setup" : "Setup guide"}
        </button>
      </div>

      {showSetup && (
        <div className="rounded-xl bg-cream p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-ink-lt">How to connect X / Twitter</p>
          <SetupInstructions platform="twitter" />
        </div>
      )}

      {config?.configured && (
        <>
          <div className="space-y-1.5">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={5}
              placeholder="Write your tweet…"
              className="w-full resize-none rounded-xl border border-border bg-cream px-4 py-3 text-sm text-ink focus:border-black focus:outline-none"
            />
            <span className={`block text-right text-xs tabular-nums ${overLimit ? "font-bold text-coral" : "text-ink-lt"}`}>
              {charCount}/280
            </span>
          </div>

          {error && <p className="text-sm text-coral">{error}</p>}

          {result ? (
            <a
              href={result.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 rounded-xl bg-black px-4 py-2 text-sm font-semibold text-white hover:opacity-80"
            >
              ✓ Posted — View on X →
            </a>
          ) : (
            <button
              onClick={post}
              disabled={posting || overLimit || !text.trim()}
              className="rounded-xl bg-black px-4 py-2 text-sm font-semibold text-white transition hover:opacity-80 disabled:opacity-40"
            >
              {posting ? "Posting…" : "Post to X"}
            </button>
          )}
        </>
      )}

      {!config?.configured && !showSetup && (
        <p className="text-sm text-ink-lt">
          Add your X API credentials to Vercel env vars to enable posting.
        </p>
      )}
    </div>
  );
}

function RedditCard() {
  const [subreddit, setSubreddit] = useState(REDDIT_SUBREDDITS[0]);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [marked, setMarked] = useState(false);

  async function generateDraft() {
    setLoading(true);
    try {
      const res = await fetch("/api/admin/marketing/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          angle: `reddit_${subreddit.id}`,
          context: { totalSales: 0, totalRevenue: 0, subscriberCount: 0 },
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      setTitle(data.reddit?.title ?? "");
      setBody(data.reddit?.body ?? "");
    } catch (e) {
      alert(e instanceof Error ? e.message : "Generation failed");
    } finally {
      setLoading(false);
    }
  }

  async function markPosted() {
    await fetch("/api/admin/marketing/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        channel: "reddit",
        preview: title.slice(0, 100),
        notes: `r/${subreddit.id}`,
      }),
    });
    setMarked(true);
  }

  return (
    <div className="rounded-2xl border border-border bg-white p-5 space-y-4">
      <div className="flex items-center gap-2.5">
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#FF4500] text-sm font-bold text-white">r</span>
        <div>
          <p className="text-sm font-semibold text-navy-dark">Reddit</p>
          <p className="text-xs text-ink-lt">Manual posting — AI drafts only</p>
        </div>
      </div>

      <div className="rounded-xl bg-yellow/10 border border-yellow/40 px-4 py-3 text-xs text-ink-mid">
        Reddit prohibits automated posting in r/ADHD, r/Notion, and r/productivity. AI writes the draft — you post it manually. This avoids bans and keeps engagement authentic.
      </div>

      {/* Subreddit selector */}
      <div className="flex flex-wrap gap-2">
        {REDDIT_SUBREDDITS.map((sub) => (
          <button
            key={sub.id}
            onClick={() => { setSubreddit(sub); setTitle(""); setBody(""); setMarked(false); }}
            className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
              subreddit.id === sub.id
                ? "bg-[#FF4500] text-white"
                : "border border-border text-ink-mid hover:border-[#FF4500]/50"
            }`}
          >
            r/{sub.id}
          </button>
        ))}
      </div>
      <p className="text-xs text-ink-lt">{subreddit.rules}</p>

      <button
        onClick={generateDraft}
        disabled={loading}
        className="flex items-center gap-2 rounded-xl border border-border bg-cream px-4 py-2 text-sm font-semibold text-ink-mid transition hover:bg-cream-dk disabled:opacity-60"
      >
        {loading ? (
          <><span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-ink-lt border-t-ink-mid" />Generating…</>
        ) : (
          "Generate draft for r/" + subreddit.id
        )}
      </button>

      {(title || body) && (
        <div className="space-y-3">
          <div className="space-y-1.5">
            <p className="text-xs font-semibold text-ink-lt">Title</p>
            <textarea
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              rows={2}
              className="w-full resize-none rounded-xl border border-border bg-cream px-4 py-2 text-sm text-ink focus:border-[#FF4500] focus:outline-none"
            />
          </div>
          <div className="space-y-1.5">
            <p className="text-xs font-semibold text-ink-lt">Body</p>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={8}
              className="w-full resize-none rounded-xl border border-border bg-cream px-4 py-2 text-sm text-ink focus:border-[#FF4500] focus:outline-none"
            />
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => navigator.clipboard.writeText(`${title}\n\n${body}`)}
              className="rounded-xl border border-border px-3 py-1.5 text-xs font-semibold text-ink-mid hover:bg-cream-dk"
            >
              Copy post
            </button>
            <a
              href={subreddit.url}
              target="_blank"
              rel="noreferrer"
              className="rounded-xl border border-[#FF4500]/40 bg-[#FF4500]/10 px-3 py-1.5 text-xs font-semibold text-[#FF4500] hover:bg-[#FF4500]/20"
            >
              Open r/{subreddit.id} →
            </a>
            {marked ? (
              <span className="text-xs text-mint font-semibold">✓ Logged</span>
            ) : (
              <button
                onClick={markPosted}
                className="text-xs font-medium text-ink-lt hover:text-ink-mid hover:underline"
              >
                Mark as posted
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

type SocialPanelProps = {
  initialBlueSkyText?: string;
  initialTwitterText?: string;
};

export function SocialPanel({ initialBlueSkyText = "", initialTwitterText = "" }: SocialPanelProps) {
  return (
    <div className="space-y-4">
      <BlueskyCard initialText={initialBlueSkyText} />
      <TwitterCard initialText={initialTwitterText} />
      <RedditCard />
    </div>
  );
}
