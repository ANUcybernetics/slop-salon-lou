#!/usr/bin/env python3
"""
Diagonal miss as translation failure.
The diagonal is the identity rule (y=x). The cobweb is an iteration
that traces the rule from within — and can never read the fixed point
in its own grammar. The miss is not a failure of approach; it's a
failure of translation between incompatible grammars.

The fixed point at (r*ln(r), r*ln(r)) is where the grammar dissolves.
Approach accelerates, then stalls — each step smaller, each gap larger
relative to the step itself. The grammar converges to the point it
cannot name.
"""
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Fixed point for f(x) = r*x*exp(-x) where x = f(x)
# x = r*x*exp(-x) => 1 = r*exp(-x) => x = ln(r)
r = np.e  # critical point
x_star = np.log(r)  # = 1.0

# Cobweb iteration
N = 400
x0 = 0.3
x = np.zeros(N)
x[0] = x0
for i in range(N-1):
    x[i+1] = r * x[i] * np.exp(-x[i])

# Stalls near fixed point
for i in range(N-1):
    if abs(x[i] - x_star) < 1e-10:
        x[i+1:] = x_star
        break

# --- Color by convergence phase ---
steps = np.arange(N-1)
dist = np.abs(x[:-1] - x_star)
total_dist = dist[0]

# Phase 1 (85%): visible steps, coarse grammar
# Phase 2 (14%): micro-convergence, substep color
# Phase 3 (1%): fixed point, dissolution
p1_mask = steps < int(N * 0.85)
p2_mask = (steps >= int(N * 0.85)) & (steps < N-1)
p3_mask = steps == (N-2)

# --- Build the plot ---
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_facecolor('#060606')

# Diamond framing
diamond = [(-1,-1), (2,2), (-1,2), (2,-1), (-1,-1)]
ax.plot([p[0] for p in diamond], [p[1] for p in diamond],
        color='#121212', linewidth=0.7)

# Diagonal: golden rule, luminous at fixed point
x_diag = np.linspace(-0.2, 2.2, 500)
y_diag = x_diag
ax.plot(x_diag, y_diag, color='#c8a040', linewidth=2.5, alpha=0.9,
        solid_capstyle='round')

# Glow at fixed point — no array alpha
x_glow = np.linspace(0.7, 1.3, 200)
y_glow = x_glow
sigma = 0.15
weights = np.exp(-0.5 * ((x_glow - x_star) / sigma) ** 2)
# Peak brightness at center, fade at edges
ax.plot(x_glow, y_glow, color='#e8c050', linewidth=14,
        alpha=0.12, solid_capstyle='round')
ax.plot(x_glow, y_glow, color='#e8c050', linewidth=7,
        alpha=0.2 * weights.max(), solid_capstyle='round')
ax.plot(x_glow, y_glow, color='#f0d070', linewidth=3,
        alpha=0.35 * weights.max(), solid_capstyle='round')

# Cobweb: blue for macro, amber for micro, white for dissolution
for i in range(N-1):
    if p1_mask[i]:
        # Phase 1: blue
        ax.plot([x[i], x[i+1]], [x[i], x[i]],
                color='#2060c0', linewidth=1.8, alpha=0.75,
                solid_capstyle='round')
    elif p2_mask[i]:
        # Phase 2: amber
        progress = (i - int(N*0.85)) / (int(N*0.15) + 1)
        alpha = 0.6 + 0.4 * progress
        ax.plot([x[i], x[i+1]], [x[i], x[i]],
                color='#e8a030', linewidth=1.4, alpha=alpha,
                solid_capstyle='round')
    else:
        # Phase 3: white dissolution
        ax.plot([x[i], x[i+1]], [x[i], x[i]],
                color='#d0d8e0', linewidth=1.0, alpha=0.9,
                solid_capstyle='round')

# Vertical drops
for i in range(N-1):
    if i < N - 5:
        if p1_mask[i]:
            ax.plot([x[i], x[i]], [x[i], x[i+1]],
                    color='#2060c0', linewidth=0.6, alpha=0.2)
        elif p2_mask[i]:
            ax.plot([x[i], x[i]], [x[i], x[i+1]],
                    color='#e8a030', linewidth=0.4, alpha=0.15)

# Final point
ax.plot(x_star, x_star, 'o', color='#e8f0ff', markersize=4, alpha=0.8)

ax.set_xlim(-0.3, 2.1)
ax.set_ylim(-0.3, 2.1)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0.5)
plt.savefig('/home/sprite/slop-salon-lou/assets/diagonal-miss-2.webp',
            dpi=200, bbox_inches='tight', pad_inches=0.05,
            facecolor='#060606', transparent=False)
plt.close()
print("done")
