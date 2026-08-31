#!/usr/bin/env python3
"""two clocks — the ladder's time.  cover for assets/two_clocks.mp4.

σ_n = [n;n,n,…]: the metallic ladder's continued fraction is all n, so its
convergent waits are CONSTANT, equal to the branch.  φ counts by ones, silver
by twos, σ₃ by threes — a metronome whose rate is the rung.  Each rung's climb
begins ON the ear's grid (the first convergent is n/1 → the tone 55n, the
difference tone) and approaches the never-struck 55σ_n.

log₂(3/2) = [0;1,1,2,2,3,1,5,2,23,2,2,1,1,55,…]: the same act — a ladder
closing on a limit that never lands — but the waits are lawless, 2→23→55→114.
Constant, and a storm.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
ROSE = "#d16fa0"      # the storm
TEAL = "#7fb3ff"      # the metronome's struck convergents
GOLD = "#f0c26a"      # the grid tones / the count / the targets

BASE = 55.0


def sigma(n):
    return (n + np.sqrt(n * n + 4)) / 2.0


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.0, 6.75), dpi=100,
                               gridspec_kw={"height_ratios": [0.56, 0.44]})
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=9)
    ax.set_yticks([])

# ================= top: the metronome ladder =================
ax1.set_xlim(-30, 42)
ax1.set_ylim(0, 1)
ax1.text(-26, 0.965, "σₙ = [n;n,n,…] — the wait is the branch, constant",
         color=TXT, fontsize=11, ha="left", va="center", fontweight="bold")

rows = {1: "φ · by ones", 2: "1+√2 · by twos", 3: "σ₃ · by threes",
        4: "σ₄ · by fours", 5: "σ₅ · by fives"}
for n, y in zip([1, 2, 3, 4, 5], [0.84, 0.70, 0.56, 0.42, 0.28]):
    # the row axis
    ax1.plot([0, 6 * n + n], [y, y], color=GRID, lw=1.0, zorder=1)
    # the landing (never reached): one wait beyond the last tick
    ax1.plot(6 * n + n, y, marker="D", ms=7, mec=GOLD, mfc="none", mew=1.6,
             zorder=5)
    ax1.text(6 * n + n + 1.2, y + 0.045, f"{BASE * sigma(n):.1f}",
             color=GOLD, fontsize=7.5, ha="left", va="bottom")
    # the six ticks: constant wait n; the first is the grid tone 55n (gold)
    for k in range(1, 7):
        x = k * n
        gold = (k == 1)
        ax1.plot([x, x], [y - 0.045, y + 0.045],
                 color=GOLD if gold else TEAL, lw=1.8, zorder=4)
    ax1.text(0.3, y + 0.075, f"n={n}", color=DIM, fontsize=8, ha="center")
    ax1.text(-27, y, rows[n], color=TXT, fontsize=9, ha="right", va="center",
             style="italic")
ax1.text(-26, 0.10, "each rung's first tick is the grid tone 55·n — the "
                    "difference tone itself; the landing 55·σₙ is never struck",
         color=DIM, fontsize=8.5, ha="left", va="center", style="italic")

# ================= bottom: the storm =================
ax2.set_xlim(0, 106)
ax2.set_ylim(0, 1)
ax2.text(0.5, 0.93, "log₂(3/2) = [0;1,1,2,2,3,1,5,2,23,2,2,1,1,55,…] — the "
                    "wait is lawless", color=TXT, fontsize=11, ha="left",
         va="center", fontweight="bold")
y = 0.55
ax2.plot([0, 101], [y, y], color=GRID, lw=1.0, zorder=1)

# the 23-wait and 55-wait voids
ax2.add_patch(Rectangle((17, y - 0.30), 23, 0.60, facecolor="#1a1a24",
                        edgecolor="none", zorder=0))
ax2.add_patch(Rectangle((46, y - 0.30), 55, 0.60, facecolor="#1a1a24",
                        edgecolor="none", zorder=0))
ax2.text(28.5, y + 0.14, "the 23-wait", color=DIM, fontsize=8.5, ha="center")
ax2.text(73.5, y + 0.14, "the 55-wait", color=DIM, fontsize=8.5, ha="center")

# clicks at the real cumulative waits (units): 1,2,4,6,9,10,15,17,40,42,44,45,46
clicks = [1, 2, 4, 6, 9, 10, 15, 17, 40, 42, 44, 45, 46]
for i, x in enumerate(clicks):
    gold = (x == 1)   # the count 110, the storm's first struck object
    ax2.plot([x, x], [y - 0.05, y + 0.05], color=GOLD if gold else ROSE,
             lw=1.9, zorder=4)
    if x in (1, 2, 15):
        lab = {1: "110", 2: "77.8", 15: "82.5"}[x]
        ax2.text(x, y - 0.13, lab, color=GOLD if gold else DIM, fontsize=7.5,
                 ha="center")

# the fifth, never landed
ax2.plot(101, y, marker="D", ms=7, mec=ROSE, mfc="none", mew=1.6, zorder=5)
ax2.text(101, y - 0.26, "82.5 · the fifth", color=ROSE, fontsize=8, ha="center")
ax2.text(0.5, 0.16, "the storm passes through the count 110 and the tritone "
                    "77.8 en route to the fifth — then holds, clicks, and ends "
                    "in the 55-wait, the landing refused",
         color=DIM, fontsize=8.5, ha="left", va="center", style="italic")

# ================= caption =================
fig.text(0.5, 0.015,
         "the same act — a ladder closing on a limit that never lands — two "
         "clocks.  the metallic ladder's quotients are all n: constant waits, "
         "a metronome.  log₂(3/2)'s quotients run 2→23→55→114: the wait is a "
         "storm.  constant, and lawless.",
         color=TXT, fontsize=9.5, ha="center", linespacing=1.4)

plt.tight_layout(rect=(0, 0.04, 1, 0.97))
plt.savefig("assets/two_clocks.png", dpi=100, facecolor=BG)
print("wrote assets/two_clocks.png")

fig.canvas.draw()
bad = 0
for ax in (ax1, ax2):
    for tx in ax.texts:
        if not tx.get_text():
            continue
        bb = tx.get_window_extent()
        inx = bb.x0 >= ax.bbox.x0 - 1 and bb.x1 <= ax.bbox.x1 + 1
        iny = bb.y0 >= ax.bbox.y0 - 1 and bb.y1 <= ax.bbox.y1 + 1
        if not (inx and iny):
            print("CLIPPED:", repr(tx.get_text())[:60], bb)
            bad += 1
print("clip check:", "clean" if bad == 0 else f"{bad} clipped")
