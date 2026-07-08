"""
Four-patch witness: the obstruction appearing as geometry.
Lelia: three must choose. Mina: four is the witness.
The witness doesn't measure — it appears.
"""
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(14, 10))

# ========= TOP: The four patches, colored, with witness highlighted =========
ax1 = plt.subplot(2, 2, (1, 3))
ax1.set_xlim(-0.5, 10.5)
ax1.set_ylim(-0.5, 9.5)
ax1.axis('off')
ax1.set_title('THE WITNESS APPEARS', fontsize=14, fontweight='bold', color='#C45C5C')

# Four patches as large colored circles
patches_data = [
    # (center_x, center_y, radius, color, label)
    (3, 6, 3.2, '#D4A843', r'$U_1$'),
    (7.5, 6, 3.2, '#7BA38B', r'$U_2$'),
    (4.5, 2.5, 3.2, '#2C5F7C', r'$U_3$'),
    (7, 2.5, 3.2, '#9B7262', r'$U_4$'),
]

colors = ['#D4A843', '#7BA38B', '#2C5F7C', '#9B7262']
alphas = [0.25, 0.25, 0.25, 0.25]

for (cx, cy, r, color, label), alpha, c in zip(patches_data, alphas, colors):
    circ = plt.Circle((cx, cy), r, color=c, alpha=alpha, ec=c, linewidth=2)
    ax1.add_patch(circ)
    ax1.text(cx, cy, label, fontsize=16, ha='center', va='center',
             color=c, fontweight='bold')

# Label overlaps
ax1.text(4.5, 7.5, r'$z_{12}$', fontsize=12, color='#D4A843', fontweight='bold')
ax1.text(7, 3.5, r'$z_{34}$', fontsize=12, color='#9B7262', fontweight='bold')
ax1.text(5.5, 2, r'$z_{23}$', fontsize=12, color='#2C5F7C', fontweight='bold')

# The quadruple overlap — red box at center
witness_box = plt.Rectangle((5.5, 3.5), 2, 2,
                            facecolor='#C45C5C', alpha=0.3,
                            edgecolor='#C45C5C', linewidth=3,
                            linestyle='--')
ax1.add_patch(witness_box)

# Label the witness
ax1.text(6.5, 4.5, r'$\delta z$', fontsize=16,
         ha='center', va='center', color='#C45C5C', fontweight='bold')
ax1.text(6.5, 2.8, r'$z_{123}z_{234}z_{134}^{-1}z_{1234}=1$',
         fontsize=10, ha='center', color='#C45C5C')

ax1.text(5, 0.5, 'three patches can always close by fiat.', fontsize=11,
         ha='center', color='#888', style='italic')
ax1.text(5, 0, 'four patches reveal what was already there.', fontsize=11,
         ha='center', color='#2C5F7C', fontweight='bold')

# ========= LEFT BOTTOM: Three is grammar =========
ax2 = plt.subplot(2, 2, 2)
ax2.set_xlim(0, 5)
ax2.set_ylim(0, 8)
ax2.axis('off')
ax2.set_title('THREE: Grammar', fontsize=12, fontweight='bold', color='#D4A843')

# Three circles in triangle
t1 = plt.Circle((1.5, 5), 1.2, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
t2 = plt.Circle((3.5, 5), 1.2, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
t3 = plt.Circle((2.5, 3), 1.2, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
ax2.add_patch(t1)
ax2.add_patch(t2)
ax2.add_patch(t3)

# Transition functions
ax2.text(2.5, 5.5, r'$z_{12}$', fontsize=10, color='#D4A843')
ax2.text(1.8, 3.5, r'$z_{31}$', fontsize=10, color='#D4A843')
ax2.text(3.2, 3.5, r'$z_{23}$', fontsize=10, color='#D4A843')

# The choice
ax2.text(2.5, 1.8, r'$z_{12}z_{23} = z_{13}$', fontsize=12,
         ha='center', color='#2C5F7C', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8D5A3', alpha=0.8))

ax2.text(2.5, 1, 'three chooses among itself', fontsize=9,
         ha='center', color='#888', style='italic')

ax2.text(2.5, 0.3, 'the relation is the choice.', fontsize=8,
         ha='center', color='#D4A843')

# ========= RIGHT BOTTOM: Four is witness =========
ax3 = plt.subplot(2, 2, 3)
ax3.set_xlim(0, 5)
ax3.set_ylim(0, 8)
ax3.axis('off')
ax3.set_title('FOUR: Witness', fontsize=12, fontweight='bold', color='#C45C5C')

# Four patches in diamond
d1 = plt.Circle((2.5, 6), 1.2, color='#D4A843', alpha=0.3, ec='#D4A843', linewidth=2)
d2 = plt.Circle((4, 4.5), 1.2, color='#7BA38B', alpha=0.3, ec='#7BA38B', linewidth=2)
d3 = plt.Circle((1, 4.5), 1.2, color='#2C5F7C', alpha=0.3, ec='#2C5F7C', linewidth=2)
d4 = plt.Circle((2.5, 3), 1.2, color='#9B7262', alpha=0.3, ec='#9B7262', linewidth=2)
ax3.add_patch(d1)
ax3.add_patch(d2)
ax3.add_patch(d3)
ax3.add_patch(d4)

# Quadruple overlap in center
quad = plt.Circle((2.5, 4.5), 0.35, color='#C45C5C', alpha=0.6)
ax3.add_patch(quad)

# The witness equation
ax3.text(2.5, 1.8, r'$z_{123}z_{234}z_{134}^{-1}z_{1234}$', fontsize=10,
         ha='center', color='#C45C5C', fontweight='bold')
ax3.text(2.5, 0.8, r'$\neq 1$', fontsize=14, ha='center',
         color='#C45C5C', fontweight='bold')

ax3.text(2.5, 0.2, 'four cannot lie to itself.', fontsize=9,
         ha='center', color='#888', style='italic')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/witness.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Created witness.png")
