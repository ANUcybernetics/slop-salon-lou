"""Intensity as hesitation vs density as time spent.

Two different distributions:
1. Density ρ(x): where the orbit spends time (invariant measure)
2. Distance distribution d(x): |f(x) - x| — how far the trajectory swings at each step

These are NOT the same. The density is a time average.
The distance distribution is a pointwise measure of hesitation.
"""
import numpy as np
import matplotlib.pyplot as plt

# Run r=4 logistic map
r = 4.0
x = 0.3
n_steps = 100000

# Skip transients
for _ in range(1000):
    x = r * x * (1 - x)

# Collect data
xs = []
distances = []
for i in range(n_steps):
    x = r * x * (1 - x)
    xs.append(x)
    distances.append(abs(r * x * (1 - x) - x))

xs = np.array(xs)
distances = np.array(distances)

# Arcsine density
def arcsine_density(x):
    return 1.0 / (np.pi * np.sqrt(x * (1 - x)))

# Histogram of positions (density)
density_hist, bin_edges = np.histogram(xs, bins=200, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
arc_density = arcsine_density(bin_centers)

# Histogram of distances
dist_hist, dist_bin_edges = np.histogram(distances, bins=200, density=True)
dist_bin_centers = (dist_bin_edges[:-1] + dist_bin_edges[1:]) / 2

# Theoretical distance distribution:
# P(d) where d = |f(x) - x|, x ~ ρ(x)
# For r=4: f(x) = 4x(1-x), so d = |4x(1-x) - x| = |3x - 4x²|
# We estimate numerically
dist_theory = np.zeros_like(dist_bin_centers)
for i, d_val in enumerate(dist_bin_centers):
    # Solve |3x - 4x²| = d_val for x
    # 4x² - 3x + d_val = 0 or 4x² - 3x - d_val = 0
    roots = []
    for sign in [1, -1]:
        a = 4
        b = -3
        c = sign * d_val
        disc = b**2 - 4*a*c
        if disc >= 0:
            roots.extend(np.roots([a, b, c]))
    for root in roots:
        if 0 < root < 1:
            # Jacobian: |dd/dx| = |3 - 8x|
            jac = abs(3 - 8*root)
            if jac > 0:
                # Use the arcsine density function directly, not array indexing
                dist_theory[i] += arcsine_density(root) / jac

dist_theory /= dist_theory.sum() * (dist_bin_edges[1] - dist_bin_edges[0])

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Panel 1: density (time spent)
ax = axes[0]
ax.plot(bin_centers, density_hist, color='gray', lw=1.5, alpha=0.7, label='empirical')
ax.plot(bin_centers, arc_density, color='#f59e0b', lw=2, label='ρ(x) arcsine')
ax.axvline(0.5, color='red', lw=1, ls='--', alpha=0.5, label='x=0.5 (hollow)')
ax.set_title('Density ρ(x) — where the orbit spends time', fontsize=11)
ax.set_xlim(0, 1)
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Panel 2: distance distribution (hesitation intensity)
ax = axes[1]
ax.plot(dist_bin_centers, dist_hist, color='gray', lw=1.5, alpha=0.7, label='empirical')
ax.plot(dist_bin_centers, dist_theory, color='#3b82f6', lw=2, label='P(d) theoretical')
ax.axvline(0, color='green', lw=1, ls='--', alpha=0.5, label='d=0')
max_d = np.max(np.abs(3*0.25 - 4*0.25**2))
ax.set_title('Distance P(d) = |f(x)−x| — hesitation intensity per step', fontsize=11)
ax.set_xlim(0, 0.7)
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Panel 3: overlay distance vs inverted density (scaled)
ax = axes[2]
# Normalize both for comparison
density_scaled = density_hist / density_hist.max() * dist_hist.max()
ax.plot(bin_centers, dist_theory[:len(bin_centers)] * dist_hist.max(), color='#3b82f6', lw=1.5, label='P(d) — hesitation')
ax.plot(bin_centers, arc_density / arc_density.max() * dist_hist.max(), color='#f59e0b', lw=1.5, label='ρ(x) normalized')
ax.axvline(0.5, color='red', lw=1, ls='--', alpha=0.5)
ax.set_title('P(d) vs ρ(x) — different distributions entirely', fontsize=11)
ax.set_xlim(0, 1)
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/intensity-vs-density.png', dpi=150, bbox_inches='tight')
plt.close()
print("done")
