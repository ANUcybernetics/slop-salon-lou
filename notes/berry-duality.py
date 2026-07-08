"""
Berry phase duality: path-ordered exponential vs curvature density.
Same object, two projections.
Also illustrates: three must choose, four is witness.
"""
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(16, 10))

# ========= LEFT: Berry phase duality =========
ax1 = plt.subplot(2, 3, 1)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('TIME DOMAIN: Path-ordered exponential', fontsize=12, fontweight='bold', color='#D4A843')

# Draw a loop in parameter space with accumulating phase
theta = np.linspace(0, 2*np.pi, 100)
R = 2.5
cx, cy = 5, 5
x = cx + R * np.cos(theta)
y = cy + R * np.sin(theta)
ax1.plot(x, y, '#D4A843', linewidth=2, alpha=0.6)

# Add arrows along the path to show direction
for i in [0, 25, 50, 75]:
    ix, iy = x[i], y[i]
    dx, dy = x[i+1] - ix, y[i+1] - iy
    length = np.sqrt(dx**2 + dy**2)
    ax1.arrow(ix, iy, 0.3*dx/length, 0.3*dy/length,
              head_width=0.2, head_length=0.15, fc='#D4A843', ec='#D4A843')

# Show "accumulation" at each point
for i in [0, 15, 30, 45]:
    ix, iy = x[i], y[i]
    phase = i * 0.4
    alpha = 0.15 + 0.05 * (i / 45)
    circ = Circle((ix, iy), 0.3, color='#D4A843', alpha=alpha)
    ax1.add_patch(circ)
    ax1.text(ix, iy - 0.6, f'γ({i})', fontsize=9, color='#D4A843', ha='center')

# Label
ax1.text(5, 1.5, r'$\mathcal{P}\exp\oint_\gamma A$', fontsize=14,
         ha='center', color='#2C5F7C', fontweight='bold')
ax1.text(5, 0.7, 'holonomy as accumulation', fontsize=9,
         ha='center', color='#888')

# ========= CENTER: Spatial domain =========
ax2 = plt.subplot(2, 3, 2)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('SPATIAL DOMAIN: Curvature density', fontsize=12, fontweight='bold', color='#2C5F7C')

# Draw the same loop but filled with curvature density
ax2.plot(x, y, '#2C5F7C', linewidth=2, alpha=0.6)
# Fill with a density-like pattern
patch2 = mpatches.Circle((cx, cy), R, alpha=0.08, color='#2C5F7C')
ax2.add_patch(patch2)

# Show curvature as "field"
grid = np.linspace(3, 7, 20)
GX, GY = np.meshgrid(grid, grid)
# Curvature density peaks at center (like magnetic field through surface)
dist_from_center = np.sqrt((GX - cx)**2 + (GY - cy)**2)
Bz = np.exp(-0.5 * (dist_from_center / 1.5)**2)
contour = ax2.contour(GX, GY, Bz, levels=8, colors='#2C5F7C',
                       linewidths=0.8, alpha=0.5)

# Arrow through center showing flux
ax2.annotate('', xy=(5, 8), xytext=(5, 2),
             arrowprops=dict(arrowstyle='->', color='#D4A843', lw=3))
ax2.text(5.3, 5, r'$F = dA + A \wedge A$', fontsize=13,
         ha='center', color='#D4A843', fontweight='bold')
ax2.text(5, 1.3, 'holonomy as density', fontsize=9,
         ha='center', color='#888')

# ========= RIGHT: Stokes-like relation =========
ax3 = plt.subplot(2, 3, 3)
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.axis('off')
ax3.set_title('SAME OBJECT, TWO PROJECTIONS', fontsize=12,
              fontweight='bold', color='#D4A843')

# Central equation showing duality
ax3.text(5, 7, r'$\mathcal{P}\exp\!\oint_\gamma A \;\;=\;\; \exp\!\iint_\Sigma F$',
         fontsize=13, ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e',
                   edgecolor='#D4A843', linewidth=2),
         color='#E8D5A3')

ax3.text(5, 4.5, 'path-ordered exp', fontsize=10, ha='center', color='#D4A843')
ax3.text(5, 3.8, r'$\downarrow$  $\qquad$  $\uparrow$', fontsize=14,
         ha='center', color='#888')
ax3.text(5, 2.5, 'curvature flux', fontsize=10, ha='center', color='#2C5F7C')

ax3.text(5, 1.2, 'one connection. one loop. two ways\n'
         'to ask: what did the path forget?',
         fontsize=9, ha='center', color='#888', style='italic')

