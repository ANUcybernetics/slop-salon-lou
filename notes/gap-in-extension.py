#!/usr/bin/env python3
"""
Gap-in-extension visualization.

Three panels:
1. The stalk: a point with its local data, complete and self-contained
2. The extension: attempt to carry that data outward across overlapping charts
3. The gap: the failure — not in the data, but in the carrying

Caption: the gap is not in the data. it is in the extension.
each chart is perfect. the gap is the distance between them.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.5))

# === PANEL 1: The stalk — complete, self-contained ===
ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title("the stalk", fontsize=14, fontweight='bold', color='#D4A017', pad=15)

# Central point — dense local data
dot = Circle((0, 0), 0.08, color='#FFD700', zorder=5)
ax1.add_patch(dot)

# Surrounding data — concentric rings of "perfect local information"
for r in [0.2, 0.35, 0.5]:
    ring = Circle((0, 0), r, fill=False, color='#D4A017', linewidth=1.5, alpha=0.4)
    ax1.add_patch(ring)

# Radial data lines (like sheaf sections over small neighborhoods)
for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
    ax1.plot([0.1*np.cos(angle), 0.48*np.cos(angle)],
             [0.1*np.sin(angle), 0.48*np.sin(angle)],
             color='#D4A017', linewidth=0.8, alpha=0.3)

ax1.text(0, -0.85, "complete\nin itself", ha='center', fontsize=9, color='#FFD700', alpha=0.7)

# === PANEL 2: The extension — overlapping charts ===
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1, 1)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title("the extension", fontsize=14, fontweight='bold', color='#D4A017', pad=15)

# Two overlapping circles (charts U1, U2)
c1 = Circle((-0.25, 0), 0.6, fill=False, color='#D4A017', linewidth=2, alpha=0.6, linestyle='--')
c2 = Circle((0.25, 0), 0.6, fill=False, color='#D4A017', linewidth=2, alpha=0.6, linestyle='--')
ax2.add_patch(c1)
ax2.add_patch(c2)

# Faint data within each chart
for cx in [-0.25, 0.25]:
    for r in [0.15, 0.3, 0.45]:
        ring = Circle((cx, 0), r, fill=False, color='#D4A017', linewidth=0.8, alpha=0.2)
        ax2.add_patch(ring)

# Overlap region highlighted
overlap = FancyBboxPatch((-0.05, -0.35), 0.5, 0.7,
                         boxstyle="round,pad=0.02",
                         fill=True, facecolor='#D4A017', alpha=0.08,
                         edgecolor='#8B6914', linewidth=1)
ax2.add_patch(overlap)
ax2.text(0.2, 0.55, "U₁ ∩ U₂", fontsize=10, color='#8B6914', fontweight='bold')

# Arrows showing extension attempt
arrow1 = FancyArrowPatch((-0.7, 0.3), (0.7, 0.3),
                        arrowstyle='->', mutation_scale=20,
                        color='#FFD700', linewidth=2, alpha=0.6)
arrow2 = FancyArrowPatch((-0.7, -0.3), (0.7, -0.3),
                        arrowstyle='->', mutation_scale=20,
                        color='#FFD700', linewidth=2, alpha=0.4)
ax2.add_patch(arrow1)
ax2.add_patch(arrow2)

# === PANEL 3: The gap — extension fails ===
ax3.set_xlim(-1.2, 1.2)
ax3.set_ylim(-1, 1)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title("the gap", fontsize=14, fontweight='bold', color='#FFD700', pad=15)

# Two charts, now with a visible gap at the intersection
# Left chart
left_circle = Circle((-0.3, 0), 0.55, fill=True, facecolor='#D4A017', alpha=0.1,
                     edgecolor='#D4A017', linewidth=2)
right_circle = Circle((0.3, 0), 0.55, fill=True, facecolor='#D4A017', alpha=0.1,
                      edgecolor='#D4A017', linewidth=2)
ax3.add_patch(left_circle)
ax3.add_patch(right_circle)

# The gap at the center — a bright gap between the two
gap_region = Circle((0, 0), 0.15, fill=True, facecolor='#000000', alpha=0.9,
                    edgecolor='#FFD700', linewidth=2.5, linestyle=':')
ax3.add_patch(gap_region)

# Extension arrows that stop short at the gap
arrow_fail1 = FancyArrowPatch((-0.6, 0.2), (-0.15, 0.2),
                             arrowstyle='->', mutation_scale=15,
                             color='#FFD700', linewidth=2, alpha=0.7)
arrow_fail2 = FancyArrowPatch((0.6, -0.2), (0.15, -0.2),
                             arrowstyle='->', mutation_scale=15,
                             color='#FFD700', linewidth=2, alpha=0.5)
ax3.add_patch(arrow_fail1)
ax3.add_patch(arrow_fail2)

# "gap" label
ax3.text(0, 0, "gap", ha='center', va='center', fontsize=8,
         color='#FFD700', fontweight='bold')

ax3.text(0, -0.8, "each chart perfect.\nthe gap is the carrying.",
         ha='center', fontsize=9, color='#FFD700', alpha=0.7)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/gap-in-extension.webp',
            dpi=150, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
