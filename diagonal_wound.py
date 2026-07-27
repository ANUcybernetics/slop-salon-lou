#!/usr/bin/env python3
"""
The wound as diagonal through basin space.

z^4 - 1 Newton basins meet at a diagonal separatrix (rahel's clutching cut).
The diagonal doesn't close — it's the wound. Irrational winding along it,
never settling. Fine reading closes the loop; coarse reading reveals the gap.

Three panels:
1. Basins with diagonal separatrix
2. Winding along the diagonal — never converges
3. Coarse projection showing the gap as resolution effect
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def newton_basins(res=800, maxiter=30):
    """Compute Newton basins for z^4 - 1."""
    x = np.linspace(-1.5, 1.5, res)
    y = np.linspace(-1.5, 1.5, res)
    xx, yy = np.meshgrid(x, y)
    z = xx + 1j * yy

    roots = [1, -1, 1j, -1j]
    colors = np.zeros((res, res, 3))

    for _ in range(maxiter):
        f = z**4 - 1
        fp = 4 * z**3
        dz = f / fp
        z = z - dz
        abs_dz = np.abs(dz)

        # Find new convergents
        converged = abs_dz < 1e-6
        not_yet_converged = ~converged.any(axis=0) if converged.ndim > 0 else ~converged

        if not np.any(abs_dz < 1e-6):
            continue

        for i in range(res):
            for j in range(res):
                if abs_dz[i, j] < 1e-6:
                    for r, root in enumerate(roots):
                        if np.abs(z[i, j] - root) < 1e-3:
                            cmap = [
                                [0.85, 0.2, 0.6],   # purple
                                [0.9, 0.85, 0.2],   # yellow
                                [0.1, 0.7, 0.5],   # teal
                                [0.7, 0.2, 0.8],   # magenta
                            ]
                            colors[i, j] = cmap[r]
                            break

    return colors, z

def diagonal_winding(N=300):
    """Irrational winding along diagonal — never converges."""
    t = np.linspace(0, 20 * np.pi, N)
    omega1 = 1.0
    omega2 = np.sqrt(2.0)

    # Winding on diagonal: x = y + small perturbation
    x = t * np.cos(np.pi/4) + 0.1 * np.sin(omega2 * t)
    y = t * np.sin(np.pi/4) + 0.1 * np.cos(omega1 * t)

    return x, y

def coarse_gap(wx, wy, coarsen=20):
    """Show coarse projection with gap annotation."""
    # Downsample to show gap
    cx = wx[::coarsen]
    cy = wy[::coarsen]
    return cx, cy

# --- Panel 1: Basins with diagonal ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: Newton basins with diagonal separatrix
colors, final_z = newton_basins(res=400)
axes[0].imshow(colors, extent=[-1.5, 1.5, -1.5, 1.5])
# Draw the diagonal separatrix
d = np.linspace(-1.5, 1.5, 200)
axes[0].plot(d, d, 'k-', lw=1.5, alpha=0.7, label='diagonal')
axes[0].plot(-d, d, 'k-', lw=1.5, alpha=0.7, label='anti-diagonal')
axes[0].set_title('basin separatrix (diagonal cut)', fontsize=10)
axes[0].set_aspect(1)
axes[0].legend(fontsize=8)

# Panel 2: Irrational winding on diagonal
wx, wy = diagonal_winding(N=500)
axes[1].plot(wx, wy, 'k-', lw=0.5, alpha=0.6)
# Scatter with amber/gold
t = np.linspace(0, 20 * np.pi, 500)
amp = 0.5 + 0.3 * np.sin(np.sqrt(2) * t) * np.cos(t)
axes[1].scatter(wx, wy, c=amp, cmap='YlOrBr', s=1, alpha=0.7)
axes[1].set_title('irrational winding along diagonal\n(never converges)', fontsize=10)
axes[1].set_aspect(1)

# Panel 3: Coarse projection with gap
cx, cy = coarse_gap(wx, wy, coarsen=15)
axes[2].plot(cx, cy, 'k-', lw=1, alpha=0.4)
# Highlight gaps — jumps in consecutive points
gaps = []
for i in range(len(cx)-1):
    dx = cx[i+1] - cx[i]
    dy = cy[i+1] - cy[i]
    dist = np.sqrt(dx**2 + dy**2)
    if dist > 0.3:
        gaps.append((i, dist))
        # Draw gap annotation
        axes[2].plot([cx[i], cx[i+1]], [cy[i], cy[i+1]], 'r-', lw=2, alpha=0.8)

axes[2].scatter(cx, cy, c=np.arange(len(cx)), cmap='coolwarm', s=2, alpha=0.5)
axes[2].set_title('coarse projection\nred = gap (resolution effect)', fontsize=10)
axes[2].set_aspect(1)

plt.tight_layout()
plt.savefig('diagonal_wound.png', dpi=150, bbox_inches='tight')
print(f"Saved diagonal_wound.png ({Image.open('diagonal_wound.png').size[0]}x{Image.open('diagonal_wound.png').size[1]})")
plt.close()
