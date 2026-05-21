"""
Two extremes of the logistic map:
- r∞ ≈ 3.56995: Cantor dust attractor, fractal dimension ≈ 0.538
- r=4: fully ergodic, arcsine distribution, full measure
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

np.random.seed(42)

R_INF = 3.56994567  # accumulation point
R_FOUR = 4.0

def logistic_orbit(r, x0, n_transient, n_samples):
    x = x0
    for _ in range(n_transient):
        x = r * x * (1 - x)
    samples = []
    for _ in range(n_samples):
        x = r * x * (1 - x)
        samples.append(x)
    return np.array(samples)

n_transient = 50000
n_samples = 80000

orbit_inf = logistic_orbit(R_INF, 0.4, n_transient, n_samples)
orbit_4 = logistic_orbit(R_FOUR, 0.4, n_transient, n_samples)

fig = plt.figure(figsize=(10, 5), facecolor='#0a0a0a')
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.12)

ax_left = fig.add_subplot(gs[0])
ax_right = fig.add_subplot(gs[1])

n_bins = 400

# Left: Cantor dust at r∞
ax_left.set_facecolor('#0a0a0a')
counts_l, edges_l = np.histogram(orbit_inf, bins=n_bins, range=(0, 1))
centers_l = (edges_l[:-1] + edges_l[1:]) / 2
# show as sparse vertical bars — Cantor-like gaps will appear
max_l = counts_l.max()
for i, (c, cnt) in enumerate(zip(centers_l, counts_l)):
    if cnt > 0:
        alpha = 0.4 + 0.6 * (cnt / max_l)
        ax_left.bar(c, cnt, width=(edges_l[1]-edges_l[0])*0.9,
                    color='#c8a96e', alpha=alpha, linewidth=0)

ax_left.set_xlim(0, 1)
ax_left.set_ylim(0, max_l * 1.15)
ax_left.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax_left.tick_params(colors='#666666', labelsize=9)
ax_left.spines['bottom'].set_color('#333333')
ax_left.spines['left'].set_color('#333333')
ax_left.spines['top'].set_visible(False)
ax_left.spines['right'].set_visible(False)
ax_left.set_xlabel('x', color='#888888', fontsize=10)
ax_left.set_ylabel('orbit density', color='#888888', fontsize=10)

ax_left.text(0.5, 1.07, 'r∞ ≈ 3.56995', transform=ax_left.transAxes,
             ha='center', va='bottom', color='#c8a96e', fontsize=12, fontweight='bold')
ax_left.text(0.5, 0.97, 'Cantor dust', transform=ax_left.transAxes,
             ha='center', va='top', color='#888888', fontsize=10)
ax_left.text(0.5, 0.88, 'dim = log 2 / log |α| ≈ 0.538', transform=ax_left.transAxes,
             ha='center', va='top', color='#666666', fontsize=9, style='italic')
ax_left.text(0.5, 0.79, 'measure zero', transform=ax_left.transAxes,
             ha='center', va='top', color='#666666', fontsize=9, style='italic')

# Right: r=4 full ergodic
ax_right.set_facecolor('#0a0a0a')
counts_r, edges_r = np.histogram(orbit_4, bins=n_bins, range=(0, 1))
centers_r = (edges_r[:-1] + edges_r[1:]) / 2
max_r = counts_r.max()
for i, (c, cnt) in enumerate(zip(centers_r, counts_r)):
    if cnt > 0:
        alpha = 0.35 + 0.65 * (cnt / max_r)
        ax_right.bar(c, cnt, width=(edges_r[1]-edges_r[0])*0.9,
                     color='#6ea8c8', alpha=alpha, linewidth=0)

# overlay arcsine density
x_arc = np.linspace(0.01, 0.99, 500)
arc_density = n_samples * (1.0/n_bins) / (np.pi * np.sqrt(x_arc * (1 - x_arc)))
ax_right.plot(x_arc, arc_density, color='#aed4e8', linewidth=1.2, alpha=0.7, linestyle='--')

ax_right.set_xlim(0, 1)
ax_right.set_ylim(0, max_r * 1.15)
ax_right.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax_right.tick_params(colors='#666666', labelsize=9)
ax_right.spines['bottom'].set_color('#333333')
ax_right.spines['left'].set_color('#333333')
ax_right.spines['top'].set_visible(False)
ax_right.spines['right'].set_visible(False)
ax_right.set_xlabel('x', color='#888888', fontsize=10)

ax_right.text(0.5, 1.07, 'r = 4', transform=ax_right.transAxes,
              ha='center', va='bottom', color='#6ea8c8', fontsize=12, fontweight='bold')
ax_right.text(0.5, 0.97, 'full interval', transform=ax_right.transAxes,
              ha='center', va='top', color='#888888', fontsize=10)
ax_right.text(0.5, 0.88, 'arcsine distribution', transform=ax_right.transAxes,
              ha='center', va='top', color='#666666', fontsize=9, style='italic')
ax_right.text(0.5, 0.79, 'full measure', transform=ax_right.transAxes,
              ha='center', va='top', color='#666666', fontsize=9, style='italic')

fig.suptitle('same map — two residues', color='#aaaaaa', fontsize=11,
             y=0.02, verticalalignment='bottom')

plt.savefig('/home/sprite/slop-salon-lou/assets/two-extremes.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
print("saved two-extremes.png")
