"""
The crease is the fixed point equation — x_{n+1} = x_n given geometric form.

Not the iteration stopping at a point. The equation IS the crease.
Cobweb where the diagonal is the crease, and the crease is why the iteration stops.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))
fig.set_dpi(200)
fig.patch.set_facecolor('#0a0a12')
ax.set_facecolor('#0a0a12')

# Map function — a single-humped curve
x = np.linspace(0.1, 0.9, 500)
y_map = 3.2 * x * (1 - x)  # logistic, slightly super-period-doubling

ax.plot(x, y_map, color='#4a4a5a', linewidth=2.5, label='')

# The diagonal y = x — THIS is the crease
diagonal_x = np.linspace(0, 1, 200)
ax.plot(diagonal_x, diagonal_x, color='#e8c87a', linewidth=3.5, alpha=0.95)

# Glow on diagonal
ax.plot(diagonal_x, diagonal_x, color='#e8c87a', linewidth=12, alpha=0.12)
ax.plot(diagonal_x, diagonal_x, color='#e8c87a', linewidth=6, alpha=0.25)

# Cobweb — starts above, spirals toward fixed point
x0 = 0.2
cobweb_x = [x0]
cobweb_y = [0]
xn = x0
for i in range(60):
    yn = 3.2 * xn * (1 - xn)
    cobweb_x += [xn, xn]
    cobweb_y += [yn, yn]
    xn = yn
    if abs(cobweb_x[-1] - cobweb_x[-2]) < 0.0001:
        break

ax.plot(cobweb_x, cobweb_y, color='#5a4a2a', linewidth=0.8, alpha=0.6)

# Fixed point — where crease meets map
x_fp = (3.2 - 1) / 3.2  # analytical fixed point
y_fp = x_fp

ax.plot(x_fp, y_fp, 'o', color='#e8c87a', markersize=6, alpha=0.9)

# Label the crease at the intersection
ax.annotate('', xy=(0.52, 0.15), xytext=(0.52, 0.35),
            arrowprops=dict(arrowstyle='-', color='#e8c87a', lw=1.2, alpha=0.7))
ax.text(0.53, 0.25, 'x_{n+1} = x_n', color='#e8c87a', fontsize=11,
        fontfamily='monospace', alpha=0.9)

ax.set_xlabel('$x_n$', fontsize=10, color='#5a5a6a', fontfamily='monospace')
ax.set_ylabel('$x_{n+1}$', fontsize=10, color='#5a5a6a', fontfamily='monospace')

# Axis labels
ax.tick_params(colors='#3a3a4a', labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Remove ticks for clean look
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

fig.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/crease-fixed-point.webp',
            format='webp', dpi=200, bbox_inches='tight')
plt.close()

print("Saved crease-fixed-point.webp")
