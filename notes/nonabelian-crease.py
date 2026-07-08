"""
Nonabelian Berry phase: U(1) vs SU(2) crease.
U(1): crease = single phase number (same loop → same holonomy)
SU(2): crease = matrix (same loop, different parameterization → different holonomy)
"""
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import matplotlib.patches as mpatches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ========= LEFT: U(1) Abelian case =========
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('U(1): Single Phase (Abelian)', fontsize=13, fontweight='bold', color='#2C5F7C')

# Draw a circular path
theta = np.linspace(0, 2*np.pi, 50)
R = 3
x = 5 + R * np.cos(theta)
y = 5 + R * np.sin(theta)
ax1.plot(x, y, '#2C5F7C', linewidth=2.5, alpha=0.7)

# Arrow direction
ax1.annotate('', xy=(x[5], y[5]), xytext=(x[4], y[4]),
             arrowprops=dict(arrowstyle='->', color='#2C5F7C', lw=2))

# Single phase accumulation shown as one number
ax1.text(5, 1.5, r'$\gamma$', fontsize=14, ha='center', color='#2C5F7C')
ax1.text(5, 0.7, r'$\mathcal{P}\!\oint_\gamma A \;=\; e^{i\gamma}$', fontsize=12,
         ha='center', color='#D4A843', fontweight='bold')
ax1.text(5, 0.1, 'same loop → same holonomy', fontsize=9,
         ha='center', color='#888', style='italic')

# ========= RIGHT: SU(2) Nonabelian case =========
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('SU(2): Matrix Crease (Nonabelian)', fontsize=13, fontweight='bold', color='#C45C5C')

# Draw TWO paths that are homotopic but give different holonomies
theta1 = np.linspace(0, 2*np.pi, 50)
R = 2.5
x1 = 3.5 + R * np.cos(theta1)
y1 = 5.5 + R * np.sin(theta1)
ax2.plot(x1, y1, '#2C5F7C', linewidth=2.5, alpha=0.7)
ax2.annotate('', xy=(x1[5], y1[5]), xytext=(x1[4], y1[4]),
             arrowprops=dict(arrowstyle='->', color='#2C5F7C', lw=2))

# Second path — homotopic but different parameterization
x2 = 7 + R * np.cos(theta1)
y2 = 5.5 + R * np.sin(theta1)
ax2.plot(x2, y2, '#C45C5C', linewidth=2.5, alpha=0.7)
ax2.annotate('', xy=(x2[5], y2[5]), xytext=(x2[4], y2[4]),
             arrowprops=dict(arrowstyle='->', color='#C45C5C', lw=2))

# Labels
ax2.text(3.5, 2.5, r'$\gamma_1$', fontsize=12, color='#2C5F7C', fontweight='bold')
ax2.text(7, 2.5, r'$\gamma_2$', fontsize=12, color='#C45C5C', fontweight='bold')

# Show they're homotopic
ax2.text(5, 8.5, r'$\gamma_1 \simeq \gamma_2$', fontsize=11,
         ha='center', color='#888', style='italic')

# But different holonomies
ax2.text(5, 7.5, r'P-exp(A) $\neq$ P-exp(A)', fontsize=12,
         ha='center', color='#C45C5C', fontweight='bold')
ax2.text(5, 6.8, r'$(U(1)\!:\, e^{i\gamma_1} = e^{i\gamma_2})$', fontsize=9,
         ha='center', color='#2C5F7C')

# The key insight
ax2.text(5, 4.5, 'path-ordering matters', fontsize=10,
         ha='center', color='#D4A843', fontweight='bold')
ax2.text(5, 3.7, 'the crease indexes by trajectory', fontsize=10,
         ha='center', color='#888', style='italic')
ax2.text(5, 2.8, r'no single holonomy —', fontsize=9,
         ha='center', color='#C45C5C')
ax2.text(5, 2.2, r'only a field of creases', fontsize=9,
         ha='center', color='#C45C5C')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/nonabelian-crease.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Created nonabelian-crease.png")
