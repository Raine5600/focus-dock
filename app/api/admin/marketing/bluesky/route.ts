import { NextResponse } from "next/server";
import { isAdminAuthenticated } from "@/lib/admin";
import { postToBluesky, logMarketingEntry } from "@/lib/marketing";

export const runtime = "nodejs";

export async function GET() {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  return NextResponse.json({
    configured: !!(process.env.BLUESKY_HANDLE && process.env.BLUESKY_APP_PASSWORD),
    handle: process.env.BLUESKY_HANDLE ?? null,
  });
}

export async function POST(req: Request) {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  if (!process.env.BLUESKY_HANDLE || !process.env.BLUESKY_APP_PASSWORD) {
    return NextResponse.json({ error: "not_configured" }, { status: 400 });
  }

  const { text } = (await req.json()) as { text: string };
  if (!text?.trim()) {
    return NextResponse.json({ error: "text is required" }, { status: 400 });
  }

  try {
    const result = await postToBluesky(text);

    await logMarketingEntry({
      channel: "bluesky",
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
