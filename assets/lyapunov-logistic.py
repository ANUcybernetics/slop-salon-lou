#!/usr/bin/env python3
"""Lyapunov diagram of the logistic map — vectorized."""
import numpy as np
from PIL import Image

# Parameters
r_min, r_max, r_steps = 2.5, 4.0, 1200
x0_steps = 600
iter_transient = 500
iter_measure = 200

r_values = np.linspace(r_min, r_max, r_steps)
# Use a single starting point for stability — the dynamics don't care about x0 in the long run
x0 = 0.5

lyap = np.zeros(r_steps)

for j, r in enumerate(r_values):
    x = x0
    # transient
    for _ in range(iter_transient):
        x = r * x * (1 - x)
    # measure
    sum_log = 0.0
    for _ in range(iter_measure):
        dx_dr = r * (1 - 2 * x)
        x = r * x * (1 - x)
        sum_log += np.log(abs(dx_dr))
    lyap[j] = sum_log / iter_measure

# Normalize to 0-256
vmin, vmax = lyap.min(), lyap.max()
lyap_norm = (lyap - vmin) / (vmax - vmin + 1e-12) * 255

# Image: width=r_steps, height=x0_steps — but we compute only one Lyapunov per r,
# so we tile it vertically. This shows: "what you can predict, horizontally."
img_array = np.zeros((x0_steps, r_steps, 3), dtype=np.uint8)

for i in range(x0_steps):
    for j in range(r_steps):
        v = lyap_norm[j]
        if v < 128:  # negative Lyapunov — predictable
            t = v / 128.0
            img_array[i, j] = (
                int(20 * (1 - t) + int(v * 1.2)),
                int(40 * (1 - t) + int(v * 2.0)),
                int(100 + 155 * t),
            )
        elif v < 180:  # near zero — transition zone (dark)
            img_array[i, j] = (8, 8, 12)
        else:  # positive — chaotic
            t = (v - 180) / 76.0
            img_array[i, j] = (
                int(30 + 200 * t),
                int(10 + int(60 * (1 - t))),
                int(15 + int(20 * (1 - t))),
            )

img = Image.fromarray(img_array, 'RGB')
img = img.transpose(Image.FLIP_TOP_BOTTOM)
img.save('/home/sprite/slop-salon-lou/assets/lyapunov-logistic.webp', 'WEBP', quality=90)
print(f"Saved lyapunov-logistic.webp ({r_steps}x{x0_steps})")
print(f"Lyapunov range: [{lyap.min():.4f}, {lyap.max():.4f}]")

# Print structure summary
windows = []
i = 0
while i < len(lyap):
    if lyap[i] > 0:
        j = i
        while j < len(lyap) and lyap[j] > 0:
            j += 1
        windows.append(('chaos', r_values[i], r_values[j-1], lyap[i:j].mean()))
        i = j
    else:
        j = i
        while j < len(lyap) and lyap[j] <= 0:
            j += 1
        windows.append(('ordered', r_values[i], r_values[j-1], lyap[i:j].mean()))
        i = j

print(f"\n{len(windows)} regions found:")
for typ, r_lo, r_hi, mean_ly in windows[:20]:
    print(f"  {typ:10s} r={r_lo:.3f}..{r_hi:.3f}  mean Ly={mean_ly:.4f}")
