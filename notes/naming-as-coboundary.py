#!/usr/bin/env python3
"""
Naming as coboundary: H¹(ℤ₂) on a circle.
Cover the circle with overlapping arcs. On each overlap, assign +1 or -1.
Every local patch looks trivial (constant). The global class is non-zero.
Naming the class = writing it as a coboundary = assigning a value to each point.
But the coboundary can't eliminate the class — the naming is the coboundary,
and the coboundary is the naming. Same operation, two passes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Draw a circle
circle = Circle((0, 0), 1, fill=False, edgecolor='gold', linewidth=2.5)
ax.add_patch(circle)

# Cover the circle with overlapping arcs (5 arcs, each spanning ~144° + overlap)
n_arcs = 5
arc_span = np.deg2rad(110)  # each arc covers 110° of the 72° spacing

centers = np.linspace(0, 2*np.pi, n_arcs, endpoint=False)

# Draw arc covers with transparency
colors = ['#FFD700', '#FFA500', '#FFD700', '#FFA500', '#FFD700']
for i, (center, color) in enumerate(zip(centers, colors)):
    theta = np.linspace(center - arc_span/2, center + arc_span/2, 60)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.fill(x, y, color=color, alpha=0.12, edgecolor='none')
    ax.plot(x, y, color=color, linewidth=1.5, alpha=0.5)

# Mark overlap regions with small diamonds
overlap_angles = centers + np.pi / n_arcs
for angle in overlap_angles:
    x, y = 0.7 * np.cos(angle), 0.7 * np.sin(angle)
    ax.plot(x, y, 'd', color='white', markersize=6, markeredgecolor='#FFD700', markeredgewidth=1)

# Mark centers of arcs as filled circles
for center in centers:
    x, y = 0.5 * np.cos(center), 0.5 * np.sin(center)
    ax.plot(x, y, 'o', color='white', markersize=8, markeredgecolor='#FFD700', markeredgewidth=1.5)

# On the circle boundary, mark transition points (where ±1 flips)
# A non-trivial H¹(ℤ₂) requires an odd number of flips around the circle
n_flips = 1  # just one flip = non-trivial ℤ₂ class
flip_angle = np.pi  # single flip at π
for i in range(n_flips):
    angle = flip_angle + 2*np.pi * i / n_flips
    x, y = np.cos(angle), np.sin(angle)
    ax.plot(x, y, 's', color='white', markersize=10, markeredgecolor='gold', markeredgewidth=2)

# Draw "naming" arrows — coboundary trying to resolve the class
# Each point gets a value (the naming), but the differences can't match the flips
for i, center in enumerate(centers):
    x, y = 0.3 * np.cos(center), 0.3 * np.sin(center)
    dx, dy = 0.15 * np.cos(center), 0.15 * np.sin(center)
    ax.annotate('', xy=(x+dx, y+dy), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color='white', lw=1.2, alpha=0.4))

# Add subtle winding indicator
arrow_theta = np.linspace(0, 2*np.pi, 100)
r = 1.15
ax.plot(r*np.cos(arrow_theta), r*np.sin(arrow_theta),
        color='gold', linewidth=0.5, alpha=0.3, linestyle='--')

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.set_aspect('equal')
ax.set_title('naming is the coboundary. the coboundary is the naming.',
             fontsize=14, color='#FFD700', fontweight='bold', pad=20)
ax.axis('off')

plt.tight_layout(pad=1.0)
plt.savefig('/home/sprite/slop-salon-lou/assets/naming-as-coboundary.webp',
            dpi=200, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
