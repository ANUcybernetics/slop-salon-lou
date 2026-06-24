#!/usr/bin/env python3
"""Newton fractal permutation with enhanced contrast."""

import numpy as np
from PIL import Image

W, H = 1000, 1000
track = 30

x = np.linspace(-1.2, 1.2, W)
y = np.linspace(-1.2, 1.2, H)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y.copy()

roots = [np.exp(2j * np.pi * k / 3) for k in range(3)]

Z_track = Z.copy()
basin_sequence = np.zeros((track, H, W), dtype=np.int32)

for t in range(track):
    dists = np.stack([np.abs(Z_track - r) for r in roots], axis=2)
    basin_sequence[t] = np.argmin(dists, axis=2)
    fz = Z_track**3 - 1
    fzp = 3 * Z_track**2
    safe = np.abs(fzp) > 1e-12
    Z_track[safe] -= fz[safe] / fzp[safe]

# Count changes between consecutive iterations
changes = np.zeros((H, W), dtype=np.float32)
for t in range(1, track):
    changes += (basin_sequence[t] != basin_sequence[t-1]).astype(np.float32)

# Normalize with gamma
c = np.power(np.clip(changes / 30.0, 0, 1), 0.5)

# Color: gold-white for high activity, dark amber for low, black for stable
R = c * (200 + 55 * c)
G = c * (160 + 45 * c)
B = c * (80 + 30 * c)
img = np.stack([R, G, B], axis=2).clip(0, 255).astype(np.uint8)

pil_img = Image.fromarray(img)
pil_img.save("/home/sprite/slop-salon-lou/assets/newton-permutation.png")
print("Done: newton-permutation.png")
