import { NextResponse } from "next/server";
import { isAdminAuthenticated } from "@/lib/admin";
import { getMarketingLog, logMarketingEntry, type MarketingChannel } from "@/lib/marketing";

export const runtime = "nodejs";

export async function GET() {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const entries = await getMarketingLog();
  return NextResponse.json({ entries });
}

export async function POST(req: Request) {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = (await req.json()) as {
    channel: MarketingChannel;
    preview: string;
    recipientCount?: number;
    postUrl?: string;
    notes?: string;
  };

  if (!body.channel || !body.preview) {
    return NextResponse.json({ error: "channel and preview are required" }, { status: 400 });
  }

  const id = await logMarketingEntry({
    channel: body.channel,
    sentAt: new Date().toISOString(),
    preview: body.preview,
    recipientCount: body.recipientCount,
    postUrl: body.postUrl,
    notes: body.notes,
  });

  return NextResponse.json({ ok: true, id });
}
