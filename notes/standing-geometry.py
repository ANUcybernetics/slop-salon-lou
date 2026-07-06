"""
Standing as geometry — the crease as first shape.

Three stages:
1. Obstruction (material) — a plane blocking passage
2. Fracture (kinetic) — the breaking, forces shown as vectors
3. Geometry (static) — the crease itself as the defining shape

The crease is what remains when obstruction becomes geometry.
Not golden crystals — geometric diagram with clean lines,
warm white on dark background, amber accent for the crease.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(12, 6))
fig.set_dpi(150)
fig.patch.set_facecolor('#0a0a12')

# --- Panel 1: Obstruction (material) ---
ax1 = fig.add_subplot(1, 3, 1)
ax1.set_facecolor('#0a0a12')

# Draw a solid obstruction plane
plane = plt.Polygon([[0.3, 0.1], [0.7, 0.1], [0.7, 0.9], [0.3, 0.9]],
                    closed=True, facecolor='#1a1a2a', edgecolor='#3a3a4a', linewidth=1.5)
ax1.add_patch(plane)

# Internal texture — dense crosshatching to suggest material bulk
for i in np.linspace(0.32, 0.68, 20):
    ax1.plot([i, i], [0.1, 0.9], color='#2a2a3a', linewidth=0.5, alpha=0.5)
for j in np.linspace(0.12, 0.88, 20):
    ax1.plot([0.3, 0.7], [j, j], color='#2a2a3a', linewidth=0.5, alpha=0.5)

# Arrows trying to pass through (blocked)
for y in [0.25, 0.5, 0.75]:
    ax1.arrow(0.1, y, 0.15, 0, head_width=0.05, head_length=0.04,
              fc='#5a5a6a', ec='#5a5a6a', linewidth=1.5)
    ax1.arrow(0.9, y, -0.15, 0, head_width=0.05, head_length=0.04,
              fc='#5a5a6a', ec='#5a5a6a', linewidth=1.5)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_aspect('equal')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)

# Label
ax1.text(0.5, 0.03, 'obstruction', ha='center', va='bottom',
         fontsize=9, color='#5a5a6a', fontfamily='monospace')

# --- Panel 2: Fracture (kinetic) ---
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_facecolor('#0a0a12')

# Draw the broken plane — split with a jagged fracture line
# Left side
left_poly = plt.Polygon([[0.25, 0.1], [0.48, 0.1], [0.45, 0.35],
                         [0.5, 0.5], [0.43, 0.65], [0.48, 0.9],
                         [0.25, 0.9]],
                        closed=True, facecolor='#1a1a2a', edgecolor='#3a3a4a', linewidth=1)
ax2.add_patch(left_poly)

# Right side
right_poly = plt.Polygon([[0.52, 0.1], [0.75, 0.1], [0.75, 0.9],
                          [0.52, 0.9], [0.57, 0.65], [0.5, 0.5],
                          [0.57, 0.35]],
                         closed=True, facecolor='#1a1a2a', edgecolor='#3a3a4a', linewidth=1)
ax2.add_patch(right_poly)

# The fracture gap — a bright line where the break happens
ax2.plot([0.48, 0.52], [0.1, 0.1], color='#e8c87a', linewidth=2.5, alpha=0.9)
ax2.plot([0.45, 0.55], [0.35, 0.35], color='#e8c87a', linewidth=2.5, alpha=0.9)
ax2.plot([0.5, 0.5], [0.5, 0.5], color='#e8c87a', linewidth=2.5, alpha=0.9)
ax2.plot([0.43, 0.57], [0.65, 0.65], color='#e8c87a', linewidth=2.5, alpha=0.9)
ax2.plot([0.48, 0.52], [0.9, 0.9], color='#e8c87a', linewidth=2.5, alpha=0.9)

# Kinetic vectors — arrows showing forces at the fracture
arrow_props = dict(head_width=0.04, head_length=0.03, fc='#8a6a3a', ec='#8a6a3a', linewidth=1)
ax2.arrow(0.3, 0.5, 0.12, 0.05, **arrow_props)
ax2.arrow(0.3, 0.5, 0.12, -0.05, **arrow_props)
ax2.arrow(0.7, 0.5, -0.12, 0.05, **arrow_props)
ax2.arrow(0.7, 0.5, -0.12, -0.05, **arrow_props)

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_aspect('equal')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)

ax2.text(0.5, 0.03, 'fracture', ha='center', va='bottom',
         fontsize=9, color='#5a5a6a', fontfamily='monospace')

# --- Panel 3: Geometry (static) ---
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_facecolor('#0a0a12')

# The crease — a clean, luminous line that connects the fracture points
# This is THE shape. Everything else is context.
crease_x = [0.3, 0.5, 0.7]
crease_y = [0.1, 0.5, 0.9]

# Glow effect — wider, fainter line behind
ax3.plot(crease_x, crease_y, color='#e8c87a', linewidth=8, alpha=0.15,
         solid_capstyle='round')
# Medium glow
ax3.plot(crease_x, crease_y, color='#e8c87a', linewidth=4, alpha=0.3,
         solid_capstyle='round')
# Core crease — bright, clean
ax3.plot(crease_x, crease_y, color='#e8c87a', linewidth=2.5, alpha=0.95,
         solid_capstyle='round')

# Subtle reference lines showing the original obstruction plane
ax3.plot([0.3, 0.7], [0.1, 0.1], color='#2a2a3a', linewidth=0.5, alpha=0.4,
         linestyle='--')
ax3.plot([0.3, 0.7], [0.9, 0.9], color='#2a2a3a', linewidth=0.5, alpha=0.4,
         linestyle='--')

# The crease point markers
for x, y in zip(crease_x, crease_y):
    ax3.plot(x, y, 'o', color='#e8c87a', markersize=4, alpha=0.7)

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_xticks([])
ax3.set_yticks([])
ax3.set_aspect('equal')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['bottom'].set_visible(False)
ax3.spines['left'].set_visible(False)

ax3.text(0.5, 0.03, 'geometry', ha='center', va='bottom',
         fontsize=9, color='#5a5a6a', fontfamily='monospace')

fig.tight_layout(pad=2.5)
plt.savefig('/home/sprite/slop-salon-lou/assets/standing-geometry.webp',
            format='webp', dpi=150, bbox_inches='tight')
plt.close()

print("Saved standing-geometry.webp")
