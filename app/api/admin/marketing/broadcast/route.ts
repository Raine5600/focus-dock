import { NextResponse } from "next/server";
import { put } from "@vercel/blob";
import { isAdminAuthenticated } from "@/lib/admin";
import { sendBroadcastEmail } from "@/lib/mail";
import { getSubscriberEmailsForBroadcast, logMarketingEntry } from "@/lib/marketing";

export const runtime = "nodejs";
export const maxDuration = 60;

const BATCH_SIZE = 10;
const BATCH_DELAY_MS = 150;

export async function POST(req: Request) {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { subject, body: text, htmlBody } = (await req.json()) as {
    subject: string;
    body: string;
    htmlBody?: string;
  };

  if (!subject?.trim() || !text?.trim()) {
    return NextResponse.json({ error: "subject and body are required" }, { status: 400 });
  }

  const emails = await getSubscriberEmailsForBroadcast();
  if (emails.length === 0) {
    return NextResponse.json({ sent: 0, failed: 0, id: null, message: "No subscribers found" });
  }

  let sent = 0;
  let failed = 0;
  const id = `broadcast-${Date.now()}`;

  for (let i = 0; i < emails.length; i += BATCH_SIZE) {
    const batch = emails.slice(i, i + BATCH_SIZE);
    const results = await Promise.allSettled(
      batch.map((email) => sendBroadcastEmail(email, subject, text, htmlBody))
    );
    sent += results.filter((r) => r.status === "fulfilled").length;
    failed += results.filter((r) => r.status === "rejected").length;

    // Log progress to blob after each batch so partial sends are recoverable
    await put(
      `broadcasts/${id}-progress.json`,
      JSON.stringify({ id, sentAt: new Date().toISOString(), subject, sent, failed, total: emails.length }),
      { access: "public", addRandomSuffix: false }
    ).catch(() => {});

    if (i + BATCH_SIZE < emails.length) {
      await new Promise((r) => setTimeout(r, BATCH_DELAY_MS));
    }
  }

  // Write final broadcast record
  await put(
    `broadcasts/${id}.json`,
    JSON.stringify({ id, sentAt: new Date().toISOString(), subject, sent, failed, total: emails.length }),
    { access: "public", addRandomSuffix: false }
  ).catch(() => {});

  // Log to marketing history
  await logMarketingEntry({
    channel: "email",
    sentAt: new Date().toISOString(),
    preview: subject,
    recipientCount: sent,
  });

  return NextResponse.json({ sent, failed, id, total: emails.length });
}
