#!/usr/bin/env python3
"""Generate Focus Dock social/meta images.

Outputs:
  app/opengraph-image.jpg + app/twitter-image.jpg          (1200x630 main card)
  app/affiliates/opengraph-image.jpg + twitter-image.jpg    (affiliate variant)
  app/icon.png (512) + app/apple-icon.png (180)             (lightning bolt)
  public/images/og-focus-dock.jpg                           (fallback/JSON-LD image)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

NAVY_DARK = (18, 21, 42)
NAVY = (26, 31, 61)
CORAL = (255, 107, 74)
MINT = (61, 214, 195)
YELLOW = (255, 217, 61)
OFF_WHITE = (250, 248, 245)
MUTED = (140, 148, 184)

W, H = 1200, 630


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


def dot_grid(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, step: int = 26):
    dot = (34, 40, 74)
    for x in range(x0, x1, step):
        for y in range(y0, y1, step):
            draw.ellipse([x, y, x + 3, y + 3], fill=dot)


def chip(draw, x, y, text, font, color, pad_x=22, pad_y=12):
    tw = draw.textlength(text, font=font)
    h = font.size + pad_y * 2
    draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + h], radius=h // 2, outline=color, width=3)
    draw.text((x + pad_x, y + pad_y), text, fill=color, font=font)
    return x + tw + pad_x * 2 + 16


def task_card(draw, img, x, y, w=380, h=190):
    """White 'DO THIS NEXT' card — the product's visual signature."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=20, fill=(255, 255, 255))
    draw.rectangle([x, y + 24, x + 10, y + h - 24], fill=CORAL)
    draw.text((x + 34, y + 28), "DO THIS NEXT", fill=CORAL, font=_font(24, bold=True))
    draw.text((x + 34, y + 70), "Put 3 dishes", fill=NAVY, font=_font(40, bold=True))
    draw.text((x + 34, y + 118), "in the sink", fill=NAVY, font=_font(40, bold=True))
    # mint check circle
    cx, cy, r = x + w - 56, y + 56, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MINT)
    draw.line([(cx - 12, cy), (cx - 3, cy + 10), (cx + 13, cy - 9)], fill=NAVY_DARK, width=6, joint="curve")


def og_card(tagline: str, chips: list[str], out_paths: list[Path]):
    img = Image.new("RGB", (W, H), NAVY_DARK)
    draw = ImageDraw.Draw(img)

    dot_grid(draw, 640, 40, 1180, 300)
    dot_grid(draw, 60, 470, 500, 610)
    # accent bars
    draw.rectangle([0, 0, W, 10], fill=CORAL)
    draw.rectangle([0, H - 10, W, H], fill=MINT)

    x = 80
    draw.text((x, 88), "THE ADHD NOTION RECOVERY GUIDE", fill=MINT, font=_font(30, bold=True))
    draw.text((x, 140), "FOCUS DOCK", fill=OFF_WHITE, font=_font(112, bold=True))
    draw.rounded_rectangle([x + 4, 278, x + 344, 288], radius=5, fill=YELLOW)

    draw.text((x, 322), tagline, fill=CORAL, font=_font(44, bold=True))

    cx = x
    chip_font = _font(28, bold=True)
    cy = 420
    for label in chips:
        cx = chip(draw, cx, cy, label, chip_font, MINT if chips.index(label) % 2 == 0 else OFF_WHITE)

    draw.text((x, 530), "getfocusdock.com", fill=MUTED, font=_font(26))

    task_card(draw, img, 780, 396)

    for path in out_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, "JPEG", quality=90, optimize=True)
        print(f"Generated: {path}")


def bolt_icon(size: int, out_path: Path):
    img = Image.new("RGB", (size, size), NAVY_DARK)
    draw = ImageDraw.Draw(img)
    # subtle ring
    m = size * 0.06
    draw.ellipse([m, m, size - m, size - m], outline=NAVY, width=max(2, size // 42))
    # lightning bolt
    pts = [
        (0.56, 0.10),
        (0.30, 0.56),
        (0.47, 0.56),
        (0.42, 0.90),
        (0.72, 0.42),
        (0.53, 0.42),
    ]
    draw.polygon([(px * size, py * size) for px, py in pts], fill=YELLOW)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    print(f"Generated: {out_path}")


def main():
    og_card(
        "Stop the setup spiral. Start doing.",
        ["43 pages", "3 databases", "$27"],
        [
            ROOT / "app/opengraph-image.jpg",
            ROOT / "app/twitter-image.jpg",
            ROOT / "public/images/og-focus-dock.jpg",
        ],
    )
    og_card(
        "Affiliate program — earn 40% per sale.",
        ["$10.80 / sale", "instant tracked links"],
        [
            ROOT / "app/affiliates/opengraph-image.jpg",
            ROOT / "app/affiliates/twitter-image.jpg",
        ],
    )
    bolt_icon(512, ROOT / "app/icon.png")
    bolt_icon(180, ROOT / "app/apple-icon.png")


if __name__ == "__main__":
    main()
