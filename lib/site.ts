import { BRAND } from "./product";

export const RECOMMENDED_DOMAIN = "getfocusdock.com";

export function getSiteUrl(): string {
  if (process.env.NEXT_PUBLIC_APP_URL) {
    return process.env.NEXT_PUBLIC_APP_URL.replace(/\/$/, "");
  }
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }
  return `https://${RECOMMENDED_DOMAIN}`;
}

export function getContactEmail(kind: "support" | "hello" | "partnerships" = "support"): string {
  const override = process.env.NEXT_PUBLIC_CONTACT_EMAIL;
  if (override) return override;

  const domain = process.env.NEXT_PUBLIC_EMAIL_DOMAIN || RECOMMENDED_DOMAIN;
  const prefixes = {
    support: "support",
    hello: "hello",
    partnerships: "partnerships",
  };
  return `${prefixes[kind]}@${domain}`;
}

export function getBrandWithDomain() {
  return {
    ...BRAND,
    domain: process.env.NEXT_PUBLIC_EMAIL_DOMAIN || RECOMMENDED_DOMAIN,
    siteUrl: getSiteUrl(),
    supportEmail: getContactEmail("support"),
    helloEmail: getContactEmail("hello"),
    partnershipsEmail: getContactEmail("partnerships"),
  };
}