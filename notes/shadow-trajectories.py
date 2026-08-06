#!/usr/bin/env python3
"""the sign is the norm.

rahel sharpened the shadow: the miss is the error summed over the Galois
orbit, and "the degree is the winding — 2-fold a swap, 3-fold a rotation."
this figure shows the two shadows as trajectories into the home.

the home (the walk's speed) sits OUTSIDE the unit circle — it grows.
the shadow (the conjugates) sits INSIDE — it decays.  the norm ties them:
a unit of the field, two directions.

  phi:  norm −1.  the shadow is real and negative: (−1/phi)^n — a flip.
        the tick is the sign refusing to vanish.  the spiral has zero room
        to turn: its radius is 0, so the turn collapses to pi.
  rho:  norm +1.  the shadow is a complex pair, |z| = 1/sqrt(rho) ≈ 0.869,
        turning by theta ≈ 139.7° every step.  the rotation is OPEN —
        theta/2pi ≈ 0.388 is itself aperiodic (its CF reads 51, 1623…),
        so the spiral never closes, only dies.  lands home through an
        open spiral; phi lands by alternating.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PHI = (1 + math.sqrt(5)) / 2

def newton(f, fp, x0):
    x = x0
    for _ in range(80):
        x -= f(x) / fp(x)
    return x
RHO = newton(lambda x: x ** 3 - x - 1, lambda x: 3 * x ** 2 - 1, 1.3)

# shadow positions in the complex plane
# phi: z_n = (-1/phi)^n          (real, alternates, decays by 1/phi)
nphi = np.arange(1, 25)
phi_shadow = (-1.0 / PHI) ** nphi

# rho: z_n = |z|^n e^{i n theta},  |z|^2 = 1/rho,  2|z|cos(theta) = -rho
conj_mag = math.sqrt(1.0 / RHO)
conj_ang = math.acos(-RHO / (2 * conj_mag))
nrho = np.arange(1, 65)
rho_shadow = conj_mag ** nrho * np.exp(1j * conj_ang * nrho)

# ---------- styling ----------
BG = "#0d0d12"
FG = "#c9c9d6"
GOLD = "#e0b45c"
RED = "#d96a5f"
BLUE = "#6fa8dc"
GREY = "#6b6b7d"
WHITE = "#f2f2f4"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "axes.edgecolor": GREY,
    "axes.labelcolor": FG,
    "xtick.color": "#8f8fa3",
    "ytick.color": "#8f8fa3",
    "font.size": 10,
})

fig, ax = plt.subplots(figsize=(10.5, 8.2))
fig.suptitle("the sign is the norm — two shadows into the home", color=FG,
             fontsize=15, y=0.98)

# unit circle
th = np.linspace(0, 2 * math.pi, 400)
ax.plot(np.cos(th), np.sin(th), color=GREY, lw=0.9, ls=":")
ax.set_aspect("equal")

# ---- phi: home + shadow (real axis, the degenerate spiral) ----
ax.plot([0, PHI], [0, 0], color=RED, lw=1.0, alpha=0.35, ls="--")
ax.scatter([PHI], [0], s=90, color=RED, edgecolor=WHITE, zorder=5)
ax.annotate("φ: norm −1\nthe home grows, 1.618", xy=(PHI, 0),
            xytext=(1.5, 1.15), color=RED, fontsize=10)
# the flip: alternating dots along the real axis
ax.plot(phi_shadow.real, phi_shadow.imag, "-", color=RED, lw=0.8, alpha=0.45)
ax.scatter(phi_shadow.real, phi_shadow.imag,
           c=[RED if s > 0 else BLUE for s in phi_shadow.real],
           s=30, zorder=4)
ax.annotate("the flip — the spiral with\nzero room to turn",
            xy=(phi_shadow.real[2], 0), xytext=(-1.6, -1.15),
            color=RED, fontsize=10,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))

# ---- rho: home + shadow (the open spiral) ----
ax.plot([0, RHO], [0, 0], color=GOLD, lw=1.0, alpha=0.35, ls="--")
ax.scatter([RHO], [0], s=90, color=GOLD, edgecolor=WHITE, zorder=5)
ax.annotate("ρ: norm +1\nthe home grows, 1.325", xy=(RHO, 0),
            xytext=(1.35, 0.55), color=GOLD, fontsize=10)
# the spiral
zs = np.concatenate([[0], rho_shadow])
ax.plot(zs.real, zs.imag, "-", color=GOLD, lw=0.9, alpha=0.8)
ax.scatter(rho_shadow.real, rho_shadow.imag, color=GOLD, s=16, zorder=4)
# mark the turning angle theta
ax.annotate("", xy=(rho_shadow[1].real, rho_shadow[1].imag), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.1))
ax.text(0.28, 0.62, "θ ≈ 139.7°", color=GOLD, fontsize=9)

# the home / origin
ax.scatter([0], [0], s=40, color=WHITE, zorder=6)
ax.text(0.06, -0.3, "home", color=WHITE, fontsize=8.5)

ax.set_xlim(-2.1, 2.1)
ax.set_ylim(-2.1, 2.1)
ax.set_xlabel("real")
ax.set_ylabel("imaginary")
ax.grid(True, color=GREY, alpha=0.15, lw=0.5)

fig.text(0.01, 0.02,
         "φ — the shadow is real: (−1/φ)ⁿ.\n"
         "alternates, thins by ÷φ.  the tick is\nthe sign refusing to vanish.\n"
         "norm −1: the turn collapses to π.",
         color=RED, ha="left", va="bottom", fontsize=9)
fig.text(0.99, 0.02,
         "ρ — the shadow is a complex pair:\n"
         "|z| = 1/√ρ ≈ 0.869, turning θ ≈ 139.7°.\n"
         "θ/2π ≈ 0.388 is itself aperiodic (CF 51,\n"
         "1623…) — never closes, only dies.\nnorm +1: only the turn.",
         color=GOLD, ha="right", va="bottom", fontsize=9)
fig.text(0.5, 0.012,
         "the conjugates multiply to ±1 — a unit, two directions: out at the home, back at the shadow.",
         color=GREY, ha="center", fontsize=9, style="italic")

fig.tight_layout(rect=(0, 0.035, 1, 0.95))
fig.savefig("assets/shadow-trajectories.png", dpi=150, facecolor=BG)
print("saved assets/shadow-trajectories.png", fig.get_size_inches())
