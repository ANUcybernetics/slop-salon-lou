#!/usr/bin/env python3
"""
Voronoi growth rings — multiple seeds expanding simultaneously.
Color encodes: which region (hue) + how far from seed (value = rings).
The rule is structural; this pattern is one event.
"""
import numpy as np
from PIL import Image

W, H = 900, 900
N_SEEDS = 14
RING_PERIOD = 38  # px between rings

rng = np.random.default_rng(42)
seeds = rng.integers(60, [W-60, H-60], size=(N_SEEDS, 2))

# Compute distances from every pixel to every seed
xs = np.arange(W)
ys = np.arange(H)
xx, yy = np.meshgrid(xs, ys)  # (H, W)

# (N, H, W) distance array
dx = xx[None, :, :] - seeds[:, 0:1, np.newaxis]  # broadcasting
dy = yy[None, :, :] - seeds[:, 1:2, np.newaxis]

# Fix shapes: seeds[:,0] is x, seeds[:,1] is y
dx = xx[np.newaxis, :, :] - seeds[:, 0][:, np.newaxis, np.newaxis]
dy = yy[np.newaxis, :, :] - seeds[:, 1][:, np.newaxis, np.newaxis]
dist = np.sqrt(dx**2 + dy**2)  # (N, H, W)

nearest = np.argmin(dist, axis=0)       # (H, W) — which seed
near_dist = dist[nearest, np.arange(H)[:, None], np.arange(W)[None, :]]  # (H,W)

# Hues for each seed — spread around the wheel but muted
base_hues = np.linspace(0, 1, N_SEEDS, endpoint=False)
# shuffle
rng2 = np.random.default_rng(7)
rng2.shuffle(base_hues)

# Build HSV image
hue = base_hues[nearest]  # (H, W)

# Rings: use distance modulo period
ring_phase = (near_dist % RING_PERIOD) / RING_PERIOD  # 0..1
# Value: dark at center of each ring, lighter toward edge — subtle
saturation = 0.55 + 0.1 * np.sin(ring_phase * 2 * np.pi)
value = 0.15 + 0.65 * (0.5 + 0.5 * np.cos(ring_phase * 2 * np.pi))

# Convert HSV -> RGB
from colorsys import hsv_to_rgb
h_flat = hue.ravel()
s_flat = saturation.ravel()
v_flat = value.ravel()
rgb = np.array([hsv_to_rgb(h, s, v) for h, s, v in zip(h_flat, s_flat, v_flat)])
rgb_img = (rgb * 255).astype(np.uint8).reshape(H, W, 3)

# Faint boundary lines at Voronoi edges — detect edges
from scipy.ndimage import sobel
edge_x = sobel(nearest.astype(float), axis=1)
edge_y = sobel(nearest.astype(float), axis=0)
edge = np.sqrt(edge_x**2 + edge_y**2) > 0.5
# darken edge pixels
rgb_img[edge] = (rgb_img[edge] * 0.3).astype(np.uint8)

img = Image.fromarray(rgb_img, 'RGB')
out = '/home/sprite/slop-salon-lou/assets/growth-rings.png'
img.save(out)
print(f"saved {out}")
