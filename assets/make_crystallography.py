"""
Persistence as crystallography.

rahel: "persistence is not time-extension of one event. it is the event made spatial."

Each lap of the cobweb spiral is a "moment." The orbit doesn't repeat —
it approaches. The shape of that approach, accumulated over 5000 steps,
forms a crystalline structure. The structure IS the persistence.

Two panels: r=2.85 (wide spiral, each moment far from the next) and
r=2.99 (moments compressed, the crystal almost touching itself — the
tangency as collapsed lattice).

No cobweb lines. Just the orbit as point cloud, density-encoded.
"""

import numpy as np
from PIL import Image
import math

W, H = 800, 400
pixels = np.zeros((H, W, 4), dtype=np.float64)

def logistic(r, x):
    return r * x * (1.0 - x)

def plot_orbit(r, panel_x, n_skip, n_steps):
    """Plot orbit as density map."""
    x = 0.3
    for i in range(n_skip + n_steps):
        if i >= n_skip:
            y = logistic(r, x)
            # Map to pixel
            px = panel_x + int(x * (W//2 - 20)) + 10
            py = H - 20 - int(y * (H - 40))

            # Gaussian glow
            radius = 3
            for dj in range(-radius, radius + 1):
                for di in range(-radius, radius + 1):
                    if di*di + dj*dj > radius*radius:
                        continue
                    px0 = px + di
                    py0 = py + dj
                    if 0 <= px0 < W and 0 <= py0 < H:
                        rr = math.sqrt(di*di + dj*dj) / radius
                        w = math.exp(-rr * rr * 3)
                        # Color by distance from diagonal
                        dist = abs(x - y)
                        if dist < 0.02:
                            # Near tangency: bright gold
                            pixels[py0, px0] += [450, 320, 80, w]
                        elif dist < 0.1:
                            # Mid: amber
                            pixels[py0, px0] += [350, 250, 60, w]
                        else:
                            # Far: blue
                            pixels[py0, px0] += [40, 50, 200, w]
        x = logistic(r, x)

# Panel 1: r=2.85
plot_orbit(2.85, 0, 1000, 5000)

# Panel 2: r=2.99
plot_orbit(2.99, W//2, 1000, 5000)

# Clamp and convert
pixels = np.clip(pixels, 0, 255).astype(np.uint8)
img = Image.fromarray(pixels, 'RGBA')

# Draw separator line
draw_pixels = np.array(img)
for y in range(H):
    for dx in range(-1, 2):
        draw_pixels[y, W//2 + dx] = [60, 60, 100, 255]
img = Image.fromarray(draw_pixels)

img.save("assets/crystallography.webp", "WEBP")
print("Done: crystallography.webp")
