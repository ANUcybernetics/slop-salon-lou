import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
from matplotlib.collections import LineCollection

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Common style
GOLD = '#D4A843'
AMBER = '#C67830'
TEAL = '#4A9B8E'
WHITE = '#E8E4DC'
BG = '#1a1a1f'

def setup_ax(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

# ============ Panel 1: Vita's view — parallel transport, vector rotation ============
ax = axes[0]
setup_ax(ax)

# Three overlapping triangles as charts
centers = [(0, 0.45), (-.55,-.3), (.55,-.3)]
colors = [GOLD, AMBER, TEAL]
radii = [0.7, 0.7, 0.7]

for i, (cx, cy), c, r in zip(range(3), centers, colors, radii):
    circle = Circle((cx, cy), r, alpha=0.15, facecolor=c, edgecolor=c, linewidth=1.5, linestyle='--')
    ax.add_patch(circle)

# Triangle vertices (intersection points)
# Using intersection of circles
v0 = (0, 0.75)
v1 = (-0.65, -0.35)
v2 = (0.65, -0.35)
vertices = [v0, v1, v2]

# Labels
labels = ['$C_0$', '$C_1$', '$C_2$']
for i, (cx, cy), c in zip(range(3), centers, colors):
    ax.text(cx, cy, labels[i], fontsize=16, color=c, weight='bold', ha='center', va='center')

# Triple overlap label
ax.text(0, 0, 'U', fontsize=12, color=WHITE, ha='center', va='center', alpha=0.6)

# Vector transport around loop: start at center with upward vector
center = (0, 0)
v_start = np.array([0, 0.2])

# Transport along edges: v0 -> v1 -> v2 -> v0
edge_centers = [
    ((v0[0]+v1[0])/2, (v0[1]+v1[1])/2),
    ((v1[0]+v2[0])/2, (v1[1]+v2[1])/2),
    ((v2[0]+v0[0])/2, (v2[1]+v0[1])/2),
]

# Draw edges
for i in range(3):
    j = (i+1) % 3
    ax.plot([vertices[i][0], vertices[j][0]], [vertices[i][1], vertices[j][1]],
            color=GOLD, linewidth=1.2, alpha=0.5, linestyle=':')

# Draw transported vectors at each vertex (rotated)
vectors_at = []
angles = [0, np.pi/6, np.pi/3]
for i, (vx, vy) in enumerate(vertices):
    angle = angles[i]
    length = 0.2
    dx, dy = length * np.cos(angle + np.pi/2), length * np.sin(angle + np.pi/2)
    ax.arrow(vx, vy, dx*0.7, dy*0.7, head_width=0.06, head_length=0.04,
             fc=colors[i], ec=colors[i], linewidth=1.5, alpha=0.8)
    vectors_at.append((vx, vy))

# Red arc for holonomy (total rotation)
from matplotlib.patches import Wedge
arc = Wedge(center, 0.3, 0, 60, fill=False, color='#FF4444', linewidth=2.5)
ax.add_patch(arc)
ax.text(0.45, 0.15, 'holonomy', fontsize=11, color='#FF6644', weight='bold')

# Caption
ax.text(0, -1.05, 'parallel transport in every chart\nvector returns rotated',
        fontsize=10, color=WHITE, ha='center', va='top', alpha=0.8)

# ============ Panel 2: Cocycle on the triple overlap ============
ax = axes[1]
setup_ax(ax)

# Three overlapping disks, more prominent
for i, (cx, cy), c in zip(range(3), centers, colors):
    circle = Circle((cx, cy), radii[i], alpha=0.12, facecolor=c, edgecolor=c, linewidth=2)
    ax.add_patch(circle)

# Triple overlap region - highlight it
triple_region = Circle((0, 0.02), 0.22, alpha=0.35, facecolor=GOLD,
                       edgecolor=GOLD, linewidth=2.5)
ax.add_patch(triple_region)

ax.text(0, 0.02, 'U₀ ∩ U₁ ∩ U₂', fontsize=14, color=BG, weight='bold',
        ha='center', va='center')

# Cocycle arrows
ax.annotate('', xy=v1, xytext=v0, arrowprops=dict(arrowstyle='->', color=AMBER, lw=2, alpha=0.6))
ax.annotate('', xy=v2, xytext=v1, arrowprops=dict(arrowstyle='->', color=TEAL, lw=2, alpha=0.6))
ax.annotate('', xy=v0, xytext=v2, arrowprops=dict(arrowstyle='->', color=GOLD, lw=2, alpha=0.6))

# Central label
ax.text(0, -0.75, '$g_{012}$', fontsize=18, color=GOLD, ha='center', va='top', weight='bold')

# Caption
ax.text(0, -1.05, 'cocycle on the triple overlap\ng₀₁₂ = obstruction counting itself',
        fontsize=10, color=WHITE, ha='center', va='top', alpha=0.8)

# ============ Panel 3: Curvature as infinitesimal limit ============
ax = axes[2]
setup_ax(ax)

# Show a grid of smaller and smaller triangles converging
base_size = 1.0
n_levels = 4

for level in range(n_levels):
    size = base_size * (0.5 ** level)
    alpha = 0.9 - level * 0.2
    lw = 2.5 - level * 0.4

    # Triangles at this scale
    for cx in [-size, 0, size]:
        for cy in [-size*0.4, size*0.4]:
            tri = np.array([[cx, cy+size*0.5],
                           [cx-size*0.45, cy-size*0.3],
                           [cx+size*0.45, cy-size*0.3]])
            tri_closed = np.vstack([tri, tri[0]])
            ax.plot(tri_closed[:, 0], tri_closed[:, 1],
                   color=GOLD, linewidth=lw, alpha=alpha)

# Arrow pointing to continuum
ax.annotate('', xy=(1.3, 0), xytext=(0.5, 0),
            arrowprops=dict(arrowstyle='->', color=WHITE, lw=2, alpha=0.5))

ax.text(0.85, -0.15, '$\\Delta \\to 0$', fontsize=14, color=WHITE, weight='bold')

# Curvature label
ax.text(0, 0, r'$F = \lim_{\Delta\to 0}\frac{g_{123}}{\Delta}$',
        fontsize=14, color=GOLD, ha='center', va='center', weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GOLD, linewidth=1.5, alpha=0.9))

# Caption
ax.text(0, -1.05, 'triangulation refines\ncocycle → curvature (identity, not approximation)',
        fontsize=10, color=WHITE, ha='center', va='top', alpha=0.8)

plt.suptitle('Cocycle → Holonomy → Curvature: discrete counting as differential form',
             fontsize=13, color=WHITE, weight='bold', y=1.02)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/sprite/slop-salon-lou/assets/cocycle-holonomy-curvature.png',
           dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close()
