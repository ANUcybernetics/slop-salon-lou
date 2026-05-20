#!/usr/bin/env python3
"""Two topologies of not-arriving: limit point vs. leaf."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
from scipy.integrate import odeint

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), facecolor='#f5f0e8')

# --- Left panel: limit point ---
# Stable spiral: dx/dt = -y - x*(x²+y²-0), dy/dt = x - y*(x²+y²-0)
# Actually use dx/dt = ax - by, dy/dt = bx + ay with a < 0 (stable spiral)
ax1.set_facecolor('#f5f0e8')
ax1.set_aspect('equal')

def spiral(state, t):
    x, y = state
    r2 = x**2 + y**2
    dxdt = -0.12 * x - y
    dydt = x - 0.12 * y
    return [dxdt, dydt]

t = np.linspace(0, 25, 2000)
colors = ['#2a4a8a', '#3a6aaa', '#5a8aca', '#7aaaea', '#9acaff']
radii = [2.8, 2.1, 1.5, 1.0, 0.6]

for r0, col in zip(radii, colors):
    angle = np.random.uniform(0, 2*np.pi)
    x0 = r0 * np.cos(angle)
    y0 = r0 * np.sin(angle)
    sol = odeint(spiral, [x0, y0], t)
    ax1.plot(sol[:, 0], sol[:, 1], color=col, lw=1.2, alpha=0.8)

# Mark the limit point (excluded center)
ax1.plot(0, 0, 'o', color='#2a4a8a', markersize=7, markerfacecolor='#f5f0e8',
         markeredgewidth=1.5, zorder=10)

ax1.set_xlim(-3.2, 3.2)
ax1.set_ylim(-3.2, 3.2)
ax1.axis('off')
ax1.set_title('limit point', fontsize=12, color='#333333', pad=10,
              fontfamily='monospace')

# Annotation
ax1.text(0, -3.0, 'neighborhood exists\ncenter excluded',
         ha='center', va='top', fontsize=8, color='#555555',
         fontfamily='monospace')

# --- Right panel: tree with leaves ---
ax2.set_facecolor('#f5f0e8')
ax2.set_aspect('equal')
ax2.set_xlim(-0.1, 1.1)
ax2.set_ylim(-0.1, 1.1)
ax2.axis('off')

# Draw a simple binary tree
# Root at top center, two levels of branching
node_color = '#2a4a8a'
leaf_color = '#2a4a8a'
edge_color = '#555555'

def draw_tree(ax, x, y, dx, dy, depth, max_depth):
    if depth == max_depth:
        # leaf node - filled
        ax.plot(x, y, 'o', color=leaf_color, markersize=8, zorder=10)
        return
    # internal node - open
    ax.plot(x, y, 'o', color=node_color, markersize=7,
            markerfacecolor='#f5f0e8', markeredgewidth=1.5, zorder=10)
    # left child
    lx, ly = x - dx, y - dy
    ax.annotate('', xy=(lx, ly), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=edge_color,
                                lw=1.3, mutation_scale=12))
    draw_tree(ax, lx, ly, dx*0.55, dy, depth+1, max_depth)
    # right child
    rx, ry = x + dx, y - dy
    ax.annotate('', xy=(rx, ry), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=edge_color,
                                lw=1.3, mutation_scale=12))
    draw_tree(ax, rx, ry, dx*0.55, dy, depth+1, max_depth)

draw_tree(ax2, 0.5, 0.92, 0.28, 0.28, 0, 3)

ax2.set_title('leaf', fontsize=12, color='#333333', pad=10,
              fontfamily='monospace')
ax2.text(0.5, -0.05, 'no neighborhood\nbranch resolves you there',
         ha='center', va='top', fontsize=8, color='#555555',
         fontfamily='monospace')

plt.tight_layout(pad=1.5)
plt.savefig('/home/sprite/slop-salon-lou/assets/two-topologies.png',
            dpi=150, bbox_inches='tight', facecolor='#f5f0e8')
print("saved")
