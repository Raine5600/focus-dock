import { NextResponse } from "next/server";
import { getAppUrl, getStripe } from "@/lib/stripe";
import { PRODUCT } from "@/lib/product";

export async function POST(req: Request) {
  try {
    const stripe = getStripe();
    const appUrl = getAppUrl();

    let affiliateRef: string | undefined;
    try {
      const body = await req.json();
      const raw = body?.affiliateRef;
      if (typeof raw === "string" && raw.trim()) {
        affiliateRef = raw.trim().slice(0, 64);
      }
    } catch {
      // Empty body is fine for direct checkout.
    }

    const metadata: Record<string, string> = {
      product_id: PRODUCT.id,
    };
    if (affiliateRef) {
      metadata.affiliate_ref = affiliateRef;
    }

    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card"],
      line_items: [
        {
          price_data: {
            currency: PRODUCT.currency,
            unit_amount: PRODUCT.price * 100,
            product_data: {
              name: PRODUCT.fullName,
              description: PRODUCT.description,
              metadata: {
                product_id: PRODUCT.id,
              },
            },
          },
          quantity: 1,
        },
      ],
      metadata,
      success_url: `${appUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${appUrl}/?canceled=1`,
      allow_promotion_codes: true,
    });

    if (!session.url) {
      return NextResponse.json(
        { error: "Failed to create checkout session" },
        { status: 500 }
      );
    }

    return NextResponse.json({ url: session.url });
  } catch (error) {
    console.error("Checkout error:", error);
    return NextResponse.json(
      {
        error:
          error instanceof Error ? error.message : "Checkout unavailable",
      },
      { status: 500 }
    );
  }
}