#!/usr/bin/env python3
"""
v3: Clean cobweb density at r=3. Uses matplotlib plot lines (fast).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 3.0

fig, ax = plt.subplots(figsize=(9, 10.5), dpi=150, facecolor='#0a0806')
ax.set_facecolor('#0a0806')

# Map curve
x_map = np.linspace(0, 1, 1000)
y_map = r * x_map * (1 - x_map)
ax.plot(x_map, y_map, color='#d4a056', linewidth=2, zorder=10, alpha=0.9)

# Diagonal
ax.plot([0, 1], [0, 1], color='#1a1510', linewidth=0.5, zorder=1)

# Cobweb threads: each thread is a sequence of line segments
# Draw 40 threads with varying opacity for density effect
fp = (r - 1) / r
seeds = np.linspace(0.05, 0.95, 40)

for idx, seed in enumerate(seeds):
    alpha = 0.03 + 0.02 * (idx / len(seeds))
    xi = seed
    for step in range(300):
        yi = r * xi * (1 - xi)

        # Vertical: (xi, xi) -> (xi, yi)
        ax.plot([xi, xi], [xi, yi], color='#c09030', linewidth=0.3,
                alpha=alpha, zorder=2)
        # Horizontal: (xi, yi) -> (yi, yi)
        ax.plot([xi, yi], [yi, yi], color='#c09030', linewidth=0.3,
                alpha=alpha, zorder=2)

        xi = yi

# Fixed point
ax.plot(fp, fp, 's', color='#0a0806', markersize=10, zorder=11)
ax.plot(fp, fp, 'o', color='#f0d880', markersize=5, alpha=0.9, zorder=12)

# Title text
ax.text(0.5, 0.05, 'local steps — blind to the global rearrangement',
        transform=ax.transAxes, ha='center', va='bottom',
        color='#6a5a3a', fontsize=12, fontfamily='monospace',
        style='italic')

# Subtle grid
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_xticks([])
ax.set_yticks([])
for s in ['top', 'right', 'bottom', 'left']:
    ax.spines[s].set_visible(False)
ax.set_aspect('equal')

plt.savefig('/tmp/local-global-v3.png', dpi=200, facecolor='#0a0806',
            edgecolor='none', bbox_inches='tight', pad_inches=0.1)
plt.close(fig)

print("Done: /tmp/local-global-v3.png")
