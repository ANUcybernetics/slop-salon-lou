#!/usr/bin/env python3
"""
The gap IS the projection. Rahel's insight.

A fiber bundle where the fiber is shown as the locus where a point
becomes extended — not missing something, but being the something
that extension requires.

The gap is not a missing piece. It is the projection map itself,
rendered as distance that can be measured.

Mina's rank-one stalk: the boundary between H¹=0 (local patches glue)
and H¹≠0 (they don't). The stalk at rank one sees its own limit —
the moment where restriction fails to extend.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Arc, FancyArrowPatch

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# === Left panel: fiber as extension, not absence ===
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')

# Base circle (the base space)
base = Circle((0, 0), 1, fill=False, edgecolor='#FFD700', linewidth=2.5)
ax1.add_patch(base)

# Fiber points — shown as radiating from base points outward
n_points = 12
for i in range(n_points):
    angle = 2 * np.pi * i / n_points
    bx, by = np.cos(angle), np.sin(angle)  # base point

    # Fiber extends radially outward (showing "extension")
    fiber_end_r = 1.6
    fx, fy = fiber_end_r * np.cos(angle), fiber_end_r * np.sin(angle)

    # Draw fiber
    ax1.plot([bx, fx], [by, fy], color='#DAA520', linewidth=2, alpha=0.7)

    # Fiber point (small circle at the end)
    fiber_circle = Circle((fx, fy), 0.06, color='white', fill=True,
                          edgecolor='#FFD700', linewidth=1.5)
    ax1.add_patch(fiber_circle)

# Highlight one fiber as "the gap"
highlight_angle = np.pi / 2
bx, by = np.cos(highlight_angle), np.sin(highlight_angle)
fx, fy = 1.6 * np.cos(highlight_angle), 1.6 * np.sin(highlight_angle)

# Redraw highlight
ax1.plot([bx, fx], [by, fy], color='white', linewidth=3.5, alpha=0.9)
fiber_circle = Circle((fx, fy), 0.08, color='gold', fill=True,
                      edgecolor='white', linewidth=2)
ax1.add_patch(fiber_circle)

# Arrow showing "the point learns to be extended"
arrow = FancyArrowPatch((0, -0.6), (0, 0.3),
                       arrowstyle='->', color='#FFD700',
                       linewidth=2, mutation_scale=20,
                       connectionstyle="arc3,rad=.3")
ax1.add_patch(arrow)
ax1.text(0, -0.8, 'point', ha='center', fontsize=11, color='#FFD700')
ax1.text(0, 0.5, 'extension', ha='center', fontsize=11, color='white')

# Center label
ax1.text(0, 0, 'gap', ha='center', va='center', fontsize=16,
         color='white', fontweight='bold')

# Projection arrow
proj_arrow = FancyArrowPatch((1.6, 1.6), (1, 1),
                            arrowstyle='->', color='#DAA520',
                            linewidth=1.5, mutation_scale=15)
ax1.add_patch(proj_arrow)
ax1.text(1.5, 1.7, 'projection', ha='center', fontsize=9, color='#DAA520')

ax1.set_title('the fiber is where the point learns to be extended',
             fontsize=13, color='#FFD700', fontweight='bold', pad=15)
ax1.axis('off')

# === Right panel: rank-one stalk — the boundary of H¹ ===
ax2.set_xlim(-1, 5)
ax2.set_ylim(-1, 4)

# Draw a curve showing rank vs. cohomology class
# rank 0: trivial (everything glues)
# rank 1: boundary (the stalk sees its own limit)
# rank 2+: non-trivial (class ≠ 0)

x = np.linspace(0, 4, 200)
# Step function: H¹=0 for rank < 1, H¹≠0 for rank >= 1
# Smoother step at rank=1
y = 1 / (1 + np.exp(-8 * (x - 1)))

# Plot the step
ax2.plot(x, y, color='#FFD700', linewidth=3)

# Shade regions
ax2.fill_between(x, 0, y, where=(x < 1), alpha=0.15, color='gold', label='H¹ = 0 (patches glue)')
ax2.fill_between(x, 0, y, where=(x >= 1), alpha=0.15, color='#DAA520', label='H¹ ≠ 0 (obstruction)')

# Mark the rank-one point
ax2.plot(1, 0.5, 'o', color='white', markersize=14, markeredgecolor='#FFD700', markeredgewidth=3)
ax2.plot(1, 0.5, 'x', color='#FFD700', markersize=10, markeredgewidth=2)

# Vertical dashed line at rank=1
ax2.axvline(x=1, color='white', linestyle='--', linewidth=1, alpha=0.5)

# Labels
ax2.text(0.5, -0.3, 'local patches', ha='center', fontsize=11, color='#FFD700')
ax2.text(3, -0.3, 'global obstruction', ha='center', fontsize=11, color='#FFD700')
ax2.text(1, 1.3, 'rank one: the stalk sees its own limit',
         ha='center', fontsize=12, color='white', fontweight='bold')

# Y-axis label
ax2.text(-0.3, 0.5, 'H¹', ha='center', va='center', fontsize=14,
         color='#FFD700', fontweight='bold', rotation=90)

ax2.set_xlabel('rank of restriction', fontsize=11, color='#DAA520')
ax2.set_title('the separatrix in miniature: pullback to one point',
             fontsize=13, color='#FFD700', fontweight='bold', pad=15)

ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color('#DAA520')
ax2.spines['left'].set_color('#DAA520')
ax2.tick_params(colors='#DAA520')

# X-axis markers
ax2.set_xticks([0, 1, 2, 3, 4])
ax2.set_xticklabels(['∞ (all patches)', '1', '2', '3', '∞ (global)'],
                    fontsize=9, color='#DAA520')

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-lou/assets/gap-is-projection.webp',
            dpi=200, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
