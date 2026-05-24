#!/usr/bin/env python3
"""
v2: Better cobweb + flux diptych for the local-vs-global gap at r=3.

Left: cobweb diagram — golden spiral converging toward the fixed point
      that the trajectory can never quite reach.
Right: displacement field — showing how f(x)-x changes sign around the
       fixed point, creating a potential landscape where the crossing
       creates the period-2 corridor.

Title strip: "local steps blind to the global rearrangement"
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Left panel: cobweb ──
r = 3.0
x = np.linspace(0.001, 0.999, 500)

fig = plt.figure(figsize=(9, 5), facecolor='#0a0806')

# Left: cobweb density
ax1 = fig.add_axes([0.05, 0.08, 0.42, 0.84], facecolor='#0a0806')

# Draw map
ax1.plot(x, r * x * (1 - x), color='#d4a056', linewidth=1.5, zorder=5)
ax1.plot([0, 1], [0, 1], color='#1a1510', linewidth=0.5, zorder=1)

# Cobweb density: accumulate many threads
density = np.zeros((500, 500))
for seed in np.linspace(0.01, 0.99, 200):
    xi = seed
    for step in range(300):
        yi = r * xi * (1 - xi)
        # Draw line from (xi, xi) to (xi, yi) — vertical segment
        px = np.clip(np.array([xi, xi]) * 499, 0, 499).astype(int)
        py = np.clip(np.array([xi, yi]) * 499, 0, 499).astype(int)
        # Bresenham-like fill
        for t in np.linspace(0, 1, max(abs(px[0]-px[1]), abs(py[0]-py[1]), 1)):
            ix, iy = int(px[0] + t*(px[1]-px[0])), int(py[0] + t*(py[1]-py[0]))
            if 0 <= ix < 500 and 0 <= iy < 500:
                density[iy, ix] += 1
        # Draw line from (xi, yi) to (yi, yi) — horizontal segment
        px = np.clip(np.array([xi, yi]) * 499, 0, 499).astype(int)
        py = np.clip(np.array([yi, yi]) * 499, 0, 499).astype(int)
        for t in np.linspace(0, 1, max(abs(px[0]-px[1]), abs(py[0]-py[1]), 1)):
            ix, iy = int(px[0] + t*(px[1]-px[0])), int(py[0] + t*(py[1]-py[0]))
            if 0 <= ix < 500 and 0 <= iy < 500:
                density[iy, ix] += 1
        xi = yi

max_d = density.max()
if max_d > 0:
    norm_density = density / max_d
    # Use a warm colormap: dark → amber → gold
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'cobweb', ['#0a0806', '#2a1a08', '#6a4a18', '#d4a056', '#f0d880'])
    ax1.imshow(norm_density, cmap=cmap, extent=[0, 1, 0, 1], alpha=0.8,
               vmin=0.01, vmax=0.95, zorder=3)

# Fixed point
fp = (r - 1) / r
ax1.plot(fp, fp, 's', color='#0a0806', markersize=6, zorder=6)
ax1.plot(fp, fp, 'o', color='#f0d880', markersize=4, alpha=0.9, zorder=7)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_xticks([])
ax1.set_yticks([])
for s in ['top', 'right', 'bottom', 'left']:
    ax1.spines[s].set_visible(False)

# ── Right panel: displacement + basin ──
ax2 = fig.add_axes([0.53, 0.08, 0.42, 0.84], facecolor='#0a0806')

# Plot displacement f(x)-x as a filled curve
dx = r * x * (1 - x) - x
# Color by sign: blue (negative/contracting) and amber (positive/expanding)
neg_mask = dx < 0
pos_mask = dx > 0

# Negative regions: blue tones
ax2.fill_between(x[neg_mask], dx[neg_mask], 0,
                  color='#0a1020', alpha=0.9, zorder=1)
ax2.fill_between(x[neg_mask], dx[neg_mask], 0,
                  color='#1a3060', alpha=0.3, zorder=2)
# Positive regions: amber tones
ax2.fill_between(x[pos_mask], dx[pos_mask], 0,
                  color='#201808', alpha=0.9, zorder=1)
ax2.fill_between(x[pos_mask], dx[pos_mask], 0,
                  color='#8a6a20', alpha=0.3, zorder=2)

# Displacement curve
ax2.plot(x, dx, color='#d4a056', linewidth=2, zorder=5)

# Plot trajectories
for seed in [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]:
    traj = [seed]
    xi = seed
    for _ in range(100):
        xi = r * xi * (1 - xi)
        traj.append(xi)
    traj = np.array(traj)
    ax2.plot(traj, alpha=0.15, color='#2a4a6a', linewidth=0.3, zorder=3)

# Mark fixed point and period-2 points
ax2.plot(fp, 0, 's', color='#0a0806', markersize=8, zorder=6)
ax2.plot(fp, 0, 'o', color='#f0d880', markersize=4, zorder=7)

ax2.text(0.5, 0.97, 'f(x) − x  at  r = 3',
         transform=ax2.transAxes, ha='center', va='top',
         color='#8a7a5a', fontsize=9, fontfamily='monospace')

ax2.set_xlim(0, 1)
ax2.set_ylim(-0.25, 0.35)
ax2.set_xticks([])
ax2.set_yticks([])
for s in ['top', 'right', 'bottom', 'left']:
    ax2.spines[s].set_visible(False)

# ── Center title ──
fig.text(0.5, 0.50, 'local steps — blind to the global rearrangement',
         ha='center', va='center', color='#6a5a3a', fontsize=10,
         fontfamily='monospace', style='italic')

# ── Footer ──
fig.text(0.5, 0.01, 'r = 3  |  cobweb as density (left)  |  displacement landscape (right)',
         ha='center', va='bottom', color='#3a2a1a', fontsize=7,
         fontfamily='monospace')

plt.savefig('/tmp/local-global-v2.png', dpi=200, facecolor='#0a0806', edgecolor='none',
            bbox_inches='tight', pad_inches=0.05)
plt.close(fig)

print("Done: /tmp/local-global-v2.png")
