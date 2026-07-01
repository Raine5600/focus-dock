import type { Metadata } from "next";
import { BRAND, PRODUCT } from "@/lib/product";
import { getSiteUrl } from "@/lib/site";

const SITE_NAME = BRAND.name;
export const DEFAULT_OG_IMAGE = "/images/og-focus-dock.jpg";
export const DEFAULT_OG_IMAGE_WIDTH = 1200;
export const DEFAULT_OG_IMAGE_HEIGHT = 630;

const DEFAULT_KEYWORDS = [
  "ADHD Notion guide",
  "ADHD productivity PDF",
  "Notion template abandoned",
  "plansturbation Notion",
  "executive dysfunction Notion",
  "ADHD task management",
  "Notion recovery guide",
  "ADHD friendly Notion setup",
  "task sequences Notion",
  BRAND.name,
  "getfocusdock",
] as const;

type PageSeoOptions = {
  title: string;
  description: string;
  path?: string;
  keywords?: string[];
  ogImage?: string;
  noIndex?: boolean;
};

export function buildPageMetadata(options: PageSeoOptions): Metadata {
  const siteUrl = getSiteUrl();
  const path = options.path ?? "";
  const canonical = `${siteUrl}${path}`;
  const ogImage = options.ogImage ?? DEFAULT_OG_IMAGE;
  const ogImageUrl = ogImage.startsWith("http") ? ogImage : `${siteUrl}${ogImage}`;

  const title = options.title.includes(SITE_NAME)
    ? options.title
    : `${options.title} | ${SITE_NAME}`;

  const keywords = [...DEFAULT_KEYWORDS, ...(options.keywords ?? [])];

  return {
    title,
    description: options.description,
    keywords: [...new Set(keywords)],
    authors: [{ name: SITE_NAME, url: siteUrl }],
    creator: SITE_NAME,
    publisher: SITE_NAME,
    metadataBase: new URL(siteUrl),
    alternates: { canonical },
    robots: options.noIndex
      ? { index: false, follow: false }
      : {
          index: true,
          follow: true,
          googleBot: {
            index: true,
            follow: true,
            "max-image-preview": "large",
            "max-snippet": -1,
            "max-video-preview": -1,
          },
        },
    openGraph: {
      type: "website",
      locale: "en_US",
      url: canonical,
      siteName: SITE_NAME,
      title,
      description: options.description,
      images: [
        {
          url: ogImageUrl,
          secureUrl: ogImageUrl,
          width: DEFAULT_OG_IMAGE_WIDTH,
          height: DEFAULT_OG_IMAGE_HEIGHT,
          type: "image/jpeg",
          alt: `Focus Dock — ADHD Notion Recovery Guide for adults with executive dysfunction`,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description: options.description,
      images: [ogImageUrl],
    },
    category: "Productivity",
  };
}

export function homeMetadata(): Metadata {
  return buildPageMetadata({
    title: `${BRAND.name} — ADHD Notion Recovery Guide`,
    description: `${PRODUCT.description} Summer sale: $${PRODUCT.price} (reg. $${PRODUCT.compareAt}). Instant PDF download.`,
    path: "/",
    keywords: [
      "buy ADHD Notion PDF",
      "Notion plansturbation fix",
      "ADHD executive dysfunction guide",
    ],
  });
}

export function affiliatesMetadata(): Metadata {
  return buildPageMetadata({
    title: `Affiliate Program — Earn 40% Commission`,
    description: `Partner with ${BRAND.name} and earn 40% ($10.80) per sale promoting our $${PRODUCT.price} ADHD Notion recovery guide. For ADHD/Notion creators and productivity YouTubers.`,
    path: "/affiliates",
    keywords: [
      "ADHD affiliate program",
      "Notion creator partnership",
      "productivity affiliate",
      "40 percent commission",
    ],
  });
}

export function productJsonLd() {
  const siteUrl = getSiteUrl();

  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": `${siteUrl}/#organization`,
        name: BRAND.name,
        url: siteUrl,
        logo: `${siteUrl}${DEFAULT_OG_IMAGE}`,
        image: `${siteUrl}${DEFAULT_OG_IMAGE}`,
        email: "hello@getfocusdock.com",
        description: BRAND.tagline,
      },
      {
        "@type": "WebSite",
        "@id": `${siteUrl}/#website`,
        url: siteUrl,
        name: BRAND.name,
        description: BRAND.tagline,
        publisher: { "@id": `${siteUrl}/#organization` },
        inLanguage: "en-US",
      },
      {
        "@type": "Product",
        "@id": `${siteUrl}/#product`,
        name: PRODUCT.fullName,
        description: PRODUCT.description,
        image: `${siteUrl}${DEFAULT_OG_IMAGE}`,
        brand: { "@type": "Brand", name: BRAND.name },
        offers: {
          "@type": "Offer",
          url: siteUrl,
          priceCurrency: PRODUCT.currency.toUpperCase(),
          price: PRODUCT.price,
          availability: "https://schema.org/InStock",
          itemCondition: "https://schema.org/NewCondition",
        },
        audience: {
          "@type": "PeopleAudience",
          audienceType: "Adults with ADHD using Notion",
        },
      },
    ],
  };
}

export function affiliatesJsonLd() {
  const siteUrl = getSiteUrl();

  return {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: `${BRAND.name} Affiliate Program`,
    description: `Earn 40% commission promoting the ${PRODUCT.name}.`,
    url: `${siteUrl}/affiliates`,
    isPartOf: { "@id": `${siteUrl}/#website` },
    about: { "@id": `${siteUrl}/#product` },
    inLanguage: "en-US",
  };
}