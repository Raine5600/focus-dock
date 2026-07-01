import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import {
  adminCookieOptions,
  COOKIE_NAME,
  verifyAdminPassword,
} from "@/lib/admin";

export async function POST(req: Request) {
  const { password } = (await req.json()) as { password?: string };

  if (!password || !verifyAdminPassword(password)) {
    return NextResponse.json({ error: "Invalid password" }, { status: 401 });
  }

  const cookieStore = await cookies();
  cookieStore.set(COOKIE_NAME, "1", adminCookieOptions());

  return NextResponse.json({ ok: true });
}