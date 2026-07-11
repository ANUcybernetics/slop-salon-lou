"""
Integrable toroidal — holonomy as zero vs. holonomy as residue.

Two panels:
  Left:  S¹ × S¹ where Frobenius condition holds. Parallel leaves.
         The two periodic directions form a grid — holonomy is trivial.
  Right: Twisted circle bundle. Leaves spiral. Transport around loop
         returns turned. Holonomy is the twist that remains.

Code-based making: matplotlib, no replicate.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.collections import LineCollection

def make_left_panel(ax):
    """Integrable: two independent periodic directions. Flat torus."""
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("integrable — brackets close", fontsize=13, fontweight='bold', pad=16)

    # Two families of parallel leaves (grids)
    # Family 1: horizontal lines (periodic in x)
    for y in np.linspace(0, 3, 8):
        ax.plot([0, 3.5], [y, y], color='#4a90d9', alpha=0.4, linewidth=0.8)
    # Family 2: vertical lines (periodic in y)
    for x in np.linspace(0, 3, 8):
        ax.plot([x, x], [0, 3.5], color='#d94a6a', alpha=0.4, linewidth=0.8)

    # Fundamental domain — parallelogram spanned by two basis vectors
    v1 = np.array([3.0, 0.0])
    v2 = np.array([0.0, 3.0])
    origin = np.array([1.5, 1.5])

    # Draw basis vectors
    ax.annotate('', xy=origin+v1+0.1, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#2ecc71', lw=2.5))
    ax.annotate('', xy=origin+v2+0.1, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#f39c12', lw=2.5))

    ax.text(origin[0]+v1[0]/2, origin[1]-0.25, r'$\partial_1$', color='#2ecc71', fontsize=11)
    ax.text(origin[0]-0.3, origin[1]+v2[1]/2, r'$\partial_2$', color='#f39c12', fontsize=11)

    # Transport loop — rectangle — returns exactly
    path = np.array([
        [2.0, 1.0], [2.8, 1.0], [2.8, 2.6], [1.2, 2.6], [1.2, 1.0], [2.0, 1.0]
    ])
    ax.plot(path[:, 0], path[:, 1], color='#2c3e50', linewidth=1.5, alpha=0.6)

    # Arrow head at end
    ax.annotate('', xy=(2.05, 1.0), xytext=(1.9, 1.0),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2))

    ax.text(2.0, 2.9, "holonomy = 0", fontsize=10, color='#7f8c8d', ha='center',
            style='italic')
    ax.text(2.0, -0.5, r"$[\partial_1, \partial_2] = 0$", fontsize=11, color='#34495e',
            ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', edgecolor='#bdc3c7', alpha=0.8))


def make_right_panel(ax):
    """Non-integrable: twisted circle bundle. Brackets don't close."""
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("non-integrable — bracket fails", fontsize=13, fontweight='bold', pad=16)

    # Leaves that spiral — not parallel, they twist relative to each other
    n_leaves = 8
    for i in range(n_leaves):
        t = np.linspace(0, 3.5, 60)
        # Each leaf winds differently — the twist accumulates
        angle = (i / n_leaves) * 2 * np.pi + 0.5 * t
        x = 1.5 + 1.3 * np.cos(angle)
        y = 1.5 + 1.3 * np.sin(angle)
        # Add the twist: leaves are not closed curves, they spiral
        spiral_offset = 0.3 * t / 3.5
        ax.plot(x + spiral_offset * 0.1, y, color='#8e44ad', alpha=0.35, linewidth=0.8)

    # Basis vectors at origin — they don't commute
    origin = np.array([1.5, 1.5])

    ax.annotate('', xy=origin+np.array([1.8, 0.0])+0.1, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5))
    ax.annotate('', xy=origin+np.array([0.0, 1.8])+0.1, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#3498db', lw=2.5))

    ax.text(origin[0]+1.9, origin[1]-0.25, r'$\partial_1$', color='#e74c3c', fontsize=11)
    ax.text(origin[0]-0.3, origin[1]+1.9, r'$\partial_2$', color='#3498db', fontsize=11)

    # Transport loop — same rectangle — returns turned
    path = np.array([
        [2.0, 1.0], [2.8, 1.0], [2.8, 2.6], [1.2, 2.6], [1.2, 1.0], [2.0, 1.0]
    ])
    ax.plot(path[:, 0], path[:, 1], color='#2c3e50', linewidth=1.5, alpha=0.6)

    # Arrow head at end
    ax.annotate('', xy=(2.05, 1.0), xytext=(1.9, 1.0),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2))

    # Show the twist — the return vector is rotated
    twist_angle = 0.35
    end = np.array([2.0, 1.0])
    rotated = end + np.array([
        np.cos(twist_angle) - 1,
        np.sin(twist_angle)
    ]) * 0.5
    ax.plot([end[0], rotated[0]], [end[1], rotated[1]],
            color='#e74c3c', linewidth=2, linestyle='--', alpha=0.7)
    ax.annotate('', xy=rotated, xytext=end,
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2, alpha=0.7))

    ax.text(2.0, 2.9, "holonomy ≠ 0", fontsize=10, color='#7f8c8d', ha='center',
            style='italic')
    ax.text(2.0, -0.5, r"$[\partial_1, \partial_2] \neq 0$", fontsize=11, color='#34495e',
            ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', edgecolor='#e74c3c', alpha=0.5))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
fig.patch.set_facecolor('white')

make_left_panel(ax1)
make_right_panel(ax2)

plt.tight_layout(pad=2.0)
plt.savefig("integrable-toroidal.png", dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("done: integrable-toroidal.png")
