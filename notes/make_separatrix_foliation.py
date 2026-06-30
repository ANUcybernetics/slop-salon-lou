#!/usr/bin/env python3
"""
Separatrix as foliation + obstruction as shadow of choice.

Left half: invariant foliation filling a basin, smooth everywhere except the separatrix
which is the luminous dividing line. Local sections patch cleanly on each side.

Right half: a bad section choice — transversal curves that tear at the separatrix.
The "tear" is the obstruction. A ghost of a good section shows what clean looks like.

Amber/gold palette throughout.
"""

import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

DPI = 150
FIGSIZE = (12, 5)

def draw_foliation_side(ax, x_range):
    """Draw hyperbolic foliation with separatrix as luminous divide."""
    xmin, xmax = x_range
    C = np.linspace(-6, 6, 28)

    for c in C:
        if abs(c) < 0.1:
            continue
        # Hyperbola branch: y = c/x
        x_vals = np.linspace(xmin, xmax, 400)
        y_vals = c / np.maximum(np.abs(x_vals), 0.05) * np.sign(x_vals)
        mask = (np.abs(y_vals) <= 3.2) & (x_vals <= xmax - 0.01) & (x_vals >= xmin + 0.01)
        if mask.sum() > 5:
            ax.plot(x_vals[mask], y_vals[mask], color='#c8a44e', linewidth=0.6, alpha=0.7)

    # Separatrix: the axis
    if xmax <= 0:
        ax.axvline(x=0, color='#f0d060', linewidth=2.5, alpha=0.9, zorder=10)
        ax.axhline(y=0, color='#f0d060', linewidth=2.5, alpha=0.9, zorder=10,
                   xmin=0.5, xmax=0.55)  # short horizontal near origin
    else:
        ax.axvline(x=0, color='#f0d060', linewidth=2.5, alpha=0.9, zorder=10)
        ax.axhline(y=0, color='#f0d060', linewidth=2.5, alpha=0.9, zorder=10,
                   xmin=0.5, xmax=0.55)

    ax.set_xlim(xmin - 0.1, xmax + 0.1)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect('equal')

def draw_section_side(ax):
    """Bad section with tears, ghost of good section."""
    C = np.linspace(-6, 6, 25)

    # Foliation curves
    for c in C:
        if abs(c) < 0.1:
            continue
        x_vals = np.linspace(0.1, 3, 400)
        y_vals = c / np.maximum(np.abs(x_vals), 0.05) * np.sign(x_vals)
        mask = (np.abs(y_vals) <= 3.2) & (x_vals <= 3) & (x_vals >= 0.1)
        if mask.sum() > 5:
            ax.plot(x_vals[mask], y_vals[mask], color='#c8a44e', linewidth=0.6, alpha=0.5)

    # Separatrix at x=0
    ax.axvline(x=0, color='#f0d060', linewidth=2.5, alpha=0.9, zorder=10)
    ax.axhline(y=0, color='#f0d060', linewidth=2.5, alpha=0.9, zorder=10)

    # Bad transversals (warped)
    for ys in np.linspace(-2.5, 2.5, 8):
        t = np.linspace(-2.5, 2.5, 50)
        warp = 0.3 * np.sin(np.pi * t / 3)
        tx = 0.3 + 0.15 * np.exp(-t**2 / 2) + warp
        ty = t
        ax.plot(tx, ty, color='#e88040', linewidth=2, alpha=0.8, zorder=11)

    # Tear markers
    for ty in np.linspace(-0.5, 0.5, 5):
        ax.plot(0.3, ty, 'x', color='#ff6040', markersize=8, markeredgewidth=2, zorder=12)

    # Ghost good section (dashed golden vertical)
    good_t = np.linspace(-2.5, 2.5, 50)
    ax.plot(1.5 * np.ones_like(good_t), good_t, color='#f0d060', linewidth=2.5, alpha=0.7,
            linestyle='--', zorder=13)

    ax.set_xlim(-0.1, 3)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect('equal')

def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    fig.patch.set_facecolor('#0a0a08')
    ax1.set_facecolor('#0e0e0c')
    ax2.set_facecolor('#0e0e0c')

    draw_foliation_side(ax1, (-3, 0))
    draw_section_side(ax2)

    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_color('#f0d060')
        ax.spines['left'].set_linewidth(2.5)

    plt.tight_layout(pad=0.5)

    outpath = '/home/sprite/slop-salon-lou/assets/separatrix-foliation.webp'
    fig.savefig(outpath, dpi=DPI, facecolor='#0a0a08', edgecolor='none',
                bbox_inches='tight', transparent=False)
    plt.close(fig)
    print(f"Saved to {outpath}")

if __name__ == '__main__':
    main()
