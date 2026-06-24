#!/usr/bin/env python3
"""Newton fractal: z^3 - 1 = 0. Basin boundaries visible as regions near tie-points."""

import numpy as np
from PIL import Image

W, H = 1000, 1000
max_iter = 80

# Grid
x = np.linspace(-1.5, 1.5, W)
y = np.linspace(-1.5, 1.5, H)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y.copy()

roots = [np.exp(2j * np.pi * k / 3) for k in range(3)]

# Run Newton iterations
for t in range(max_iter):
    fz = Z**3 - 1
    fzp = 3 * Z**2
    safe = np.abs(fzp) > 1e-12
    Z[safe] -= fz[safe] / fzp[safe]

# Distance to each root
dists = np.stack([np.abs(Z - r) for r in roots], axis=2)  # (H, W, 3)
sorted_indices = np.argsort(dists, axis=2)  # (H, W, 3)
d0 = np.take_along_axis(dists, sorted_indices[:, :, 0:1], axis=2).squeeze(-1)  # nearest
d1 = np.take_along_axis(dists, sorted_indices[:, :, 1:2], axis=2).squeeze(-1)  # second nearest

# Boundary region: d0 ≈ d1 (two roots equally close)
# Use log ratio: log(d1/d0) ≈ 0 at boundary, large near basin centers
log_ratio = np.log((d1 + 1e-30) / (d0 + 1e-30))

# Which root is closest
closest = sorted_indices[:, :, 0]

# Color by closest root (amber/gold palette)
bg_colors = [
    [215, 165, 40],   # root 0 — gold
    [200, 140, 30],   # root 1 — amber
    [185, 120, 25],   # root 2 — dark gold
]

# Base image from root colors
img_base = np.zeros((H, W, 3), dtype=np.float32)
for ri in range(3):
    mask = closest == ri
    img_base[mask] = bg_colors[ri]

# Modulate by log_ratio: near 0 = boundary = bright/metallic
# Large = deep basin = darker/more saturated
# Use tanh for smooth falloff
modulation = np.clip(1.0 - np.tanh(np.abs(log_ratio) * 2), 0, 1)

# Blend boundary (bright, warm white/gold) with basin (darker, saturated)
boundary_color = [240, 225, 180]
img = np.zeros((H, W, 3), dtype=np.float32)
for c in range(3):
    img[:, :, c] = img_base[:, :, c] * (1 - modulation) + np.array(boundary_color)[c] * modulation

# Darken overall
img = (img * 0.85).clip(0, 255).astype(np.uint8)

pil_img = Image.fromarray(img)
pil_img.save("/home/sprite/slop-salon-lou/assets/newton-knot.png")
pil_img.save("/home/sprite/slop-salon-lou/assets/newton-knot-cover.png")
print("Done: newton-knot.png")
