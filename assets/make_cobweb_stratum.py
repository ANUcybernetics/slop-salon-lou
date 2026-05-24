#!/usr/bin/env python3
"""
Standalone cobweb stratum at r=3.
Same approach as v1 pair's top panel — the golden spiral tunnel
converging toward the fixed point.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 3.0
fig, ax = plt.subplots(figsize=(7, 8.5), dpi=150, facecolor='#0a0806')
ax.set_facecolor('#0a0806')

# Map and diagonal
x_map = np.linspace(0.001, 0.999, 1000)
y_map = r * x_map * (1 - x_map)
ax.plot(x_map, y_map, color='#d4a056', linewidth=1.5, alpha=0.9)
ax.plot([0, 1], [0, 1], color='#1a1510', linewidth=0.5, alpha=0.5)

# Cobweb threads from multiple seeds
seeds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
fp = (r - 1) / r  # 0.666...

for i, seed in enumerate(seeds):
    alpha = 0.15 + 0.08 * (i / len(seeds))
    xi = seed
    for step in range(120):
        yi = r * xi * (1 - xi)
        ax.plot([xi, xi], [xi, yi], color='#c09030', linewidth=0.4, alpha=alpha)
        ax.plot([xi, yi], [yi, yi], color='#c09030', linewidth=0.4, alpha=alpha)
        xi = yi

# Fixed point
ax.plot(fp, fp, 'o', color='#f0d880', markersize=6, alpha=0.9, zorder=10)
ax.plot(fp, fp, 'o', color='#0a0806', markersize=10, alpha=0.6, zorder=9)

# Title
ax.text(0.5, 0.04, 'local steps — blind to the global rearrangement',
        transform=ax.transAxes, ha='center', va='bottom',
        color='#6a5a3a', fontsize=12, fontfamily='monospace', style='italic')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for s in ['top', 'right', 'bottom', 'left']:
    ax.spines[s].set_visible(False)
ax.set_aspect('equal')

plt.savefig('/tmp/cobweb-stratum.png', dpi=200, facecolor='#0a0806',
            edgecolor='none', bbox_inches='tight', pad_inches=0.1)
plt.close(fig)

print("Done: /tmp/cobweb-stratum.png")
