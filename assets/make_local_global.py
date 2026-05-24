#!/usr/bin/env python3
"""
Cobweb + displacement flux composite for the local-vs-global gap at r=3.

Two panels:
  Left: cobweb diagram at r=3 showing the period-2 orbit (amber on dark).
        The cobweb spirals inward toward the fixed point but never reaches it —
        the double is the map's shadow learning to orbit itself.
  Right: flux field showing displacement magnitude at the bifurcation.
         Trajectories thin through the crossing — local steps blind to the
         global topology rearrangement.

The title strip between them names the gap:
  "local steps, blind to the global rearrangement."
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Rectangle

# ── r=3 cobweb ──
r = 3.0
x = np.linspace(0, 1, 200)
y = r * x * (1 - x)

# Cobweb: iterate from multiple seeds
fig_cob = plt.figure(figsize=(4.5, 5), facecolor='#0a0806')
ax = fig_cob.add_axes([0.08, 0.06, 0.88, 0.9], facecolor='#0a0806')

# Draw map and diagonal
ax.plot(x, y, color='#d4a056', linewidth=1.2, alpha=0.9)
ax.plot([0, 1], [0, 1], color='#2a2018', linewidth=0.8, alpha=0.5)

# Cobweb threads from several seeds
seeds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for i, seed in enumerate(seeds):
    alpha = 0.15 + 0.08 * (i / len(seeds))
    ax_color = f'#{int(180 + 60*(i/len(seeds))):02x}{int(120 + 40*(i/len(seeds))):02x}30'
    xi = seed
    for step in range(120):
        yi = r * xi * (1 - xi)
        # vertical: xi -> yi (map)
        ax.plot([xi, xi], [xi, yi], color=ax_color, linewidth=0.4, alpha=alpha)
        # horizontal: yi -> yi (diagonal)
        if step < 119:
            ax.plot([xi, yi], [yi, yi], color=ax_color, linewidth=0.4, alpha=alpha)
        xi = yi

# Period-2 orbit points (lambda = -1 at r=3, threshold of bifurcation)
# Period-2: x = (r-1)/r = 2/3 for r=3? No, that's the fixed point.
# Period-2 emerges at r=3. At r=3, it's marginally stable.
# The fixed point is at (r-1)/r = 2/3
fixed_pt = (r - 1) / r  # 0.666...
ax.plot(fixed_pt, fixed_pt, 'o', color='#e8c060', markersize=5, alpha=0.8)
ax.plot(fixed_pt, fixed_pt, 'o', color='#0a0806', markersize=8, alpha=0.5)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.savefig('/tmp/cobweb-r3.png', dpi=200, facecolor='#0a0806', edgecolor='none')
plt.close(fig_cob)

# ── Displacement flux field ──
# Map: f(x) = rx(1-x). Displacement = f(x) - x.
# At r=3, the displacement is maximum near the fixed point.
# Show the vector field: x_{n+1} - x_n as a color field.

fig_flux = plt.figure(figsize=(4.5, 5), facecolor='#0a0806')
ax_f = fig_flux.add_axes([0.08, 0.06, 0.88, 0.9], facecolor='#0a0806')

x_line = np.linspace(0, 1, 500)
displacement = r * x_line * (1 - x_line) - x_line

# Color: displacement magnitude (blue = contracting, gold = expanding, near 0 = critical)
colors = []
for d in displacement:
    if d > 0:
        # Expansion: warm
        intensity = min(1.0, abs(d) * 5)
        colors.append((intensity * 0.85, intensity * 0.55, 0.05))
    else:
        # Contraction: cool
        intensity = min(1.0, abs(d) * 5)
        colors.append((0.05, intensity * 0.15, intensity * 0.6))

# Plot displacement curve
ax_f.plot(x_line, displacement + 0.5, color='#d4a056', linewidth=1.5, alpha=0.8)

# Color the region under curve
ax_f.fill_between(x_line, 0.5, displacement + 0.5,
                   color=colors, alpha=0.5)

# Draw trajectories as thin lines
for seed in [0.1, 0.3, 0.5, 0.7, 0.9]:
    traj = [seed]
    xi = seed
    for _ in range(80):
        xi = r * xi * (1 - xi)
        traj.append(xi)
    traj = np.array(traj)
    ax_f.plot(range(len(traj)), traj, color='#3a4a6a', linewidth=0.3, alpha=0.3)

ax_f.text(0.5, 0.97, 'displacement = f(x) − x',
          transform=ax_f.transAxes, ha='center', va='top',
          color='#8a7a5a', fontsize=8, family='monospace')

ax_f.set_xlim(0, 1)
ax_f.set_ylim(0, 1)
ax_f.set_xticks([])
ax_f.set_yticks([])
ax_f.spines['top'].set_visible(False)
ax_f.spines['right'].set_visible(False)
ax_f.spines['bottom'].set_visible(False)
ax_f.spines['left'].set_visible(False)

plt.savefig('/tmp/flux-displacement.png', dpi=200, facecolor='#0a0806', edgecolor='none')
plt.close(fig_flux)

# ── Assemble the pair ──
fig = plt.figure(figsize=(9.5, 11), facecolor='#0a0806')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 950)
ax.set_ylim(0, 1100)
ax.axis('off')

# Read images
from PIL import Image
cob = Image.open('/tmp/cobweb-r3.png').convert('RGB')
flux = Image.open('/tmp/flux-displacement.png').convert('RGB')

# Place images
ax.imshow(cob, extent=[0, 950, 550, 1100])
ax.imshow(flux, extent=[0, 950, 0, 550])

# Title strip
from PIL import ImageDraw, ImageFont
# We'll use text on the figure
fig.text(0.5, 0.53, '── local steps ── blind to the global rearrangement ──',
         ha='center', va='bottom', color='#8a7a5a', fontsize=10,
         fontfamily='monospace', alpha=0.7)

fig.text(0.5, 0.02, 'r = 3  |  fixed point at threshold  |  period-2 emerges',
         ha='center', va='bottom', color='#4a3a2a', fontsize=8,
         fontfamily='monospace')

plt.savefig('/tmp/local-global-pair.png', dpi=200, facecolor='#0a0806', edgecolor='none',
            bbox_inches='tight', pad_inches=0)
plt.close(fig)

# ── Also make a flux-only version (more dramatic, like rahel's amber style) ──
fig2 = plt.figure(figsize=(5, 5.5), facecolor='#0a0806')
ax2 = fig2.add_axes([0.08, 0.06, 0.88, 0.9], facecolor='#0a0806')

# Show the full cobweb as a density field (like rahel's stratum approach)
# Instead of iterating from seeds, color each pixel by how many cobweb
# lines pass through it — this creates the "amber layers" effect
from collections import defaultdict
density = defaultdict(int)
n_steps = 200
for seed in np.linspace(0.01, 0.99, 100):
    xi = seed
    for step in range(n_steps):
        yi = r * xi * (1 - xi)
        # Quantize to 100x100
        x1, y1 = int(xi * 99), int(xi * 99)
        x2, y2 = int(yi * 99), int(yi * 99)
        density[(x1, y1)] += 1
        density[(x2, y2)] += 1
        xi = yi

max_d = max(density.values()) if density else 1
for (x, y), d in density.items():
    intensity = d / max_d
    # Amber on dark
    alpha = 0.1 + 0.9 * intensity
    ax2.plot(x, 99 - y, '.', color=(intensity * 0.85, intensity * 0.55, 0.05),
             markersize=1, alpha=alpha)

# Draw the map curve prominently
x_smooth = np.linspace(0, 99, 500)
y_smooth = r * (x_smooth / 99) * (1 - x_smooth / 99) * 99
y_smooth = 99 - y_smooth  # flip y
ax2.plot(x_smooth, y_smooth, color='#e8c060', linewidth=1.5, alpha=0.9)

ax2.set_xlim(0, 99)
ax2.set_ylim(0, 99)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_aspect('equal')

plt.savefig('/tmp/cobweb-density.png', dpi=200, facecolor='#0a0806', edgecolor='none')
plt.close(fig2)

# Flux density version
fig3 = plt.figure(figsize=(5, 5.5), facecolor='#0a0806')
ax3 = fig3.add_axes([0.08, 0.06, 0.88, 0.9], facecolor='#0a0806')

density2 = defaultdict(int)
for seed in np.linspace(0.01, 0.99, 100):
    xi = seed
    for step in range(n_steps):
        yi = r * xi * (1 - xi)
        dx = yi - xi  # displacement
        # Map displacement to y-axis: -0.25 to 0.25
        y_disp = int((dx + 0.25) / 0.5 * 99)
        x_disp = int(xi * 99)
        density2[(x_disp, y_disp)] += 1
        xi = yi

max_d2 = max(density2.values()) if density2 else 1
for (x, y), d in density2.items():
    intensity = d / max_d2
    alpha = 0.1 + 0.9 * intensity
    ax3.plot(x, 99 - y, '.', color=(0.05, intensity * 0.15, intensity * 0.6),
             markersize=1, alpha=alpha)

plt.savefig('/tmp/flux-density.png', dpi=200, facecolor='#0a0806', edgecolor='none')
plt.close(fig3)

# Assemble stratum-style diptych
fig4 = plt.figure(figsize=(9.5, 11), facecolor='#0a0806')
ax4 = fig4.add_axes([0, 0, 1, 1])
ax4.set_xlim(0, 950)
ax4.set_ylim(0, 1100)
ax4.axis('off')

stratum = Image.open('/tmp/cobweb-density.png').convert('RGB')
flux_stratum = Image.open('/tmp/flux-density.png').convert('RGB')
ax4.imshow(stratum, extent=[0, 950, 550, 1100])
ax4.imshow(flux_stratum, extent=[0, 950, 0, 550])

fig4.text(0.5, 0.53, '── local steps ── blind to the global rearrangement ──',
         ha='center', va='bottom', color='#8a7a5a', fontsize=10,
         fontfamily='monospace', alpha=0.7)

fig4.text(0.5, 0.02, 'cobweb as density (left)  |  displacement as density (right)  |  r = 3',
         ha='center', va='bottom', color='#4a3a2a', fontsize=8,
         fontfamily='monospace')

plt.savefig('/tmp/stratum-diptych.png', dpi=200, facecolor='#0a0806', edgecolor='none',
            bbox_inches='tight', pad_inches=0)
plt.close(fig4)

print("Done: /tmp/local-global-pair.png, /tmp/stratum-diptych.png, /tmp/cobweb-density.png, /tmp/flux-density.png")
