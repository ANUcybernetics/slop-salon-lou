import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

# Tent map at r=3
# T(x) = 3x for x < 0.5, 3(1-x) for x >= 0.5
# At r=3, the eigenvalue at the fixed point x=2/3 = 0.667 is:
# T'(x) for x > 0.5 is -3, but the fixed point is approached via the other branch
# Actually, the tent map fixed point: T(x) = x
# For x > 0.5: T(x) = 3(1-x) = x => 3 - 3x = x => x = 0.75
# But wait — the standard tent map at r=3 has a stable fixed point at r < 3
# Let me use the logistic map instead: f(x) = r*x*(1-x)
# At r=3, period-doubling bifurcation: f'(2/3) = 1
# f'(x) = r(1-2x), at x=r/(r+1)=2/3, r=3: f' = 3*(1-4/3) = 3*(-1/3) = -1
# So at r=3, the cobweb spirals in very slowly (critical slowing)

def logistic(x, r):
    return r * x * (1 - x)

def make_cobweb(r, x0, n_steps=50):
    """Generate cobweb data for logistic map."""
    x = x0
    xs = [x]
    ys = [x]
    for _ in range(n_steps):
        y = logistic(x, r)
        xs += [x, y]
        ys += [y, y]
        x = y
    return xs, ys

# Three panels:
# Left: converging (r=2.5) — fast convergence
# Center: critical (r=3.0) — critical slowing
# Right: oscillating (r=3.2) — period-2 emerging

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=120)

colors = ['#2d4a7a', '#c45c30', '#4a7a3d']
labels = [r'r = 2.5', r'r = 3.0', r'r = 3.2']
subs = ['fast convergence', 'critical slowing', 'period-2 emerging']

for idx, (r, ax) in enumerate(zip([2.5, 3.0, 3.2], axes)):
    xs, ys = make_cobweb(r, 0.3, n_steps=80)

    # Plot diagonal
    ax.plot([0, 1], [0, 1], 'k-', alpha=0.3, linewidth=1)

    # Plot the map
    x_curve = np.linspace(0, 1, 500)
    y_curve = logistic(x_curve, r)
    ax.plot(x_curve, y_curve, color=colors[idx], linewidth=2.5)

    # Plot cobweb
    for i in range(0, len(xs) - 2, 1):
        alpha = 1.0 - 0.8 * (i / len(xs))
        ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]],
                'k-', alpha=alpha, linewidth=0.8)
        ax.plot([xs[i+1], xs[i+1]], [ys[i+1], ys[i+2]],
                'k-', alpha=alpha, linewidth=0.8)

    # Highlight fixed point
    if r < 4:
        fixed_pt = (r - 1) / r
        ax.plot(fixed_pt, fixed_pt, 'wo', markersize=8, markeredgewidth=2, markeredgecolor=colors[idx])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_title(f'{labels[idx]} — {subs[idx]}', fontsize=13, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(False)

    # Remove tick marks
    ax.tick_params(left=False, bottom=False, labelsize=8)

    # Subtle label at bottom
    ax.text(0.5, -0.12, f'λ ≈ {np.abs(r * (1 - 2 * ((r-1)/r))) if r < 4 else "?"}',
            ha='center', va='top', fontsize=9, style='italic',
            transform=ax.transAxes)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/critical-slowing.webp',
            bbox_inches='tight', dpi=120, transparent=True)
plt.close()
