import { NextRequest, NextResponse } from "next/server";
import {
  AFFILIATE_COOKIE,
  AFFILIATE_COOKIE_MAX_AGE,
  logAffiliateClick,
  normalizeRef,
} from "@/lib/affiliates";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Affiliate entry link: https://<domain>/a/<code>
 * Sets a 30-day last-touch attribution cookie, logs the click,
 * and lands on the homepage with ?ref=<code> as a visible fallback.
 */
export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ code: string }> }
) {
  const { code: raw } = await params;
  const code = normalizeRef(raw);

  const target = new URL(code ? `/?ref=${code}` : "/", req.nextUrl.origin);
  const res = NextResponse.redirect(target, 307);

  if (code) {
    res.cookies.set(AFFILIATE_COOKIE, code, {
      maxAge: AFFILIATE_COOKIE_MAX_AGE,
      path: "/",
      sameSite: "lax",
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
    });
    await logAffiliateClick(code);
  }

  return res;
}
