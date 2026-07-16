#!/usr/bin/env python3
"""Focus Dock cover — Version 2.

Full-bleed navy design: dot-grid texture, big title block, a card-stack
illustration of the "one visible next task" promise, feature chips, and the
five-segment dock motif. Output: assets/focus_dock_cover_v2.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "focus_dock_cover_v2.png"

W, H = 1700, 2200

NAVY = (26, 31, 61)
NAVY_DEEP = (20, 24, 48)
NAVY_LIGHT = (40, 47, 88)
NAVY_LIGHTER = (54, 62, 110)
CORAL = (255, 107, 74)
MINT = (61, 214, 195)
YELLOW = (255, 217, 61)
OFF_WHITE = (250, 248, 245)
WHITE = (255, 255, 255)
MUTED = (150, 156, 190)
CARD_GHOST_TEXT = (98, 106, 150)


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


def _tracked_text(draw, xy, text, font, fill, tracking=0):
    """Draw text with letter-spacing; returns end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, fill=fill, font=font)
        x += draw.textlength(ch, font=font) + tracking
    return x


def _tracked_width(draw, text, font, tracking=0):
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)


def _check_circle(draw, cx, cy, r, circle=MINT, mark=NAVY):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=circle)
    w = max(4, r // 4)
    draw.line([(cx - r * 0.45, cy + r * 0.05), (cx - r * 0.1, cy + r * 0.4)], fill=mark, width=w)
    draw.line([(cx - r * 0.1, cy + r * 0.4), (cx + r * 0.5, cy - r * 0.35)], fill=mark, width=w)


def _dot_grid(draw, x0, y0, x1, y1, gap=46, r=2, color=NAVY_LIGHT):
    y = y0
    while y <= y1:
        x = x0
        while x <= x1:
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
            x += gap
        y += gap


def _ghost_card(draw, x, y, w, h, radius=22):
    """Dimmed background card with placeholder text bars."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=NAVY_LIGHT)
    draw.rounded_rectangle([x + 36, y + 34, x + 200, y + 56], radius=10, fill=CARD_GHOST_TEXT)
    draw.rounded_rectangle([x + 36, y + 76, x + w - 220, y + 104], radius=12, fill=NAVY_LIGHTER)


def generate() -> Path:
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # --- Backdrop: deep base, angled sheen, corner dot grids -----------------
    draw.rectangle([0, 0, W, H], fill=NAVY)
    draw.polygon([(0, 0), (W, 0), (W, 330), (0, 520)], fill=NAVY_DEEP)
    draw.polygon([(0, H), (W, H), (W, H - 260), (0, H - 130)], fill=NAVY_DEEP)
    _dot_grid(draw, 90, 620, 560, 900)
    _dot_grid(draw, W - 560, 1580, W - 90, 1860)

    # coral corner accent
    draw.polygon([(W, 0), (W, 190), (W - 190, 0)], fill=CORAL)
    draw.polygon([(0, H), (0, H - 190), (190, H)], fill=MINT)

    # --- Title block ----------------------------------------------------------
    eyebrow_font = _font(30, bold=True)
    eyebrow = "THE ADHD NOTION RECOVERY GUIDE"
    ew = _tracked_width(draw, eyebrow, eyebrow_font, tracking=10)
    _tracked_text(draw, ((W - ew) / 2, 210), eyebrow, eyebrow_font, MINT, tracking=10)

    title_font = _font(172, bold=True)
    title = "FOCUS DOCK"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 275), title, fill=OFF_WHITE, font=title_font)

    # yellow underline bar
    bar_w = 300
    draw.rounded_rectangle([(W - bar_w) // 2, 500, (W + bar_w) // 2, 512], radius=6, fill=YELLOW)

    tag_font = _font(42, bold=True)
    tagline = "Stop the setup spiral. Start doing."
    tg = draw.textlength(tagline, font=tag_font)
    draw.text(((W - tg) / 2, 552), tagline, fill=CORAL, font=tag_font)

    # --- Card stack illustration ---------------------------------------------
    stack_w = 1180
    stack_x = (W - stack_w) // 2
    # two ghost cards peeking behind
    _ghost_card(draw, stack_x + 90, 760, stack_w - 180, 150)
    _ghost_card(draw, stack_x + 45, 830, stack_w - 90, 165)

    # front card — the one visible task
    card_y, card_h = 930, 330
    draw.rounded_rectangle([stack_x + 14, card_y + 16, stack_x + stack_w + 14, card_y + card_h + 16],
                           radius=26, fill=NAVY_DEEP)  # shadow
    draw.rounded_rectangle([stack_x, card_y, stack_x + stack_w, card_y + card_h],
                           radius=26, fill=WHITE, outline=CORAL, width=4)
    draw.rounded_rectangle([stack_x + 22, card_y + 26, stack_x + 38, card_y + card_h - 26],
                           radius=8, fill=CORAL)
    draw.text((stack_x + 74, card_y + 44), "DO THIS NEXT", fill=CORAL, font=_font(34, bold=True))
    draw.text((stack_x + 74, card_y + 118), "Put 3 dishes in the sink",
              fill=NAVY, font=_font(62, bold=True))
    draw.text((stack_x + 74, card_y + 226), "Everything else stays hidden until this is done.",
              fill=(110, 116, 150), font=_font(30))
    _check_circle(draw, stack_x + stack_w - 96, card_y + card_h // 2, 52, circle=MINT, mark=NAVY)

    # --- Feature chips ---------------------------------------------------------
    chip_font = _font(30, bold=True)
    chips = ["3 databases — not 14", "One visible task", "No streak shame"]
    pad_x, chip_h, gap = 38, 78, 30
    widths = [draw.textlength(c, font=chip_font) + 2 * pad_x for c in chips]
    total = sum(widths) + gap * (len(chips) - 1)
    cx = (W - total) / 2
    cy = 1400
    for c, cw in zip(chips, widths):
        draw.rounded_rectangle([cx, cy, cx + cw, cy + chip_h], radius=chip_h // 2,
                               outline=MINT, width=3)
        draw.text((cx + pad_x, cy + (chip_h - 36) / 2), c, fill=OFF_WHITE, font=chip_font)
        cx += cw + gap

    # --- Supporting promise lines ----------------------------------------------
    line_font = _font(33)
    lines = [
        "A recovery protocol for everyone who abandoned",
        "yet another Notion template — install a working",
        "3-database system in one sitting.",
    ]
    ly = 1580
    for ln in lines:
        lw = draw.textlength(ln, font=line_font)
        draw.text(((W - lw) / 2, ly), ln, fill=MUTED, font=line_font)
        ly += 52

    # --- Dock motif + footer -----------------------------------------------------
    seg_w, seg_gap, seg_y = 96, 28, 1830
    total = 5 * seg_w + 4 * seg_gap
    x0 = (W - total) // 2
    for i in range(5):
        color = MINT if i == 0 else NAVY_LIGHTER
        draw.rounded_rectangle([x0 + i * (seg_w + seg_gap), seg_y,
                                x0 + i * (seg_w + seg_gap) + seg_w, seg_y + 14],
                               radius=7, fill=color)
    label_font = _font(24, bold=True)
    label = "5 SECTIONS · READ ONLY WHAT YOU NEED"
    lw = _tracked_width(draw, label, label_font, tracking=6)
    _tracked_text(draw, ((W - lw) / 2, seg_y + 44), label, label_font, MUTED, tracking=6)

    footer_font = _font(24)
    draw.line([(120, H - 120), (W - 120, H - 120)], fill=NAVY_LIGHTER, width=2)
    footer = "getfocusdock.com · Version 2 · July 2026"
    fw = draw.textlength(footer, font=footer_font)
    draw.text(((W - fw) / 2, H - 92), footer, fill=MUTED, font=footer_font)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Generated: {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    generate()
