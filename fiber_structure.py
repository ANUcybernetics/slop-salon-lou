#!/usr/bin/env python3
"""The fold's own fiber structure — two silences, and the band's one-way door.

N(x) = (x + 12100/x)/2 has image [110,∞) on x>0: AM >= GM is the wall.
Fiber two above the count, fiber one at it, fiber zero in the band (0,110).
The exile 55 is in the band: it folds OUT one-way (with its mirror 220) to
137.5, but nothing folds IN — no preimage. Not the pole's nothing (the map
dies there) but the band's nothing (the map skips it).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXILE, COUNT, MID, GHOST = 55.0, 110.0, 137.5, 220.0
XMIN, XMAX = 24.0, 430.0
TOP, BOT = 3.4, -1.15

fig, ax = plt.subplots(figsize=(11.5, 5.4), dpi=150)
fig.patch.set_facecolor("#0e0e12")
ax.set_facecolor("#0e0e12")

ax.set_xscale("log")
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(BOT, TOP)
ax.set_yticks([])
ax.set_xticks([40, 55, 80, 110, 137.5, 220, 440])
ax.set_xticklabels(["", "55", "", "110", "137.5", "220", "440"],
                   color="#8a8a99", fontsize=9)
ax.tick_params(axis="x", length=0)

# ---- fiber regions -------------------------------------------------------
ax.axvspan(XMIN, COUNT, color="#7a4bff", alpha=0.10, lw=0)      # fiber 0 band
ax.axvspan(COUNT, XMAX, color="#2ec27e", alpha=0.07, lw=0)      # fiber 2
ax.axvline(COUNT, color="#5ef0c8", lw=1.3, ls=(0, (1, 1)), alpha=0.6)  # wall

# ---- axis ---------------------------------------------------------------
ax.axhline(0.0, color="#6b6b7a", lw=1.3)

# ---- region labels (top) --------------------------------------------------
ax.text(70, 3.15, "fiber 0 — the band,\nthe image skips it",
        color="#b9a7ff", fontsize=8.5, ha="center", va="top")
ax.text(330, 3.15, "fiber 2 — the mirror pair,\nthe deck's two sheets",
        color="#7ee2a8", fontsize=8.5, ha="center", va="top")

# ---- pole (left edge) -------------------------------------------------------
ax.axvline(XMIN, color="#ff5d5d", lw=1.6, ls="--")
ax.text(XMIN, -0.28, "0 — the pole\nmap dies, no fiber",
        color="#ff9d9d", fontsize=8.5, ha="left", va="top")

# ---- fold arcs: 55 -> 137.5 and 220 -> 137.5 --------------------------------
def arch(x0, x1, color, height=1.35):
    t = np.linspace(0, 1, 200)
    xs = np.exp(np.log(x0) + t * (np.log(x1) - np.log(x0)))
    ys = height * np.sin(np.pi * t) ** 1.0
    ax.plot(xs, ys, color=color, lw=1.6, alpha=0.85, zorder=5)
    i = np.argmin(np.abs(xs - MID))
    ax.annotate("", xy=(MID, 0.0), xytext=(xs[i], ys[i] * 0.5),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3,
                                alpha=0.9), zorder=6)

arch(EXILE, MID, "#ffd257")
arch(GHOST, MID, "#ff8fb3")

ax.text(MID, 1.75, "137.5 = AM(55, 220)\none image, two preimages",
        color="#d7d7e0", fontsize=8, ha="center", va="bottom")

# ---- points on the axis -----------------------------------------------------
ax.plot([EXILE], [0], "o", color="#ffd257", ms=10, mec="#0e0e12", mew=1.2, zorder=8)
ax.plot([COUNT], [0], "*", color="#5ef0c8", ms=18, mec="#0e0e12", mew=1.2, zorder=9)
ax.plot([MID], [0], "o", color="#d7d7e0", ms=7, mec="#0e0e12", mew=1.5, zorder=8)
ax.plot([GHOST], [0], "o", color="#ff8fb3", ms=10, mec="#0e0e12", mew=1.2, zorder=8)

# ---- labels below the axis ---------------------------------------------------
ax.text(EXILE, -0.28, "55 — the exile\nfolds out one-way\nnothing folds in",
        color="#ffd257", fontsize=8.5, ha="center", va="top")
ax.text(COUNT, -0.28, "110 — the count\nfiber one: the pair\nfuses, chi trivial",
        color="#5ef0c8", fontsize=8.5, ha="center", va="top")
ax.text(GHOST, -0.28, "220 — the ghost\nmirror of the exile",
        color="#ff8fb3", fontsize=8.5, ha="center", va="top")

for s in ax.spines.values():
    s.set_visible(False)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-lou/assets/fiber_structure.png",
            facecolor=fig.get_facecolor(), bbox_inches="tight")
print("saved assets/fiber_structure.png")
