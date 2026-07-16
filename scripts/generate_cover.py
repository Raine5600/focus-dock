#!/usr/bin/env python3
"""Generate full-page PDF cover — clean two-zone layout, title on top.

v2 refresh: drawn check circles (no [OK] text tokens), tighter hierarchy,
version bump. Layout stays the full-bleed thumbnail style.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "focus_dock_cover.png"

W, H = 1700, 2200
BAND_H = 660  # ~30% navy header band

NAVY = (26, 31, 61)
NAVY_LIGHT = (38, 45, 84)
CORAL = (255, 107, 74)
MINT = (61, 214, 195)
YELLOW = (255, 217, 61)
OFF_WHITE = (250, 248, 245)
DARK = (26, 26, 46)
MID = (61, 61, 92)
WHITE = (255, 255, 255)


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


def _check_circle(draw, cx, cy, r):
    """Mint circle with a hand-drawn white check mark."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MINT)
    w = max(4, r // 4)
    draw.line([(cx - r * 0.45, cy + r * 0.05), (cx - r * 0.1, cy + r * 0.4)],
              fill=WHITE, width=w)
    draw.line([(cx - r * 0.1, cy + r * 0.4), (cx + r * 0.5, cy - r * 0.35)],
              fill=WHITE, width=w)


def generate() -> Path:
    img = Image.new("RGB", (W, H), OFF_WHITE)
    draw = ImageDraw.Draw(img)

    # Navy header band with subtle inner panel + coral base rule
    draw.rectangle([0, 0, W, BAND_H], fill=NAVY)
    draw.rectangle([0, BAND_H - 8, W, BAND_H], fill=CORAL)
    # faint dock "segments" motif along the band bottom (5 lanes)
    seg_w, seg_gap, seg_y = 88, 26, BAND_H - 64
    total = 5 * seg_w + 4 * seg_gap
    x0 = (W - total) // 2
    for i in range(5):
        color = MINT if i == 0 else NAVY_LIGHT
        draw.rounded_rectangle(
            [x0 + i * (seg_w + seg_gap), seg_y, x0 + i * (seg_w + seg_gap) + seg_w, seg_y + 12],
            radius=6, fill=color,
        )

    title_font = _font(118, bold=True)
    sub_font = _font(40)
    tag_font = _font(34, bold=True)
    bullet_font = _font(31)
    small_font = _font(22)

    title = "FOCUS DOCK"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 96), title, fill=OFF_WHITE, font=title_font)

    subtitle = "The ADHD Notion Recovery Guide"
    sw = draw.textlength(subtitle, font=sub_font)
    draw.text(((W - sw) / 2, 250), subtitle, fill=MINT, font=sub_font)

    bar_w = int(tw * 0.5)
    draw.rounded_rectangle(
        [(W - bar_w) // 2, 330, (W + bar_w) // 2, 338], radius=4, fill=YELLOW,
    )

    tagline = "Stop the setup spiral. Start doing."
    tg = draw.textlength(tagline, font=tag_font)
    draw.text(((W - tg) / 2, 372), tagline, fill=CORAL, font=tag_font)

    # Body zone — promise bullets with drawn check circles
    bullets = [
        "Step-by-step recovery install",
        "3 databases — not 14",
        "One visible next task, always",
        "Task sequences for when you can't start",
        "Copy-paste formulas included",
        "No streak shame · short Sunday reset",
    ]
    y = BAND_H + 96
    for b in bullets:
        _check_circle(draw, 148, y + 18, 20)
        draw.text((196, y), b, fill=DARK, font=bullet_font)
        y += 74

    # Preview card — the product promise made concrete
    card_y = y + 56
    card_h = 240
    card_x = 120
    card_w = W - 240
    draw.rounded_rectangle([card_x + 8, card_y + 10, card_x + card_w + 8, card_y + card_h + 10],
                           radius=18, fill=(233, 229, 222))  # soft shadow
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                           radius=18, fill=WHITE, outline=CORAL, width=3)
    draw.rectangle([card_x, card_y + 14, card_x + 12, card_y + card_h - 14], fill=CORAL)
    draw.text((card_x + 36, card_y + 28), "DO THIS NEXT", fill=CORAL, font=_font(26, bold=True))
    draw.text((card_x + 36, card_y + 80), "Put 3 dishes in the sink", fill=NAVY, font=_font(48, bold=True))
    draw.text((card_x + 36, card_y + 158), "One task visible  ·  3 databases  ·  0 streak shame",
              fill=MID, font=_font(24))

    # Footer strip
    footer_y = H - 100
    draw.line([(100, footer_y), (W - 100, footer_y)], fill=MID, width=1)
    footer = "getfocusdock.com · Version 1 · July 2026"
    fw = draw.textlength(footer, font=small_font)
    draw.text(((W - fw) / 2, footer_y + 24), footer, fill=MID, font=small_font)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Generated: {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    generate()
