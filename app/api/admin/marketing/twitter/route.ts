import { NextResponse } from "next/server";
import { isAdminAuthenticated } from "@/lib/admin";
import { postToTwitter, logMarketingEntry } from "@/lib/marketing";

export const runtime = "nodejs";

export async function GET() {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  return NextResponse.json({
    configured: !!(
      process.env.X_API_KEY &&
      process.env.X_API_KEY_SECRET &&
      process.env.X_ACCESS_TOKEN &&
      process.env.X_ACCESS_TOKEN_SECRET
    ),
  });
}

export async function POST(req: Request) {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const missing =
    !process.env.X_API_KEY ||
    !process.env.X_API_KEY_SECRET ||
    !process.env.X_ACCESS_TOKEN ||
    !process.env.X_ACCESS_TOKEN_SECRET;

  if (missing) {
    return NextResponse.json({ error: "not_configured" }, { status: 400 });
  }

  const { text } = (await req.json()) as { text: string };
  if (!text?.trim()) {
    return NextResponse.json({ error: "text is required" }, { status: 400 });
  }

  try {
    const result = await postToTwitter(text);

    await logMarketingEntry({
      channel: "twitter",
      sentAt: new Date().toISOString(),
      preview: text.slice(0, 100),
      postUrl: result.url,
    });

    return NextResponse.json(result);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
