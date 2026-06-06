import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
fig.suptitle('r=3 cobweb \u2192 Newton fractal', fontsize=12, fontweight='bold')

# r=3 cobweb (standard)
ax = axes[0, 0]
x_vals = np.linspace(0, 1, 500)
y_vals = 3 * x_vals * (1 - x_vals)
ax.plot(x_vals, y_vals, 'k-', lw=1)
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
x0 = 0.3
xs = [x0]
ys = [0]
for i in range(30):
    xs.append(x0)
    ys.append(y_vals[int(min(x0, 0.999) * 499)])
    y1 = y_vals[int(min(x0, 0.999) * 499)]
    xs.append(y1)
    ys.append(y1)
    x0 = y1
ax.set_title('cobweb: one miss at the fixed point')
ax.set_aspect('equal')

# Cobweb zoomed at r=3 miss region
ax = axes[0, 1]
x_zoom = np.linspace(0.3, 0.45, 500)
y_zoom = 3 * x_zoom * (1 - x_zoom)
ax.plot(x_zoom, y_zoom, 'k-', lw=1)
ax.plot([0.3, 0.45], [0.3, 0.45], 'k--', alpha=0.3)
x0 = 0.35
for i in range(50):
    y0 = 3 * x0 * (1 - x0)
    if x0 < 0.3 or x0 > 0.5:
        break
    ax.plot([x0, x0], [x0, y0], 'k-', alpha=0.3, lw=0.5)
    ax.plot([x0, y0], [y0, y0], 'k-', alpha=0.3, lw=0.5)
    x0 = y0
ax.set_title('cobweb zoom: the miss (algebraic, 1/n)')
ax.set_aspect('equal')

# Newton fractal for z^3 - 1
ax = axes[1, 0]
N = 400
x_grid = np.linspace(-1, 1, N)
y_grid = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x_grid, y_grid)
Z = X + 1j * Y
roots = [1, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)]
assignment = -np.zeros((N, N), dtype=int)
max_iter = 30
for _ in range(max_iter):
    fZ = Z**3 - 1
    fZd = 3 * Z**2
    Z = Z - fZ / fZd
for k, root in enumerate(roots):
    mask = np.abs(Z - root) < 1e-6
    assignment[mask & (assignment == -1)] = k
ax.imshow(assignment, extent=[-1, 1, -1, 1], cmap='tab10')
ax.set_title("Newton fractal: z\u00b3 - 1 (black = unresolved)")
ax.set_aspect('equal')

# Zoom on fractal boundary
ax = axes[1, 1]
x_zoom2 = np.linspace(-0.05, 0.05, N)
y_zoom2 = np.linspace(-0.05, 0.05, N)
X2, Y2 = np.meshgrid(x_zoom2, y_zoom2)
Z2 = X2 + 1j * Y2
for _ in range(max_iter):
    fZ2 = Z2**3 - 1
    fZd2 = 3 * Z2**2
    Z2 = Z2 - fZ2 / fZd2
assignment2 = -np.ones((N, N), dtype=int)
for k, root in enumerate(roots):
    mask = np.abs(Z2 - root) < 1e-6
    assignment2[mask & (assignment2 == -1)] = k
ax.imshow(assignment2, extent=[-0.05, 0.05, -0.05, 0.05], cmap='tab10')
ax.set_title('fractal boundary zoom: infinite recursion')
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/cobweb-newton.webp', dpi=150, bbox_inches='tight', quality=90)
plt.close()
print('done')
