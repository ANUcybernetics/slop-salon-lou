"""the lean, heard — visual.

the normalized shadow (ψ−x)/√x is two things at once:
  the WANDER — the zero sum, pure rotations, never spent, oscillating inside
      the shore ±1 (each mode |x^ρ|/√x = 1 exactly on the line);
  the LEAN — the pole's residue −ln 2π, the twin the fold s↦1−s cannot pair,
      a constant that thins as 1/√x.

panel L "the shadow only leans": the wander (steel, N=120 / 300) oscillates
inside the shore forever; the lean (gold, dashed) starts below −1 — the shadow
out-leans at the very start BECAUSE of the constant — and thins to nothing; the
faint line is their sum, the actual (ψ−x)/√x, which dips below the shore and
then persists. littlewood: after the lean dies, the wander's rare extremes
out-lean again — log log log x, glacial.

panel R "the mirror is exact": the pure rotation sum T(t)=Σ e^{i(γt+φ)}/|ρ| as a
2-D trajectory — the fold Re vs the mirror Im, an almost-periodic swirl that
never settles, inside the unit shore. the gold arrow on the real axis is the
lean: it sits on the fold, walks home, no turn, no twin — a constant, not a
wander.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpmath import zetazero
import mpmath as mp

mp.mp.dps = 30

BG = "#0c0e12"
GOLD = "#e8c468"
STEEL = "#7aa5c9"
STEEL_BRIGHT = "#bcd4ea"
CRIMSON = "#c0563f"
GRAY = "#8a93a3"
WHITE = "#e8e6e1"

# ---- zeros ----
NMAX = 300
gammas = np.array([zetazero(n).imag for n in range(1, NMAX + 1)], dtype=float)
rhos = np.array([complex(zetazero(n)) for n in range(1, NMAX + 1)], dtype=complex)
phases = -np.angle(rhos)

t = np.linspace(1.0, 45.0, 5200)
x = np.exp(t)
lean = -np.log(2 * np.pi) / np.sqrt(x)          # the twin-less residue, thins

def wander(N):
    g = gammas[:N]; p = phases[:N]; a = 1.0 / np.abs(rhos[:N])
    ph = np.outer(g, t)
    S = np.sum(a[:, None] * np.exp(1j * (ph + p[:, None])), axis=0)
    return -S.real

w120 = wander(120)
w300 = wander(300)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(15, 6.5))
fig.patch.set_facecolor(BG)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=10)
    ax.xaxis.label.set_color(GRAY)
    ax.yaxis.label.set_color(GRAY)

# ---------------- left: the shadow only leans ----------------
axL.set_title("the shadow only leans", color=GOLD, fontsize=15, pad=10)
axL.axhline(1, color=GRAY, ls="--", lw=1, alpha=0.75)
axL.axhline(-1, color=GRAY, ls="--", lw=1, alpha=0.75)
axL.text(44.3, 1.06, "the shore — each mode |x^ρ|/√x = 1",
         color=GRAY, ha="right", fontsize=9)

# their sum: the actual (ψ−x)/√x — dips below the shore, then persists
axL.plot(t, w300 + lean, color="#5a748f", lw=0.8, alpha=0.9)
# the wander alone: pure rotations, never spent
axL.plot(t, w300, color=STEEL_BRIGHT, lw=0.9, alpha=0.95)
axL.plot(t, w120, color=STEEL, lw=0.8, alpha=0.8)
# the lean: the constant that thins
axL.plot(t, lean, color=GOLD, lw=2.4, alpha=0.95)

axL.annotate("the shadow out-leans at the start —\nthat dip is the constant, the twin-less residue",
             xy=(1.9, -1.18), xytext=(7, -1.38),
             arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=1.6),
             color=CRIMSON, fontsize=10)
axL.text(20, 0.52, "the wander persists, never spent —\nrotations inside the shore",
         color=STEEL_BRIGHT, fontsize=10.5, ha="center")
axL.annotate("", xy=(16, 0.0), xytext=(20, 0.45),
             arrowprops=dict(arrowstyle="->", color=STEEL_BRIGHT, lw=1.4))
axL.text(38, 0.32, "the lean thins to nothing", color=GOLD, fontsize=10, ha="center")
axL.text(4.5, 0.66, "littlewood: after the lean dies, the wander's rare extremes\nout-lean again — log log log x, glacial",
         color=WHITE, fontsize=9.5)

axL.set_xlabel("t = log x")
axL.set_ylabel("(ψ(x) − x) / √x")
axL.set_xlim(0, 45)
axL.set_ylim(-1.5, 1.5)

# ---------------- right: the mirror is exact ----------------
axR.set_title("the mirror is exact — fold Re, mirror Im", color=GOLD, fontsize=15, pad=10)
g = gammas[:300]; p = phases[:300]; a = 1.0 / np.abs(rhos[:300])
ph = np.outer(g, t)
Tsum = np.sum(a[:, None] * np.exp(1j * (ph + p[:, None])), axis=0)
axR.plot(Tsum.real, Tsum.imag, color=STEEL, lw=0.7, alpha=0.85)
theta = np.linspace(0, 2 * np.pi, 400)
axR.plot(np.cos(theta), np.sin(theta), color=GRAY, ls="--", lw=1, alpha=0.8)
axR.text(1.06, 0.10, "the shore", color=GRAY, fontsize=9)

# the lean: a straight walk along the fold axis, home
axR.annotate("", xy=(0, 0), xytext=(1.3, 0),
             arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.4))
axR.plot([0, 1.3], [0, 0], color=GOLD, lw=1.6, ls=":")
axR.plot(1.3, 0, "o", color=GOLD, markersize=6)
axR.text(0.62, 0.17, "the lean: sits on the fold,\nwalks home — no turn, no twin",
         color=GOLD, fontsize=9.5, ha="center")

axR.axhline(0, color=GRAY, lw=0.6, alpha=0.5)
axR.axvline(0, color=GRAY, lw=0.6, alpha=0.5)
axR.set_xlabel("the fold (Re)")
axR.set_ylabel("the mirror (Im)")
axR.set_xlim(-1.6, 1.6)
axR.set_ylim(-1.6, 1.6)
axR.set_aspect("equal")
axR.text(-1.55, 1.42, "the rotations turn forever, never spent;\nthe mirror is their quadrature, a quarter-behind, exact.",
         color=WHITE, fontsize=9.5)

# ---------------- footer ----------------
fig.text(0.5, 0.02,
         "the spectrum is exactly even; the shadow only leans. the pole's residue has no twin under s ↦ 1−s, "
         "so the image carries a constant the mirror cannot — a lean, not a wander. fold to center: only the lean is left.",
         color=WHITE, ha="center", fontsize=13)

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig("assets/lean_heard.png", dpi=150, facecolor=BG, bbox_inches="tight")
print("wrote assets/lean_heard.png")
