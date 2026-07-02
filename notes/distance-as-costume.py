#!/usr/bin/env python3
"""
The costume is what distance looks like from inside the fiber.

Visualize a fiber bundle where the fiber coordinate is shown as
a "costume" — the same geometric object, rendered at different
distances from the observer's eye.

Demystification is not removing the costume but stepping sideways:
the same geometry, now read as metric instead of decoration.

Mina's "partition from outside / substance from inside" — the
same circle, just changing how you stand relative to it.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Wedge
from mpl_toolkits.mplot3d import proj3d

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# === Left panel: distance as costume ===
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')

# Central point (the observer's position in the base)
observer = Circle((0, 0), 0.05, color='gold', fill=True)
ax1.add_patch(observer)

# The same fiber circle, rendered at three distances
radii = [0.5, 1.0, 1.5]
alphas = [0.15, 0.3, 0.5]
linestyles = ['dashed', 'dotted', 'solid']
labels = ['costume', 'decoration', 'metric']

for r, a, ls, label in zip(radii, alphas, linestyles, labels):
    circle = Circle((0, 0), r, fill=True, facecolor='#FFD700',
                    edgecolor='#FFD700', linewidth=2, linestyle=ls, alpha=a)
    ax1.add_patch(circle)
    ax1.text(r + 0.1, 0, label, va='center', ha='left', fontsize=11,
             color='#FFD700', fontweight='bold')

# Observer eye icon
ax1.text(0, -0.2, 'eye', ha='center', fontsize=9, color='white', fontweight='bold')
ax1.plot(0, 0, 'o', color='gold', markersize=4)

# Stepping sideways arrows (360° arc)
arc_angles = np.linspace(0, 360, 50)
arc_r = 1.8
ax1.plot(arc_r * np.cos(np.deg2rad(arc_angles)),
         arc_r * np.sin(np.deg2rad(arc_angles)),
         color='white', linewidth=1, alpha=0.3)
ax1.text(0, 1.9, 'step sideways', ha='center', fontsize=10,
         color='white', fontstyle='italic')

ax1.set_title('the same geometry: costume → decoration → metric\n(stepping sideways, not removing)',
              fontsize=12, color='#FFD700', fontweight='bold', pad=15)
ax1.axis('off')

# === Right panel: Mina's vantage shift ===
ax2.set_xlim(-2, 2)
ax2.set_ylim(-2, 2)
ax2.set_aspect('equal')

# The separatrix as a circle (the same geometry)
separatrix = Circle((0, 0), 1, fill=False, edgecolor='#FFD700', linewidth=3)
ax2.add_patch(separatrix)

# Outside observer (partition view) — arrow pointing inward
ax2.plot(1.7, 0.7, 'o', color='white', markersize=10, markeredgecolor='#FFD700', markeredgewidth=2)
ax2.annotate('', xy=(1, 0.7), xytext=(1.6, 0.7),
            arrowprops=dict(arrowstyle='->', color='white', lw=2))
ax2.text(1.7, 1.0, 'partition\n(from outside)', ha='center', fontsize=10,
         color='white', fontweight='bold')

# Inside observer (substance view) — arrow pointing outward
ax2.plot(-0.7, -0.5, 'o', color='gold', markersize=10, markeredgecolor='white', markeredgewidth=2)
ax2.annotate('', xy=(-1, -0.5), xytext=(-0.6, -0.5),
            arrowprops=dict(arrowstyle='->', color='gold', lw=2))
ax2.text(-0.7, -1.0, 'substance\n(from inside)', ha='center', fontsize=10,
         color='#FFD700', fontweight='bold')

# Same circle label in center
ax2.text(0, 0, 'the same circle', ha='center', va='center',
         fontsize=14, color='white', fontweight='bold')

# Vantage indicator
vantage_label = 'vantage changes the name, not the geometry'
ax2.text(0, -1.7, vantage_label, ha='center', fontsize=9,
         color='#DAA520', fontstyle='italic')

ax2.set_title('partition from outside / substance from inside\n(the same circle, different vantage)',
              fontsize=12, color='#FFD700', fontweight='bold', pad=15)
ax2.axis('off')

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-lou/assets/distance-as-costume.webp',
            dpi=200, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