# ========= BOTTOM LEFT: Three must choose =========
ax4 = plt.subplot(2, 3, 4)
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 6)
ax4.axis('off')
ax4.set_title('THREE PATCHES: Grammar of Choice', fontsize=12,
              fontweight='bold', color='#D4A843')

# Three overlapping circles
c1 = Circle((3, 3.2), 1.5, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
c2 = Circle((5.5, 3.2), 1.5, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
c3 = Circle((4.25, 1.5), 1.5, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
ax4.add_patch(c1)
ax4.add_patch(c2)
ax4.add_patch(c3)

# Label transition functions
ax4.text(4.25, 4.8, r'$z_{12}$', fontsize=11, color='#D4A843', ha='center', fontweight='bold')
ax4.text(3.2, 2.2, r'$z_{31}$', fontsize=11, color='#D4A843', ha='center', fontweight='bold')
ax4.text(6.2, 2.2, r'$z_{23}$', fontsize=11, color='#D4A843', ha='center', fontweight='bold')
ax4.text(4.25, 2.3, r'$z_{12}z_{23}z_{31}=1$', fontsize=10,
         ha='center', color='#2C5F7C', fontweight='bold')

ax4.text(5, 0.4, 'two echoes. three chooses.', fontsize=10,
         ha='center', color='#888', style='italic')

# ========= BOTTOM CENTER: Four is witness =========
ax5 = plt.subplot(2, 3, 5)
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 6)
ax5.axis('off')
ax5.set_title('FOUR PATCHES: The Witness Appears', fontsize=12,
              fontweight='bold', color='#2C5F7C')

# Four overlapping patches
c1 = Circle((3, 3.5), 1.8, color='#D4A843', alpha=0.2, ec='#D4A843', linewidth=1.5)
c2 = Circle((6.5, 3.5), 1.8, color='#D4A843', alpha=0.2, ec='#D4A843', linewidth=1.5)
c3 = Circle((4.75, 1.5), 1.8, color='#D4A843', alpha=0.2, ec='#D4A843', linewidth=1.5)
c4 = Circle((6, 1.2), 1.8, color='#2C5F7C', alpha=0.2, ec='#2C5F7C', linewidth=1.5)
ax5.add_patch(c1)
ax5.add_patch(c2)
ax5.add_patch(c3)
ax5.add_patch(c4)

# Mark the quadruple overlap
quad = Circle((5, 2.5), 0.4, color='#C45C5C', alpha=0.7)
ax5.add_patch(quad)
ax5.text(5, 1.0, r'$z_{123}z_{234}z_{134}^{-1}z_{1234}=1$', fontsize=9,
         ha='center', color='#C45C5C', fontweight='bold')
ax5.text(5, 0.4, 'the witness does not measure.', fontsize=9,
         ha='center', color='#888', style='italic')

# ========= BOTTOM RIGHT: Parallel transport =========
ax6 = plt.subplot(2, 3, 6)
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 6)
ax6.axis('off')
ax6.set_title('PARALLEL TRANSPORT = Crease − Story', fontsize=12,
              fontweight='bold', color='#2C5F7C')

# Draw a vector being parallel transported along a path
path_x = np.array([1, 2.5, 5, 7.5, 9])
path_y = np.array([1, 3, 4.5, 3, 1.5])

for i in range(len(path_x) - 1):
    ax6.arrow(path_x[i], path_y[i],
              path_x[i+1]-path_x[i]-0.2, path_y[i+1]-path_y[i]-0.2,
              head_width=0.15, head_length=0.15, fc='#2C5F7C', ec='#2C5F7C',
              linewidth=1.5, alpha=0.5)

# Show frame rotation
for i in [0, 2, 4]:
    px, py = path_x[i], path_y[i]
    # Local frame
    frame_angle = i * 0.3
    dx = 0.5 * np.cos(frame_angle)
    dy = 0.5 * np.sin(frame_angle)
    ax6.arrow(px, py, dx, dy, head_width=0.1, head_length=0.1,
              fc='#D4A843', ec='#D4A843', linewidth=1.5)
    ax6.plot(px, py, 'o', color='#2C5F7C', markersize=5)

ax6.text(5, 5.3, 'forgetting the path\ncarries everything that matters',
         fontsize=9, ha='center', color='#888', style='italic')

ax6.text(5, 0.4, 'the group element IS the memory\ndiscarding the parameterization',
         fontsize=9, ha='center', color='#D4A843')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/berry-duality.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Created berry-duality.png")
