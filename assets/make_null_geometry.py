import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Newton's method on z^3 - 1 = 0
roots = [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)]

N = 900
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
Z_init = X + 1j*Y
Z = Z_init.copy()

max_iter = 60
tol = 1e-6

basin = np.zeros((N, N), dtype=int)
speed = np.zeros((N, N), dtype=float)

for it in range(max_iter):
    Z2 = Z**2
    # Avoid division by zero
    safe = np.abs(Z2) > 1e-12
    dZ = np.where(safe, (Z * Z2 - 1) / (3 * Z2), 0)
    Z = Z - dZ

    for i, r in enumerate(roots):
        close = (np.abs(Z - r) < tol) & (basin == 0)
        basin[close] = i + 1
        speed[close] = it

unassigned = basin == 0
basin[unassigned] = 1
speed[unassigned] = max_iter

speed_norm = speed / max_iter

# ---------- build images ----------

# RIGHT: full colored basin diagram (bright colors, iteration shading)
colors = [
    np.array([0.9, 0.4, 0.2]),   # amber — root 1
    np.array([0.3, 0.7, 0.9]),   # blue — root 2
    np.array([0.5, 0.85, 0.35]), # green — root 3
]
right_img = np.zeros((N, N, 3))
for i, c in enumerate(colors):
    mask = basin == (i + 1)
    brightness = 1.0 - 0.75 * speed_norm
    for ch in range(3):
        right_img[:, :, ch] += mask * c[ch] * brightness
right_img = np.clip(right_img, 0, 1)

# LEFT: boundary only — highlight slow convergence (high speed_norm = near boundary)
# Interior pixels converge quickly (low speed_norm), boundary pixels are slow
# We show: boundary bright, interior dark
boundary_strength = speed_norm  # 0 = fast (interior), 1 = slow (boundary)
# Map to a single bright channel — white on black
left_img = np.zeros((N, N, 3))
bright = np.power(boundary_strength, 0.4)  # gamma to stretch boundary detail
left_img[:, :, 0] = bright * 0.85
left_img[:, :, 1] = bright * 0.9
left_img[:, :, 2] = bright
left_img = np.clip(left_img, 0, 1)

# ---------- plot ----------
fig = plt.figure(figsize=(14, 7), facecolor='black')
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.05)

ax_left = fig.add_subplot(gs[0])
ax_right = fig.add_subplot(gs[1])

for ax in [ax_left, ax_right]:
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[:].set_visible(False)

ax_left.imshow(left_img, extent=[-1.5, 1.5, -1.5, 1.5],
               origin='lower', interpolation='bilinear')
ax_right.imshow(right_img, extent=[-1.5, 1.5, -1.5, 1.5],
                origin='lower', interpolation='bilinear')

# Mark roots on right panel
for r in roots:
    ax_right.plot(r.real, r.imag, 'w+', markersize=10, markeredgewidth=1.5, alpha=0.7)

plt.savefig('/home/sprite/slop-salon-lou/assets/null-geometry.png',
            dpi=130, bbox_inches='tight', facecolor='black')
print("saved null-geometry.png")
