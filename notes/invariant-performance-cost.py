#!/usr/bin/env python3
"""
Invariant/performance register — enactment vs verification.

Skew product: base circle rotation (invariant preserved) with fiber twist
(the cost of applying the rule).

Left: base-fiber decomposition showing rule application at each point.
Right: the orbit weaving through — not verifying, performing.
"""

import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# === LEFT: Base-fiber view ===
theta = np.linspace(0, 2*np.pi, 200)
circle_r = 0.6

# Draw base circle (golden, invariant measure)
ax1.plot(circle_r * np.cos(theta), circle_r * np.sin(theta),
         color='#D4A017', linewidth=2, alpha=0.3, zorder=1)

# Draw fiber lines from base to cost surface
fiber_theta = np.linspace(0, 2*np.pi, 40)
for ft in fiber_theta:
    idx = np.argmin(np.abs(theta - ft))
    # Fiber extends radially outward by cost amount
    cost_val = np.sin(theta[idx] * 3) * np.exp(-0.5 * np.abs(np.sin(theta[idx]/2)))
    fiber_len = 0.15 + 0.25 * (cost_val + 1) / 2
    bx = circle_r * np.cos(ft)
    by = circle_r * np.sin(ft)
    fx = bx + fiber_len * np.cos(ft)
    fy = by + fiber_len * np.sin(ft)
    bright = 0.3 + 0.7 * (fiber_len - 0.15) / 0.25
    ax1.plot([bx, fx], [by, fy],
             color=(bright*0.55, bright*0.46, 0.0),
             linewidth=1, alpha=0.6, zorder=2)

ax1.set_xlim(-1.1, 1.1)
ax1.set_ylim(-1.1, 1.1)
ax1.set_aspect('equal')
ax1.axis('off')

# === RIGHT: Orbit as enactment ===
n_steps = 500
orbit_theta = np.linspace(0, 2*np.pi * 3.5, n_steps)
# Spiral: starts at center-ish, weaves outward as cost accumulates
cost_at_step = np.sin(orbit_theta * 3) * np.exp(-0.3 * orbit_theta / (2*np.pi))
orbit_r = 0.2 + 0.5 * (0.5 + 0.5 * cost_at_step)
orbit_x = orbit_r * np.cos(orbit_theta)
orbit_y = orbit_r * np.sin(orbit_theta)

# Color by step (dark gold → bright gold)
t_frac = np.linspace(0, 1, n_steps)
for i in range(min(len(orbit_x) - 1, 2000)):
    alpha = 0.3 + 0.7 * t_frac[i]
    bright = 0.3 + 0.7 * t_frac[i]
    ax2.plot(orbit_x[i:i+2], orbit_y[i:i+2],
             color=(bright*0.55, bright*0.46, 0.0),
             linewidth=1.5, alpha=alpha, zorder=2)

# Show the base circle faintly
ax2.plot(circle_r * np.cos(theta), circle_r * np.sin(theta),
         color='#D4A017', linewidth=1, alpha=0.15, zorder=1)

# Mark start and end
ax2.plot(orbit_x[0], orbit_y[0], 'o', color='#FFD700', markersize=8, zorder=4,
         markeredgecolor='#8B6914', markeredgewidth=1)
ax2.plot(orbit_x[-1], orbit_y[-1], 'o', color='#FFF8DC', markersize=8, zorder=4,
         markeredgecolor='#D4A017', markeredgewidth=2)

ax2.set_xlim(-1.1, 1.1)
ax2.set_ylim(-1.1, 1.1)
ax2.set_aspect('equal')
ax2.axis('off')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/invariant-performance-enact.webp',
            dpi=150, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
