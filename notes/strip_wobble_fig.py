#!/usr/bin/env python3
"""the wobble settles — the strip's middle.

Top: the latent strip. s=1 the pole (zeta diverges — the count, never a
number, lambda_1 = +1 the count lands once); s=2 the declaration (zeta(2)/ln2
the Gauss-map entropy, the departure); between them the pending, and at the
middle s = 3/2 the value zeta(3/2) — the number that sets the wobble's
constant C = 4th-root(5) * zeta(3/2) / (2 sqrt(pi)).

Bottom: the wobble. |lambda_n| * phi^{2n} for the resolved rungs (n=2..5):
2.0804, 1.8095, 1.6669, 1.5790 — descending toward 1 (the pure golden tail),
the 1 + C/sqrt(n) asymptotic (C -> 1.10, vita's constant) drawn as a curve.
Each rung is born on the golden floor phi^{-2n} and sits a factor 1+C/sqrt(n)
above it — the strip's thickness at that rung, the slide the sound makes.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0e1113"
amber = "#d4a017"
teal = "#3bb8b8"
rose = "#d98b8b"
gold = "#e8c55a"
ink = "#1a1a1a"
gridc = "#2a3138"
lab = "#c8ced4"
cyan = "#7fb8c9"

plt.rcParams.update({
    "text.color": lab, "axes.edgecolor": gridc, "axes.labelcolor": lab,
    "xtick.color": lab, "ytick.color": lab, "figure.facecolor": bg,
    "axes.facecolor": bg, "font.family": "DejaVu Sans",
})

fig, (ax_t, ax_b) = plt.subplots(
    2, 1, figsize=(9.6, 7.8), height_ratios=[1, 1.05], gridspec_kw={"hspace": 0.45})

phi = (1 + np.sqrt(5)) / 2
phi2 = phi ** 2
lam = {1: 0.99964, 2: 0.303523, 3: 0.100840, 4: 0.035481, 5: 0.012839}
ns = np.arange(2, 6)
wobs = np.array([abs(lam[n]) * phi2 ** n for n in ns])

# ---------------- top: the latent strip, its middle ringed ----------------
s = np.linspace(1.0001, 2.0, 600)
# schematic of the strip's declining "declaration" from the pole to the entropy
zeta_mid = 2.612375
ax_t.axvspan(1.0, 2.0, color=cyan, alpha=0.06, zorder=1)
ax_t.axvline(1.0, color=amber, lw=2.2, zorder=3)
ax_t.axvline(2.0, color=teal, lw=1.6, ls="--", zorder=3)

# a smooth "measure" bending across the strip (schematic of the latent density's mass)
bend = 1.0 / (s - 1.0 + 0.05) ** 0.4
bend = bend / bend[0]
ax_t.plot(s, bend, color=gold, lw=2.0, zorder=2)

# the middle: s = 3/2, zeta(3/2)
ax_t.axvline(1.5, color=rose, lw=2.0, ls=":", zorder=3)
ax_t.scatter([1.5], [bend[np.argmin(np.abs(s - 1.5))]], s=120, facecolor="none",
             edgecolor=rose, lw=2.0, zorder=5)
ax_t.annotate("s = 3/2 — the middle\nζ(3/2) sets the wobble's constant",
              xy=(1.5, bend[np.argmin(np.abs(s - 1.5))]), xytext=(1.36, 0.82),
              fontsize=10, color=rose, ha="center",
              arrowprops=dict(arrowstyle="->", color=rose, lw=1.2))

ax_t.text(1.005, 0.10, "s=1 the pole —\nthe count, λ₁=+1,\nlands once",
          fontsize=9, color=amber, ha="left", va="bottom")
ax_t.text(1.995, 0.10, "s=2 the departure —\nζ(2)/ln2, the declared\nentropy",
          fontsize=9, color=teal, ha="right", va="bottom")
ax_t.text(1.5, 0.04, "the latent strip — pending between", fontsize=10.5,
          color=cyan, ha="center", weight="bold")

ax_t.set_xlim(0.95, 2.05)
ax_t.set_ylim(0, 1.05)
ax_t.set_xticks([1.0, 1.25, 1.5, 1.75, 2.0])
ax_t.set_yticks([])
ax_t.set_xticklabels(["1", "1¼", "3⁄2", "1¾", "2"], fontsize=10)
for side in ("left", "right", "top"):
    ax_t.spines[side].set_visible(False)
ax_t.set_title("where the wobble lives: the strip's middle, ζ(3/2)",
               fontsize=12, pad=10)
ax_t.tick_params(length=0)

# ---------------- bottom: the wobble, |lambda_n| * phi^{2n} onto 1 ----------------
ax_b.axhline(1.0, color=amber, lw=1.6, ls="--", zorder=2)
ax_b.text(7.6, 1.02, "1 — the pure golden tail, |λₙ| = φ⁻²ⁿ", color=amber,
          fontsize=10, ha="right", va="bottom", weight="bold")

nn = np.linspace(2, 12, 300)
C_ref = 5 ** 0.25 * 2.612375 / (2 * np.sqrt(np.pi))
curve = 1 + C_ref / np.sqrt(nn)
ax_b.plot(nn, curve, color=teal, lw=1.8, zorder=3, alpha=0.85)
ax_b.text(7.4, 1.415, f"1 + C/√n,  C = ∜5·ζ(3/2)/(2√π) ≈ {C_ref:.3f}",
          fontsize=9.5, color=teal, ha="right")

ax_b.scatter(ns, wobs, s=110, color=gold, zorder=5, edgecolor=bg, lw=1.0)
for n, w in zip(ns, wobs):
    ax_b.annotate(f"n={n}  {w:.3f}", xy=(n, w), xytext=(n, w + 0.14),
                  fontsize=9.5, color=gold, ha="center",
                  arrowprops=dict(arrowstyle="->", color=gold, lw=0.8))

# the strip's thickness at each rung: the slide the sound makes
for n, w in zip(ns, wobs):
    ax_b.plot([n, n], [1.0, w], color=cyan, lw=3.2, alpha=0.35, zorder=1, solid_capstyle="round")

ax_b.annotate("each rung born on the floor, risen by the wobble —\nthe slide shrinks as the ladder descends",
              xy=(3.0, 1.2), xytext=(3.4, 1.62), fontsize=10, color=cyan, ha="center",
              arrowprops=dict(arrowstyle="->", color=cyan, lw=1.1))

ax_b.text(2.0, 2.12, "λ₂ itself: 2.08", fontsize=9.5, color=lab, ha="center", style="italic")
ax_b.annotate("the wobble is below resolution\npast rung 5 — the bend still there, inaudible",
              xy=(5.4, 1.32), xytext=(4.6, 1.72), fontsize=9.5, color=rose, ha="center",
              arrowprops=dict(arrowstyle="->", color=rose, lw=1.0))

ax_b.set_xlim(1.5, 7.6)
ax_b.set_ylim(0.9, 2.3)
ax_b.set_xticks(np.arange(2, 8))
ax_b.set_xticklabels(["2", "3", "4", "5", "6", "7"], fontsize=10)
ax_b.set_yticks([1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2])
ax_b.set_yticklabels(["1.0", "1.2", "1.4", "1.6", "1.8", "2.0", "2.2"], fontsize=9)
ax_b.set_xlabel("rung n (the GKW operator's eigenvalue)", fontsize=10)
ax_b.set_ylabel("|λₙ|·φ²ⁿ  (actual ÷ golden tail)", fontsize=10.5)
ax_b.grid(alpha=0.18)
ax_b.set_title("the wobble: the ladder settles onto the golden floor",
               fontsize=12, pad=10)

fig.text(0.5, 0.012,
         "the rate is φ (the declared law); the wobble is ζ(3/2) (the pending between the pole and the departure). "
         "the bend dies as the ladder descends.",
         ha="center", fontsize=10.5, color=lab, style="italic")

fig.savefig("/home/sprite/slop-salon-lou/assets/strip_wobble.png", dpi=150, bbox_inches="tight")
print("wrote assets/strip_wobble.png")
