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

# Tone-on-tone navy shades for depth (duotone look: navy + one coral accent)
NAVY_L1 = lerp(NAVY, (255, 255, 255), 0.06)
NAVY_L2 = lerp(NAVY, (255, 255, 255), 0.11)
NAVY_L3 = lerp(NAVY, (255, 255, 255), 0.17)

# --- Back: broad, soft tone-on-tone swells (subtle topography) ---------------
back = [
    # (base_y, amp, thickness, color, alpha, blur, drift)
    (h * 0.42, 90 * SS, 420 * SS, NAVY_L1, 160, 40 * SS, 0.015),
    (h * 0.62, 100 * SS, 400 * SS, NAVY_L2, 130, 30 * SS, -0.02),
    (h * 0.80, 80 * SS, 360 * SS, NAVY_L3, 110, 24 * SS, 0.01),
]
for base_y, amp, th, col, alpha, blur, drift in back:
    freqs = [(0.7, 1.0), (1.6, 0.4), (2.9, 0.15)]
    phases = [random.uniform(0, 2 * math.pi) for _ in freqs]
    img = Image.alpha_composite(img, ribbon(base_y, amp, th, freqs, phases, col, alpha, blur, drift))

# --- Accent: one crisp coral line with a soft echo ---------------------------
phases_main = [random.uniform(0, 2 * math.pi) for _ in range(3)]
freqs_main = [(1.0, 1.0), (2.1, 0.35), (3.8, 0.12)]
# soft wide glow under the line
img = Image.alpha_composite(
    img, ribbon(h * 0.52, 85 * SS, 60 * SS, freqs_main, phases_main, CORAL, 46, 26 * SS, -0.015)
)
# the line itself
img = Image.alpha_composite(
    img, ribbon(h * 0.53, 85 * SS, 9 * SS, freqs_main, phases_main, CORAL, 235, 1.5 * SS, -0.015)
)
# thin quiet echo below, same family
phases_echo = [p + 0.9 for p in phases_main]
img = Image.alpha_composite(
    img, ribbon(h * 0.68, 70 * SS, 5 * SS, freqs_main, phases_echo, lerp(CORAL, NAVY, 0.45), 150, 1.5 * SS, -0.01)
)

# --- Vignette to ground the edges --------------------------------------------
ground = Image.new("RGBA", (w, h), (0, 0, 0, 0))
gg = ImageDraw.Draw(ground)
for y in range(int(h * 0.6), h):
    t = (y - h * 0.6) / (h * 0.4)
    gg.line([(0, y), (w, y)], fill=NAVY_DARK + (int(120 * t**1.8),))
img = Image.alpha_composite(img, ground)

# --- Downsample + save --------------------------------------------------------
out = img.convert("RGB").resize((W, H), Image.LANCZOS)
out.save("public/images/notion-cover.jpg", quality=90)
print("wrote public/images/notion-cover.jpg")
