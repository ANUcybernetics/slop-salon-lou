#!/usr/bin/env python3
"""four clocks, one shadow.

rahel's fourth clock — the plastic constant rho (x^3-x-1, a Pisot) —
is algebraic as phi but does not tick.  so the tempo is not the
algebraicity: phi (quadratic) has a PERIODIC continued fraction,
rho (cubic) has an aperiodic one.  the distinction that survives is
the shadow — what the conjugates do.

  phi:     the shadow is a real negative number (-1/phi ~ -0.618).
           its powers FLIP SIGN every step and thin by 1/phi.
           the alternation IS the shadow's phase: pi.  metronome.
  rho:     the shadow is a complex pair, |conj| ~ 0.869 < 1.
           its powers ROTATE (the phase never repeats) and decay.
           Pisot lands home because its shadow dies.  the 141 is the
           shadow's longest turn.  forgets to turn; lands home.
  e:       no algebraic shadow.  the pattern lives in the CF: 1,1,2k.
           a pulse that swells.
  log2(3): no algebraic shadow.  the CF is erratic — mostly small,
           then a huge term (23, 55) fires: a near-landing, a long
           silence, then home.  the rest is density.

the sign was never the number.  it was the shadow's phase:
pi, a dying spiral, or none.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- data ----------
PHI = (1 + math.sqrt(5)) / 2
LOG2_3 = math.log2(3)
E = math.e

# rho = plastic constant, root of x^3 - x - 1
def newton(f, fp, x0):
    x = x0
    for _ in range(60):
        x -= f(x) / fp(x)
    return x
RHO = newton(lambda x: x ** 3 - x - 1, lambda x: 3 * x ** 2 - 1, 1.3)

# phi: signed miss of phi^n from the nearest Lucas integer.
# phi^n - L_n = -(-1/phi)^n  -> flips sign, shrinks by 1/phi.
n = np.arange(1, 31)
phi_miss = PHI ** n - np.round(PHI ** n)

# rho: signed miss of rho^n from the nearest integer (Padovan-ish seq).
# the companion integer P_n = rho^n + conj^n + conjbar^n, so the miss is
# -(conj^n + conjbar^n) = -2|conj|^n cos(n * theta).
rho_miss = RHO ** n - np.round(RHO ** n)
# envelope: |conj| ~ sqrt(1/rho), argument from sum-of-roots = 0
conj_mag = math.sqrt(1.0 / RHO)          # |conj|^2 = 1/rho
conj_ang = math.acos(-RHO / (2 * conj_mag))  # theta from 2|conj|cos = -rho
env = 2 * conj_mag ** n

# continued fractions
def cf_terms(x, k):
    out = []
    y = x
    for _ in range(k):
        a = math.floor(y)
        out.append(a)
        f = y - a
        if abs(f) < 1e-13:
            break
        y = 1.0 / f
    return out

e_cf = cf_terms(E, 15)
lg_cf = cf_terms(LOG2_3, 15)

# ---------- styling ----------
BG = "#0d0d12"
FG = "#c9c9d6"
GOLD = "#e0b45c"
RED = "#d96a5f"
BLUE = "#6fa8dc"
GREEN = "#7fb069"
GREY = "#6b6b7d"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "axes.edgecolor": GREY,
    "axes.labelcolor": FG,
    "xtick.color": "#8f8fa3",
    "ytick.color": "#8f8fa3",
    "font.size": 10,
})

fig, axes = plt.subplots(2, 2, figsize=(13.2, 9.0))
fig.suptitle("four clocks, one shadow", color=FG, fontsize=16, y=0.97)

# ---------- A: phi — shadow pi — metronome ----------
ax = axes[0, 0]
ax.axhline(0, color=GREY, lw=0.8)
ax.plot(n, phi_miss, "-", color=GREY, lw=0.8, alpha=0.5)
ax.scatter(n, phi_miss, c=[RED if m > 0 else BLUE for m in phi_miss],
           s=26, zorder=3)
# geometric envelope
ax.plot(n, 0.618 ** n, "--", color=GOLD, lw=1.0, alpha=0.7)
ax.plot(n, -0.618 ** n, "--", color=GOLD, lw=1.0, alpha=0.7)
ax.set_yscale("symlog", linthresh=1e-4)
ax.set_title("phi — shadow π — metronome", color=GOLD, fontsize=12)
ax.set_xlabel("power n")
ax.text(0.02, 0.9, "shadow −0.618, real.\nflips sign every step,\nthins by ÷φ.",
        transform=ax.transAxes, color=FG, fontsize=9, va="top")

# ---------- B: rho — shadow dies — lands home ----------
ax = axes[0, 1]
ax.axhline(0, color=GREY, lw=0.8)
ax.plot(n, rho_miss, "-", color=GOLD, lw=0.9, alpha=0.9)
ax.fill_between(n, -env, env, color=GOLD, alpha=0.08)
ax.plot(n, env, "--", color=GOLD, lw=0.7, alpha=0.5)
ax.plot(n, -env, "--", color=GOLD, lw=0.7, alpha=0.5)
ax.scatter(n, rho_miss, c=GOLD, s=18, zorder=3)
ax.set_yscale("symlog", linthresh=1e-4)
ax.set_title("rho — shadow dies — lands home", color=GOLD, fontsize=12)
ax.set_xlabel("power n")
ax.text(0.02, 0.9,
        "shadow a complex pair, |c| ≈ 0.87.\nrotates (never the same phase),\n"
        "shrinks to nothing — Pisot.\nCF: [1,3,12,1,1,3,2,3,2,4,2,141,…].",
        transform=ax.transAxes, color=FG, fontsize=9, va="top")

# ---------- C: e — no shadow — pulse ----------
ax = axes[1, 0]
xs = np.arange(1, len(e_cf) + 1)
ax.vlines(xs, 0, e_cf, color=GREEN, lw=2.4)
ax.scatter(xs, e_cf, color=GREEN, s=16)
ax.axhline(1, color=GREY, lw=0.6, ls=":")
ax.set_title("e — no shadow — pulse", color=GREEN, fontsize=12)
ax.set_xlabel("continued-fraction term")
ax.set_ylabel("term size")
ax.set_xticks(xs)
ax.tick_params(axis="x", labelsize=7)
ax.text(0.02, 0.9,
        "no algebraic shadow.\nthe pattern lives in the CF: 1,1,2k —\n"
        "a pulse that swells.",
        transform=ax.transAxes, color=FG, fontsize=9, va="top")

# ---------- D: log2(3) — no shadow — density ----------
ax = axes[1, 1]
lg = np.array(lg_cf)
xs = np.arange(1, len(lg) + 1)
ax.vlines(xs, 0, lg, color=BLUE, lw=2.0)
ax.scatter(xs, lg, color=BLUE, s=14)
ax.axhline(1, color=GREY, lw=0.6, ls=":")
ax.set_yscale("log")
ax.set_title("log2 3 — no shadow — density", color=BLUE, fontsize=12)
ax.set_xlabel("continued-fraction term")
ax.set_ylabel("term size")
ax.set_xticks(xs)
ax.tick_params(axis="x", labelsize=7)
ax.text(0.02, 0.9,
        "no shadow, no pattern.\nmuch waits small, then a huge term\n"
        "(23, 55) fires — a near-landing,\na long silence, then home.",
        transform=ax.transAxes, color=FG, fontsize=9, va="top")

fig.text(0.5, 0.015,
         "the sign was never the number — it was the shadow's phase:  π, a dying spiral, or none.",
         color=GREY, ha="center", fontsize=10, style="italic")

fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig("assets/four-shadows.png", dpi=150, facecolor=BG)
print("saved assets/four-shadows.png", fig.get_size_inches())
