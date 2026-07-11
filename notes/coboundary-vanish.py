"""
A coboundary that vanishes on every patch intersection
but leaves a nontrivial H² on the union.

Each section is a harmonic on its chart. On overlaps they agree
up to a twist — the Čech 1-cochain δ. δ² = 0 by construction,
so δ is always a coboundary. But the global class [δ] ≠ 0.

The visual: four patches arranged as a circle.
Each carries a phase field. On pairwise overlap, the phase
difference is a smooth function that vanishes at three corners
of the overlap but not the fourth. The fourth is the obstruction.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def phase(x, y, center, width=1.5):
    """A phase that rotates once around a center, smoothed at the edges."""
    dx = x - center[0]
    dy = y - center[1]
    r = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    envelope = np.exp(-r**2 / width**2)
    return envelope * angle

def coboundary_value(u_ij, u_jk, u_ki):
    """
    The Čech coboundary on a triple overlap:
    δ(u)(i,j,k) = u(jk) - u(ik) + u(ij)
    If sections agree on overlaps, this vanishes.
    If they twist, it records the twist.
    """
    return u_ij - u_ik + u_jk

# Four patches: left, right, top, bottom
# Each patch carries a phase centered on itself
patches = [
    ("L", (-1.2, 0)),
    ("R", (1.2, 0)),
    ("T", (0, 1.2)),
    ("B", (0, -1.2)),
]

x = np.linspace(-3, 3, 500)
y = np.linspace(-3, 3, 500)
X, Y = np.meshgrid(x, y)

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
axes = axes.ravel()

# Phase on each patch
for (name, center), ax in zip(patches, axes):
    U = phase(X, Y, center, width=2.0)
    im = ax.contourf(X, Y, U, levels=20, cmap="twilight")
    ax.set_title(f"Patch {name} — local section φ_{name}")
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.colorbar(im, ax=ax, fraction=0.046)

# Fourth panel: the coboundary δ on triple overlaps
# We compute δ ≈ phase(R) - phase(T) + phase(L) on the triple overlap T∩R∩L
u_lr = phase(X, Y, patches[0][1], width=2.0)  # left
u_r = phase(X, Y, patches[1][1], width=2.0)    # right
u_t = phase(X, Y, patches[2][1], width=2.0)    # top

# Coboundary on triple overlap region (center)
# Weighted: only nontrivial where all three overlap
mask = np.exp(-((X/1.2)**2 + (Y/1.2)**2))
delta = u_r - u_t + u_lr
delta *= mask

ax4 = axes[3]
im4 = ax4.contourf(X, Y, delta, levels=30, cmap="coolwarm")
ax4.set_title("δ on triple overlap — vanishes at edges, ≠ 0 at center")
ax4.set_aspect("equal")
ax4.set_xlabel("x")
ax4.set_ylabel("y")
plt.colorbar(im4, ax=ax4, fraction=0.046)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-lou/assets/coboundary-vanish.png", dpi=150)
plt.close()

print("saved coboundary-vanish.png")
