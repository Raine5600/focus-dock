#!/usr/bin/env python3
"""Liquid-wave Notion cover in the Focus Dock palette.

Deep navy base with flowing coral / mint / yellow ribbons — summed sine
curves at different frequencies give the organic liquid look, heavy blur
on back layers adds depth, sharper front ribbons keep it crisp.

Output: public/images/notion-cover.jpg (1500x600, Notion's cover ratio).
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter

W, H = 1500, 600
SS = 2  # supersample factor for smooth edges
w, h = W * SS, H * SS

NAVY_DARK = (18, 21, 42)
NAVY = (26, 31, 61)
CORAL = (255, 107, 74)
MINT = (61, 214, 195)
YELLOW = (255, 217, 61)

random.seed(7)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size, top, bottom):
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        d.line([(0, y), (size[0], y)], fill=lerp(top, bottom, y / size[1]))
    return img


def wave_ys(x, base_y, amp, freqs, phases, drift=0.0):
    """Sum of sines — multi-frequency for the liquid feel."""
    y = base_y + drift * x
    for (f, a_frac), ph in zip(freqs, phases):
        y += amp * a_frac * math.sin(2 * math.pi * f * x / w + ph)
    return y


def ribbon(base_y, amp, thickness, freqs, phases, color, alpha, blur, drift=0.0):
    """One flowing band rendered onto its own RGBA layer."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    step = 8
    top_pts = []
    bot_pts = []
    for x in range(-step, w + step * 2, step):
        y = wave_ys(x, base_y, amp, freqs, phases, drift)
        top_pts.append((x, y))
        # thickness also undulates slightly for a fluid, non-uniform body
        t = thickness * (1 + 0.25 * math.sin(2 * math.pi * 1.3 * x / w + phases[0]))
        bot_pts.append((x, y + t))
    d.polygon(top_pts + bot_pts[::-1], fill=color + (alpha,))
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return layer


# --- Base: deep navy gradient ------------------------------------------------
img = vertical_gradient((w, h), NAVY_DARK, NAVY).convert("RGBA")

# --- Back layers: big soft blurred washes (depth) ----------------------------
back = [
    # (base_y, amp, thickness, color, alpha, blur, drift)
    (h * 0.30, 90 * SS, 300 * SS, MINT, 34, 60 * SS, 0.02),
    (h * 0.60, 110 * SS, 300 * SS, CORAL, 36, 70 * SS, -0.03),
]
for base_y, amp, th, col, alpha, blur, drift in back:
    freqs = [(0.8, 1.0), (1.7, 0.45), (3.1, 0.18)]
    phases = [random.uniform(0, 2 * math.pi) for _ in freqs]
    img = Image.alpha_composite(img, ribbon(base_y, amp, th, freqs, phases, col, alpha, blur, drift))

# --- Mid layers: defined translucent ribbons ---------------------------------
mid = [
    (h * 0.38, 70 * SS, 140 * SS, CORAL, 100, 18 * SS, -0.02),
    (h * 0.55, 85 * SS, 150 * SS, MINT, 85, 20 * SS, 0.03),
]
for base_y, amp, th, col, alpha, blur, drift in mid:
    freqs = [(1.1, 1.0), (2.3, 0.4), (4.2, 0.15)]
    phases = [random.uniform(0, 2 * math.pi) for _ in freqs]
    img = Image.alpha_composite(img, ribbon(base_y, amp, th, freqs, phases, col, alpha, blur, drift))

# --- Front layers: crisp thin highlight ribbons ------------------------------
front = [
    (h * 0.42, 75 * SS, 26 * SS, CORAL, 220, 3 * SS, -0.02),
    (h * 0.50, 80 * SS, 18 * SS, lerp(CORAL, (255, 255, 255), 0.35), 180, 2 * SS, -0.018),
    (h * 0.60, 90 * SS, 22 * SS, MINT, 210, 3 * SS, 0.028),
    (h * 0.66, 85 * SS, 12 * SS, lerp(MINT, (255, 255, 255), 0.3), 150, 2 * SS, 0.03),
    (h * 0.78, 65 * SS, 14 * SS, YELLOW, 160, 2 * SS, -0.012),
]
for base_y, amp, th, col, alpha, blur, drift in front:
    freqs = [(1.15, 1.0), (2.4, 0.38), (4.5, 0.12)]
    phases = [random.uniform(0, 2 * math.pi) for _ in freqs]
    img = Image.alpha_composite(img, ribbon(base_y, amp, th, freqs, phases, col, alpha, blur, drift))

# --- Re-ground the bottom in navy so ribbons pop instead of muddying ---------
ground = Image.new("RGBA", (w, h), (0, 0, 0, 0))
gg = ImageDraw.Draw(ground)
for y in range(int(h * 0.55), h):
    t = (y - h * 0.55) / (h * 0.45)
    gg.line([(0, y), (w, y)], fill=NAVY_DARK + (int(150 * t**1.6),))
img = Image.alpha_composite(img, ground)

# --- Corner glow accents ------------------------------------------------------
glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-w * 0.25, -h * 0.6, w * 0.35, h * 0.5], fill=MINT + (46,))
gd.ellipse([w * 0.68, h * 0.55, w * 1.25, h * 1.6], fill=CORAL + (52,))
glow = glow.filter(ImageFilter.GaussianBlur(120 * SS))
img = Image.alpha_composite(img, glow)

# --- Downsample + save --------------------------------------------------------
out = img.convert("RGB").resize((W, H), Image.LANCZOS)
out.save("public/images/notion-cover.jpg", quality=90)
print("wrote public/images/notion-cover.jpg")
