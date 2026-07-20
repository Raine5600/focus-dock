import { NextRequest, NextResponse } from "next/server";
import { AFFILIATE_COOKIE, normalizeRef } from "@/lib/affiliates";
import { deriveSource, logTrafficEvent } from "@/lib/traffic";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const EVENTS = new Set(["pv", "checkout_click"]);
const BOT_RE = /bot|crawl|spider|slurp|preview|headless|monitor|curl|wget/i;

/**
 * First-party traffic beacon. No PII: random session id, coarse country
 * (Vercel geo header), device class, path, derived source. Bots and
 * admin/API paths are ignored.
 */
export async function POST(req: NextRequest) {
  try {
    if (!process.env.BLOB_READ_WRITE_TOKEN) {
      return new NextResponse(null, { status: 204 });
    }

    const ua = req.headers.get("user-agent") ?? "";
    if (!ua || BOT_RE.test(ua)) {
      return new NextResponse(null, { status: 204 });
    }

    const body = (await req.json()) as {
      ev?: string;
      path?: string;
      sid?: string;
      ref?: string;
      utm?: string;
    };

    const ev = body.ev && EVENTS.has(body.ev) ? body.ev : null;
    const path =
      typeof body.path === "string" && body.path.startsWith("/")
        ? body.path.split("?")[0].slice(0, 120)
        : null;
    const sid =
      typeof body.sid === "string" && /^[a-z0-9-]{8,40}$/i.test(body.sid)
        ? body.sid
        : null;
    if (!ev || !path || !sid) {
      return new NextResponse(null, { status: 204 });
    }
    if (path.startsWith("/admin") || path.startsWith("/api")) {
      return new NextResponse(null, { status: 204 });
    }

    const affiliateRef = normalizeRef(
      req.cookies.get(AFFILIATE_COOKIE)?.value ?? null
    );
    const src = deriveSource(
      typeof body.ref === "string" ? body.ref.slice(0, 300) : null,
      typeof body.utm === "string" ? body.utm.slice(0, 60) : null,
      affiliateRef
    );

    await logTrafficEvent({
      ts: new Date().toISOString(),
      sid,
      ev: ev as "pv" | "checkout_click",
      path,
      src,
      country: req.headers.get("x-vercel-ip-country") ?? "",
      device: /mobile|android|iphone|ipad/i.test(ua) ? "mobile" : "desktop",
    });
  } catch {
    // Tracking must never break the site.
  }
  return new NextResponse(null, { status: 204 });
}
