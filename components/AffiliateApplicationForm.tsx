"use client";

import { useState, type FormEvent } from "react";
import { getContactEmail } from "@/lib/site";

type FormState = {
  name: string;
  email: string;
  phone: string;
  instagram: string;
  tiktok: string;
  youtube: string;
  website: string;
  audienceSize: string;
  message: string;
};

const INITIAL: FormState = {
  name: "",
  email: "",
  phone: "",
  instagram: "",
  tiktok: "",
  youtube: "",
  website: "",
  audienceSize: "",
  message: "",
};

export function AffiliateApplicationForm() {
  const [form, setForm] = useState<FormState>(INITIAL);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle"
  );
  const [errorMessage, setErrorMessage] = useState("");

  const helloEmail = getContactEmail("hello");

  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  const hasContact =
    Boolean(form.phone.trim()) ||
    Boolean(form.instagram.trim()) ||
    Boolean(form.tiktok.trim()) ||
    Boolean(form.youtube.trim()) ||
    Boolean(form.website.trim());

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("loading");
    setErrorMessage("");

    try {
      const response = await fetch("/api/affiliate-apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const payload = await response.json();

      if (!response.ok) {
        setStatus("error");
        setErrorMessage(payload.error || "Something went wrong. Please try again.");
        return;
      }

      setStatus("success");
      setForm(INITIAL);
    } catch {
      setStatus("error");
      setErrorMessage(
        `Something went wrong. You can also email ${helloEmail} directly.`
      );
    }
  }

  const inputClass =
    "mt-1.5 w-full rounded-xl border border-border bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-sage focus:ring-2 focus:ring-sage/20";

  const labelClass = "block text-sm font-medium text-navy-dark";

  if (status === "success") {
    return (
      <div className="rounded-2xl border border-sage/30 bg-sage-lt p-8 text-center">
        <p className="font-display text-2xl font-semibold text-navy-dark">
          Application sent
        </p>
        <p className="mt-3 text-sm leading-relaxed text-ink-mid">
          Thanks for applying. We&apos;ll review your details and reply to your
          email within a few business days.
        </p>
        <button
          type="button"
          onClick={() => setStatus("idle")}
          className="mt-6 text-sm font-semibold text-sage hover:underline"
        >
          Submit another application
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 text-left">
      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="affiliate-name" className={labelClass}>
            Your name <span className="text-rose">*</span>
          </label>
          <input
            id="affiliate-name"
            name="name"
            type="text"
            required
            autoComplete="name"
            value={form.name}
            onChange={(e) => updateField("name", e.target.value)}
            className={inputClass}
          />
        </div>
        <div>
          <label htmlFor="affiliate-email" className={labelClass}>
            Email <span className="text-rose">*</span>
          </label>
          <input
            id="affiliate-email"
            name="email"
            type="email"
            required
            autoComplete="email"
            value={form.email}
            onChange={(e) => updateField("email", e.target.value)}
            className={inputClass}
          />
        </div>
      </div>

      <div>
        <p className={labelClass}>
          How can we find you? <span className="text-rose">*</span>
        </p>
        <p className="mt-1 text-xs text-ink-lt">
          Fill in at least one (phone is optional). Email above is always required.
        </p>
        <div className="mt-3 grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="affiliate-phone" className="text-xs text-ink-mid">
              Phone
            </label>
            <input
              id="affiliate-phone"
              name="phone"
              type="tel"
              autoComplete="tel"
              placeholder="Optional"
              value={form.phone}
              onChange={(e) => updateField("phone", e.target.value)}
              className={inputClass}
            />
          </div>
          <div>
            <label htmlFor="affiliate-instagram" className="text-xs text-ink-mid">
              Instagram handle
            </label>
            <input
              id="affiliate-instagram"
              name="instagram"
              type="text"
              placeholder="@username"
              value={form.instagram}
              onChange={(e) => updateField("instagram", e.target.value)}
              className={inputClass}
            />
          </div>
          <div>
            <label htmlFor="affiliate-tiktok" className="text-xs text-ink-mid">
              TikTok handle
            </label>
            <input
              id="affiliate-tiktok"
              name="tiktok"
              type="text"
              placeholder="@username"
              value={form.tiktok}
              onChange={(e) => updateField("tiktok", e.target.value)}
              className={inputClass}
            />
          </div>
          <div>
            <label htmlFor="affiliate-youtube" className="text-xs text-ink-mid">
              YouTube channel
            </label>
            <input
              id="affiliate-youtube"
              name="youtube"
              type="text"
              placeholder="URL or @handle"
              value={form.youtube}
              onChange={(e) => updateField("youtube", e.target.value)}
              className={inputClass}
            />
          </div>
          <div className="sm:col-span-2">
            <label htmlFor="affiliate-website" className="text-xs text-ink-mid">
              Website or blog
            </label>
            <input
              id="affiliate-website"
              name="website"
              type="url"
              placeholder="https://"
              value={form.website}
              onChange={(e) => updateField("website", e.target.value)}
              className={inputClass}
            />
          </div>
        </div>
        {!hasContact && (
          <p className="mt-2 text-xs text-amber">
            Add at least one contact field besides email.
          </p>
        )}
      </div>

      <div>
        <label htmlFor="affiliate-audience" className={labelClass}>
          Audience size
        </label>
        <input
          id="affiliate-audience"
          name="audienceSize"
          type="text"
          placeholder="e.g. 45K on Instagram"
          value={form.audienceSize}
          onChange={(e) => updateField("audienceSize", e.target.value)}
          className={inputClass}
        />
      </div>

      <div>
        <label htmlFor="affiliate-message" className={labelClass}>
          Anything else we should know?
        </label>
        <textarea
          id="affiliate-message"
          name="message"
          rows={4}
          value={form.message}
          onChange={(e) => updateField("message", e.target.value)}
          className={`${inputClass} resize-y`}
        />
      </div>

      {status === "error" && (
        <p className="rounded-xl border border-rose/30 bg-rose/10 px-4 py-3 text-sm text-rose">
          {errorMessage}
        </p>
      )}

      <button
        type="submit"
        disabled={status === "loading" || !hasContact}
        className="w-full rounded-full bg-sage px-8 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-[#4d7762] disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
      >
        {status === "loading" ? "Sending…" : "Submit application"}
      </button>
    </form>
  );
}