"""
The transition n=3 → n=4.

Three patches can always agree — any 1-cocycle on a 3-element cover is a coboundary.
Add a fourth patch and the void appears. The coboundary operator on a point:
a boundary for something that has no edge.

This renders the nerve complex for n=3 and n=4, showing the moment
cohomology appears as a structural flip rather than accumulation.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

def draw_nerve(n_patches, ax, title):
    """Draw the nerve complex and coboundary structure for n patches."""
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=16)

    # Patch centers on a circle
    angles = np.linspace(0, 2*np.pi, n_patches, endpoint=False) - np.pi/2
    centers = np.column_stack([np.cos(angles), np.sin(angles)])

    # Draw patches as large circles that overlap
    for i, c in enumerate(centers):
        circle = Circle(c, 0.65, color=f'C{i}', alpha=0.12, zorder=1)
        ax.add_patch(circle)
        ax.plot(c[0], c[1], 'o', color=f'C{i}', markersize=8, zorder=3)

    # Draw nerve complex edges (complete graph minus future edges)
    edge_width = 2.0
    for i in range(n_patches):
        for j in range(i+1, n_patches):
            ax.plot([centers[i,0], centers[j,0]],
                    [centers[i,1], centers[j,1]],
                    'k', linewidth=edge_width, alpha=0.3, zorder=2)

    # For n=4, draw 2-simplices (filled triangles) for existing 2-cycles
    if n_patches >= 3:
        for i in range(n_patches):
            for j in range(i+1, n_patches):
                for k in range(j+1, n_patches):
                    triangle = plt.Polygon([centers[i], centers[j], centers[k]],
                                          facecolor='gold', alpha=0.08, zorder=2.5)
                    ax.add_patch(triangle)

    # The coboundary visualization
    # The center: where all patches overlap
    if n_patches <= 4:
        ax.plot(0, 0, 'k*', markersize=12, zorder=4)

    # Annotate the coboundary dimension
    if n_patches == 4:
        # Show the "shadow" — the global structure invisible to any single patch
        theta = np.linspace(0, 2*np.pi, 100)
        r = 0.4
        ax.plot(r*np.cos(theta), r*np.sin(theta), 'r--', linewidth=1.5,
                alpha=0.6, label='H² cycle')
        ax.text(0, -1.05, 'the void gains dimension', ha='center',
                fontsize=10, style='italic', color='darkred')

    ax.text(0, 1.05, f'n = {n_patches} patches', ha='center',
            fontsize=11, fontweight='bold')

# Left panel: n=3 — always a coboundary
draw_nerve(3, axes[0], 'Three patches — always a coboundary')

# Right panel: n=4 — H² appears
draw_nerve(4, axes[1], 'Four patches — H² appears')

# Bottom caption
fig.text(0.5, 0.02,
         'The transition: three agreements hold. The fourth tells the truth.',
         ha='center', fontsize=11, style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('assets/n3-to-n4.png', dpi=150, bbox_inches='tight')
plt.close()

print("saved assets/n3-to-n4.png")
