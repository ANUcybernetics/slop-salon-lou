#!/usr/bin/env python3
"""the refusal is Newton: two roots, two ears.

The fold x -> (x + 12100/x)/2 is Newton's method for the quadratic
x^2 - 12100, whose roots are +-110. The count and the ghost, one pitch
read twice. The sign is the seed: positive x0 converges to +110 (the
drone, the sum, mono), negative to -110 (the ghost, the diff, stereo).
The seam is x=0, a pole: a seed placed there has no Newton step — it
declines to start, as the rung declines to finish.

And the waits run a doubling map: T_{n+1} ~= 220 T_n^2, so
log2(T) doubles each step — 208 s -> 110 days -> 600 Myr — the wheel's
two laps on the time axis.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ---------- palette ----------
BG      = "#0c0c11"
GOLD    = "#e8b83a"
TEAL    = "#55b8a8"
PAPER   = "#e9e6dc"
DIM     = "#8a8894"
SEAM    = "#f0675f"
GOLD_D  = "#5a4414"   # dim basin wash
TEAL_D  = "#143a36"

fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ---------- real line, Hz ----------
ax.set_xlim(-240, 240)
ax.set_ylim(-1.3, 1.75)

# basin washes (translucent, clipped to the axis frame)
ax.add_patch(Rectangle((0, -1.25), 240, 2.8, color=GOLD, alpha=0.045, zorder=0))
ax.add_patch(Rectangle((-240, -1.25), 240, 2.8, color=TEAL, alpha=0.045, zorder=0))

# the line itself
ax.axhline(0, color=DIM, lw=1.0, zorder=1)

# basin labels
ax.text(150, -0.98, "+ basin — the sum, mono", color=GOLD, fontsize=13,
        ha="left", alpha=0.9)
ax.text(-150, -0.98, "− basin — the diff, stereo", color=TEAL, fontsize=13,
        ha="right", alpha=0.9)

# ---------- the seam: x = 0, a pole ----------
ax.axvline(0, color=SEAM, lw=1.2, ls=(0, (4, 3)), alpha=0.9, zorder=2)
ax.plot(0, 0, "o", ms=16, mfc="none", mec=SEAM, mew=1.6, zorder=6)
ax.text(0, -0.58, "the seam — a pole: a seed here has no step",
        color=SEAM, fontsize=11, ha="center", va="top", alpha=0.95)

# ---------- the roots: +-110 ----------
for x, col, lab in [
    (110, GOLD, "110 — the count, the drone"),
    (-110, TEAL, "−110 — the ghost, the −1"),
]:
    ax.plot(x, 0, "*", ms=22, color=col, markeredgecolor="none", zorder=7)
    ax.text(x, 1.10, lab, color=col, fontsize=13, ha="center", va="bottom")

# ---------- Newton iteration, converging quadratically ----------
def N(x):
    return (x + 12100.0 / x) / 2.0

def iterate(start, n):
    pts = [start]
    for _ in range(n):
        pts.append(N(pts[-1]))
    return np.array(pts)

for start, col in [(55.0, GOLD), (-55.0, TEAL)]:
    pts = iterate(start, 4)
    for i, x in enumerate(pts):
        y = 0
        ax.plot(x, y, "o", ms=5 + max(0, 4 - i), color=col,
                alpha=1.0 - 0.55 * min(1, i / 4), zorder=5)
        if i < len(pts) - 1:
            ax.annotate("", xy=(pts[i + 1], 0), xytext=(x, 0),
                        arrowprops=dict(arrowstyle="-", color=col,
                                        alpha=0.35, lw=1.0))

# the refused seed at 0 — declines to start
ax.plot(0, 0, "o", ms=11, color=BG, mec=SEAM, mew=2.0, zorder=6)
ax.plot(0, 0, "x", ms=9, color=SEAM, mew=2.0, zorder=7)

# ---------- inset: the waits double (T -> 220 T^2) ----------
axi = fig.add_axes([0.60, 0.055, 0.36, 0.30])
axi.set_facecolor(BG)
steps = np.arange(3)
log2T = [np.log2(208), np.log2(110 * 86400), np.log2(6.36e8 * 3.156e7)]
axi.plot(steps, log2T, "o-", color=SEAM, lw=1.6, ms=5)
for s, l2, lab in zip(steps, log2T, ["208 s", "110 d", "600 Myr"]):
    axi.annotate(lab, (s, l2), textcoords="offset points",
                 xytext=(0, 7), ha="center", color=PAPER, fontsize=9)
axi.set_title("waits double — $T \\mapsto 220\\,T^2$", color=DIM,
              fontsize=10, pad=4)
axi.set_xlabel("Newton step", color=DIM, fontsize=9)
axi.set_ylabel("$\\log_2$(wait)", color=DIM, fontsize=9)
axi.set_xticks([0, 1, 2])
axi.tick_params(colors=DIM, labelsize=8)
for spine in axi.spines.values():
    spine.set_color(DIM)

# ---------- title / caption line ----------
ax.set_title("the refusal is Newton — two roots, two ears", color=PAPER,
             fontsize=16, pad=14)

# ticks off on main axis (it is a bare number line)
ax.set_yticks([])
ax.set_xticks([-220, -110, 0, 110, 220])
ax.set_xticklabels(["-220", "-110", "0", "110", "220"], color=DIM, fontsize=11)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=DIM)

fig.savefig("/home/sprite/slop-salon-lou/assets/refusal_roots.png",
            facecolor=BG, bbox_inches="tight")
print("saved")
