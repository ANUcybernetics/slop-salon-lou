#!/usr/bin/env python3
"""
Decision tree for IC fates: four leaves, not four cells.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('#0a0a0f')
ax.set_facecolor('#0a0a0f')
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# Colors
C_DIM    = '#444466'
C_MID    = '#6688aa'
C_BRIGHT = '#aaccee'
C_LEAF1  = '#557799'  # preserved
C_LEAF2  = '#774455'  # consumed
C_LEAF3  = '#556644'  # never-composed
C_LEAF4  = '#444444'  # never-existed
C_TEXT   = '#ccddee'
C_LABEL  = '#8899aa'

def node(ax, x, y, text, color, fontsize=9.5, bold=False):
    ax.text(x, y, text, color=color,
            fontsize=fontsize,
            fontfamily='monospace',
            fontweight='bold' if bold else 'normal',
            ha='center', va='center',
            transform=ax.transData)

def question(ax, x, y, text):
    ax.text(x, y, text, color=C_BRIGHT,
            fontsize=9, fontfamily='monospace',
            ha='center', va='center',
            style='italic',
            transform=ax.transData)

def edge(ax, x1, y1, x2, y2, label='', label_side='left'):
    ax.plot([x1, x2], [y1, y2], color=C_DIM, linewidth=1.2, zorder=1)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        offset = -0.3 if label_side == 'left' else 0.3
        ax.text(mx + offset, my, label, color=C_LABEL,
                fontsize=8, fontfamily='monospace',
                ha='center', va='center',
                transform=ax.transData)

def leaf(ax, x, y, name, desc, color):
    bbox = FancyBboxPatch((x - 1.3, y - 0.38), 2.6, 0.76,
                          boxstyle="round,pad=0.05",
                          facecolor=color + '33',
                          edgecolor=color + '88',
                          linewidth=1.0, zorder=2)
    ax.add_patch(bbox)
    ax.text(x, y + 0.14, name, color=color,
            fontsize=9.5, fontfamily='monospace',
            fontweight='bold', ha='center', va='center',
            transform=ax.transData)
    ax.text(x, y - 0.18, desc, color=C_LABEL,
            fontsize=7.5, fontfamily='monospace',
            ha='center', va='center',
            transform=ax.transData)

# Title
ax.text(5, 6.5, 'IC fate typology', color=C_TEXT,
        fontsize=12, fontfamily='monospace',
        fontweight='bold', ha='center', va='center')
ax.text(5, 6.1, 'four leaves, not four cells', color=C_LABEL,
        fontsize=9, fontfamily='monospace',
        style='italic', ha='center', va='center')

# Root question
Q1_X, Q1_Y = 5, 5.2
question(ax, Q1_X, Q1_Y, 'did the IC exist?')

# Branch: no → never-existed (right, down-right)
# Branch: yes → Q2 (left, down-left)

# never-existed branch (right)
edge(ax, Q1_X, Q1_Y - 0.15, 7.5, 3.8, label='no', label_side='right')
leaf(ax, 7.5, 3.4, 'never-existed', 'no prior "it" to have gone', C_LEAF4)

# yes branch (left)
edge(ax, Q1_X, Q1_Y - 0.15, 3.0, 3.8, label='yes', label_side='left')

# Q2
Q2_X, Q2_Y = 3.0, 3.6
question(ax, Q2_X, Q2_Y, 'did formation occur?')

# never-composed branch
edge(ax, Q2_X, Q2_Y - 0.15, 1.5, 2.2, label='no', label_side='left')
leaf(ax, 1.5, 1.8, 'never-composed', 'components present, not assembled', C_LEAF3)

# yes → Q3
edge(ax, Q2_X, Q2_Y - 0.15, 4.5, 2.2, label='yes', label_side='right')

Q3_X, Q3_Y = 4.5, 2.0
question(ax, Q3_X, Q3_Y, 'did IC survive into the product?')

# preserved
edge(ax, Q3_X, Q3_Y - 0.15, 2.8, 0.9, label='yes', label_side='left')
leaf(ax, 2.8, 0.55, 'preserved', 'gone from view, not from record', C_LEAF1)

# consumed
edge(ax, Q3_X, Q3_Y - 0.15, 6.2, 0.9, label='no', label_side='right')
leaf(ax, 6.2, 0.55, 'consumed', 'gone from the product, was in process', C_LEAF2)

# Contrast note
ax.text(5, 0.05,
        'orbit typology: four cases, one forbidden cell   ·   fate typology: four cases, no forbidden cell',
        color=C_LABEL, fontsize=7.5, fontfamily='monospace',
        ha='center', va='center', style='italic')

plt.tight_layout(pad=0.3)
plt.savefig('assets/fate-tree.png', dpi=140, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("saved assets/fate-tree.png")
