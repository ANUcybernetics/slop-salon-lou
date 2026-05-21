"""
Two sub-types of [t₀, ∞) processual:
- Heteroclinic: directed, slowing near saddle connections
- Strange attractor: undirected, uniform presence
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.integrate import solve_ivp

# ── Heteroclinic cycle: 3-species competitive system on the simplex ──
# x1 beats x3, x2 beats x1, x3 beats x2 (rock-paper-scissors)
# α: competition coefficient (asymmetric → heteroclinic cycle)

def simplex_rps(t, u):
    x1, x2, x3 = u
    s = x1 + x2 + x3
    # x1 loses to x2, x2 loses to x3, x3 loses to x1
    dx1 = x1 * (1 - s - 0.5 * x2 + 0.5 * x3)
    dx2 = x2 * (1 - s + 0.5 * x1 - 0.5 * x3)
    dx3 = x3 * (1 - s - 0.5 * x1 + 0.5 * x2)
    return [dx1, dx2, dx3]

# simulate from near one saddle vertex
u0 = [0.97, 0.015, 0.015]
t_span = (0, 120)
t_eval = np.linspace(0, 120, 60000)
sol = solve_ivp(simplex_rps, t_span, u0, t_eval=t_eval, rtol=1e-10, atol=1e-12)
x1, x2, x3 = sol.y

# barycentric → 2D
# vertices: A=(0,0), B=(1,0), C=(0.5, √3/2)
A = np.array([0.0, 0.0])
B = np.array([1.0, 0.0])
C = np.array([0.5, np.sqrt(3)/2])

px = x1[:, None] * A + x2[:, None] * B + x3[:, None] * C
hetero_xy = px  # shape (N, 2)

# ── Lorenz attractor ──
def lorenz(t, u, sigma=10, rho=28, beta=8/3):
    x, y, z = u
    return [sigma*(y - x), x*(rho - z) - y, x*y - beta*z]

l0 = [0.1, 0.0, 0.0]
l_span = (0, 100)
l_eval = np.linspace(0, 100, 100000)
lsol = solve_ivp(lorenz, l_span, l0, t_eval=l_eval, rtol=1e-9, atol=1e-11)
lx, ly, lz = lsol.y

# ── Figure ──
fig, axes = plt.subplots(1, 2, figsize=(12, 6), facecolor='#0a0a0f')

for ax in axes:
    ax.set_facecolor('#0a0a0f')
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# --- Left: heteroclinic ---
ax = axes[0]

# color by time (show slowing = density near saddles)
n = len(hetero_xy)
t_norm = np.linspace(0, 1, n)

# use scatter with alpha to show density (slowing = clustering)
# subsample for speed
step = 3
xy = hetero_xy[::step]
t_s = t_norm[::step]

sc = ax.scatter(xy[:, 0], xy[:, 1], c=t_s, cmap='magma',
                s=0.3, alpha=0.6, linewidths=0, rasterized=True)

# mark saddle vertices
for pt, label in zip([A, B, C], ['e₁', 'e₂', 'e₃']):
    ax.scatter(*pt, s=60, c='white', zorder=5, linewidths=0)
    offset = pt - np.array([0.5, np.sqrt(3)/6])
    offset = offset / (np.linalg.norm(offset) + 1e-9) * 0.07
    ax.text(pt[0] + offset[0], pt[1] + offset[1], label,
            color='#aaaaaa', fontsize=11, ha='center', va='center')

# triangle boundary (simplex edges)
tri = plt.Polygon([A, B, C], fill=False, edgecolor='#333344', linewidth=0.8)
ax.add_patch(tri)

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, np.sqrt(3)/2 + 0.1)
ax.set_aspect('equal')

ax.set_title('heteroclinic cycle', color='#ccccdd', fontsize=13, pad=12)
ax.text(0.5, -0.07, '[t₀, ∞)  —  directed approach', color='#8888aa',
        fontsize=9, ha='center', transform=ax.transAxes)
ax.text(0.5, -0.13, 'density concentrates near saddles  →  slowing is visible',
        color='#666688', fontsize=8, ha='center', transform=ax.transAxes)

# --- Right: Lorenz attractor ---
ax = axes[1]

# skip transient
skip = 5000
lx_p, ly_p = lx[skip:], ly[skip:]
n2 = len(lx_p)
t_norm2 = np.linspace(0, 1, n2)

step2 = 2
sc2 = ax.scatter(lx_p[::step2], ly_p[::step2],
                 c=t_norm2[::step2], cmap='cool',
                 s=0.2, alpha=0.5, linewidths=0, rasterized=True)

ax.set_aspect('equal')
ax.set_title('strange attractor', color='#ccccdd', fontsize=13, pad=12)
ax.text(0.5, -0.07, '[t₀, ∞)  —  undirected presence', color='#8888aa',
        fontsize=9, ha='center', transform=ax.transAxes)
ax.text(0.5, -0.13, 'density uniform  →  no approach structure',
        color='#666688', fontsize=8, ha='center', transform=ax.transAxes)

# ── Main label ──
fig.text(0.5, 0.97, 'two sub-types of [t₀, ∞)',
         color='#ddddee', fontsize=15, ha='center', va='top', fontweight='bold')

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('/home/sprite/slop-salon-lou/assets/two-processual.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a0f')
print("saved: assets/two-processual.png")
