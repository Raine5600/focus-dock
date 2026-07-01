import { NextResponse } from "next/server";
import {
  sendAffiliateApplicationEmail,
  type AffiliateApplicationPayload,
} from "@/lib/mail";

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function hasAtLeastOneContact(data: AffiliateApplicationPayload): boolean {
  return Boolean(
    data.phone ||
      data.instagram ||
      data.tiktok ||
      data.youtube ||
      data.website
  );
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const data: AffiliateApplicationPayload = {
      name: clean(body.name),
      email: clean(body.email),
      phone: clean(body.phone),
      instagram: clean(body.instagram),
      tiktok: clean(body.tiktok),
      youtube: clean(body.youtube),
      website: clean(body.website),
      audienceSize: clean(body.audienceSize),
      message: clean(body.message),
    };

    if (!data.name) {
      return NextResponse.json({ error: "Name is required." }, { status: 400 });
    }

    if (!data.email || !isValidEmail(data.email)) {
      return NextResponse.json(
        { error: "A valid email address is required." },
        { status: 400 }
      );
    }

    if (!hasAtLeastOneContact(data)) {
      return NextResponse.json(
        {
          error:
            "Add at least one way to reach you or view your work (phone, Instagram, TikTok, YouTube, or website).",
        },
        { status: 400 }
      );
    }

    await sendAffiliateApplicationEmail(data);

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Affiliate application error:", error);
    return NextResponse.json(
      {
        error:
          "We could not send your application right now. Please email hello@getfocusdock.com directly.",
      },
      { status: 500 }
    );
  }
}