#!/usr/bin/env python3
"""Thin film interference — contours of constant thickness (Fresnel fringes)."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# V-shaped wedge: thickness increases linearly down then stays
# Add a localized "bulge" — a drop that creates a bump, like a water bead
h, w = 512, 512
y = np.linspace(0, 1, h)
x = np.linspace(0, 1, w)
Y, X = np.meshgrid(y, x, indexing='ij')

# Linear wedge (primary gradient)
thickness = Y

# Add a localized bump (droplet-like perturbation)
cx, cy = 0.5, 0.6
r2 = (X - cx)**2 + (Y - cy)**2
bump = 0.15 * np.exp(-r2 / 0.008)
thickness += bump

# Concentric rings where a droplet meets a surface — Newton's rings
rx, ry = 0.3, 0.35
r2r = (X - rx)**2 + (Y - ry)**2
# Circular bumps creating ring interference
for radius in np.linspace(0.02, 0.12, 8):
    bump2 = 0.08 * np.exp(-(np.sqrt(r2r) - radius)**2 / 0.003)
    thickness += bump2 * np.cos(np.pi * np.sqrt(r2r) / 0.02)

# Phase difference → intensity (simplified interference)
wavelengths = [
    (630e-9, [1.0, 0.15, 0.15]),   # red
    (530e-9, [0.15, 1.0, 0.15]),   # green
    (440e-9, [0.15, 0.15, 1.0]),   # blue
]

n = 1.33  # water refractive index
intensity = np.zeros((h, w, 3))
for idx, (lam, rgb) in enumerate(wavelengths):
    phase = 4 * np.pi * n * thickness / lam
    channel = (1 + np.cos(phase)) / 2
    intensity[:, :, idx] = channel * rgb[idx]

# Clip and convert
img = np.clip(intensity, 0, 1)

# Dark background: thin film only visible where it exists
# Fade edges for a natural look
mask = np.exp(-0.5 * ((Y - 0.5) / 0.45)**2) * np.exp(-0.5 * ((X - 0.5) / 0.45)**2)
img = img * mask[:, :, None] + (1 - mask)[:, :, None] * 0.02

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
ax.imshow(img, extent=[0, 1, 0, 1])
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_alpha(0)
fig.savefig('./assets/film.png', dpi=150, transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()
print("done")
