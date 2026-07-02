#!/usr/bin/env python3
"""
The gap is in the gluing. Not in the data — in the transition function.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# === Left: data vs gluing ===
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)

patch1 = FancyBboxPatch((1, 3), 4, 4, boxstyle="round,pad=0.1",
                        edgecolor='#FFD700', linewidth=2.5)
patch1.set_facecolor('#FFD700')
patch1.set_alpha(0.1)
ax1.add_patch(patch1)

patch2 = FancyBboxPatch((4, 3), 4, 4, boxstyle="round,pad=0.1",
                        edgecolor='#DAA520', linewidth=2.5)
patch2.set_facecolor('#DAA520')
patch2.set_alpha(0.1)
ax1.add_patch(patch2)

overlap = FancyBboxPatch((4, 3), 1, 4, boxstyle="round,pad=0.05",
                         edgecolor='white', linewidth=3, linestyle='--',
                         facecolor='white')
overlap.set_alpha(0.15)
ax1.add_patch(overlap)

# Data points on each patch
for x in [2, 3]:
    for y in [4, 5, 6, 7]:
        ax1.plot(x, y, 'o', color='#FFD700', markersize=8)
for x in [5, 6, 7]:
    for y in [4, 5, 6, 7]:
        ax1.plot(x, y, 'o', color='#DAA520', markersize=8)

# Transition function arrow in overlap
ax1.annotate('', xy=(5.5, 5.5), xytext=(4.5, 6.5),
            arrowprops=dict(arrowstyle='->', color='white', lw=2.5, linestyle='dotted'))
ax1.text(5, 7.5, 'g12: U1 intersection U2 -> G', ha='center', fontsize=11,
         color='white', fontweight='bold')
ax1.text(5, 2, 'gluing = the gap', ha='center', fontsize=13,
         color='#FFD700', fontweight='bold')
ax1.text(3, 9, 'U1', ha='center', fontsize=12, color='#FFD700')
ax1.text(7, 9, 'U2', ha='center', fontsize=12, color='#DAA520')

ax1.set_title('data is locally complete. the gap is in g12.',
              fontsize=13, color='#FFD700', fontweight='bold', pad=15)
ax1.axis('off')

# === Right: coboundary as constructor ===
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)

steps = [
    ('cochain', 'local differences', '#FFD700'),
    ('coboundary', 'delta constructs the comparison', 'white'),
    ('comparison', 'the obstruction', '#DAA520'),
    ('class', 'H1 != 0 — gap confirmed', 'white')
]

y_positions = [8, 6, 4, 2]
for i, (name, desc, color) in enumerate(steps):
    box = FancyBboxPatch((2, y_positions[i]-0.4), 6, 1, boxstyle="round,pad=0.1",
                         edgecolor=color, linewidth=2)
    box.set_facecolor(color)
    box.set_alpha(0.2)
    ax2.add_patch(box)
    ax2.text(5, y_positions[i], name, ha='center', va='center',
             fontsize=11, color=color, fontweight='bold')
    if i < len(steps) - 1:
        ax2.annotate('', xy=(5, y_positions[i]-0.5), xytext=(5, y_positions[i+1]+0.4),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

ax2.set_title('delta constructs the comparison. not detection — construction.',
              fontsize=12, color='#FFD700', fontweight='bold', pad=15)
ax2.axis('off')

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-lou/assets/gap-in-gluing.webp',
            dpi=200, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
