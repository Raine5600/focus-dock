import { NextResponse } from "next/server";
import { put, list } from "@vercel/blob";
import nodemailer from "nodemailer";
import { createHash } from "node:crypto";

function emailHash(email: string) {
  return createHash("sha256").update(email.toLowerCase().trim()).digest("hex").slice(0, 16);
}

async function alreadySubscribed(email: string): Promise<boolean> {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return false;
  try {
    const { blobs } = await list({ prefix: `subscribers/${emailHash(email)}` });
    return blobs.length > 0;
  } catch {
    return false;
  }
}

async function saveSubscriber(email: string) {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return;
  await put(
    `subscribers/${emailHash(email)}.json`,
    JSON.stringify({ email, subscribedAt: new Date().toISOString() }),
    { access: "private", contentType: "application/json", addRandomSuffix: false, allowOverwrite: true }
  );
}

async function sendWelcomeEmail(to: string) {
  if (!process.env.SMTP_USER || !process.env.SMTP_APP_PASSWORD) return;

  const transporter = nodemailer.createTransport({
    host: "smtp.zoho.com",
    port: 465,
    secure: true,
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_APP_PASSWORD },
  });

  await transporter.sendMail({
    from: `"Focus Dock" <${process.env.SMTP_USER}>`,
    to,
    subject: "Your Brain Dump formula 🧠",
    text: `Hey — here's the Brain Dump formula from Focus Dock.

THE 2-SECOND BRAIN DUMP FORMULA
─────────────────────────────────
When a thought hits: open your Brain Dump database in Notion and type it in. That's it. One field. No tags, no priority, no due date. Just capture and move on.

Once a week (Sunday works well) spend 10 minutes sorting what's there. Anything that needs doing becomes a task. Anything that doesn't gets archived or deleted.

The rule: capture takes 2 seconds. Processing happens later. Never at the same time.

─────────────────────────────────
That's the whole thing. Simple by design — because complexity is what broke your last system.

If you want the full 43-page recovery protocol that this fits into, it's at getfocusdock.com for $27.

— Cameron
Builder of Focus Dock
`,
    html: `
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f3ef;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <div style="max-width:560px;margin:40px auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <div style="background:#1a2b4a;padding:32px 40px;">
      <p style="margin:0;color:#5de6c8;font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">Focus Dock</p>
      <h1 style="margin:8px 0 0;color:#ffffff;font-size:24px;font-weight:700;line-height:1.3;">Your Brain Dump formula</h1>
    </div>
    <div style="padding:36px 40px;">
      <p style="margin:0 0 24px;color:#4a5568;font-size:16px;line-height:1.6;">Hey — here's the 2-second capture method, straight from the guide.</p>

      <div style="background:#f5f3ef;border-left:4px solid #e8643c;border-radius:8px;padding:24px 28px;margin-bottom:28px;">
        <p style="margin:0 0 8px;color:#e8643c;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">The formula</p>
        <p style="margin:0;color:#1a2b4a;font-size:16px;font-weight:600;line-height:1.5;">When a thought hits → open Brain Dump → type it → close it. Done.</p>
      </div>

      <p style="margin:0 0 16px;color:#4a5568;font-size:15px;line-height:1.7;"><strong style="color:#1a2b4a;">One field. No tags. No priority. No due date.</strong> Just the thought, captured in under 2 seconds. Processing happens later — never at the same time as capture.</p>

      <p style="margin:0 0 16px;color:#4a5568;font-size:15px;line-height:1.7;">Once a week (Sunday works), spend 10 minutes sorting what's there. Anything actionable becomes a task. Everything else gets archived or deleted.</p>

      <p style="margin:0 0 28px;color:#4a5568;font-size:15px;line-height:1.7;">That's the whole system. Simple on purpose — complexity is what broke your last setup.</p>

      <div style="border-top:1px solid #e8e6e1;padding-top:24px;">
        <p style="margin:0 0 16px;color:#4a5568;font-size:15px;line-height:1.7;">This is one piece of the full Focus Dock system — 43 pages covering the complete ADHD-friendly Notion rebuild, from recovering abandoned setups to staying consistent long-term.</p>
        <a href="https://www.getfocusdock.com" style="display:inline-block;background:#e8643c;color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;padding:14px 28px;border-radius:100px;">See the full guide — $27</a>
      </div>

      <p style="margin:32px 0 0;color:#9ca3af;font-size:13px;">— Cameron, Builder of Focus Dock<br><a href="https://www.getfocusdock.com" style="color:#9ca3af;">getfocusdock.com</a></p>
    </div>
  </div>
  <p style="text-align:center;color:#9ca3af;font-size:12px;padding:20px;">You signed up at getfocusdock.com. No spam, ever.</p>
</body>
</html>
    `.trim(),
  });
}

export async function POST(req: Request) {
  try {
    const { email } = (await req.json()) as { email?: string };
    if (!email || !email.includes("@")) {
      return NextResponse.json({ error: "Invalid email" }, { status: 400 });
    }

    const dupe = await alreadySubscribed(email);
    if (!dupe) {
      await Promise.all([saveSubscriber(email), sendWelcomeEmail(email)]);
    }

    // Return success even for dupes — no need to reveal whether email exists
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("[subscribe]", err);
    return NextResponse.json({ error: "Failed" }, { status: 500 });
  }
}
