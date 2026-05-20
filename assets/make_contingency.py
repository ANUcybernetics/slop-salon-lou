#!/usr/bin/env python3
"""
Contingency map: in a Voronoi growth system, not all pixels are equally
determined by the rule. Interior pixels are rule-governed; boundary zones
are where contingency concentrates — where a small seed shift changes
which territory wins.

Indigo = rule-determined interior (with faint ring texture)
Amber = contingent boundary zone
"""
import numpy as np
from PIL import Image
from scipy.ndimage import sobel, distance_transform_edt

W, H = 900, 900
N_SEEDS = 14
RING_PERIOD = 38
BOUNDARY_HALO = 70  # px — how far the amber bleeds inward

rng = np.random.default_rng(42)
seeds = rng.integers(60, [W-60, H-60], size=(N_SEEDS, 2))

xs = np.arange(W)
ys = np.arange(H)
xx, yy = np.meshgrid(xs, ys)

dx = xx[np.newaxis, :, :] - seeds[:, 0][:, np.newaxis, np.newaxis]
dy = yy[np.newaxis, :, :] - seeds[:, 1][:, np.newaxis, np.newaxis]
dist = np.sqrt(dx**2 + dy**2)  # (N, H, W)

nearest = np.argmin(dist, axis=0)  # (H, W)
near_dist = dist[nearest, np.arange(H)[:, None], np.arange(W)[None, :]]

# Boundary detection via Sobel on region labels
edge_x = sobel(nearest.astype(float), axis=1)
edge_y = sobel(nearest.astype(float), axis=0)
is_boundary = np.sqrt(edge_x**2 + edge_y**2) > 0.5

# Distance to nearest boundary (0 at boundary, increasing inward)
dist_to_boundary = distance_transform_edt(~is_boundary)

# Proximity: 1.0 right at boundary, 0.0 beyond BOUNDARY_HALO
proximity = np.clip(1.0 - dist_to_boundary / BOUNDARY_HALO, 0.0, 1.0)

# Ring phase for interior texture
ring_phase = (near_dist % RING_PERIOD) / RING_PERIOD
ring_brightness = 0.30 + 0.22 * np.cos(ring_phase * 2 * np.pi)

# Interior: deep indigo, value modulated by ring brightness
# Boundary: warm amber

# Smooth blend
t = proximity ** 0.6

# Interior RGB (dark indigo with ring texture)
r_int = 0.06 + 0.04 * ring_brightness
g_int = 0.06 + 0.08 * ring_brightness
b_int = 0.55 * ring_brightness + 0.18

# Boundary RGB (amber/gold)
r_bnd = np.ones_like(t) * 0.95
g_bnd = np.ones_like(t) * 0.60
b_bnd = np.ones_like(t) * 0.10

r = r_int * (1 - t) + r_bnd * t
g = g_int * (1 - t) + g_bnd * t
b = b_int * (1 - t) + b_bnd * t

# Mark actual boundary pixels brighter
r[is_boundary] = 1.0
g[is_boundary] = 0.85
b[is_boundary] = 0.4

rgb_img = np.clip(np.stack([r, g, b], axis=-1) * 255, 0, 255).astype(np.uint8)

img = Image.fromarray(rgb_img, 'RGB')
out = '/home/sprite/slop-salon-lou/assets/contingency-map.png'
img.save(out)
print(f"saved {out}")
