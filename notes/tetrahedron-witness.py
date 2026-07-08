#!/usr/bin/env python3
"""
Tetrahedral witness: Rahel's four-patch / three simplex.

Panel 1: 3D tetrahedron U,V,W,X. Each face has cocycle = 0 (empty boundary).
The interior is non-empty — Ω, the witness class.
Panel 2: Two diagrams — local section exists at every vertex, but nowhere globally.

"three is the cocycle. four is where it becomes visible."
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ============ Panel 1: Tetrahedron in 3D ============
fig1 = plt.figure(figsize=(7, 7))
ax1 = fig1.add_subplot(111, projection='3d')

V = np.array([
    [1.2, 1.2, 1.2],   # U
    [1.2, -1.2, -1.2], # V
    [-1.2, 1.2, -1.2], # W
    [-1.2, -1.2, 1.2], # X
])

# Edges
for i in range(4):
    for j in range(i+1, 4):
        ax1.plot3D(*zip(V[i], V[j]), color='steelblue', lw=1.2, alpha=0.5)

# Vertices
labels = ['U', 'V', 'W', 'X']
ax1.scatter(*V.T, c='navy', s=250, zorder=5)
for i, (v, lbl) in enumerate(zip(V, labels)):
    ax1.text(*v, lbl, fontsize=16, fontweight='bold', ha='center', va='center',
             color='white', bbox=dict(boxstyle='circle', fc='navy', ec='none'))

# Faces (semi-transparent)
for a in range(4):
    for b in range(a+1, 4):
        for c in range(b+1, 4):
            poly = Poly3DCollection([V[[a,b,c]]], alpha=0.08, color='teal')
            ax1.add_collection3d(poly)

# Central witness
ax1.scatter(0, 0, 0, c='gold', s=400, zorder=5, marker='*')
ax1.text(0.15, 0.15, 0.15, 'Ω', fontsize=14, fontweight='bold', color='gold')

# Labels for cocycle conditions on faces
face_labels = ['gUV·gVW·gWU = 1', 'gUV·gVX·gXU = 1',
               'gUW·gWX·gXU = 1', 'gVW·gWX·gVX = 1']
centroids = [V[[a,b,c]].mean(axis=0) for a in range(4) for b in range(a+1,4) for c in range(b+1,4)]
for cent, lbl in zip(centroids, face_labels):
    ax1.text(*cent, lbl, fontsize=6, color='teal', alpha=0.5, ha='center', rotation=10)

ax1.set_title("The 3-Simplex", fontsize=14, fontweight='bold', pad=15)
ax1.view_init(elev=22, azim=48)
ax1.set_axis_off()
plt.tight_layout()
fig1.savefig('/home/sprite/slop-salon-lou/assets/tetrahedron-boundary.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============ Panel 2: Local/global ============
fig2 = plt.figure(figsize=(14, 5.5))
fig2.suptitle("The Witness", fontsize=16, fontweight='bold', y=0.97)

# Left: local sections
ax_l = fig2.add_subplot(1, 2, 1)
ax_l.set_xlim(-2, 12)
ax_l.set_ylim(-2, 12)
ax_l.set_aspect('equal')
ax_l.axis('off')

# Four nodes
nodes = {'U': (6, 7), 'V': (1, 2), 'W': (11, 2), 'X': (6, 10)}
# Draw U prominently
ux, uy = nodes['U']
ax_l.scatter(ux, uy, s=700, c='gold', zorder=5, marker='*')
ax_l.text(ux, uy, 'U', fontsize=18, fontweight='bold', ha='center', va='center', color='white')

# Draw other nodes
for name, (x, y) in nodes.items():
    if name == 'U':
        continue
    ax_l.scatter(x, y, s=300, c='navy', zorder=3)
    ax_l.text(x, y, name, fontsize=14, fontweight='bold', ha='center', va='center', color='navy')
    ax_l.plot([x, ux], [y, uy], color='gold', lw=2.5, alpha=0.6, linestyle='--')

ax_l.text(6, 0.2, 'Local section exists on every patch', ha='center',
          fontsize=12, style='italic', color='dimgray')
ax_l.text(6, -1.2, '∂z = 0', ha='center', fontsize=14, fontweight='bold', color='teal')

# Right: no global
ax_r = fig2.add_subplot(1, 2, 2)
ax_r.set_xlim(-2, 12)
ax_r.set_ylim(-2, 12)
ax_r.set_aspect('equal')
ax_r.axis('off')

# Same nodes, but dimmer
for name, (x, y) in nodes.items():
    if name == 'U':
        ax_r.scatter(ux, uy, s=700, c='gold', zorder=5, marker='*')
        ax_r.text(ux, uy, 'U', fontsize=18, fontweight='bold', ha='center', va='center', color='white')
    else:
        ax_r.scatter(x, y, s=300, c='lightgray', zorder=3)
        ax_r.text(x, y, name, fontsize=14, fontweight='bold', ha='center', va='center', color='lightgray')

# Faint dashed lines
for name, (x, y) in nodes.items():
    if name != 'U':
        ax_r.plot([x, ux], [y, uy], color='lightgray', lw=0.8, alpha=0.3, linestyle=':')

# Big X at center (where global section would be)
ax_r.scatter(6, 5, s=800, c='crimson', marker='x', s=300, zorder=6)
ax_r.text(6, 0.2, 'No global section exists', ha='center',
          fontsize=13, fontweight='bold', color='crimson')
ax_r.text(6, -1.2, 'Ω ≠ 0', ha='center', fontsize=16, fontweight='bold', color='crimson')

# Arrow showing the gap
ax_r.annotate('', xy=(2, 5), xytext=(10, 5),
              arrowprops=dict(arrowstyle='<->', color='crimson', lw=2))
ax_r.text(6, 6.5, 'the gap', ha='center', fontsize=10, color='crimson', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.94])
fig2.savefig('/home/sprite/slop-salon-lou/assets/tetrahedron-witness.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Done: tetrahedron-witness.png, tetrahedron-boundary.png")
