#!/usr/bin/env python3
"""
Field as actor: trajectories as what the landscape does, not decisions.
Vector field shown as the primary geometry; basins emerge from the field's shape.
No separate trajectories — the field IS the motion.
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)

# Double-well potential (asymmetric)
U = (X**2 - 1)**2 + 0.3 * Y**2 - 0.5 * X * Y**2

# Gradient of potential (the field)
dUdx = np.gradient(U, axis=1)
dUdy = np.gradient(U, axis=0)

# Normalize for visualization
mag = np.sqrt(dUdx**2 + dUdy**2)
mag[mag < 1e-10] = 1e-10
dUdx_n = dUdx / mag
dUdy_n = dUdy / mag

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Background potential (magma)
contourf = ax.contourf(X, Y, U, levels=25, cmap='magma', alpha=0.5)

# Vector field — the primary visual
ax.quiver(X, Y, -dUdx, -dUdy, mag, cmap='autumn', alpha=0.6, scale=25, width=0.003)

# Mark fixed points
ax.plot(-1, 0, 'o', color='white', markersize=12, markeredgecolor='#FFD700', markeredgewidth=2)
ax.plot(1, 0, 'o', color='white', markersize=12, markeredgecolor='#FFD700', markeredgewidth=2)
ax.plot(0, 0, 's', color='white', markersize=8, markeredgecolor='#FFD700', markeredgewidth=2)

ax.set_aspect('equal')
ax.set_title('the field does not decide. it acts.', fontsize=14, color='#FFD700', fontweight='bold', pad=20)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout(pad=1.0)
plt.savefig('/home/sprite/slop-salon-lou/assets/field-as-actor.webp', dpi=200, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
