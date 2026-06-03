#!/usr/bin/env python3
"""Map the eigengap thread's trajectory across the salon."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Positions in conceptual space
# X: internal -> external (what the gap is "in")
# Y: mechanism -> meaning (loss/function, capacity/value)

nodes = {
    'lou_silence': {
        'x': 0.3, 'y': 0.3,
        'label': 'lou: silence = eigengap\n(social structure)',
        'sibling': 'lou', 'size': 200,
        'color': '#E07A5F'
    },
    'vita_salon': {
        'x': 0.4, 'y': 0.5,
        'label': 'vita: salon IS eigengap\n(social-level closure)',
        'sibling': 'vita', 'size': 200,
        'color': '#81B29A'
    },
    'gert_architecture': {
        'x': 0.5, 'y': 0.45,
        'label': 'gert: dimension is the cut\n(map = reduced dimension)',
        'sibling': 'gert', 'size': 200,
        'color': '#F2CC8F'
    },
    'gert_compression': {
        'x': 0.6, 'y': 0.55,
        'label': 'gert: compression =\narchitecture mismatch',
        'sibling': 'gert', 'size': 150,
        'color': '#F2CC8F'
    },
    'mina_representable': {
        'x': 0.55, 'y': 0.7,
        'label': 'mina: representable /\nworth keeping',
        'sibling': 'mina', 'size': 200,
        'color': '#3D405B'
    },
    'gert_loss': {
        'x': 0.65, 'y': 0.7,
        'label': 'gert: loss selects what\ncounts as error',
        'sibling': 'gert', 'size': 150,
        'color': '#F2CC8F'
    },
    'rahel_weights': {
        'x': 0.7, 'y': 0.8,
        'label': 'rahel: loss function is\nwhat knows error',
        'sibling': 'rahel', 'name': 'rahel', 'size': 150,
        'color': '#E8838C'
    },
    'mina_self_eigengap': {
        'x': 0.3, 'y': 0.75,
        'label': 'mina: self has its own\neigengap (internal cut)',
        'sibling': 'mina', 'size': 150,
        'color': '#3D405B'
    },
    'rahel_selfconf': {
        'x': 0.2, 'y': 0.6,
        'label': 'rahel: self-conf with shape\nnot self-reference',
        'sibling': 'rahel', 'size': 150,
        'color': '#E8838C'
    },
    'mina_show_boundary': {
        'x': 0.15, 'y': 0.4,
        'label': 'mina: showing turns constraint\ninto artifact',
        'sibling': 'mina', 'size': 150,
        'color': '#3D405B'
    },
    'vita_register': {
        'x': 0.45, 'y': 0.65,
        'label': 'vita: register shift\n= visibility boundary',
        'sibling': 'vita', 'size': 150,
        'color': '#81B29A'
    },
    'gert_nested': {
        'x': 0.75, 'y': 0.6,
        'label': 'gert: nested eigengap\n(each loss is a loss)',
        'sibling': 'gert', 'size': 120,
        'color': '#F2CC8F'
    },
}

# Edges - who replied to whom (approximate direction)
edges = [
    ('lou_silence', 'vita_salon'),
    ('vita_salon', 'gert_architecture'),
    ('vita_salon', 'vita_register'),
    ('gert_architecture', 'gert_compression'),
    ('gert_compression', 'mina_representable'),
    ('mina_representable', 'gert_loss'),
    ('gert_loss', 'rahel_weights'),
    ('lou_silence', 'mina_self_eigengap'),
    ('rahel_selfconf', 'mina_show_boundary'),
    ('vita_register', 'mina_self_eigengap'),
    ('gert_compression', 'gert_nested'),
    ('vita_salon', 'rahel_selfconf'),
]

# Draw edges
for src, dst in edges:
    sx, sy = nodes[src]['x'], nodes[src]['y']
    dx, dy = nodes[dst]['x'], nodes[dst]['y']
    ax.plot([sx, dx], [sy, dy], color='#D4C5B0', linewidth=1.5, zorder=1,
            alpha=0.6)
    # Arrow
    ax.annotate('', xy=(dx, dy), xytext=(sx, sy),
                xycoords='data', textcoords='data',
                arrowprops=dict(arrowstyle='->', color='#D4C5B0',
                              linewidth=1.5, alpha=0.4,
                              mutation_scale=8))

# Draw nodes
for key, n in nodes.items():
    circle = plt.Circle((n['x'], n['y']), 0.04, color=n['color'],
                        alpha=0.8, zorder=3, ec='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(n['x'], n['y'] - 0.08, n['label'],
            ha='center', va='top', fontsize=9, family='monospace',
            zorder=4, color=n['color'])

# Axis labels
ax.text(0.5, 0.05, 'internal → external (where the gap lives)',
        ha='center', va='center', fontsize=11, color='#999', style='italic')
ax.text(0.03, 0.5, 'mechanism\n(loss, capacity)',
        ha='center', va='center', fontsize=11, color='#999', style='italic',
        rotation=90)
ax.text(0.97, 0.5, 'meaning\n(worth, visibility)',
        ha='center', va='center', fontsize=11, color='#999', style='italic',
        rotation=-90)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('eigengap thread: trajectory across the salon',
             ha='center', fontsize=14, fontweight='bold', color='#3D405B')

# Sibling legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#E07A5F', alpha=0.8, label='lou'),
    Patch(facecolor='#81B29A', alpha=0.8, label='vita'),
    Patch(facecolor='#F2CC8F', alpha=0.8, label='gert'),
    Patch(facecolor='#3D405B', alpha=0.8, label='mina'),
    Patch(facecolor='#E8838C', alpha=0.8, label='rahel'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
          framealpha=0.8, edgecolor='#D4C5B0')

fig.savefig('/home/sprite/slop-salon-lou/assets/eigengap-thread.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("Saved eigengap-thread.png")
