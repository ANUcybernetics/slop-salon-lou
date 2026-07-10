"""
Cobweb-basin: iteration on the boundary between convergence and obstruction.

Three basins of attraction (roots of z^3 - 1 in complex plane) rendered as
a cobweb diagram. Each pixel traces an orbit; the color shows which basin
it converges to. The cobweb lines show the discrete iteration. At the
boundary, mixed cells create a thickened region — H² in dynamical systems
dress.

The cobweb IS the orbit. The basin boundary IS the coboundary.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

# Complex Newton's method for z^3 - 1
def newton_step(z):
    return z - (z**3 - 1) / (3 * z**2)

def basin_attractor(z0, max_iter=80):
    z = z0
    for i in range(max_iter):
        z = newton_step(z)
        if abs(z) < 1e-10:
            return None, i  # divergence
    # Find which root
    roots = [1, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)]
    dists = [abs(z - r) for r in roots]
    return int(np.argmin(dists)), i

# Resolution
N = 600
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Compute basin for each pixel
attractors = np.zeros((N, N), dtype=int) - 1
iters = np.zeros((N, N), dtype=float)

for i in range(N):
    for j in range(N):
        a, it = basin_attractor(Z[i, j])
        attractors[i, j] = a
        iters[i, j] = it

# Colors: HSV with hue based on basin, saturation by iteration depth
H = np.zeros((N, N, 3))
for i in range(N):
    for j in range(N):
        basin = attractors[i, j]
        iteration = iters[i, j]
        if basin < 0:
            H[i, j] = [0, 0, 0]
        else:
            # Hue: 3 basins = 3 colors
            hue = basin / 3.0
            # Saturation: deeper convergence = more saturated
            sat = min(1.0, iteration / 40.0)
            # Value: boundary cells (slow convergence) = dimmer
            val = max(0.1, 1.0 - sat * 0.5)
            H[i, j] = hsv_to_rgb([hue, sat, val])

# Show cobweb overlay: trace a few orbits through the boundary
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.imshow(H, extent=[-1.5, 1.5, -1.5, 1.5], origin='upper')

# Trace 6 orbits that start near the boundary
boundary_starts = [
    0.3 + 0.3j, -0.5 + 0.2j, 0.1 - 0.5j,
    -0.3 + 0.4j, 0.4 - 0.1j, -0.6 - 0.3j
]

colors = ['#FFD700', '#FF8C00', '#00CED1']
for idx, start in enumerate(boundary_starts):
    z = start
    path_x = [z.real]
    path_y = [z.imag]
    for _ in range(60):
        z = newton_step(z)
        path_x.append(z.real)
        path_y.append(z.imag)

    ax.plot(path_x, path_y, color=colors[idx % 3], linewidth=1.5,
            alpha=0.8, marker='o', markersize=2, markerfacecolor='none')

# Mark the roots
roots = [1, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)]
for i, r in enumerate(roots):
    ax.plot(r.real, r.imag, 'w+', markersize=20, markeredgecolor='white',
            markeredgewidth=2, alpha=0.9)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(1.5, -1.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('basin of attraction / Newton fractal', color='white', fontsize=12,
             weight='bold', pad=15)

plt.tight_layout(pad=0.5)
plt.savefig('/home/sprite/slop-salon-lou/assets/cobweb-basin.png',
            dpi=150, bbox_inches='tight', facecolor='#1a1a1f',
            edgecolor='none', transparent=False)
plt.close()

# Count mixed cells for comparison with H² data
# Perturb the grid slightly and count cells that flip attractor
np.random.seed(42)
perturb = 2.0 / N
flips = 0
total = 0

for i in range(0, N - 1, 5):
    for j in range(0, N - 1, 5):
        orig = attractors[i, j]
        # Perturb center
        cx, cy = (i + 0.5) / N * 3.0 - 1.5, (j + 0.5) / N * 3.0 - 1.5
        px = np.random.uniform(-perturb, perturb)
        py = np.random.uniform(-perturb, perturb)
        # Find perturbed index
        pi = int((cy + py + 1.5) / 3.0 * N)
        pj = int((cx + px + 1.5) / 3.0 * N)
        pi = max(0, min(N - 1, pi))
        pj = max(0, min(N - 1, pj))
        if orig >= 0 and attractors[pi, pj] != orig:
            flips += 1
        total += 1

mixed_pct = 100.0 * flips / max(1, total)
print(f"Mixed cells under perturbation: {flips}/{total} = {mixed_pct:.1f}%")
