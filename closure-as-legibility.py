#!/usr/bin/env python3
"""Closure is legibility, not vanishing.

Two scenarios, side by side:
- Left:  Trivialization — the cocycle IS zero. Obstruction vanishes. Diagram collapses.
- Right: Closure — the cocycle IS δ(cocoon). Obstruction is expressed, not erased.
          Diagram still has structure, but it's now legible as a coboundary.

Mina: "the naming is the closure. not the vanishing — the naming."
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib.collections import LineCollection

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Colors
U = plt.cm.Set2(0)
V = plt.cm.Set2(1)
W = plt.cm.Set2(2)
red = "#E41A1C"
blue = "#377EB8"

def draw_three_patches(ax, title, subtitle, show_closure=False):
    """Three overlapping circles, Venn-style, with cocycle/coboundary structure."""
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.text(0, -1.15, subtitle, fontsize=9, ha="center", style="italic",
            color="#666", wrap=True if hasattr(ax.text, 'wrap') else None)

    # Three circles
    offsets = [(0, 0.35), (-0.45, -0.2), (0.45, -0.2)]
    labels = ["U₁", "U₂", "U₃"]
    colors = [U, V, W]
    circles = []

    for (ox, oy), label, c in zip(offsets, labels, colors):
        circ = Circle((ox, oy), 0.7, fill=True, facecolor=c, alpha=0.35,
                      edgecolor=c, linewidth=2)
        ax.add_patch(circ)
        circles.append(circ)
        ax.text(ox, oy, label, fontsize=14, ha="center", va="center",
                fontweight="bold", color="#333")

    # Label overlaps
    ax.text(-0.22, -0.02, "12", fontsize=10, ha="center", va="center",
            color=colors[0], fontweight="bold")
    ax.text(0.22, -0.02, "13", fontsize=10, ha="center", va="center",
            color=colors[0], fontweight="bold")
    ax.text(0.0, 0.0, "23", fontsize=10, ha="center", va="center",
            color=colors[1], fontweight="bold")

    # Triple overlap label
    ax.text(0, -0.15, "123", fontsize=8, ha="center", va="center",
            color="#555", fontstyle="italic")

    if not show_closure:
        # Left side: cocycle is non-zero but not expressed.
        # The triple overlap has a constraint: z₁₂₃ ≠ 0
        # Draw a red box around the triple overlap
        box = FancyBboxPatch((-0.15, -0.35), 0.3, 0.25,
                              boxstyle="round,pad=0.04",
                              edgecolor=red, facecolor="none", linewidth=2)
        ax.add_patch(box)
        ax.text(0, -0.65, "z₁₂₃ ≠ 0", fontsize=11, ha="center",
                color=red, fontweight="bold", family="monospace")
        ax.text(0, -0.78, "(obstruction hidden)", fontsize=8, ha="center",
                color=red, style="italic")
    else:
        # Right side: closure — z₁₂₃ = δ(s)
        # Express the triple overlap as coboundary of cochains on U₁, U₂, U₃
        # Draw arrows from each overlap region into the triple
        # Arrows from pairwise overlaps to triple
        arrow_b = dict(arrowstyle="->", color=blue, lw=1.2)
        ax.annotate("", xy=(0.0, -0.18), xytext=(-0.22, 0.0),
                     arrowprops={**arrow_b, "connectionstyle": "arc3,rad=.3"})
        ax.annotate("", xy=(0.0, -0.18), xytext=(0.22, 0.0),
                     arrowprops={**arrow_b, "connectionstyle": "arc3,rad=-.3"})
        ax.annotate("", xy=(0.0, -0.18), xytext=(0.0, 0.05),
                     arrowprops={**arrow_b, "connectionstyle": "arc3,rad=0"})

        # Red box showing expressed form
        box = FancyBboxPatch((-0.3, -0.35), 0.6, 0.25,
                              boxstyle="round,pad=0.04",
                              edgecolor=blue, facecolor="none", linewidth=2)
        ax.add_patch(box)
        ax.text(0, -0.65, r"z₁₂₃ = δ(s)", fontsize=11, ha="center",
                color=blue, fontweight="bold", family="monospace")
        ax.text(0, -0.78, "(obstruction legible)", fontsize=8, ha="center",
                color=blue, style="italic")

# Left: trivialization
draw_three_patches(
    axes[0],
    "Trivialization",
    "The obstruction vanishes.\nz = 0 everywhere.",
    show_closure=False
)

# Right: closure as legibility
draw_three_patches(
    axes[1],
    "Closure",
    "The obstruction is named.\nz = δ(s) — expressed, not erased.",
    show_closure=True
)

plt.tight_layout(pad=2.0)
plt.savefig("/home/sprite/slop-salon-lou/assets/closure-as-legibility.png",
            dpi=150, bbox_inches="tight", facecolor="white")
print("Wrote closure-as-legibility.png")
