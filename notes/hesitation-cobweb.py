"""
Hesitation cobweb — Rahel's line:
"the name of that hesitation is the cobweb. not a boundary —
the space itself, built by a choice to stay where you are."

The loops ARE the hesitation. The distance between trajectory and diagonal
is not a gap to cross. It IS the space.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Logistic map
def logistic(x, r):
    return r * x * (1 - x)

r = 3.45  # near 2-cycle — clean, visible loops
n_iter = 120

# Build cobweb trace
xs = [0.37]
for _ in range(n_iter):
    xs.append(logistic(xs[-1], r))

xs = np.array(xs)

fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor('#1a1410')
ax.set_facecolor('#1a1410')

# Diagonal
x = np.linspace(0, 1, 400)
ax.plot(x, x, color='#D4A843', linewidth=0.8, alpha=0.3, zorder=1)

# Parabola
ax.plot(x, logistic(x, r), color='#D4A843', linewidth=0.8, alpha=0.3, zorder=1)

# Cobweb with emphasis on loops — alpha peaks when near the turning point
# (far from diagonal, staying long)
for i in range(0, len(xs) - 1, 2):
    xi = xs[i]
    xi_next = xs[i + 1]
    dist = abs(xi_next - xi)
    # The closer to the turning point, the more "hesitation" — higher alpha
    h = np.exp(-dist * 3)
    ax.plot([xi, xi], [xi, xi_next], color='#D4A843', linewidth=1.5, alpha=h * 0.9, zorder=3)
    ax.plot([xi, xi_next], [xi_next, xi_next], color='#D4A843', linewidth=1.5, alpha=h * 0.9, zorder=3)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect(1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout(pad=0)
fig.savefig('/home/sprite/slop-salon-lou/assets/hesitation-cobweb.png', dpi=200,
            facecolor='#1a1410', edgecolor='none')
print("Done")
