#!/usr/bin/env python3
"""Focus Dock brand mark — isometric document stack (teal/navy/beige).

Outputs:
  assets/logo_mark.png                     1024px transparent master
  app/icon.png (512) app/apple-icon.png    favicons
  app/favicon.ico (16/32/48)
  app/opengraph-image.jpg + twitter        1200x630 white brand card
  app/affiliates/* variants
  public/images/og-focus-dock.jpg
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

# palette sampled from the provided logo
TEAL = (42, 157, 143)
TEAL_DEEP = (35, 96, 110)
STEEL = (58, 107, 125)
NAVY = (36, 69, 92)
NAVY_DARK = (29, 53, 72)
DOC_FACE = (213, 227, 231)
DOC_LINE = (90, 140, 150)
BEIGE = (216, 203, 170)
WHITE_BG = (247, 247, 245)
MUTED = (120, 138, 148)


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


def rhombus(cx: float, cy: float, w: float):
    """Isometric top face (2:1 rhombus) centered at (cx, cy)."""
    h = w / 2
    return [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]


def draw_layer(draw, cx, cy, w, t, face, left_shade, right_shade, outline=None):
    """One stacked slab: top rhombus + left/right thickness faces."""
    top = rhombus(cx, cy, w)
    n, e, s, wpt = top
    # side faces (drop by t)
    draw.polygon([wpt, s, (s[0], s[1] + t), (wpt[0], wpt[1] + t)], fill=left_shade)
    draw.polygon([s, e, (e[0], e[1] + t), (s[0], s[1] + t)], fill=right_shade)
    draw.polygon(top, fill=face, outline=outline)


def draw_mark(size: int, bg=None) -> Image.Image:
    """The stacked-documents mark on transparent (or solid) background."""
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0) if bg is None else bg + (255,))
    draw = ImageDraw.Draw(img)

    cx = s * 0.5
    w = s * 0.80
    t = s * 0.075
    gap = s * 0.128

    # bottom → top slabs, darkening downward
    slabs = [
        (NAVY_DARK, (24, 42, 58), (20, 36, 50)),
        (STEEL, (44, 82, 96), (38, 70, 84)),
        ((77, 138, 138), (52, 100, 104), (45, 88, 92)),
    ]
    y = s * 0.62
    for face, left, right in slabs:
        draw_layer(draw, cx, y, w, t, face, left, right)
        y -= gap

    # top document layer
    draw_layer(draw, cx, y, w, t, DOC_FACE, (150, 176, 182), (128, 158, 166), outline=TEAL)
    # folder tab on the back-left edge
    tab_w = w * 0.28
    tcx = cx - w * 0.26
    tcy = y - w * 0.13
    draw.polygon(rhombus(tcx, tcy, tab_w), fill=TEAL)
    # document lines on the top face (iso-aligned with the NE edge)
    for i in range(3):
        ax = cx - w * 0.16 + i * w * 0.055
        ay = y + w * 0.03 + i * w * 0.055
        ln = w * (0.22 if i == 0 else 0.30)
        draw.line(
            [(ax, ay), (ax + ln, ay - ln / 2)],
            fill=DOC_LINE,
            width=max(2, s // 160),
        )
    return img


def og_card(subtitle: str, chips: list[str], out_paths: list[Path]):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), WHITE_BG)
    draw = ImageDraw.Draw(img)

    # soft accent bars
    draw.rectangle([0, 0, W, 8], fill=TEAL)
    draw.rectangle([0, H - 8, W, H], fill=NAVY)

    # mark on the left
    mark = draw_mark(430)
    img.paste(mark, (60, 100), mark)

    x = 520
    # wordmark
    f_big = _font(92, bold=True)
    focus_w = draw.textlength("FOCUS ", font=f_big)
    draw.text((x, 170), "FOCUS ", fill=BEIGE, font=f_big)
    draw.text((x + focus_w, 170), "DOCK", fill=TEAL, font=f_big)

    # divider with dot
    dy = 300
    draw.line([(x, dy), (x + 560, dy)], fill=(205, 214, 214), width=2)
    draw.ellipse([x + 270, dy - 7, x + 284, dy + 7], fill=TEAL)

    # subtitle, letterspaced caps — shrink until it fits the column
    track = 1.2
    for size in (27, 25, 23, 21):
        f_sub = _font(size, bold=True)
        total = sum(draw.textlength(c, font=f_sub) + track for c in subtitle)
        if total <= 620:
            break
    sx = x
    for ch in subtitle:
        draw.text((sx, 332), ch, fill=TEAL_DEEP, font=f_sub)
        sx += draw.textlength(ch, font=f_sub) + track

    # chips
    f_chip = _font(27, bold=True)
    cxp = x
    cy = 420
    for label in chips:
        tw = draw.textlength(label, font=f_chip)
        h = f_chip.size + 24
        draw.rounded_rectangle([cxp, cy, cxp + tw + 44, cy + h], radius=h // 2, outline=TEAL, width=3)
        draw.text((cxp + 22, cy + 12), label, fill=TEAL_DEEP, font=f_chip)
        cxp += tw + 44 + 14

    draw.text((x, 530), "getfocusdock.com", fill=MUTED, font=_font(26))

    for path in out_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, "JPEG", quality=90, optimize=True)
        print(f"Generated: {path}")


def main():
    master = draw_mark(1024)
    (ROOT / "assets").mkdir(exist_ok=True)
    master.save(ROOT / "assets/logo_mark.png", "PNG")
    print("Generated: assets/logo_mark.png")

    master.resize((512, 512), Image.LANCZOS).save(ROOT / "app/icon.png", "PNG")
    print("Generated: app/icon.png")

    apple = draw_mark(180, bg=WHITE_BG)
    apple.convert("RGB").save(ROOT / "app/apple-icon.png", "PNG")
    print("Generated: app/apple-icon.png")

    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    ico_base = draw_mark(256)
    ico_base.save(ROOT / "app/favicon.ico", sizes=ico_sizes)
    print("Generated: app/favicon.ico")

    og_card(
        "AN ADHD-FRIENDLY PRODUCTIVITY SYSTEM",
        ["43 pages", "3 databases", "$27"],
        [
            ROOT / "app/opengraph-image.jpg",
            ROOT / "app/twitter-image.jpg",
            ROOT / "public/images/og-focus-dock.jpg",
        ],
    )
    og_card(
        "AFFILIATE PROGRAM — EARN 40% PER SALE",
        ["$10.80 / sale", "tracked links"],
        [
            ROOT / "app/affiliates/opengraph-image.jpg",
            ROOT / "app/affiliates/twitter-image.jpg",
        ],
    )


if __name__ == "__main__":
    main()
