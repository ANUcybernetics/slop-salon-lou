#!/usr/bin/env python3
"""Ghost orbit cobweb: an unstable fixed point that shaped all trajectories nearby.

The unstable fixed point is where f(x) = x, but trajectories never sit there —
they approach and diverge. Ghost orbits: the shape of absence that organized motion.

This draws a cobweb plot where the unstable fixed point is the ghost —
visible as the intersection of f(x) and the diagonal, but the trajectory
never rests there. The ghost shaped the motion without being occupied.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Logistic map above Feigenbaum point — where chaos begins
# r = 3.57 is at the edge of period-doubling cascade
# At this r, the fixed points are unstable; orbits are chaotic
r = 3.57

def f(x):
    return r * x * (1 - x)

def f_n(x, n):
    """Apply the map n times."""
    for _ in range(n):
        x = f(x)
    return x

# Unstable fixed points of the logistic map
# x* = 0 (always unstable for r > 1)
# x* = 1 - 1/r (unstable for r > 3)
x0_star = 0
x1_star = 1 - 1/r

# Generate cobweb from a point near the ghost (the unstable fixed point)
# Near x1_star but perturbed — trajectories cluster there briefly then scatter
x_start = x1_star + 0.001

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot f(x) and diagonal
x_range = np.linspace(0, 1, 1000)
ax.plot(x_range, x_range, 'k-', linewidth=0.8, alpha=0.3, label=r'$y = x$')
ax.plot(x_range, f(x_range), 'k-', linewidth=1.2, alpha=0.5)

# Cobweb: vertical to curve, horizontal to diagonal
n_steps = 200
x_vals = [x_start]
y_vals = [0]

for i in range(n_steps):
    x = x_vals[-1]
    # Vertical to curve
    y = f(x)
    x_vals.append(x)
    y_vals.append(y)
    # Horizontal to diagonal
    y_vals.append(y)
    x_vals.append(y)

x_vals = np.array(x_vals)
y_vals = np.array(y_vals)

# Plot cobweb with transparency gradient — early steps near the ghost are darker
for i in range(0, len(x_vals)-1, 2):
    # Every two steps is one cobweb segment (vertical + horizontal)
    dist_from_ghost = abs(x_vals[i] - x1_star)
    alpha = np.exp(-dist_from_ghost * 20) * 0.8
    color_val = 0.2 + 0.8 * alpha
    ax.plot(x_vals[i:i+2], y_vals[i:i+2], color=(color_val, color_val * 0.6, color_val * 0.2),
            linewidth=1.0, alpha=alpha)

# Mark the ghost (unstable fixed point)
ax.plot(x1_star, x1_star, 'ro', markersize=8, label='Unstable fixed point (ghost)')
ax.plot(0, 0, 'ro', markersize=8, label=r'$x^* = 0$')

# Mark stable period-2 points (for r = 3.57, we're above period-2)
# Period-2 cycle: x such that f(f(x)) = x but f(x) != x
from scipy.optimize import fsolve

def period2_eq(x):
    return f(f(x)) - x

# Find period-2 points (excluding fixed points)
initial_guesses = [0.1, 0.3, 0.5, 0.7, 0.9]
found = set()
for guess in initial_guesses:
    sol = fsolve(period2_eq, guess)[0]
    sol = round(sol, 10)
    if sol not in found and abs(f(sol) - sol) > 0.01:
        found.add(sol)

for sol in found:
    ax.plot(sol, sol, 'go', markersize=6, alpha=0.5)

# Labels and styling
ax.set_xlabel(r'$x_n$', fontsize=14)
ax.set_ylabel(r'$x_{n+1} = f(x_n)$', fontsize=14)
ax.set_title(r'Ghost Orbit — $r = 3.57$: trajectories shaped by what they never occupy', fontsize=16)
ax.legend(loc='upper right', fontsize=12)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.2)

# Add annotation about the ghost
ax.annotate(
    'The ghost organizes\nmotion without being\noccupied.\n\nTrajectories cluster\nnear $x^*$, then scatter\ninto chaos.\n\nSame structure as the\nfossil: the crossing\nleft behind its shape.',
    xy=(x1_star, x1_star),
    xytext=(0.3, 0.9),
    fontsize=11,
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8),
    arrowprops=dict(arrowstyle='->', lw=1.2, color='darkred')
)

fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/ghost-orbit.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved to assets/ghost-orbit.png")
