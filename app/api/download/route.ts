import fs from "fs";
import { NextRequest, NextResponse } from "next/server";
import { resolveDownloadFile } from "@/lib/download";
import { getStripe } from "@/lib/stripe";
import { PRODUCT } from "@/lib/product";

export const runtime = "nodejs";

export async function GET(req: NextRequest) {
  const sessionId = req.nextUrl.searchParams.get("session_id");

  if (!sessionId) {
    return NextResponse.json({ error: "Missing session_id" }, { status: 400 });
  }

  try {
    const stripe = getStripe();
    const session = await stripe.checkout.sessions.retrieve(sessionId);

    if (session.payment_status !== "paid") {
      return NextResponse.json(
        { error: "Payment not completed" },
        { status: 403 }
      );
    }

    if (session.metadata?.product_id !== PRODUCT.id) {
      return NextResponse.json({ error: "Invalid product" }, { status: 403 });
    }

    const fileParam = req.nextUrl.searchParams.get("file");
    const downloadFile = resolveDownloadFile(fileParam);

    if (!downloadFile) {
      console.error(
        "Download file unavailable:",
        fileParam === "formulas" ? "formulas" : "pdf"
      );
      return NextResponse.json(
        { error: "Product file unavailable" },
        { status: 500 }
      );
    }

    const buffer = fs.readFileSync(downloadFile.filePath);

    return new NextResponse(buffer, {
      status: 200,
      headers: {
        "Content-Type": downloadFile.contentType,
        "Content-Disposition": `attachment; filename="${downloadFile.fileName}"`,
        "Content-Length": String(buffer.length),
        "Cache-Control": "private, no-store",
      },
    });
  } catch (error) {
    console.error("Download error:", error);
    const isInvalidSession =
      error instanceof Error && "type" in error &&
      (error as { type?: string }).type === "StripeInvalidRequestError";
    return NextResponse.json(
      { error: "Unable to verify purchase" },
      { status: isInvalidSession ? 403 : 500 }
    );
  }
}