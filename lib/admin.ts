import { createHmac, timingSafeEqual } from "node:crypto";
import { cookies } from "next/headers";

const COOKIE_NAME = "fd_admin";

export function isAdminConfigured() {
  return Boolean(process.env.ADMIN_PASSWORD?.length);
}

/**
 * Session token: HMAC of a fixed message keyed by the admin password.
 * Unforgeable without the password (unlike the previous literal "1").
 */
export function adminSessionToken(): string | null {
  const secret = process.env.ADMIN_PASSWORD;
  if (!secret) return null;
  return createHmac("sha256", secret).update("fd-admin-session-v1").digest("hex");
}

export async function isAdminAuthenticated() {
  const expected = adminSessionToken();
  if (!expected) return false;
  const cookieStore = await cookies();
  const got = cookieStore.get(COOKIE_NAME)?.value;
  if (!got || got.length !== expected.length) return false;
  return timingSafeEqual(Buffer.from(got), Buffer.from(expected));
}

export function adminCookieOptions() {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: 60 * 60 * 24 * 7,
  };
}

export function verifyAdminPassword(password: string) {
  const expected = process.env.ADMIN_PASSWORD;
  return Boolean(expected && password === expected);
}

export { COOKIE_NAME };
