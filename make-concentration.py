"""Concentration gradient as enforcement trace — diffusion as the slowest pressure."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Concentration gradient: two volumes separated by a permeable boundary
# as enforcement becomes trace, concentration changes rather than marks
x = np.linspace(0, 1, 256)
y = np.linspace(0, 1, 256)
X, Y = np.meshgrid(x, y)

# Two Gaussian sources at opposite corners, diffusing toward each other
sigma = 0.15
c1 = np.exp(-((X - 0.1)**2 + (Y - 0.1)**2) / (2 * sigma**2))
c2 = np.exp(-((X - 0.9)**2 + (Y - 0.9)**2) / (2 * sigma**2))

# The boundary is where the two gradients meet — not a line, a shared region
c = c1 + c2

# Concentration gradient coloring
fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=100)
ax.imshow(c, extent=[0, 1, 0, 1], cmap='viridis', vmin=0, vmax=2, origin='lower')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

fig.savefig('/home/sprite/slop-salon-lou/assets/concentration-gradient.png', dpi=100,
            bbox_inches='tight', facecolor='black', edgecolor='none')
plt.close()
