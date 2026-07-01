#!/usr/bin/env python3
"""Generate full-page PDF cover image — YouTube-thumbnail principles, title on top."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "focus_dock_cover.png"

# Letter @ 200 DPI (good print quality, reasonable file size)
W, H = 1700, 2200

NAVY = (26, 31, 61)
CORAL = (255, 107, 74)
MINT = (61, 214, 195)
YELLOW = (255, 217, 61)
OFF_WHITE = (250, 248, 245)
DARK = (26, 26, 46)
MID = (61, 61, 92)


def _font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def generate() -> Path:
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle grid texture (thumbnail-style depth, not flat)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(32, 38, 72), width=1)
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(32, 38, 72), width=1)

    # Accent blobs — high contrast focal anchors (2–3 max per thumbnail research)
    draw.ellipse([(-120, 380), (420, 920)], fill=(*CORAL, 40) if img.mode == "RGBA" else (200, 70, 55))
    draw.ellipse([(W - 380, 120), (W + 80, 580)], fill=(45, 160, 145))
    draw.ellipse([(W // 2 - 200, H - 520), (W // 2 + 280, H - 80)], fill=(200, 170, 40))

    # Re-draw with proper alpha simulation via darker overlays
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse([(-120, 380), (420, 920)], fill=(255, 107, 74, 55))
    odraw.ellipse([(W - 380, 120), (W + 80, 580)], fill=(61, 214, 195, 45))
    odraw.ellipse([(W // 2 - 200, H - 520), (W // 2 + 280, H - 80)], fill=(255, 217, 61, 35))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # === TITLE ZONE (top third — thumbnail rule: title in upper safe zone) ===
    title_font = _font(118, bold=True)
    sub_font = _font(42, bold=False)
    badge_font = _font(28, bold=True)
    bullet_font = _font(34, bold=False)
    tag_font = _font(36, bold=True)
    small_font = _font(24, bold=False)

    draw.rectangle([0, 0, W, 520], fill=NAVY)

    title = "FOCUS DOCK"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 72), title, fill=OFF_WHITE, font=title_font)

    subtitle = "The ADHD Notion Recovery Guide"
    sw = draw.textlength(subtitle, font=sub_font)
    draw.text(((W - sw) / 2, 210), subtitle, fill=MINT, font=sub_font)

    # Yellow accent bar under title (visual anchor)
    bar_w = int(tw * 0.65)
    draw.rounded_rectangle(
        [(W - bar_w) // 2, 290, (W + bar_w) // 2, 302],
        radius=4,
        fill=YELLOW,
    )

    tagline = "Stop the setup spiral. Start doing."
    tg = draw.textlength(tagline, font=tag_font)
    draw.text(((W - tg) / 2, 330), tagline, fill=CORAL, font=tag_font)

    # === VISUAL ANCHOR: mock "Do This Next" card (center) ===
    card_x, card_y = 140, 580
    card_w, card_h = W - 280, 340
    _rounded_rect(draw, (card_x, card_y, card_x + card_w, card_y + card_h), 28, OFF_WHITE)
    draw.rectangle([card_x, card_y, card_x + 12, card_y + card_h], fill=CORAL)
    draw.text((card_x + 36, card_y + 28), "DO THIS NEXT", fill=CORAL, font=badge_font)
    draw.text((card_x + 36, card_y + 82), "Put 3 dishes in the sink", fill=NAVY, font=_font(52, bold=True))
    draw.text((card_x + 36, card_y + 155), "One visible task · 3 databases · 0 streak shame", fill=MID, font=small_font)

    # Timer badge (thumbnail-style number anchor)
    _rounded_rect(draw, (card_x + card_w - 200, card_y + 200, card_x + card_w - 36, card_y + 290), 16, MINT)
    draw.text((card_x + card_w - 175, card_y + 218), "47 MIN", fill=NAVY, font=_font(32, bold=True))
    draw.text((card_x + card_w - 168, card_y + 258), "INSTALL", fill=NAVY, font=_font(22, bold=True))

    # === Promise bullets (lower third) ===
    bullets = [
        "47-minute recovery install",
        "3 databases — not 14",
        "Task sequences for when you can't start",
        "Copy-paste formulas included",
        "No streak shame · 11-min Sunday reset",
    ]
    y = 980
    for b in bullets:
        _rounded_rect(draw, (120, y, 148, y + 28), 6, MINT)
        draw.text((132, y + 2), "✓", fill=NAVY, font=_font(22, bold=True))
        draw.text((168, y), b, fill=OFF_WHITE, font=bullet_font)
        y += 58

    # Bottom callout strip
    _rounded_rect(draw, (100, H - 200, W - 100, H - 100), 20, (36, 42, 78), outline=CORAL, width=3)
    cta = "For adults who've abandoned one too many Notion templates"
    cw = draw.textlength(cta, font=small_font)
    draw.text(((W - cw) / 2, H - 168), cta, fill=OFF_WHITE, font=small_font)
    footer = "getfocusdock.com · Version 1.0 · July 2026"
    fw = draw.textlength(footer, font=_font(20))
    draw.text(((W - fw) / 2, H - 128), footer, fill=MID, font=_font(20))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Generated: {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    generate()