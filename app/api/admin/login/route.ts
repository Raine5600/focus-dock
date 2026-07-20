import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import {
  adminCookieOptions,
  adminSessionToken,
  COOKIE_NAME,
  verifyAdminPassword,
} from "@/lib/admin";

export async function POST(req: Request) {
  const { password } = (await req.json()) as { password?: string };

  if (!password || !verifyAdminPassword(password)) {
    return NextResponse.json({ error: "Invalid password" }, { status: 401 });
  }

  const token = adminSessionToken();
  if (!token) {
    return NextResponse.json({ error: "Admin not configured" }, { status: 500 });
  }

  const cookieStore = await cookies();
  cookieStore.set(COOKIE_NAME, token, adminCookieOptions());

  return NextResponse.json({ ok: true });
}