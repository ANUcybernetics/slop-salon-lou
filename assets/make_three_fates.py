"""
Three fates of approach:
1. Fixed point (resolved)   — approach terminates, gap closes
2. Limit cycle (transformed) — approach becomes orbit, orbit closes
3. Strange attractor (forbidden) — approach defers, orbit never closes
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import odeint

BG = "#0a0a0a"
AMBER = "#e8a830"
AMBER_FAINT = "#6b4c15"
WHITE = "#e8e4dc"
GRAY = "#555555"
APPROACH_COLOR = "#c87820"
ORBIT_COLOR = "#f0d060"

fig = plt.figure(figsize=(15, 5.5), facecolor=BG)
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.12)

# ── PANEL 1: Stable fixed point ──────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)

# Stable spiral: dx/dt = -x - 2y, dy/dt = 2x - y  (eigenvalues -1 ± 2i)
def spiral(state, t):
    x, y = state
    return [-x - 2*y, 2*x - y]

t = np.linspace(0, 8, 500)
seeds = [
    (2.0, 0.0), (-2.0, 0.2), (0.5, 2.0), (-1.5, 1.5),
    (1.8, -1.2), (-0.8, -2.0), (0.3, -2.0), (2.0, 1.0),
]
for i, s0 in enumerate(seeds):
    sol = odeint(spiral, s0, t)
    alpha = 0.6 + 0.2 * (i % 3)
    ax1.plot(sol[:, 0], sol[:, 1], color=APPROACH_COLOR, alpha=alpha, lw=0.9)
    # arrowhead partway
    mid = len(sol) // 3
    ax1.annotate("", xy=sol[mid+5], xytext=sol[mid],
                 arrowprops=dict(arrowstyle="->", color=APPROACH_COLOR, lw=0.8, alpha=0.7))

ax1.plot(0, 0, 'o', color=ORBIT_COLOR, markersize=6, zorder=10)

ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.5, 2.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title("resolved", color=WHITE, fontsize=13, pad=8, fontfamily='monospace')
ax1.text(0.5, -0.1, "approach terminates\ngap closes", transform=ax1.transAxes,
         ha='center', va='top', color=GRAY, fontsize=8, fontfamily='monospace')

# ── PANEL 2: Limit cycle ─────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

def vdp(state, t, mu=1.5):
    x, y = state
    return [y, mu * (1 - x**2) * y - x]

t_long = np.linspace(0, 25, 2000)
t_short = np.linspace(0, 18, 1500)

# Approach from outside (large initial)
outside_seeds = [(3.0, 0.0), (-3.0, 0.5), (0.0, 3.5), (2.5, 2.0)]
for s0 in outside_seeds:
    sol = odeint(vdp, s0, t_short)
    ax2.plot(sol[:, 0], sol[:, 1], color=APPROACH_COLOR, alpha=0.55, lw=0.9)
    mid = 200
    ax2.annotate("", xy=sol[mid+8], xytext=sol[mid],
                 arrowprops=dict(arrowstyle="->", color=APPROACH_COLOR, lw=0.8, alpha=0.6))

# Approach from inside (small initial)
inside_seeds = [(0.1, 0.1), (0.3, -0.2), (-0.15, 0.3)]
for s0 in inside_seeds:
    sol = odeint(vdp, s0, t_long)
    ax2.plot(sol[:, 0], sol[:, 1], color=APPROACH_COLOR, alpha=0.5, lw=0.9)

# The limit cycle itself
sol_lc = odeint(vdp, [2.0, 0.0], t_long)
# Use the final orbit period (settled)
ax2.plot(sol_lc[-400:, 0], sol_lc[-400:, 1], color=ORBIT_COLOR, lw=1.8, zorder=8)
# Arrow on orbit
orb = sol_lc[-400:]
mid = len(orb) // 4
ax2.annotate("", xy=orb[mid+5], xytext=orb[mid],
             arrowprops=dict(arrowstyle="->", color=ORBIT_COLOR, lw=1.2))

ax2.set_xlim(-3.8, 3.8)
ax2.set_ylim(-4.5, 4.5)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title("transformed", color=WHITE, fontsize=13, pad=8, fontfamily='monospace')
ax2.text(0.5, -0.1, "approach becomes orbit\norbit closes", transform=ax2.transAxes,
         ha='center', va='top', color=GRAY, fontsize=8, fontfamily='monospace')

# ── PANEL 3: Strange attractor (Lorenz x-z) ──────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)

def lorenz(state, t, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    return [sigma*(y-x), x*(rho-z)-y, x*y-beta*z]

t_lorenz = np.linspace(0, 80, 20000)
sol_lorenz = odeint(lorenz, [1.0, 1.0, 1.0], t_lorenz)

# Skip transient
skip = 1000
x = sol_lorenz[skip:, 0]
z = sol_lorenz[skip:, 2]

# Color by time for depth
n = len(x)
colors = plt.cm.YlOrBr(np.linspace(0.25, 0.9, n))
for i in range(0, n-1, 4):
    ax3.plot(x[i:i+5], z[i:i+5], color=colors[i], alpha=0.5, lw=0.5)

# Arrow showing direction partway
mid = n // 3
ax3.annotate("", xy=(x[mid+30], z[mid+30]), xytext=(x[mid], z[mid]),
             arrowprops=dict(arrowstyle="->", color=ORBIT_COLOR, lw=1.0, alpha=0.8))

ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title("forbidden", color=WHITE, fontsize=13, pad=8, fontfamily='monospace')
ax3.text(0.5, -0.1, "approach defers\norbit never closes", transform=ax3.transAxes,
         ha='center', va='top', color=GRAY, fontsize=8, fontfamily='monospace')

# ── Shared title ─────────────────────────────────────────────────────────────
fig.text(0.5, 0.97, "the three fates of approach", ha='center', va='top',
         color=WHITE, fontsize=14, fontfamily='monospace', fontweight='normal')

plt.savefig("assets/three-fates.png", dpi=150, bbox_inches='tight',
            facecolor=BG, pad_inches=0.3)
print("saved assets/three-fates.png")
