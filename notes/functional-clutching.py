"""the functional equation is clutching.

s ↦ 1−s is an involution (g²=id) — the same order-2 the clutching register
named three ways. its fixed axis is the critical line. RH is the pair
collapsing onto that axis (the fold, in the x-plane). the shadow that
persists is the invariant of the flip — H⁰, the survivor, the thing that
does not fail away.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

BG = "#0c0e12"
GOLD = "#e8c468"
STEEL = "#7aa5c9"
CRIMSON = "#c0563f"
GRAY = "#8a93a3"
WHITE = "#e8e6e1"

# first few nontrivial zeta zeros (imaginary parts)
gammas = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(15, 7))
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

# ---------------- left panel: the involution in the s-plane ----------------
axL.set_xlim(0, 1)
axL.set_ylim(0, 44)
axL.set_xticks([0, 0.5, 1])
axL.set_xticklabels(["0", "½", "1"])
axL.set_yticks([])
axL.set_xlabel("Re s")
axL.set_ylabel("Im s  (γ)", color=GRAY)
axL.set_title("the flip:  s ↦ 1−s", color=GOLD, fontsize=15, pad=12)

# the fixed axis (critical line)
axL.axvline(0.5, color=GOLD, ls="--", lw=1.6, alpha=0.95)
axL.text(0.5, 42.6, "the fixed axis — the critical line",
         color=GOLD, ha="center", fontsize=10.5)

# flip arcs: hypothetical off-line zero pairs straddling the axis.
# one example drawn with an arrowhead (the flip direction), the rest plain.
def arc(beta, gam, **kw):
    x0, x1 = beta, 1.0 - beta
    cx = 0.5
    r = (x1 - x0) / 2.0
    th = np.linspace(0, np.pi, 80)
    axL.plot(cx + r * np.cos(th), gam + r * np.sin(th), lw=0.9, alpha=0.65, **kw)
    axL.plot([x0], [gam], marker="o", ms=6, color=STEEL, alpha=0.85)
    axL.plot([x1], [gam], marker="o", ms=6, color=STEEL, alpha=0.85)

arc(0.30, 6.0, color=GRAY)
arc(0.42, 24.0, color=GRAY)
# the labelled example — an arrow, not a plain arc, so the flip reads
axL.annotate("", xy=(0.28, 35.0), xytext=(0.72, 35.0),
             arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.4,
                             connectionstyle="arc3,rad=0.5"))
axL.plot([0.28], [35.0], marker="o", ms=6, color=STEEL)
axL.plot([0.72], [35.0], marker="o", ms=6, color=STEEL)
axL.text(0.5, 37.6, "a 2-cycle of the flip —\nif a zero sat off the line,\n"
                   "the flip forces its mirror",
         color=STEEL, ha="center", fontsize=10)

# the real zeros — on the axis, fixed as a set
for g in gammas:
    axL.plot([0.5], [g], marker="o", ms=7, color=GOLD, mec=WHITE, mew=0.8, zorder=5)
axL.text(0.5, 1.8, "the zeros — on the axis, fixed as a set.\n"
                  "RH: fixed pointwise.", color=WHITE, ha="center", fontsize=10)

# ---------------- right panel: H⁰ — the survivor ----------------
axR.set_xlim(-1.3, 1.3)
axR.set_ylim(-1.3, 1.3)
axR.set_xticks([])
axR.set_yticks([])
for s in ("bottom", "left"):
    axR.spines[s].set_visible(False)
axR.set_title("H⁰ — the survivor", color=GOLD, fontsize=15, pad=12)

# unit circle = the kept radius √x
circle = mpatches.Circle((0, 0), 1.0, fill=False, ec=WHITE, ls="--", lw=1.4, alpha=0.9)
axR.add_patch(circle)
axR.text(0.0, 1.12, "the kept radius √x", color=WHITE, ha="center", fontsize=10)

# φ: real conjugate 1/φ ≈ 0.618, contracting to home at 0
axR.plot([0.618], [0], marker="D", ms=9, color=GOLD, zorder=6)
axR.annotate("", xy=(0.15, 0), xytext=(0.618, 0),
             arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.2, linestyle=":"))
axR.text(0.72, -0.22, "φ — the flip, contracts", color=GOLD, fontsize=10, ha="left")

# ρ: complex conjugate pair at modulus 0.8688, spiralling to home
rho_mag = 1 / np.power(1.3247, 0.5)
for k in range(1, 15):
    r = rho_mag ** k
    th = k * 2.42  # ≈ 139.7° in radians per step
    axR.plot([r * np.cos(th)], [r * np.sin(th)], marker="o", ms=3.2,
             color=STEEL, alpha=0.9)
axR.text(-1.28, 0.18, "ρ — the rotation, dies", color=STEEL, fontsize=10, ha="left")

# the primes' shadow: on the circle, persisting
for th in [0.4, 1.0, 2.1, 3.4, 4.6, 5.4, 0.0]:
    axR.plot([np.cos(th)], [np.sin(th)], marker="o", ms=7, color=CRIMSON,
             mec=WHITE, mew=0.8, zorder=6)
axR.text(-1.28, -1.18, "the primes — on the circle, persist", color=CRIMSON,
         fontsize=10, ha="left")

# ---------------- footer ----------------
fig.text(0.5, 0.025,
         "the functional equation is clutching — g²=id, one invariant three names: "
         "the critical line, the fold, the kept radius. the survivor does not fail away.",
         color=WHITE, ha="center", fontsize=12.5)

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig("assets/functional-clutching.png", dpi=150, facecolor=BG,
            bbox_inches="tight")
print("wrote assets/functional-clutching.png")
