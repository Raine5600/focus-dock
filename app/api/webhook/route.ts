import { NextResponse } from "next/server";
import Stripe from "stripe";
import { sendPurchaseDeliveryEmail, sendOwnerSaleNotification } from "@/lib/mail";
import { logPurchase } from "@/lib/purchases";
import { getStripe } from "@/lib/stripe";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  const stripe = getStripe();
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  if (!webhookSecret) {
    console.error("STRIPE_WEBHOOK_SECRET is not set");
    return NextResponse.json(
      { error: "Webhook not configured" },
      { status: 500 }
    );
  }

  const body = await req.text();
  const signature = req.headers.get("stripe-signature");

  if (!signature) {
    return NextResponse.json({ error: "Missing signature" }, { status: 400 });
  }

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    console.error("Webhook signature verification failed:", err);
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  try {
    if (event.type === "checkout.session.completed") {
      const session = event.data.object as Stripe.Checkout.Session;
      if (session.payment_status === "paid") {
        const record = await logPurchase(session);
        if (record.affiliateRef) {
          console.log(
            "[affiliate]",
            JSON.stringify({
              sessionId: session.id,
              affiliateRef: record.affiliateRef,
            })
          );
        }
        await Promise.all([
          record.email
            ? sendPurchaseDeliveryEmail({
                email: record.email,
                customerName: record.customerName,
                sessionId: session.id,
              })
            : Promise.resolve(),
          sendOwnerSaleNotification({
            email: record.email ?? "unknown",
            customerName: record.customerName,
            sessionId: session.id,
            amount: record.amount,
            currency: record.currency,
            affiliateRef: record.affiliateRef,
          }),
        ]);
      }
    }
  } catch (err) {
    console.error("Webhook handler error:", err);
    return NextResponse.json({ error: "Handler failed" }, { status: 500 });
  }

  return NextResponse.json({ received: true });
}