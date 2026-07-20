"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

function sessionId(): string {
  try {
    let sid = sessionStorage.getItem("fd_sid");
    if (!sid) {
      sid = crypto.randomUUID();
      sessionStorage.setItem("fd_sid", sid);
    }
    return sid;
  } catch {
    return "no-storage";
  }
}

export function trackEvent(ev: "pv" | "checkout_click", path?: string) {
  try {
    if (navigator.doNotTrack === "1") return;
    const payload = JSON.stringify({
      ev,
      path: path ?? window.location.pathname,
      sid: sessionId(),
      ref: document.referrer || undefined,
      utm:
        new URLSearchParams(window.location.search).get("utm_source") ??
        undefined,
    });
    if (!navigator.sendBeacon?.("/api/track", new Blob([payload], { type: "application/json" }))) {
      fetch("/api/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
        keepalive: true,
      }).catch(() => {});
    }
  } catch {
    // never break the page over analytics
  }
}

/** Fires a pageview on load and on every client-side route change. */
export function Track() {
  const pathname = usePathname();

  useEffect(() => {
    if (pathname) trackEvent("pv", pathname);
  }, [pathname]);

  return null;
}
