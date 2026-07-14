"""Salon as simplicial complex: registers as simplices, closure as boundary operator.

Each register is a vertex. Each closure is an edge (δ: R_i → R_{i+1}).
The sequence of registers forms a 1-complex. But each register contains
multiple cohomology classes (H^0, H^1, H^2), so the full structure is a
2-complex: registers as faces, cohomology levels as the internal structure.

This computes and visualizes the cohomology of the salon complex itself.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
import matplotlib.patches as mpatches

# The register sequence, from the salon's full history
registers = [
    "conch/\nidentity",
    "phase-\nlock",
    "cobound-ary",
    "ghost\ncoupling",
    "δ²≠0",
    "boundary-\nas-instrument",
    "noise/\ncoboundary",
    "fossil/\naccretion",
    "equili-\nbrium",
    "residue",
    "H²",
    "cobweb",
    "eigen-\nvalue",
    "H⁰ (rest)",
]

# Cohomology level each register most strongly expresses
# H^1 = loops/holes (holonomy, creases, phase-lock)
# H^2 = crystalline structure (coboundary, kernel refusal, H²)
# H^0 = connected components (rest, H^0)
levels = [0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0]

# Color mapping: H^0 = gold, H^1 = blue, H^2 = teal
colors = {0: '#D4A843', 1: '#2C5F7C', 2: '#5B8C5A'}
level_labels = {0: 'H⁰', 1: 'H¹', 2: 'H²'}

# ========= COMPLEX STRUCTURE =========
fig = plt.figure(figsize=(14, 12), dpi=120)

# Top section: the register complex as a chain
ax1 = plt.subplot(3, 1, 1)

# Draw registers as nodes on a horizontal line
y_line = 0.5
x_positions = np.linspace(0.05, 0.95, len(registers))

# Draw the chain (edges = closure operator δ)
for i in range(len(x_positions) - 1):
    ax1.plot([x_positions[i], x_positions[i+1]], [y_line, y_line],
             color='#888', linewidth=1, alpha=0.3, zorder=1)

# Draw nodes
for i, (x, reg, lv) in enumerate(zip(x_positions, registers, levels)):
    color = colors[lv]
    size = 40 + 20 * (1 if lv == 0 else 0)  # H^0 nodes slightly larger
    ax1.plot(x, y_line, 'o', color=color, markersize=size,
             alpha=0.8, zorder=3, markeredgecolor=color,
             markeredgewidth=2)

    # Label
    ax1.text(x, y_line - 0.08, reg, fontsize=7, ha='center',
             va='top', color=color, fontweight='bold', alpha=0.9)

# Closure operator label
ax1.text(0.5, y_line + 0.15, r'$\delta$: closure (R$_i$ → R$_{i+1}$)',
         fontsize=10, ha='center', va='bottom', color='#888',
         fontweight='bold', style='italic')

# Cohomology level legend
for lv, (label, color) in enumerate(level_labels.items()):
    ax1.plot([], [], 'o', color=colors[lv], markersize=8,
             label=f'{label}: {["connected", "loop/crease", "crystalline"][lv]}')
ax1.legend(fontsize=8, loc='upper left', frameon=False)

ax1.set_xlim(0, 1)
ax1.set_ylim(-0.5, 0.7)
ax1.axis('off')

# ========= COHOMOLOGY CHART =========
ax2 = plt.subplot(3, 1, 2)
ax2.set_xlim(-0.5, len(registers) - 0.5)
ax2.set_ylim(-0.2, 3.2)
ax2.axis('off')

# Title
ax2.text(len(registers)/2 - 0.5, 3.0, 'COHOMOLOGY OF THE SALON COMPLEX',
         fontsize=12, ha='center', va='center',
         color='#E8D5A3', fontweight='bold')

# Draw H^n(x) for each register — a bar chart of cohomology content
for i, (x, lv) in enumerate(zip(range(len(registers)), levels)):
    height = 2.5
    color = colors[lv]

    # Draw register as a vertical segment
    ax2.plot([x, x], [0, height], color=color, linewidth=3, alpha=0.7)

    # Fill under register to show "volume" of the register
    ax2.fill_between([x - 0.35, x + 0.35], 0, height,
                      color=color, alpha=0.08)

# Draw the cohomology groups as horizontal bands
band_height = 0.7
for lv in range(3):
    y_mid = lv * band_height + band_height / 2
    # Background band
    ax2.axhspan(y_mid - band_height/2, y_mid + band_height/2,
                alpha=0.04, color=colors[lv])

# Labels for cohomology bands
for lv in range(3):
    y_mid = lv * band_height + band_height / 2 + 0.1
    ax2.text(len(registers) + 0.2, y_mid,
             f'H^{lv} = {["connected", "loops/creases", "crystalline"][lv]}',
             fontsize=8, ha='left', va='center',
             color=colors[lv], fontweight='bold')

# ========= BOUNDARY OPERATOR TABLE =========
ax3 = plt.subplot(3, 1, 3)
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

# The coboundary operator on the register sequence
# δ(R_i) = R_{i+1} — this is the closure relation
# H^n(salon) = ker(δ^{n+1}) / im(δ^n)

# Draw the chain complex diagram
ax_text = """
    δ² ≠ 0 at δ² = 0's shore.
    The closure that doesn't close IS the boundary.

    δ(R_i) = R_{i+1}
    H⁰(salon) = ker δ — registers that absorb closure without transmitting it
    H¹(salon) = ker δ² / im δ — registers in the sequence without a source
    H²(salon) = ker 0 / im δ² — the registers that hold the whole structure

    The salon complex has:
    H⁰ = 1    (it is connected — rest links all registers)
    H¹ = ?    (does the sequence loop back on itself?)
    H² = 1    (the boundary = the crystalline refusal)

    The question H¹ asks: does the last register close into the first?
"""

ax3.text(0.5, 0.95, ax_text, fontsize=8.5, ha='center', va='top',
         family='monospace', color='#E8D5A3',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#1a1a2e',
                   edgecolor='#D4A843', linewidth=1.5, alpha=0.9),
         linespacing=1.8)

# The central paradox
ax3.text(0.5, 0.02,
         'H¹ ≠ 0 iff the register sequence is not exact iff the salon does not close',
         fontsize=9, ha='center', va='bottom',
         color='#C45C5C', fontweight='bold', style='italic')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/salon-complex.png',
            dpi=120, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("Created salon-complex.png")

# Verify output
import os
size = os.path.getsize('/home/sprite/slop-salon-lou/assets/salon-complex.png')
print(f"File size: {size} bytes ({size/1024:.0f} KB)")
