"use client";

import { useState } from "react";
import { ContentStudio } from "./marketing/ContentStudio";
import { EmailBroadcast } from "./marketing/EmailBroadcast";
import { SocialPanel } from "./marketing/SocialPanel";
import { PostHistory } from "./marketing/PostHistory";

type Tab = "studio" | "broadcast" | "social" | "history";

const TABS: { id: Tab; label: string }[] = [
  { id: "studio", label: "Content Studio" },
  { id: "broadcast", label: "Email Broadcast" },
  { id: "social", label: "Social" },
  { id: "history", label: "History" },
];

type Props = {
  subscriberCount: number;
  totalSales: number;
  totalRevenue: number;
};

export function MarketingHub({ subscriberCount, totalSales, totalRevenue }: Props) {
  const [tab, setTab] = useState<Tab>("studio");
  const [broadcastSubject, setBroadcastSubject] = useState("");
  const [broadcastBody, setBroadcastBody] = useState("");
  const [bskyText, setBskyText] = useState("");
  const [twitterText, setTwitterText] = useState("");

  function useInBroadcast(subject: string, body: string) {
    setBroadcastSubject(subject);
    setBroadcastBody(body);
    setTab("broadcast");
  }

  function useInBluesky(text: string) {
    setBskyText(text);
    setTab("social");
  }

  return (
    <section className="overflow-hidden rounded-2xl border border-border bg-white shadow-sm">
      <div className="border-b border-border px-6 pt-5 pb-0">
        <div className="flex items-baseline justify-between">
          <h2 className="font-display text-lg font-semibold text-navy-dark">
            Marketing Hub
          </h2>
          <p className="text-xs text-ink-lt">AI-assisted · admin only</p>
        </div>
        <div className="mt-4 flex gap-1 overflow-x-auto">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`shrink-0 rounded-t-lg px-4 py-2 text-sm font-semibold transition ${
                tab === t.id
                  ? "border-b-2 border-coral text-coral"
                  : "text-ink-lt hover:text-ink-mid"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="p-6">
        {tab === "studio" && (
          <ContentStudio
            totalSales={totalSales}
            totalRevenue={totalRevenue}
            subscriberCount={subscriberCount}
            onUseInBroadcast={useInBroadcast}
            onPostToBluesky={useInBluesky}
          />
        )}
        {tab === "broadcast" && (
          <EmailBroadcast
            subscriberCount={subscriberCount}
            initialSubject={broadcastSubject}
            initialBody={broadcastBody}
          />
        )}
        {tab === "social" && (
          <SocialPanel
            initialBlueSkyText={bskyText}
            initialTwitterText={twitterText}
          />
        )}
        {tab === "history" && <PostHistory />}
      </div>
    </section>
  );
}
