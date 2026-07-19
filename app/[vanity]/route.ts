import { NextRequest, NextResponse } from "next/server";
import {
  AFFILIATE_COOKIE,
  AFFILIATE_COOKIE_MAX_AGE,
  getAffiliate,
  logAffiliateClick,
  normalizeRef,
} from "@/lib/affiliates";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Vanity affiliate links: https://<domain>/<code> (e.g. /lakwad).
 * Only codes registered in lib/affiliates.ts resolve here — everything else
 * bounces to the homepage without setting attribution. The generic
 * /a/<code> route still accepts unregistered codes.
 */
export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ vanity: string }> }
) {
  const { vanity } = await params;
  const code = normalizeRef(vanity);
  const affiliate = code ? getAffiliate(code) : undefined;

  if (!affiliate) {
    return NextResponse.redirect(new URL("/", req.nextUrl.origin), 307);
  }

  const res = NextResponse.redirect(
    new URL(`/?ref=${affiliate.code}`, req.nextUrl.origin),
    307
  );
  res.cookies.set(AFFILIATE_COOKIE, affiliate.code, {
    maxAge: AFFILIATE_COOKIE_MAX_AGE,
    path: "/",
    sameSite: "lax",
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
  });
  await logAffiliateClick(affiliate.code);
  return res;
}
