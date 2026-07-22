import nodemailer from "nodemailer";
import { PRODUCT } from "@/lib/product";
import { getSiteUrl } from "@/lib/site";

const SMTP_HOST = "smtppro.zoho.com";
const SMTP_PORT = 465;

export type AffiliateApplicationPayload = {
  name: string;
  email: string;
  phone?: string;
  instagram?: string;
  tiktok?: string;
  youtube?: string;
  website?: string;
  audienceSize?: string;
  message?: string;
};

function isSmtpConfigured(): boolean {
  return !!(process.env.SMTP_APP_PASSWORD || process.env.ZOHO_APP_PASSWORD);
}

function getSmtpConfig() {
  const user = process.env.SMTP_USER || "hello@getfocusdock.com";
  const pass = process.env.SMTP_APP_PASSWORD || process.env.ZOHO_APP_PASSWORD;

  if (!pass) {
    throw new Error("SMTP_APP_PASSWORD is not configured");
  }

  return { user, pass };
}

export type PurchaseDeliveryPayload = {
  email: string;
  customerName?: string | null;
  sessionId: string;
};

function formatPurchaseDeliveryBody(data: PurchaseDeliveryPayload): string {
  const appUrl = getSiteUrl();
  const downloadUrl = `${appUrl}/success?session_id=${data.sessionId}`;
  const greeting = data.customerName?.trim()
    ? `Hi ${data.customerName.trim()},`
    : "Hi there,";

  const lines = [
    greeting,
    "",
    `Thanks for purchasing ${PRODUCT.fullName}. Your download is ready.`,
    "",
    `Open your download page anytime:`,
    downloadUrl,
    "",
    "On that page you can download:",
    `- ${PRODUCT.fileName} (the full recovery guide)`,
    "- Focus_Dock_Formulas.txt (copy-paste Notion formulas)",
    "",
    "Start with the install protocol in the PDF. The formulas file is there when you reach the formula pages.",
    "",
    "Need help? Reply to this email or contact support@getfocusdock.com.",
    "",
    "— Focus Dock",
    "Stop the setup spiral. Start doing.",
  ];

  return lines.join("\n");
}

function formatApplicationBody(data: AffiliateApplicationPayload): string {
  const lines = [
    "New Focus Dock affiliate application",
    "",
    `Name: ${data.name}`,
    `Email: ${data.email}`,
    `Phone: ${data.phone || "(not provided)"}`,
    "",
    "Creator profiles:",
    `  Instagram: ${data.instagram || "(not provided)"}`,
    `  TikTok: ${data.tiktok || "(not provided)"}`,
    `  YouTube: ${data.youtube || "(not provided)"}`,
    `  Website: ${data.website || "(not provided)"}`,
    "",
    `Audience size: ${data.audienceSize || "(not provided)"}`,
    "",
    "Message:",
    data.message?.trim() || "(none)",
    "",
    `Submitted from: ${process.env.NEXT_PUBLIC_APP_URL || "https://getfocusdock.com"}/affiliates`,
  ];

  return lines.join("\n");
}

export async function sendPurchaseDeliveryEmail(
  data: PurchaseDeliveryPayload
): Promise<boolean> {
  if (!isSmtpConfigured()) {
    console.warn(
      "[mail] SMTP not configured — skipping purchase delivery email for",
      data.email
    );
    return false;
  }

  try {
    const { user, pass } = getSmtpConfig();
    const appUrl = getSiteUrl();
    const downloadUrl = `${appUrl}/success?session_id=${data.sessionId}`;

    const transporter = nodemailer.createTransport({
      host: SMTP_HOST,
      port: SMTP_PORT,
      secure: true,
      auth: { user, pass },
    });

    await transporter.sendMail({
      from: `"Focus Dock" <${user}>`,
      to: data.email,
      subject: `Your ${PRODUCT.name} download is ready`,
      text: formatPurchaseDeliveryBody(data),
      html: [
        `<p>${data.customerName?.trim() ? `Hi ${data.customerName.trim()},` : "Hi there,"}</p>`,
        `<p>Thanks for purchasing <strong>${PRODUCT.fullName}</strong>. Your download is ready.</p>`,
        `<p><a href="${downloadUrl}">Open your download page</a></p>`,
        `<p>On that page you can download the PDF guide and <code>Focus_Dock_Formulas.txt</code>.</p>`,
        `<p>Need help? Reply to this email.</p>`,
        `<p>— Focus Dock</p>`,
      ].join("\n"),
    });

    return true;
  } catch (err) {
    console.error("[mail] Failed to send purchase delivery email:", err);
    return false;
  }
}

export async function sendOwnerSaleNotification(
  data: PurchaseDeliveryPayload & { amount: number; currency: string; affiliateRef?: string | null }
): Promise<void> {
  if (!isSmtpConfigured()) return;
  try {
    const { user, pass } = getSmtpConfig();
    const transporter = nodemailer.createTransport({
      host: SMTP_HOST,
      port: SMTP_PORT,
      secure: true,
      auth: { user, pass },
    });

    const amountStr = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: data.currency.toUpperCase(),
    }).format(data.amount / 100);

    const lines = [
      `💸 New Focus Dock sale — ${amountStr}`,
      ``,
      `Customer: ${data.customerName ?? "Unknown"}`,
      `Email: ${data.email}`,
      `Amount: ${amountStr}`,
      `Affiliate: ${data.affiliateRef ?? "direct"}`,
      `Session: ${data.sessionId}`,
      `Time: ${new Date().toLocaleString("en-US", { timeZone: "America/New_York" })} ET`,
    ];

    await transporter.sendMail({
      from: `"Focus Dock" <${user}>`,
      to: "blacksheepdesignscontact@gmail.com",
      subject: `💸 Sale — ${amountStr}${data.affiliateRef ? ` via ${data.affiliateRef}` : ""}`,
      text: lines.join("\n"),
    });
  } catch (err) {
    console.error("[mail] Owner notification failed:", err);
  }
}

export async function sendAffiliateApplicationEmail(
  data: AffiliateApplicationPayload
): Promise<void> {
  const { user, pass } = getSmtpConfig();

  const transporter = nodemailer.createTransport({
    host: SMTP_HOST,
    port: SMTP_PORT,
    secure: true,
    auth: { user, pass },
  });

  await transporter.sendMail({
    from: `"Focus Dock" <${user}>`,
    to: user,
    replyTo: data.email,
    subject: `Affiliate Application — ${data.name}`,
    text: formatApplicationBody(data),
  });
}