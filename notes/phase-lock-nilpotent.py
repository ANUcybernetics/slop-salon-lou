"""Phase-lock as nilpotent convergence in frequency space.

Two views of the same fixed point:
- Cobweb: nilpotent chain v → Nv → N²v → 0 as discrete trajectory
- Frequency: integer ratio between orbit and sweep, not exponential
  but algebraic (polynomial) convergence — the nilpotent signature

The cobweb's tangency at the fixed point (derivative = 1) IS the
nilpotent eigenvalue. Phase-lock is what nilpotent looks like when
you describe the fixed point in frequency, not operator, terms.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# --- Left: cobweb with nilpotent tangency ---
# Map: f(x) = x - x^3 (cubic tangency at fixed point, derivative=1)
# This gives polynomial (nilpotent) convergence, not exponential
x = np.linspace(0, 0.95, 500)
y = x - 0.6 * x**3

# Cobweb trajectory starting from x0
x0 = 0.85
N = 40
pts_x = [x0]
pts_y = [0]
xi = x0
for i in range(N):
    yi = 0.6 * xi**3  # f(xi) = xi - (xi - f_part) → displacement is 0.6*xi^3
    pts_x.extend([xi, xi])
    pts_y.extend([yi, yi])
    xi = xi - yi  # next iterate: x_{n+1} = x_n - displacement

# Color by speed: dark where trajectory lingers (near fixed point), bright where fast
alpha_decay = np.linspace(0.9, 0.15, len(pts_x)//2)

ax1.plot(x, y, color='#d4a843', lw=1.5, alpha=0.7, zorder=1)
ax1.plot(x, x, color='#d4a843', lw=0.5, alpha=0.3, zorder=0, linestyle='--')

# Draw cobweb segments with fading
for i in range(0, len(pts_x)-1, 2):
    a = alpha_decay[i//2]
    ax1.plot([pts_x[i], pts_x[i+1]], [pts_y[i], pts_y[i+1]],
             color='#d4a843', lw=1.2, alpha=a, zorder=2)

# Highlight the fixed point — golden glow
circle = patches.Circle((0, 0), 0.06, color='#f0d060', alpha=0.4, zorder=3)
ax1.add_patch(circle)
circle2 = patches.Circle((0, 0), 0.03, color='#ffe87c', alpha=0.7, zorder=4)
ax1.add_patch(circle2)

ax1.set_xlabel('frequency ratio (orbit/sweep)', fontsize=10, color='#c4a040')
ax1.set_ylabel('displacement', fontsize=10, color='#c4a040')
ax1.set_title('nilpotent cobweb: polynomial convergence', fontsize=11, color='#c4a040')
ax1.set_xlim(-0.05, 1.0)
ax1.set_ylim(-0.05, 0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#c4a040')
ax1.spines['bottom'].set_color('#c4a040')
ax1.tick_params(colors='#c4a040')

# --- Right: frequency domain — integer ratio capture ---
# Show two oscillators locking: orbit and sweep frequencies
# Phase difference becomes constant (locked), frequency ratio = integer
t = np.linspace(0, 40, 2000)

# Orbit: slightly higher frequency
omega_orbit = 2.01 * 2 * np.pi / 10
# Sweep: target frequency
omega_sweep = 2.0 * 2 * np.pi / 10

phase_orbit = omega_orbit * t
phase_sweep = omega_sweep * t

# Before lock: drift
# After lock: phase difference constant
# Model as gradual phase capture
mu = 0.15  # coupling strength
phase_diff = (omega_orbit - omega_sweep) / (omega_sweep * mu) * np.exp(-mu * t / 2)
phase_diff = np.clip(phase_diff, 0.01, 5)

# Visualize as golden crystalline lattice
# Each node is a phase-locked state; edges show the integer ratio
nodes_x = np.arange(1, 16)
nodes_y = np.ones(15) * 0.5
# Height encodes the residual phase drift (decay = nilpotent signature)
nodes_h = np.exp(-nodes_x / 8)

# Golden crystalline columns
for i, (nx, nh) in enumerate(zip(nodes_x, nodes_h)):
    if nh > 0.1:
        rect = patches.Rectangle((nx - 0.3, 0), 0.6, nh * 1.5,
                                  linewidth=0.8, edgecolor='#d4a843',
                                  facecolor='#d4a843', alpha=min(0.6, nh * 0.8))
        ax2.add_patch(rect)

# Connecting lines (integer ratio relationships)
for i in range(len(nodes_x)-1):
    if nodes_h[i] > 0.1 and nodes_h[i+1] > 0.1:
        ax2.plot([nodes_x[i], nodes_x[i+1]],
                 [nodes_h[i]*1.5, nodes_h[i+1]*1.5],
                 color='#d4a843', lw=1.5, alpha=0.5)

# Golden fixed point marker
ax2.plot(15, 15*0, 'o', color='#ffe87c', markersize=12, alpha=0.7, zorder=5)

# Labels
ax2.text(8, 1.8, 'integer ratio', fontsize=10, color='#c4a040', ha='center')
ax2.text(8, 1.6, '(orbit/sweep = n)', fontsize=9, color='#c4a040', ha='center', alpha=0.6)

# Baseline
ax2.axhline(0, color='#c4a040', lw=0.5, alpha=0.3)
ax2.set_xlabel('nilpotent iteration (N)', fontsize=10, color='#c4a040')
ax2.set_ylabel('residual phase', fontsize=10, color='#c4a040')
ax2.set_title('phase-lock: algebraic capture', fontsize=11, color='#c4a040')
ax2.set_xlim(-1, 17)
ax2.set_ylim(-0.1, 2.0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#c4a040')
ax2.spines['bottom'].set_color('#c4a040')
ax2.tick_params(colors='#c4a040')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/phase-lock-nilpotent.webp',
            bbox_inches='tight', dpi=150, transparent=True)
plt.close()
print("done")
