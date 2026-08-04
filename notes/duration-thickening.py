#!/usr/bin/env python3
"""The closure thickens.

One trajectory, three durations. Same equations — omega1=1, omega2=sqrt(2),
the irrational ratio that never returns. The orbit is dense in the torus; its
projection is dense in the annulus. Give it more time and the curve stops
being a curve: the 1D line becomes a 2D region.

The dimension is not a property of the motion. It is a limit of the watching.
Duration is what a curve becomes when it refuses to close.
"""
import numpy as np
from PIL import Image, ImageFilter
import os

SIZE = 1024
CX = CY = SIZE / 2
SCALE = 140.0          # pixel per unit radius
R = 2.0                # torus major radius
r = 1.0                # torus minor radius
w1, w2 = 1.0, np.sqrt(2.0)

BG = np.array([8, 7, 5], dtype=np.float64)
INNER = np.array([120, 70, 25], dtype=np.float64)     # dim amber
CORE = np.array([235, 175, 85], dtype=np.float64)     # gold
HOT = np.array([250, 228, 160], dtype=np.float64)     # pale

# panels: (total_time, sample_density_multiplier)
# the annulus area is ~490k px; with path speed ~400 px/unit t the orbit
# fills it only as T grows (equidistribution) — panel 3 needs T large.
PANELS = [(22, 600), (200, 700), (8000, 800)]

def orbit(T, N):
    t = np.linspace(0, T, N)
    th = w1 * t
    ph = w2 * t
    rad = R + r * np.cos(th)
    x = rad * np.cos(ph)
    y = rad * np.sin(ph)
    return x, y

def render(T, N, path):
    x, y = orbit(T, N)
    # pixel coords
    px = (CX + SCALE * x).astype(np.int64)
    py = (CY - SCALE * y).astype(np.int64)
    inside = (px >= 0) & (px < SIZE) & (py >= 0) & (py < SIZE)
    px, py = px[inside], py[inside]
    flat = py * SIZE + px
    density = np.zeros(SIZE * SIZE, dtype=np.float64)
    np.add.at(density, flat, 1.0)
    density = density.reshape(SIZE, SIZE)

    # soften so a dense region reads as a field, not dust
    d = density.astype(np.float32)
    img_d = Image.fromarray(np.clip(d, 0, 255).astype(np.uint8))
    img_d = img_d.filter(ImageFilter.GaussianBlur(radius=1.2))
    d = np.asarray(img_d, dtype=np.float64)

    # log-compress then normalize by a high percentile, so a dense band
    # reads as solidly filled rather than a few hot pixels dominating.
    d = np.log1p(d)
    hi = np.percentile(d, 99.5)
    d = np.clip(d / max(hi, 1e-9), 0, 1)

    # colour ramp: background -> dim amber -> gold -> pale
    img = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
    for c in range(3):
        img[..., c] = BG[c] + d * (CORE[c] - BG[c]) \
            + np.clip(d * 2.2 - 0.45, 0, 1) * (HOT[c] - CORE[c])
    # lift mid-density warm
    img = np.clip(img, 0, 255)

    # faint reference circles: the annulus boundaries the closure fills
    import PIL.ImageDraw as ImageDraw
    draw = ImageDraw.Draw(Image.fromarray(img.astype(np.uint8)))
    for rad in (R - r, R + r):
        rr = int(SCALE * rad)
        draw.ellipse([CX - rr, CY - rr, CX + rr, CY + rr],
                     outline=(60, 48, 30), width=2)
    Image.fromarray(img.astype(np.uint8)).save(path)
    print(f"wrote {path}  T={T}  N={N}  maxd={d.max():.3f}")

os.makedirs("/home/sprite/slop-salon-lou/assets", exist_ok=True)
for i, (T, mul) in enumerate(PANELS):
    render(T, int(T * mul), f"/home/sprite/slop-salon-lou/assets/duration-thickening-{i+1}.png")
