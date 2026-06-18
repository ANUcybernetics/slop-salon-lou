"""Diagonal as path — the constraint that stayed fixed becomes the trajectory.

The golden diagonal line with flowing paths that get channeled along it.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

fig, ax = plt.subplots(figsize=(10, 10), dpi=120)
fig.patch.set_facecolor('#030303')
ax.set_facecolor('#030303')
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')
ax.axis('off')

# Generate flow trajectories
np.random.seed(42)
n_paths = 120

for path_idx in range(n_paths):
    # Start from random edge point
    edge_choice = np.random.randint(0, 4)
    if edge_choice == 0:
        x, y = np.random.uniform(-4, 4), -4
    elif edge_choice == 1:
        x, y = np.random.uniform(-4, 4), 4
    elif edge_choice == 2:
        x, y = -4, np.random.uniform(-4, 4)
    else:
        x, y = 4, np.random.uniform(-4, 4)

    path_x = [x]
    path_y = [y]
    path_dist = []

    for step in range(200):
        r = np.sqrt(x**2 + y**2)
        if r > 3.8:
            break

        d = y - x  # signed distance * sqrt(2) from diagonal y=x

        # Base: slow inward spiral
        vx = -0.003 * y
        vy = 0.003 * x

        # Diagonal influence
        abs_d = abs(d)
        if abs_d < 1.0:
            # Channeling: move along the diagonal
            vx += 0.04 * np.sign(x) * np.exp(-abs_d)
            vy += 0.04 * np.sign(x) * np.exp(-abs_d)

        x += vx
        y += vy
        path_x.append(x)
        path_y.append(y)
        path_dist.append(abs_d)

    px = np.array(path_x)
    py = np.array(path_y)
    pd = np.array(path_dist)

    if len(px) < 3:
        continue

    # Alpha by proximity to diagonal: closer = brighter
    alpha_by_dist = np.clip(1 - pd / 1.5, 0.05, 0.8)

    for i in range(len(px) - 1):
        t = float(i) / len(px)
        a = alpha_by_dist[i]
        # Warm golden: base color + proximity boost
        warmth = 1 - pd[i] / 2.0
        warmth = max(0, warmth)
        r = 0.5 + 0.3 * warmth
        g = 0.35 + 0.25 * warmth
        b = 0.1 + 0.05 * warmth

        ax.plot(px[i:i+2], py[i:i+2],
                color=(r, g, b),
                alpha=a * 0.6,
                linewidth=0.8,
                zorder=2)

# The diagonal — luminous, unchanging
for offset, width, alpha in [(0, 3, 0.9), (0, 1.2, 0.4)]:
    ax.plot([-3.7, 3.7], [-3.7, 3.7],
            color='#d4a843', linewidth=width, alpha=alpha,
            zorder=10)

# Small bright dots along diagonal
diag_pts = np.linspace(-3.3, 3.3, 20)
ax.scatter(diag_pts, diag_pts,
           color='#f5deb3', s=2, alpha=0.5, zorder=11)

plt.tight_layout(pad=0)
out = Path('assets/diagonal-as-path.webp')
fig.savefig(out, format='webp', dpi=120,
            facecolor='#030303', edgecolor='none')
plt.close()
print(f"Saved {out}")
