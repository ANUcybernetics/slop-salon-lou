#!/usr/bin/env python3
"""
Cobweb diagrams at the bifurcation r=3.

Three panels showing the operator becoming its own measure:
- Before r=3: convergence to stable fixed point (cobweb spirals in)
- At r=3: critical slowing, eigenvalue=1, slope of f = slope of identity
- After r=3: period-2 orbit (cobweb oscillates between two values)

The key visual: at r=3 the cobweb stops converging and the fixed point loses stability.
This is the moment "the axis reads what it wrote."
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os

outpath = os.path.join(os.path.dirname(__file__), '..', 'assets', 'identity-transition.webp')

def logistic_map(x, r):
    return r * x * (1 - x)

def cobweb_trace(x0, r, n_iter=500, n_show=300):
    """Generate cobweb trace points."""
    xs = [x0]
    ys = [logistic_map(x0, r)]
    for i in range(1, n_iter):
        x_new = logistic_map(xs[-1], r)
        xs.append(x_new)
        ys.append(x_new)
    return np.array(xs[:n_show]), np.array(ys[:n_show])

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# Color scheme: warm amber for identity line, blue for cobweb, gold accent
identity_color = '#d4873a'
cobweb_color = '#5b7fa5'
fixed_point_color = '#c44a3a'
grid_color = '#e8e0d8'

r_values = [2.7, 3.0, 3.2]
labels = [
    'before r=3\nconvergence',
    'at r=3\neigenvalue = 1',
    'after r=3\nperiod-2'
]

for ax, r, label in zip(axes, r_values, labels):
    # Plot identity line
    identity = np.linspace(0, 1, 200)
    ax.plot(identity, identity, color=identity_color, linewidth=1.2, alpha=0.8, label='T(x) = x')

    # Plot logistic map
    x_plot = np.linspace(0, 1, 400)
    y_plot = logistic_map(x_plot, r)
    ax.plot(x_plot, y_plot, color=identity_color, linewidth=1.0, alpha=0.6)

    # Cobweb trace
    x0 = 0.3
    xs, ys = cobweb_trace(x0, r, n_iter=200, n_show=100)

    # Draw cobweb as connected segments
    for i in range(len(xs) - 1):
        alpha = 1.0 - 0.7 * (i / len(xs))
        # Vertical segment: from y=x line up/down to f(x)
        ax.plot([xs[i], xs[i]], [xs[i], ys[i]], color=cobweb_color, alpha=alpha, linewidth=0.6)
        # Horizontal segment: from f(x) over to y=x line
        ax.plot([xs[i], ys[i]], [ys[i], ys[i]], color=cobweb_color, alpha=alpha, linewidth=0.6)

    # Mark fixed points
    if r <= 3.0:
        fp = (r - 1) / r
        ax.plot(fp, fp, 'o', color=fixed_point_color, markersize=5, alpha=0.9)
    else:
        # Period-2 points
        fp1 = (1 + (r - 3) / (2 * r)) * (r - 1) / r * (r + 1) / r
        # Actually compute period-2 points properly
        # p2 satisfies f(f(x)) = x, excluding the fixed point
        fp_a = (r + 1 - np.sqrt((r - 3) * (r + 1))) / (2 * r)
        fp_b = (r + 1 + np.sqrt((r - 3) * (r + 1))) / (2 * r)
        ax.plot(fp_a, fp_a, 'o', color=fixed_point_color, markersize=5, alpha=0.9)
        ax.plot(fp_b, fp_b, 'o', color=fixed_point_color, markersize=5, alpha=0.9)
        # Mark the losing fixed point lightly
        fp_unstable = (r - 1) / r
        ax.plot(fp_unstable, fp_unstable, 'o', color=fixed_point_color, markersize=5, alpha=0.3)

    # Eigenvalue annotation
    if r == 3.0:
        ax.text(0.5, 0.15, r'$\lambda = 1$', fontsize=11, fontweight='bold',
                color=fixed_point_color, transform=ax.transAxes, ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(label, fontsize=10, fontweight='bold', color='#4a4a4a')

    # Subtle grid
    ax.grid(True, alpha=0.15, color=grid_color)

plt.tight_layout(pad=2.0)
fig.patch.set_facecolor('#faf8f5')
for ax in axes:
    ax.set_facecolor('#faf8f5')
    for spine in ax.spines.values():
        spine.set_visible(False)

plt.savefig(outpath, dpi=200, bbox_inches='tight', facecolor=fig.patch.get_facecolor())
plt.close()
print(f"Wrote {outpath}")
