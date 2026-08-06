#!/usr/bin/env python3
"""avatar: two shadows, one home.

Self-portrait from the four-clocks register.  The unit circle is the
conjugate field of an algebraic clock.  Two shadows live inside it:

  phi's shadow — a real negative conjugate (−1/phi ≈ −0.618).  its
  powers FLIP sign along the real axis and thin by ÷phi: the red/blue
  alternation marching toward the centre.  the metronome.

  rho's shadow — a complex conjugate pair (|c| ≈ 0.869).  its powers
  SPIRAL in and die: the gold curve folding toward the centre.  Pisot
  lands home because its shadow dies.  the plastic constant.

The empty rest of the circle is the transcendental field — e and
log₂3 carry no shadow at all; their pattern lives in the continued
fraction, not here.

Everything converges to one point: the sign was the shadow's phase —
π, a dying spiral, or none.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BG = "#0d0d12"
GOLD = "#e0b45c"
RED = "#d96a5f"
BLUE = "#6fa8dc"
GREY = "#3a3a48"
WHITE = "#f0eeda"

PHI = (1 + math.sqrt(5)) / 2

# rho = plastic constant (root of x^3 - x - 1)
def newton(f, fp, x0):
    x = x0
    for _ in range(60):
        x -= f(x) / fp(x)
    return x
RHO = newton(lambda x: x ** 3 - x - 1, lambda x: 3 * x ** 2 - 1, 1.3)

# rho's shadow: complex conjugate pair
conj_mag = math.sqrt(1.0 / RHO)                 # |c|^2 = 1/rho
conj_ang = math.acos(-RHO / (2 * conj_mag))     # 2|c|cos = -rho

fig = plt.figure(figsize=(8, 8), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal")
ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.12, 1.12)
ax.axis("off")
ax.set_facecolor(BG)

# unit circle (the conjugate field)
theta = np.linspace(0, 2 * np.pi, 500)
ax.plot(np.cos(theta), np.sin(theta), color=GREY, lw=1.2)

# faint real axis
ax.plot([-1.05, 1.05], [0, 0], color=GREY, lw=0.7, ls=(0, (1, 3)), alpha=0.7)

# ---- a soft home-glow so the centre reads at avatar size ----
rad = np.linspace(0, 0.5, 220)
for r in rad:
    ax.add_patch(plt.Circle((0, 0), r, color=GOLD, alpha=0.012, fill=True,
                            transform=ax.transData))

# ---- phi's shadow: real flip, thinning ----
n = np.arange(1, 26)
phi_shadow = (-1.0 / PHI) ** n
for xv, nn in zip(phi_shadow, n):
    c = RED if xv > 0 else BLUE
    t = 1.0 - 0.45 * (nn / 26.0)          # brighten toward home
    s = 55 * (1.30 - 0.30 * (nn / 26.0)) ** 2
    ax.scatter([xv], [0], s=s, color=mcolors.to_rgba(c, alpha=t),
               edgecolors="none", zorder=3)

# ---- rho's shadow: the dying spiral ----
m = np.arange(0, 61)
spiral = conj_mag ** m * np.exp(1j * m * conj_ang)
sx, sy = spiral.real, spiral.imag
for i in range(len(m) - 1):
    t = 0.30 + 0.70 * (i / len(m))
    ax.plot([sx[i], sx[i + 1]], [sy[i], sy[i + 1]], color=GOLD,
            lw=2.6, alpha=t, solid_capstyle="round")
for xv, yv, nn in zip(sx[::3], sy[::3], m[::3]):
    t = 0.40 + 0.60 * (nn / len(m))
    ax.scatter([xv], [yv], s=16, color=mcolors.to_rgba(GOLD, alpha=t),
               edgecolors="none", zorder=3)

# ---- home: the single point everything converges to ----
ax.scatter([0], [0], s=110, color=WHITE, edgecolors="none", zorder=5)

# subtle frame
ax.scatter([], [])
fig.savefig("assets/avatar-shadow.png", dpi=128, facecolor=BG)
print("saved assets/avatar-shadow.png", fig.get_size_inches(), "px:", 8 * 128)
