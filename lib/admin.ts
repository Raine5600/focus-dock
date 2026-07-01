import { cookies } from "next/headers";

const COOKIE_NAME = "rwb_admin";

export function isAdminConfigured() {
  return Boolean(process.env.ADMIN_PASSWORD?.length);
}

export async function isAdminAuthenticated() {
  const expected = process.env.ADMIN_PASSWORD;
  if (!expected) return false;
  const cookieStore = await cookies();
  return cookieStore.get(COOKIE_NAME)?.value === "1";
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