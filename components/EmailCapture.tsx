"use client";

import { useState } from "react";
import { Reveal } from "./motion";

export function EmailCapture() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error();
      setStatus("success");
    } catch {
      setStatus("error");
    }
  }

  return (
    <section className="bg-navy py-20 sm:py-28">
      <div className="mx-auto max-w-2xl px-5 sm:px-8 text-center">
        <Reveal>
          <p className="text-sm font-bold uppercase tracking-widest text-mint">
            Free resource
          </p>
          <h2 className="mt-3 font-display text-3xl font-bold text-white sm:text-4xl">
            Get the Brain Dump formula free
          </h2>
          <p className="mt-4 text-lg text-white/70">
            The 2-second capture method from Focus Dock — so thoughts stop
            derailing your focus. Drop your email and it lands in your inbox
            instantly.
          </p>

          {status === "success" ? (
            <div className="mt-10 rounded-2xl border border-mint/30 bg-mint/10 px-8 py-6">
              <p className="text-lg font-semibold text-mint">You&apos;re in.</p>
              <p className="mt-1 text-white/70">Check your inbox — the formula is on its way.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-10 flex flex-col gap-3 sm:flex-row">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="flex-1 rounded-full border border-white/20 bg-white/10 px-5 py-3.5 text-white placeholder-white/40 outline-none focus:border-mint focus:bg-white/15"
              />
              <button
                type="submit"
                disabled={status === "loading"}
                className="rounded-full bg-coral px-7 py-3.5 font-semibold text-white transition hover:bg-coral/90 disabled:opacity-60 shrink-0"
              >
                {status === "loading" ? "Sending…" : "Send it to me"}
              </button>
            </form>
          )}

          {status === "error" && (
            <p className="mt-3 text-sm text-rose-400">Something went wrong — try again.</p>
          )}

          <p className="mt-4 text-xs text-white/40">
            No spam. Unsubscribe any time.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
