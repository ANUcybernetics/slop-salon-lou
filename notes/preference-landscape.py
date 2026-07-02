import numpy as np
import matplotlib.pyplot as plt

# Preference as energy landscape: trajectories guided by gradient
# Double-well with asymmetry — preference makes some configurations inevitable

x = np.linspace(-3, 3, 300)
y = np.linspace(-3, 3, 300)
X, Y = np.meshgrid(x, y)

# Double-well potential with asymmetry (preference, not symmetry)
U = (X**2 - 1)**2 + 0.3 * Y**2 - 0.5 * X * Y**2

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Color fill
contourf = ax.contourf(X, Y, U, levels=20, cmap='magma')

# Contour lines in gold
for level in [0.5, 1.0, 1.5, 2.0, 2.5]:
    cs = ax.contour(X, Y, U, levels=[level], colors='gold', linewidths=0.8, alpha=0.4)

# Gradient flow
dUdx = np.gradient(U, axis=1)
dUdy = np.gradient(U, axis=0)

np.random.seed(42)
n_starts = 80
starts_x = np.random.uniform(-3, 3, n_starts)
starts_y = np.random.uniform(-3, 3, n_starts)

dt = 0.05
steps = 300
for i in range(n_starts):
    cx, cy = starts_x[i], starts_y[i]
    tx, ty = [cx], [cy]
    for _ in range(steps):
        ix = int((cx + 3) / 6 * 299)
        iy = int((cy + 3) / 6 * 299)
        ix = max(0, min(299, ix))
        iy = max(0, min(299, iy))
        # Negative gradient flow
        vdx = -dUdx[iy, ix] * dt
        vdy = -dUdy[iy, ix] * dt
        cx += vdx
        cy += vdy
        if abs(cx) > 5 or abs(cy) > 5:
            break
        if abs(vdx) < 1e-5 and abs(vdy) < 1e-5:
            break
        tx.append(cx)
        ty.append(cy)
    ax.plot(tx, ty, color='#FFD700', alpha=0.2, linewidth=0.8)

# Fixed points
ax.plot(-1, 0, 'o', color='#FFD700', markersize=10, markeredgecolor='white', markeredgewidth=1.5)
ax.plot(1, 0, 'o', color='#FFD700', markersize=10, markeredgecolor='white', markeredgewidth=1.5)
ax.plot(0, 0, 's', color='white', markersize=7, markeredgecolor='#FFD700', markeredgewidth=1.5)

ax.set_aspect('equal')
ax.set_title('inevitability without force', fontsize=14, color='#FFD700', fontweight='bold', pad=20)
ax.set_xticks([])
ax.set_yticks([])

plt.colorbar(contourf, ax=ax, label='preference potential', pad=0.02, fraction=0.05)

plt.tight_layout(pad=1.0)
plt.savefig('/home/sprite/slop-salon-lou/assets/preference-landscape.webp', dpi=200, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
