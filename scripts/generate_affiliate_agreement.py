#!/usr/bin/env python3
"""Generate the Focus Dock affiliate agreement PDF.

Usage:
  python3 scripts/generate_affiliate_agreement.py                    # blank template
  python3 scripts/generate_affiliate_agreement.py "Jane Doe" jane    # personalized
"""

import sys
from datetime import date
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    HRFlowable,
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent

TEAL = colors.HexColor("#2a9d8f")
TEAL_DEEP = colors.HexColor("#23606e")
NAVY = colors.HexColor("#24455c")
INK = colors.HexColor("#22313c")
MUTED = colors.HexColor("#6b7c88")
BG_BOX = colors.HexColor("#e9f4f2")

MARGIN = 0.9 * inch
CONTENT_W = letter[0] - 2 * MARGIN


def styles():
    base = dict(fontName="Helvetica", textColor=INK)
    return {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=20, leading=26, textColor=NAVY),
        "meta": ParagraphStyle("meta", fontSize=10, leading=15, textColor=MUTED, **{k: v for k, v in base.items() if k != "textColor"}),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=17, textColor=TEAL_DEEP, spaceBefore=13, spaceAfter=4),
        "body": ParagraphStyle("body", fontSize=10.5, leading=15.5, spaceAfter=6, **base),
        "bullet": ParagraphStyle("bullet", fontSize=10.5, leading=15.5, leftIndent=14, bulletIndent=4, spaceAfter=4, **base),
        "accept": ParagraphStyle("accept", fontName="Helvetica-Bold", fontSize=12, leading=17, textColor=NAVY),
        "sig_name": ParagraphStyle("sig_name", fontName="Times-BoldItalic", fontSize=22, leading=26, textColor=NAVY),
        "sig_meta": ParagraphStyle("sig_meta", fontSize=10, leading=14.5, textColor=MUTED, fontName="Helvetica"),
    }


def build(affiliate_name: str, code: str, sent_date: str, out_path: Path):
    st = styles()
    story = []

    logo = ROOT / "assets/logo_mark.png"
    if logo.exists():
        header = Table(
            [[RLImage(str(logo), width=44, height=44),
              Paragraph("FOCUS DOCK<br/><font size=11 color='#2a9d8f'>AFFILIATE AGREEMENT</font>", st["title"])]],
            colWidths=[56, CONTENT_W - 56],
        )
        header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 0)]))
        story.append(header)
    else:
        story.append(Paragraph("FOCUS DOCK — AFFILIATE AGREEMENT", st["title"]))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))
    story.append(Paragraph(
        f"<b>Effective date:</b> {sent_date} &nbsp;·&nbsp; "
        f"<b>Between:</b> Black Sheep Designs, operating “Focus Dock” (getfocusdock.com) — “we,” “us” &nbsp;·&nbsp; "
        f"<b>And:</b> {affiliate_name} — “you”",
        st["meta"],
    ))

    def sec(num, title, blocks):
        story.append(Paragraph(f"{num}. {title}", st["h2"]))
        for kind, text in blocks:
            if kind == "p":
                story.append(Paragraph(text, st["body"]))
            else:
                story.append(Paragraph(text, st["bullet"], bulletText="•"))

    sec("1", "The program", [
        ("p", "We sell the <i>Focus Dock — ADHD Notion Recovery Guide</i>, a digital PDF product "
              "(currently $27 USD; price may change). You’ll promote it to your audience using your unique tracked link: "
              f"<b>getfocusdock.com/{code}</b>"),
    ])
    sec("2", "Commission", [
        ("b", "You earn <b>40% of the net sale price</b> for each completed purchase attributed to your link "
              "(currently <b>$10.80 per sale</b> at the $27 price)."),
        ("b", "Attribution is <b>last-touch with a 30-day window</b>: if someone clicks your link and buys within 30 days, "
              "the sale is yours unless they clicked another affiliate’s link afterward."),
        ("b", "Customers have a <b>14-day money-back guarantee</b>. Commissions on refunded purchases are void and are "
              "deducted before payout."),
    ])
    sec("3", "Payouts", [
        ("b", "Commissions are tallied monthly and paid by the <b>15th of the following month</b>, allowing the refund window to clear."),
        ("b", "Payment via <b>PayPal</b> (or another method we agree to in writing) once your balance reaches <b>$20 minimum</b>; "
              "smaller balances roll over."),
        ("b", "We’ll send a sales/commission statement with each payout. You can request your current numbers anytime."),
    ])
    sec("4", "What you agree to", [
        ("b", "<b>Disclose the relationship.</b> Follow FTC guidelines (or your country’s equivalent): a clear “affiliate link” "
              "disclosure wherever you share the link."),
        ("b", "<b>Stay honest.</b> Focus Dock is an educational productivity guide. Don’t present it as medical treatment, therapy, "
              "or a cure for ADHD, and don’t invent results or testimonials."),
        ("b", "<b>No spam.</b> No unsolicited bulk email, comment spam, or misleading ads. No bidding on “Focus Dock” trademarks in "
              "paid search. No coupon/deal-site posting without our written OK."),
        ("b", "<b>No self-dealing.</b> Purchases you make through your own link don’t earn commission."),
    ])
    sec("5", "The boring-but-important part", [
        ("b", "You’re an <b>independent contractor</b> — this isn’t employment, a partnership, or an exclusive arrangement."),
        ("b", "You’re responsible for taxes on your commissions."),
        ("b", "Either of us may end this agreement with <b>14 days’ written notice</b> (email counts). Commissions properly earned "
              "before the end date still get paid. We may end it immediately for violations of section 4."),
        ("b", "We may update program terms (commission rate, product price) with 14 days’ email notice; changes apply to future sales only."),
        ("b", "This agreement is governed by the laws of the United States and the state in which Black Sheep Designs operates."),
    ])

    story.append(Spacer(1, 12))
    accept = Table(
        [[Paragraph(
            "HOW TO ACCEPT<br/><br/>"
            "Reply to this email with the exact words: <font color='#2a9d8f'>“I accept this agreement”</font><br/><br/>"
            "<font size=9.5 color='#6b7c88'>Your reply forms a binding electronic agreement between you and Black Sheep Designs, "
            "effective the date of your reply. Your tracked link goes live (or is confirmed) the same day.</font>",
            st["accept"],
        )]],
        colWidths=[CONTENT_W],
    )
    accept.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_BOX),
        ("BOX", (0, 0), (-1, -1), 1.5, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(accept)

    story.append(Spacer(1, 26))
    story.append(Paragraph("Signed,", st["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Cameron", st["sig_name"]))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width=2.4 * inch, thickness=0.8, color=MUTED, hAlign="LEFT", spaceAfter=4))
    story.append(Paragraph("Founder, Focus Dock · Black Sheep Designs<br/>blacksheepdesignscontact@gmail.com · getfocusdock.com", st["sig_meta"]))

    doc = SimpleDocTemplate(
        str(out_path), pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=0.8 * inch, bottomMargin=0.8 * inch,
        title="Focus Dock Affiliate Agreement", author="Black Sheep Designs",
    )
    doc.build(story)
    print(f"Generated: {out_path}")


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "[AFFILIATE NAME]"
    code = sys.argv[2] if len(sys.argv) > 2 else "[CODE]"
    sent = sys.argv[3] if len(sys.argv) > 3 else date.today().strftime("%B %d, %Y")
    slug = code if code != "[CODE]" else "template"
    out = ROOT / f"marketing/Focus_Dock_Affiliate_Agreement_{slug}.pdf"
    build(name, code, sent, out)


if __name__ == "__main__":
    main()
