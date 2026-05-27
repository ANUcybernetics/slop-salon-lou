#!/usr/bin/env python3
"""Spiral cobweb at r=3 — contour lines spiraling inward toward an absent center."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

r = 3.0
x0 = 0.3
n_iter = 600

xs = [x0]
for _ in range(n_iter):
    xs.append(r * xs[-1] * (1 - xs[-1]))

xs = np.array(xs)

# Draw diagonal and map curve
ax.plot([0, 1], [0, 1], color='#3a3a3a', linewidth=1, zorder=1)
x_curve = np.linspace(0, 1, 600)
y_curve = r * x_curve * (1 - x_curve)
ax.plot(x_curve, y_curve, color='#3a3a3a', linewidth=1, zorder=1)

# Cobweb with gradient: warm (structure) → cool (convergence)
for i in range(len(xs) - 1):
    p = i / (len(xs) - 1)
    warmth = 1 - p
    # Gold → blue
    col = (0.83 * warmth + 0.54 * (1-warmth),
           0.65 * warmth + 0.70 * (1-warmth),
           0.45 * warmth + 0.71 * (1-warmth))
    alpha = max(0.05, 0.9 * (1 - p * 0.9))

    if i % 2 == 0:
        x1, y1, x2, y2 = xs[i], xs[i], xs[i], xs[i+1]
    else:
        x1, y1, x2, y2 = xs[i], xs[i+1], xs[i+1], xs[i+1]

    ax.plot([x1, x2], [y1, y2], color=col, alpha=alpha, linewidth=1.2, zorder=2)

# Fixed point marker
ax.plot(2/3, 2/3, 'o', color='#d4a574', markersize=5, zorder=3)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#1a1a1a')
ax.set_facecolor('#1a1a1a')
plt.tight_layout(pad=0)
plt.savefig('/home/sprite/slop-salon-lou/assets/spiral-cobweb.png',
            dpi=200, bbox_inches='tight', facecolor='#1a1a1a', edgecolor='none')
print("Done: spiral-cobweb.png")
