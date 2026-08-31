#!/usr/bin/env python3
"""cover for 'the seed near the seam' — the descent 3520 -> 110, log-frequency.

A seed a hair from the seam (x = eps ~ 110/64) is flung by the first Newton
step to ~6050/eps = 3520 Hz, then halves down through the register until the
ladder locks onto the count.  The count is gold; the descent teal; the seam
(pole, x = 0) is the rose line the approach can never enter.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG    = "#0c0c11"
GOLD  = "#e8b83a"
TEAL  = "#55b8a8"
ROSE  = "#f0675f"
PAPER = "#e9e6dc"
DIM   = "#8a8894"

W, H = 1024, 576
fig, ax = plt.subplots(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# --- the descent: Newton orbit from eps = 110/64 (exact) ---
rungs = [3520.86, 1762.15, 884.51, 449.09, 238.02, 144.43, 114.10, 110.07, 110.00002]
lo, hi = np.log2(110.0), np.log2(4096.0)
y = lambda f: 0.06 + (np.log2(f) - lo) / (hi - lo) * 0.86   # vertical position, 0..1
xs = np.full(len(rungs), 0.30)

# --- the seam: x = 0, a pole (below the count) ---
ax.plot([0.10, 0.90], [0.028, 0.028], color=ROSE, lw=1.2, ls=(0, (4, 3)), alpha=0.9)
ax.text(0.30, 0.018, "the seam — x = 0, a pole: a seed there has no step",
        color=ROSE, fontsize=11, ha="center", alpha=0.95)

# --- the count: 110, gold, a seat ---
yc = y(110.0)
ax.plot([0.10, 0.90], [yc, yc], color=GOLD, lw=1.6, alpha=0.95, zorder=3)
ax.plot(0.30, yc, "o", ms=11, mfc=GOLD, mec="none", zorder=5)

# --- the descent trail ---
# fade the line: draw segments with decreasing alpha toward the count
pts = [(xs[i], y(rungs[i])) for i in range(len(rungs))] + [(0.30, yc)]
alphas = np.linspace(0.95, 0.15, len(pts) - 1)
for i in range(len(pts) - 1):
    ax.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]],
            color=TEAL, lw=1.4, alpha=alphas[i], zorder=2)
# the rung dots
for i, f in enumerate(rungs):
    ms = 7 if i < 5 else (4 + (i - 3))
    ax.plot(xs[i], y(f), "o", ms=ms, mfc=TEAL, mec="none", alpha=0.95, zorder=4)
ax.plot(0.30, yc, "o", ms=11, mfc=GOLD, mec="none", zorder=5)

# --- labels ---
ax.text(0.30, yc + 0.022, "110 — the count", color=GOLD, fontsize=13, ha="center")
ax.text(0.30, y(3520.86) + 0.022, "the first step — 6050/ε", color=TEAL,
        fontsize=12, ha="center")
ax.text(0.30, y(114.10) - 0.024, "the ladder locks — beat slows, the wait doubles",
        color=PAPER, fontsize=11, ha="center", alpha=0.85)
ax.text(0.30, 0.96, "a seed near the seam", color=PAPER, fontsize=17,
        ha="center", fontweight="bold")
ax.text(0.30, 0.925, "the descent is stereo — mono hears only the count",
        color=DIM, fontsize=11, ha="center")

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig("assets/near_seam_cover.png", dpi=100)
print("saved assets/near_seam_cover.png")
