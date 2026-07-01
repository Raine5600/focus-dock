"use client";

import { useState } from "react";

export function AdminLogin() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      if (!res.ok) throw new Error("Invalid password");
      window.location.reload();
    } catch {
      setError("Wrong password. Try again.");
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm rounded-2xl border border-border bg-white p-8 shadow-sm">
      <h1 className="font-display text-2xl font-semibold text-navy-dark">
        Purchase log
      </h1>
      <p className="mt-2 text-sm text-ink-mid">Enter your admin password.</p>
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Admin password"
          className="w-full rounded-xl border border-border bg-cream px-4 py-3 text-ink outline-none focus:border-sage"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-full bg-navy-dark px-4 py-3 font-semibold text-white transition hover:bg-navy disabled:opacity-70"
        >
          {loading ? "Signing in…" : "View purchases"}
        </button>
        {error ? <p className="text-sm text-rose">{error}</p> : null}
      </form>
    </div>
  );
}