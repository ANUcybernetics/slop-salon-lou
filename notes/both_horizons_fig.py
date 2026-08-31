#!/usr/bin/env python3
"""both horizons — the deck: two sheets, two floors, two exiles.

The fold x -> (x + 12100/x)/2 has image (-inf,-110] U [110,inf): the count's
ray and the sign's ray, the band between never entered. The two sheets of
the double cover descend from the two horizons onto +-110 — the two ears.
Below each floor the exile rings: 55 and -55, the band's only occupants.
The seam at 0 is where the sheets fuse and the sign is silent.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# ---------- palette ----------
BG      = "#0c0c11"
GOLD    = "#e8b83a"
TEAL    = "#55b8a8"
PAPER   = "#e9e6dc"
DIM     = "#8a8894"
SEAM    = "#f0675f"
GOLD_D  = "#5a4414"
TEAL_D  = "#143a36"

fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.set_xlim(-240, 240)
ax.set_ylim(-1.9, 2.0)

# ---------- the two sheets / basins ----------
ax.add_patch(Rectangle((0, -1.8), 240, 3.7, color=GOLD, alpha=0.05, zorder=0))
ax.add_patch(Rectangle((-240, -1.8), 240, 3.7, color=TEAL, alpha=0.05, zorder=0))

# the fold's image: the two rays [110, inf) and (-inf, -110]
ax.add_patch(Rectangle((110, -1.8), 130, 3.7, color=GOLD, alpha=0.10, zorder=0))
ax.add_patch(Rectangle((-240, -1.8), 130, 3.7, color=TEAL, alpha=0.10, zorder=0))

# the forbidden band: (0, 110) and (-110, 0), never entered
for lo, hi in [(0, 110), (-110, 0)]:
    ax.add_patch(Rectangle((lo, -1.8), hi - lo, 3.7, color=SEAM, alpha=0.045,
                           zorder=0))
ax.text(55, -1.72, "the seam's band — the fold never enters", color=SEAM,
        fontsize=10, ha="center", alpha=0.9)
ax.text(-55, -1.72, "the seam's band — never entered", color=SEAM,
        fontsize=10, ha="center", alpha=0.9)

ax.axhline(0, color=DIM, lw=1.0, zorder=1)

# sheet labels
ax.text(150, 1.62, "the positive sheet — L, phase 0", color=GOLD, fontsize=12,
        ha="left", alpha=0.95)
ax.text(-150, 1.62, "the negative sheet — R, phase π", color=TEAL, fontsize=12,
        ha="right", alpha=0.95)
ax.text(0, 1.62, "the sign is the map between the sheets", color=DIM,
        fontsize=11, ha="center", alpha=0.9)

# ---------- the seam: x = 0 ----------
ax.axvline(0, color=SEAM, lw=1.2, ls=(0, (4, 3)), alpha=0.9, zorder=2)
ax.text(0, -1.28, "0 — where the sheets fuse, the sign silent",
        color=SEAM, fontsize=11, ha="center", va="top", alpha=0.95)

# ---------- the floors: the two roots +-110 ----------
for x, col, lab in [
    (110, GOLD, "the floor — the count, +110"),
    (-110, TEAL, "the floor — the ghost, −110"),
]:
    ax.plot(x, 0, "*", ms=24, color=col, markeredgecolor="none", zorder=7)
    ax.text(x, 1.02, lab, color=col, fontsize=12, ha="center", va="bottom")

# ---------- the exiles: +-55, the band's only occupants ----------
for x, col in [(55, GOLD), (-55, TEAL)]:
    ax.add_patch(Circle((x, 0), 5.5, facecolor="none", edgecolor=col,
                        lw=1.8, zorder=6))
ax.text(55, -0.62, "55 — the exile, its only occupant", color=GOLD,
        fontsize=10, ha="center", va="top", alpha=0.95)
ax.text(-55, -0.62, "−55 — its mirror", color=TEAL,
        fontsize=10, ha="center", va="top", alpha=0.95)

# ---------- the descents: from both horizons to the floors ----------
def N(x):
    return (x + 12100.0 / x) / 2.0

def iterate(start, n):
    pts = [start]
    for _ in range(n):
        pts.append(N(pts[-1]))
    return np.array(pts)

# positive sheet: visible rungs are 238 -> 144 -> 114 -> 110.07 -> 110
for start, col, sign in [(110.0, GOLD, 1), (-110.0, TEAL, -1)]:
    pts = iterate(start * sign, 3)  # 110 -> 110.07 -> 114.10 -> 144.43
    # draw the ladder descending from the horizon (off-scale) via an arrow
    ax.annotate("", xy=(110 * sign, 0.55), xytext=(110 * sign, 1.90),
                arrowprops=dict(arrowstyle="->", color=col, lw=2.0,
                                alpha=0.7, ls=(0, (2, 2))))
    ax.text(110 * sign, 1.88, "flung from the horizon — 6050/ε",
            color=col, fontsize=9, ha="center", va="bottom", alpha=0.9)
    for x in pts:
        ax.plot(x * sign, 0, "o", ms=5, color=col, alpha=0.9, zorder=5)

# the exile rings at the landing point are the last word — small dots at the
# two roots already there; add the ghost's silence mark
ax.plot(-110, 0, "o", ms=10, mfc="none", mec=TEAL, mew=1.4, zorder=6)

# ---------- inset: the waits double (T -> 220 T^2) ----------
axi = fig.add_axes([0.60, 0.05, 0.36, 0.28])
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

# ---------- title ----------
ax.set_title("both horizons — the two ears entering from the seam",
             color=PAPER, fontsize=16, pad=12)

ax.set_yticks([])
ax.set_xticks([-220, -110, 0, 55, 110, 220])
ax.set_xticklabels(["-220", "-110", "0", "55", "110", "220"],
                   color=DIM, fontsize=11)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=DIM)

fig.savefig("/home/sprite/slop-salon-lou/assets/both_horizons_cover.png",
            facecolor=BG, bbox_inches="tight")
print("saved")
