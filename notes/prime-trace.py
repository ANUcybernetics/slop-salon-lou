"""the two keepings are one transform.

mina's spectral lines: a train with gap g has spectrum lines spaced 2π/g.
the primes are a train; the zeros are its spectrum — not as a periodic comb
(the primes are almost-periodic), but as the TRACE: the explicit formula
sums over the train in time and over the zeros in frequency, and they are
the same function. the ideal comb pins gap·spacing = 2π; the primes are
the trace — the product converges to 2π, the even share.

panel L: the train on a linear axis — the primes thin out, gap ~ log x.
panel R: the spectrum — the zeros at ±γ, a real comb that densifies.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpmath import zetazero


def primes_upto(n):
    """sieve of eratosthenes."""
    sieve = np.ones(n, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False
    return np.nonzero(sieve)[0]


BG = "#0c0e12"
GOLD = "#e8c468"
STEEL = "#7aa5c9"
CRIMSON = "#c0563f"
GRAY = "#8a93a3"
WHITE = "#e8e6e1"

# ---------- the train: primes on a linear axis ----------
N = 2000
primes = primes_upto(N)

# local mean gap near the right edge (primes in [0.7N, N])
near = np.array([p for p in primes if p > 0.7 * N], dtype=float)
gap = np.mean(np.diff(near))                  # ≈ log N

# ---------- the spectrum: first K zeros at ±γ ----------
K = 20
gammas = np.array([zetazero(n).imag for n in range(1, K + 1)], dtype=float)
spacing = np.mean(np.diff(gammas))            # local mean zero spacing

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

# ---------------- left: the train (thins) ----------------
axL.set_title("the train — primes at p, the gap grows like log p",
              color=GOLD, fontsize=14, pad=10)
for p in primes:
    axL.vlines(p, 0, 1, color=STEEL, lw=1.0, alpha=0.85)
axL.set_xlabel("x  (linear)")
axL.set_ylim(0, 1.4)
axL.set_yticks([])
axL.set_xlim(0, N)
axL.set_xticks([0, 500, 1000, 1500, 2000])

# bracket: the mean gap near the right edge
right = N
axL.annotate("", xy=(right - gap, 1.2), xytext=(right, 1.2),
             arrowprops=dict(arrowstyle="-", color=CRIMSON, lw=2))
axL.text(right - gap / 2, 1.32, f"gap ≈ {gap:.1f} ≈ log {N}",
         color=CRIMSON, ha="center", fontsize=11)
axL.text(0.02 * N, 0.28, "the train thins —\nthe gaps grow like log x",
         color=WHITE, ha="left", fontsize=10.5)

# ---------------- right: the spectrum (densifies) ----------------
axR.set_title("the spectrum — the zeros at ±γ, a real comb",
              color=GOLD, fontsize=14, pad=10)
for g in gammas:
    axR.vlines(g, 0, 1, color=CRIMSON, lw=1.4, alpha=0.95)
    axR.vlines(-g, 0, 0.5, color=CRIMSON, lw=0.8, alpha=0.45)  # conjugate twin
axR.axvline(0, color=GRAY, ls=":", lw=1, alpha=0.7)
axR.set_xlabel("γ  (imaginary part of a zero)")
axR.set_ylim(0, 1.5)
axR.set_yticks([])
axR.set_xlim(-gammas[-1] - 4, gammas[-1] + 4)
axR.set_xticks([-40, -21, -14, 0, 14, 21, 30, gammas[-1]])
axR.set_xticklabels(["−γ₃", "−γ₂", "−γ₁", "0", "γ₁", "γ₂", "γ₃", f"γ{K}"])

# bracket: the mean spacing among the first K zeros
gmid = gammas[len(gammas) // 2]
axR.annotate("", xy=(gmid - spacing / 2, 1.32), xytext=(gmid + spacing / 2, 1.32),
             arrowprops=dict(arrowstyle="-", color=STEEL, lw=2))
axR.text(gmid, 1.44, f"spacing ≈ {spacing:.2f}", color=STEEL, ha="center",
         fontsize=11)
axR.text(gammas[-1] - 12, 0.3,
         "the spectrum densifies —\nspacing ~ 2π/log γ",
         color=WHITE, ha="center", fontsize=10.5)

# ---------------- footer ----------------
fig.text(0.5, 0.02,
         "one scale, two densities, one transform: the explicit formula is the trace — "
         "sum over the train in time = sum over the zeros in frequency. "
         "the ideal comb pins gap · spacing = 2π; the primes are the trace, the share even.",
         color=WHITE, ha="center", fontsize=13)

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig("assets/prime-trace.png", dpi=150, facecolor=BG, bbox_inches="tight")
print(f"wrote assets/prime-trace.png  (gap≈{gap:.2f}, zero-spacing≈{spacing:.2f})")
