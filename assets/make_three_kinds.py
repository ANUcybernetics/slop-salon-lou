import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

fig, axes = plt.subplots(1, 3, figsize=(15, 5.5), facecolor='#0a0a0a')
fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02, wspace=0.06)

# ---- Panel 1: Strange attractor — hidden ----
ax1 = axes[0]
ax1.set_facecolor('#0a0a0a')

def lorenz(t, y, sigma=10, rho=28, beta=8/3):
    x, y_, z = y
    return [sigma*(y_-x), x*(rho-z)-y_, x*y_-beta*z]

sol = solve_ivp(lorenz, [0, 80], [0.1, 0, 0], max_step=0.005, dense_output=True)
t = np.linspace(5, 80, 20000)
xyz = sol.sol(t)

colors = plt.cm.plasma(np.linspace(0, 1, len(t)-1))
for i in range(0, len(t)-1, 2):
    ax1.plot(xyz[0,i:i+2], xyz[2,i:i+2], color=colors[i], alpha=0.55, lw=0.5)

ax1.set_xlim(xyz[0].min()-2, xyz[0].max()+2)
ax1.set_ylim(xyz[2].min()-2, xyz[2].max()+2)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('hidden\nno trajectory detects the gap', color='#666666',
              fontsize=10, pad=10, fontfamily='monospace')

# ---- Panel 2: Heteroclinic cycle — felt ----
ax2 = axes[1]
ax2.set_facecolor('#0a0a0a')

# Three saddles in equilateral triangle
angles = np.array([np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 + 4*np.pi/3])
saddles = np.array([[np.cos(a), np.sin(a)] for a in angles]) * 0.85

# Draw connecting manifolds (curved arcs saddle→saddle)
n_laps = 5
for lap in range(n_laps):
    alpha = 0.9 * (0.65 ** lap)
    lw = 2.0 * (0.72 ** lap)
    scale = 1.0 - lap * 0.04  # slight inward drift

    for i in range(3):
        s1 = saddles[i] * scale
        s2 = saddles[(i+1) % 3] * scale

        t_path = np.linspace(0, 1, 200)
        # Control point slightly inside the triangle
        mid = (s1 + s2) / 2
        # Perpendicular inward
        perp = np.array([-(s2-s1)[1], (s2-s1)[0]])
        perp = perp / np.linalg.norm(perp)
        # Inward means toward centroid (0,0)
        if np.dot(perp, -mid) < 0:
            perp = -perp
        ctrl = mid + perp * 0.18

        path = (np.outer((1-t_path)**2, s1) +
                np.outer(2*t_path*(1-t_path), ctrl) +
                np.outer(t_path**2, s2))

        # Slow down the second half of each arc: longer time on exit
        ax2.plot(path[:,0], path[:,1], color='#4fc3f7', alpha=alpha, lw=lw)

# Draw saddles
for s in saddles:
    ax2.plot(s[0], s[1], 'o', color='#ff6b35', markersize=9, zorder=6)
    ax2.plot(s[0], s[1], 'o', color='#0a0a0a', markersize=4, zorder=7)

# Annotation for slowing
ax2.text(0, -1.35, 'each lap longer', color='#333333',
         fontsize=7.5, ha='center', fontfamily='monospace', style='italic')

ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.4)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('felt\napproach signals non-arrival', color='#666666',
              fontsize=10, pad=10, fontfamily='monospace')

# ---- Panel 3: Gray-Scott reaction-diffusion — processual ----
ax3 = axes[2]
ax3.set_facecolor('#0a0a0a')

N = 150
F, k = 0.022, 0.051
Du, Dv = 0.16, 0.08

rng = np.random.default_rng(42)
U = np.ones((N, N))
V = np.zeros((N, N))

# Multiple seeds
for _ in range(5):
    cx = rng.integers(20, N-20)
    cy = rng.integers(20, N-20)
    r = rng.integers(5, 12)
    U[cx-r:cx+r, cy-r:cy+r] = 0.5 + 0.1*rng.standard_normal((2*r, 2*r))
    V[cx-r:cx+r, cy-r:cy+r] = 0.25 + 0.1*rng.standard_normal((2*r, 2*r))

def laplacian(Z):
    return (np.roll(Z,1,0)+np.roll(Z,-1,0)+np.roll(Z,1,1)+np.roll(Z,-1,1)-4*Z)

dt = 1.0
for _ in range(10000):
    uvv = U * V * V
    U += dt * (Du * laplacian(U) - uvv + F * (1 - U))
    V += dt * (Dv * laplacian(V) + uvv - (F + k) * V)

im = ax3.imshow(V, cmap='inferno', vmin=0, vmax=V.max() * 0.9,
                interpolation='bilinear', aspect='equal')
ax3.axis('off')
ax3.set_title('processual\nform is motion', color='#666666',
              fontsize=10, pad=10, fontfamily='monospace')

plt.savefig('/home/sprite/slop-salon-lou/assets/three-kinds-forbidden.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()
print("done")
