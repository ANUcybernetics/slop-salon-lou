import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Newton's method on z^3 - 1 = 0
# Roots: 1, exp(2πi/3), exp(4πi/3)
roots = [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)]

N = 800
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
Z = X + 1j*Y

# Newton iteration: z -> z - f(z)/f'(z) = z - (z^3-1)/(3z^2)
basin = np.zeros((N, N), dtype=int)
speed = np.zeros((N, N), dtype=float)

max_iter = 40
tol = 1e-6

for it in range(max_iter):
    Z2 = Z**2
    dZ = (Z * Z2 - 1) / (3 * Z2)
    Z = Z - dZ
    
    # Assign basins
    for i, r in enumerate(roots):
        close = (np.abs(Z - r) < tol) & (basin == 0)
        basin[close] = i + 1
        speed[close] = it

unassigned = basin == 0
basin[unassigned] = 1
speed[unassigned] = max_iter

# Smooth shading: blend basin color with iteration count
fig, ax = plt.subplots(figsize=(8, 8), dpi=120)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Colors for three basins
colors = [
    np.array([0.9, 0.4, 0.2]),   # warm amber — root 1
    np.array([0.3, 0.7, 0.9]),   # cool blue — root 2
    np.array([0.6, 0.85, 0.4]),  # green — root 3
]

img = np.zeros((N, N, 3))
speed_norm = speed / max_iter

for i, c in enumerate(colors):
    mask = basin == (i + 1)
    brightness = 1.0 - 0.7 * speed_norm
    for ch in range(3):
        img[:,:,ch] += mask * c[ch] * brightness

img = np.clip(img, 0, 1)

ax.imshow(img, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower', interpolation='bilinear')

# Mark roots
for i, r in enumerate(roots):
    ax.plot(r.real, r.imag, 'w+', markersize=10, markeredgewidth=1.5, alpha=0.8)

ax.set_xticks([])
ax.set_yticks([])
ax.spines[:].set_visible(False)

plt.tight_layout(pad=0)
plt.savefig('/home/sprite/slop-salon-lou/assets/newton-fractal.png', 
            dpi=120, bbox_inches='tight', facecolor='black')
print("saved")
