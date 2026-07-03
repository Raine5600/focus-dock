#!/usr/bin/env python3
"""Generate full-page PDF cover — clean two-zone layout, title on top."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "focus_dock_cover.png"

W, H = 1700, 2200
BAND_H = 640  # ~29% navy header band

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
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def generate() -> Path:
    img = Image.new("RGB", (W, H), OFF_WHITE)
    draw = ImageDraw.Draw(img)

    # Navy header band
    draw.rectangle([0, 0, W, BAND_H], fill=NAVY)
    draw.rectangle([0, BAND_H - 6, W, BAND_H], fill=CORAL)

    title_font = _font(108, bold=True)
    sub_font = _font(38)
    tag_font = _font(32, bold=True)
    bullet_font = _font(30)
    small_font = _font(22)

    title = "FOCUS DOCK"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 100), title, fill=OFF_WHITE, font=title_font)

    subtitle = "The ADHD Notion Recovery Guide"
    sw = draw.textlength(subtitle, font=sub_font)
    draw.text(((W - sw) / 2, 230), subtitle, fill=MINT, font=sub_font)

    bar_w = int(tw * 0.55)
    draw.rounded_rectangle(
        [(W - bar_w) // 2, 300, (W + bar_w) // 2, 308],
        radius=3,
        fill=YELLOW,
    )

    tagline = "Stop the setup spiral. Start doing."
    tg = draw.textlength(tagline, font=tag_font)
    draw.text(((W - tg) / 2, 330), tagline, fill=CORAL, font=tag_font)

    # Body zone — promise bullets with clear spacing
    bullets = [
        "[OK]  Step-by-step recovery install",
        "[OK]  3 databases — not 14",
        "[OK]  One visible next task, always",
        "[OK]  Task sequences for when you can't start",
        "[OK]  Copy-paste formulas included",
        "[OK]  No streak shame · short Sunday reset",
    ]
    y = BAND_H + 80
    for b in bullets:
        draw.text((120, y), b, fill=DARK, font=bullet_font)
        y += 62

    # Simple preview card — centered in lower body, no overlap with bullets
    card_y = y + 40
    card_h = 220
    card_x = 120
    card_w = W - 240
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=CORAL, width=3)
    draw.rectangle([card_x, card_y, card_x + 10, card_y + card_h], fill=CORAL)
    draw.text((card_x + 28, card_y + 24), "DO THIS NEXT", fill=CORAL, font=_font(24, bold=True))
    draw.text((card_x + 28, card_y + 72), "Put 3 dishes in the sink", fill=NAVY, font=_font(44, bold=True))
    draw.text((card_x + 28, card_y + 140), "One task visible · 3 databases · 0 streak shame", fill=MID, font=small_font)

    # Footer strip
    footer_y = H - 100
    draw.line([(100, footer_y), (W - 100, footer_y)], fill=MID, width=1)
    footer = "getfocusdock.com · Version 1.0 · July 2026"
    fw = draw.textlength(footer, font=small_font)
    draw.text(((W - fw) / 2, footer_y + 24), footer, fill=MID, font=small_font)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Generated: {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    generate()