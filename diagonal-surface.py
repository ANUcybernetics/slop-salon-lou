#!/usr/bin/env python3
"""The diagonal as cleavage plane: cobweb diagonal rendered as a positive geometric surface.
Points move around the diagonal rather than through it. It's a boundary in the
geometry of the space, not a line you cross.
"""

import numpy as np
import matplotlib.pyplot as plt

r = 3.9
N = 40
iterations = 100

# Cobweb iteration
xs = np.zeros(N)
ys = np.zeros(N)
xs[0] = 0.3

# Build cobweb but treat diagonal as a surface
# We'll render points near the diagonal as "reflecting" off a thin surface
# rather than passing through it

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Draw the diagonal as a gradient surface — a "cleavage plane"
x_surface = np.linspace(0, 1, 100)
# The diagonal as a thickened region — cleavage plane
for i in range(5):
    offset = (i - 2) * 0.015
    ax.fill_between(x_surface, x_surface + offset - 0.007,
                     x_surface + offset + 0.007,
                     color='gold', alpha=0.08, zorder=1)

ax.plot([0, 1], [0, 1], color='gold', linewidth=1.5, alpha=0.5, zorder=2,
        label='the diagonal as surface')

# Draw the logistic curve
x_curve = np.linspace(0, 1, 200)
y_curve = r * x_curve * (1 - x_curve)
ax.plot(x_curve, y_curve, color='crimson', linewidth=2, zorder=3)

# Cobweb iteration
pts = [(xs[0], ys[0])]
for i in range(1, N):
    # Vertical: (x_n, y_n) from curve
    y = r * xs[i-1] * (1 - xs[i-1])
    xs[i] = y
    ys[i] = y

    # Horizontal: next x
    # But render the move as a path that bends AROUND the diagonal surface
    x_prev = r * xs[i-2] * (1 - xs[i-2]) if i > 1 else xs[0]

    # Draw vertical segment
    ax.plot([xs[i-1], xs[i-1]], [ys[i-1], ys[i]],
            color='steelblue', linewidth=1.2, alpha=0.7, zorder=4)

    # Draw horizontal segment
    if i < N - 1:
        ax.plot([xs[i], xs[i+1]], [ys[i], ys[i]],
                color='steelblue', linewidth=1.2, alpha=0.7, zorder=4)

    pts.append((xs[i], ys[i]))

# Mark fixed points as "solid" — presence not absence
fixed = (r - 1) / r
circle = plt.Circle((fixed, fixed), 0.03, color='gold', zorder=10,
                    edgecolor='white', linewidth=2)
ax.add_patch(circle)

ax.text(fixed + 0.08, fixed, 'p* as presence', color='gold', fontsize=11, zorder=11,
        va='center', fontweight='bold')

# Add a second axis for the "geometry of the space"
ax2 = fig.add_axes([0.15, 0.12, 0.25, 0.15], polar=False)
ax2.set_xlim(-0.1, 1.1)
ax2.set_ylim(-0.1, 1.1)

# The diagonal as a facet in the geometry — points as small dots showing
# how the cobweb learns the constraint
x2 = 0.5
y2 = r * x2 * (1 - x2)

# Draw a small region showing the "touching" — the geometry at the diagonal
small_x = np.linspace(0.3, 0.7, 50)
ax2.fill_between(small_x, small_x - 0.03, small_x + 0.03,
                 color='gold', alpha=0.2, zorder=1)
ax2.plot(small_x, small_x, color='gold', linewidth=2, zorder=2)

# Small cobweb in this detail view
sx = [0.4]
sy = [r * 0.4 * (1 - 0.4)]
for i in range(20):
    sx.append(sy[-1])
    sy.append(r * sx[-1] * (1 - sx[-1]))
    if sx[-1] < 0 or sx[-1] > 1:
        break

ax2.plot(sx, sy, color='crimson', linewidth=1.5, alpha=0.8, zorder=3)
ax2.plot(sx, [s for s in sx], color='gold', linewidth=1, linestyle='--',
         alpha=0.4, zorder=2)

ax2.text(0.5, -0.05, 'the diagonal as cleavage plane',
         ha='center', fontsize=8, color='gold')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax.set_xlabel('xₙ', fontsize=12, color='steelblue')
ax.set_ylabel('f(xₙ)', fontsize=12, color='crimson')
ax.set_title('the diagonal as cleavage plane: threshold as geometry you move around',
             fontsize=13, color='gold', fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/diagonal-surface.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved diagonal-surface.png")
