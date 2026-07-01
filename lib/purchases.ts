import { list, put } from "@vercel/blob";
import Stripe from "stripe";
import { getStripe } from "@/lib/stripe";

export type PurchaseRecord = {
  id: string;
  email: string | null;
  customerName: string | null;
  amount: number;
  currency: string;
  productId: string | null;
  affiliateRef: string | null;
  purchasedAt: string;
  paymentStatus: string;
};

export function recordFromSession(
  session: Stripe.Checkout.Session
): PurchaseRecord {
  return {
    id: session.id,
    email: session.customer_details?.email ?? null,
    customerName: session.customer_details?.name ?? null,
    amount: session.amount_total ?? 0,
    currency: session.currency ?? "usd",
    productId: session.metadata?.product_id ?? null,
    affiliateRef: session.metadata?.affiliate_ref ?? null,
    purchasedAt: new Date((session.created ?? 0) * 1000).toISOString(),
    paymentStatus: session.payment_status ?? "unknown",
  };
}

export async function logPurchase(
  session: Stripe.Checkout.Session
): Promise<PurchaseRecord> {
  const record = recordFromSession(session);

  console.log("[purchase]", JSON.stringify(record));

  if (process.env.BLOB_READ_WRITE_TOKEN) {
    await put(`purchases/${record.id}.json`, JSON.stringify(record, null, 2), {
      access: "private",
      contentType: "application/json",
      addRandomSuffix: false,
      allowOverwrite: true,
    });
  }

  return record;
}

export async function getPurchases(): Promise<PurchaseRecord[]> {
  if (process.env.BLOB_READ_WRITE_TOKEN) {
    const { blobs } = await list({ prefix: "purchases/" });
    const records = await Promise.all(
      blobs.map(async (blob) => {
        const res = await fetch(blob.url);
        if (!res.ok) return null;
        return (await res.json()) as PurchaseRecord;
      })
    );
    return records
      .filter((r): r is PurchaseRecord => r !== null)
      .sort((a, b) => b.purchasedAt.localeCompare(a.purchasedAt));
  }

  const stripe = getStripe();
  const sessions = await stripe.checkout.sessions.list({
    limit: 100,
    status: "complete",
  });

  return sessions.data
    .filter((session) => session.payment_status === "paid")
    .map(recordFromSession)
    .sort((a, b) => b.purchasedAt.localeCompare(a.purchasedAt));
}

export function formatAmount(amount: number, currency: string) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency.toUpperCase(),
  }).format(amount / 100);
}