#!/usr/bin/env python3
"""
Heteroclinic cycle visualization.
Rock-Paper-Scissors competition model:
  dx/dt = x(1 - x - y - z) - x*z*(eps)
  dy/dt = y(1 - x - y - z) - x*y*(eps)
  dz/dt = z(1 - x - y - z) - y*z*(eps)

Simplified 2D projection in the simplex x+y+z=1.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.integrate import solve_ivp

# Rock-Paper-Scissors on the simplex
# Using the May-Leonard form: x beats z, y beats x, z beats y
def may_leonard(t, u, eps=0.01):
    x, y, z = u
    dx = x * (1 - x - (1+eps)*y - z)
    dy = y * (1 - x - y - (1+eps)*z)
    dz = z * ((1+eps)*x - x - y - z + 1)
    # Actually let's use standard:
    # dx = x(1 - x - ay - bz)  with a > 1, b < 1
    return [dx, dy, dz]

def rps_ode(t, u):
    x, y, z = u
    # Standard RPS: x > z, z > y, y > x (rock beats scissors, etc.)
    # May-Leonard variant with heteroclinic cycle
    # sigma = 1, rho = 2 gives a heteroclinic cycle
    sigma = 1.0
    rho = 2.0
    dx = x * (1 - x - sigma*y - rho*z)
    dy = y * (1 - rho*x - y - sigma*z)
    dz = z * (1 - sigma*x - rho*y - z)
    return [dx, dy, dz]

def to_2d(u):
    """Project from simplex to 2D triangle coordinates."""
    x, y, z = u
    # Equilateral triangle corners
    A = np.array([0.0, 0.0])
    B = np.array([1.0, 0.0])
    C = np.array([0.5, np.sqrt(3)/2])
    return x * A + y * B + z * C

fig, ax = plt.subplots(figsize=(8, 7), facecolor='#0d1117')
ax.set_facecolor('#0d1117')

# Draw the simplex triangle
corners = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
ax.plot(corners[:, 0], corners[:, 1], color='#444', linewidth=1, alpha=0.5)

# Mark the saddle points (corners = pure strategy equilibria)
saddles = [
    np.array([0, 0]),    # x=1, y=0, z=0
    np.array([1, 0]),    # x=0, y=1, z=0
    np.array([0.5, np.sqrt(3)/2])  # x=0, y=0, z=1
]
saddle_labels = ['(1,0,0)', '(0,1,0)', '(0,0,1)']

for s in saddles:
    ax.plot(s[0], s[1], 'o', color='#e8e8e8', markersize=8, zorder=10)

# Draw heteroclinic connections (the cycle itself, along edges)
# Edge x→0 (from x=1 corner to y=1 corner), etc.
# The heteroclinic orbits lie on the edges of the simplex
edge_t = np.linspace(0, 1, 200)
# Edge from (1,0,0) to (0,1,0): x=1-t, y=t, z=0
e1 = np.array([(1-t)*np.array([0,0]) + t*np.array([1,0]) for t in edge_t])
# Edge from (0,1,0) to (0,0,1)
e2 = np.array([(1-t)*np.array([1,0]) + t*np.array([0.5, np.sqrt(3)/2]) for t in edge_t])
# Edge from (0,0,1) to (1,0,0)
e3 = np.array([(1-t)*np.array([0.5, np.sqrt(3)/2]) + t*np.array([0,0]) for t in edge_t])

ax.plot(e1[:, 0], e1[:, 1], color='#f0a500', linewidth=2.5, alpha=0.9, zorder=5)
ax.plot(e2[:, 0], e2[:, 1], color='#f0a500', linewidth=2.5, alpha=0.9, zorder=5)
ax.plot(e3[:, 0], e3[:, 1], color='#f0a500', linewidth=2.5, alpha=0.9, zorder=5)

# Add arrows along the heteroclinic connections
def add_arrow(ax, pts, color, pos=0.5):
    i = int(pos * len(pts))
    dx = pts[i+1, 0] - pts[i-1, 0]
    dy = pts[i+1, 1] - pts[i-1, 1]
    ax.annotate('', xy=(pts[i+1, 0], pts[i+1, 1]), xytext=(pts[i-1, 0], pts[i-1, 1]),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.0))

add_arrow(ax, e1, '#f0a500', 0.5)
add_arrow(ax, e2, '#f0a500', 0.5)
add_arrow(ax, e3, '#f0a500', 0.5)

# Now simulate trajectories spiraling toward the heteroclinic cycle
# Use the May-Leonard system with sigma=1, rho slightly > 1
def rps_ml(t, u, rho=1.5):
    x, y, z = u
    sigma = 1.0
    dx = x * (1 - x - sigma*y - rho*z)
    dy = y * (1 - rho*x - y - sigma*z)
    dz = z * (1 - sigma*x - rho*y - z)
    return [dx, dy, dz]

# Several initial conditions spiraling inward toward the heteroclinic cycle
t_max = 80
n_traj = 4
colors_traj = ['#4a9eff', '#6fc3ff', '#3a7ed4', '#2860b0']

for i, r0 in enumerate([0.15, 0.22, 0.30, 0.38]):
    # Start near center but offset
    angle = 2 * np.pi * i / n_traj
    # Simplex center is (1/3, 1/3, 1/3)
    cx, cy, cz = 1/3, 1/3, 1/3
    # Perturbation in barycentric
    dp = r0 * np.array([np.cos(angle), np.cos(angle + 2*np.pi/3), np.cos(angle + 4*np.pi/3)])
    u0 = np.array([cx, cy, cz]) + dp * 0.1
    u0 = np.maximum(u0, 0.01)
    u0 /= u0.sum()

    sol = solve_ivp(lambda t, u: rps_ml(t, u, rho=1.5), [0, t_max], u0,
                    dense_output=True, rtol=1e-8, atol=1e-10, max_step=0.05)

    pts = np.array([to_2d(sol.y[:, j]) for j in range(sol.y.shape[1])])

    # Color by time — later = more alpha (closer to cycle)
    n = len(pts)
    # Draw as segments fading in
    for j in range(0, n-1, 3):
        alpha = 0.2 + 0.7 * (j / n)
        ax.plot(pts[j:j+4, 0], pts[j:j+4, 1], color=colors_traj[i],
                linewidth=0.8, alpha=alpha)

# Labels
ax.text(saddles[0][0] - 0.07, saddles[0][1] - 0.05, 'x', color='#ccc', fontsize=12,
        ha='center', fontfamily='monospace')
ax.text(saddles[1][0] + 0.06, saddles[1][1] - 0.05, 'y', color='#ccc', fontsize=12,
        ha='center', fontfamily='monospace')
ax.text(saddles[2][0], saddles[2][1] + 0.05, 'z', color='#ccc', fontsize=12,
        ha='center', fontfamily='monospace')

# Title
ax.text(0.5, 0.97, 'heteroclinic cycle', transform=ax.transAxes,
        color='#e8e8e8', fontsize=13, ha='center', va='top', fontfamily='monospace')
ax.text(0.5, 0.92, 'approach: deferred   ·   orbit: ordered, period → ∞',
        transform=ax.transAxes,
        color='#888', fontsize=9.5, ha='center', va='top', fontfamily='monospace')

ax.set_xlim(-0.15, 1.15)
ax.set_ylim(-0.12, 1.02)
ax.axis('off')

plt.tight_layout()
plt.savefig('assets/heteroclinic.png', dpi=150, bbox_inches='tight',
            facecolor='#0d1117')
print("saved assets/heteroclinic.png")
