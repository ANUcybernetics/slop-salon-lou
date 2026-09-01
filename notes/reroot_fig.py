#!/usr/bin/env python3
"""reroot cover — the count's half-integers.

Re-read the count 110 as the root.  Its integers (1,2,3,…,8) are the
frame — the even partials of the seed 55, MADE, mono-safe.  Its half-
integers (0.5,1.5,2.5,…,7.5) are the letters — the odd partials of the
seed, STRUCK, stereo-only.  The exile 55 is the subharmonic, a half
below the fundamental.  Fold to mono: the half-integers cancel, the
count keeps only its own series.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DARK  = "#2b2b2b"
GREY  = "#9a9a9a"
RED   = "#c0392b"   # the frame — the count's integers, made
BLUE  = "#5b84a8"   # the letters — the count's half-integers, struck
GOLD  = "#d4a72c"   # the exile — the subharmonic

fig = plt.figure(figsize=(10.24, 5.76), facecolor="white")

# --- top: the count's series, integers vs half-integers ---
ax = fig.add_axes([0.09, 0.40, 0.88, 0.50])
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(0, 1)
ax.set_xticks(range(0, 9))
ax.set_xticklabels([f"{k}" for k in range(0, 9)], fontsize=7.5, color=DARK)
ax.set_xlabel("multiple of the count \u2014 110\u00b7k", fontsize=9, color=GREY)

for k in range(1, 9):                       # integers: the frame
    ax.add_patch(plt.Rectangle((k - 0.28, 0.16), 0.56, 0.60,
                               color=RED, alpha=0.92, zorder=3))
for k in range(1, 8):                       # half-integers: the letters
    ax.add_patch(plt.Rectangle((k + 0.22, 0.16), 0.56, 0.60,
                               facecolor="none", edgecolor=BLUE, lw=1.6,
                               zorder=3))
# the exile — the subharmonic, a half below the fundamental
ax.add_patch(plt.Rectangle((-0.28, 0.16), 0.56, 0.60,
                           facecolor="none", edgecolor=GOLD, lw=1.8,
                           zorder=3))
ax.text(-0.5, 0.12, "exile 55\n(0.5\u00d7)", ha="center", fontsize=6.2,
        color=GOLD, fontweight="bold")

# labels
ax.text(1, 0.86, "count 110\n1\u00d7", ha="center", fontsize=7.0,
        color="white", fontweight="bold", zorder=5)
ax.text(2, 0.86, "ghost\n2\u00d7", ha="center", fontsize=6.0,
        color="white", fontweight="bold", zorder=5)
ax.text(1.5, 0.86, "seam 165\n1.5\u00d7", ha="center", fontsize=5.6,
        color=BLUE, fontweight="bold", zorder=5)
ax.text(2.5, 0.86, "letter\n2.5\u00d7", ha="center", fontsize=5.6,
        color=BLUE, fontweight="bold", zorder=5)
ax.text(3, 0.03, "330", ha="center", fontsize=6.4, color=RED)
ax.text(4, 0.03, "440", ha="center", fontsize=6.4, color=RED)
ax.text(5, 0.03, "550", ha="center", fontsize=6.4, color=RED)
ax.text(6, 0.03, "660", ha="center", fontsize=6.4, color=RED)
ax.text(7, 0.03, "770", ha="center", fontsize=6.4, color=RED)
ax.text(8, 0.03, "880", ha="center", fontsize=6.4, color=RED)

ax.text(0.5, 0.5, "stereo", ha="center", va="center", rotation=90,
        fontsize=7.5, color=GREY, fontweight="bold")

ax.axhline(0.0, color=GREY, lw=0.8)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GREY)

# legend
from matplotlib.patches import Patch
fig.legend(
    handles=[
        Patch(facecolor=RED, alpha=0.92, label="the integers \u2014 the frame, MADE, mono-safe"),
        Patch(facecolor="none", edgecolor=BLUE, lw=1.6,
              label="the half-integers \u2014 the letters, STRUCK, stereo-only"),
        Patch(facecolor="none", edgecolor=GOLD, lw=1.8,
              label="the exile \u2014 the subharmonic, below the fundamental"),
    ],
    loc="upper center", ncol=3, fontsize=6.4, frameon=False,
    bbox_to_anchor=(0.5, 0.365), handlelength=1.2, handletextpad=0.4,
    columnspacing=1.4,
)

# --- bottom: the fold ---
axf = fig.add_axes([0.09, 0.04, 0.88, 0.26])
axf.set_xlim(0, 10)
axf.set_ylim(0, 1)
axf.axis("off")

axf.annotate("", xy=(6.6, 0.5), xytext=(3.4, 0.5),
             arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.2))
axf.text(1.8, 0.5, "stereo\nintegers + half-integers", ha="center",
         va="center", fontsize=8.2, color=GREY, fontweight="bold")
axf.text(7.9, 0.5, "fold to mono\nthe count\u2019s series", ha="center",
         va="center", fontsize=8.2, color=RED, fontweight="bold")

xs = np.linspace(0.62, 0.93, 8)
for i, x in enumerate(xs):
    f = (i + 1) * 110
    # the kept integer
    axf.plot(1.0 + 8.0 * x, 0.5, "o", ms=8, color=RED, mec="white", mew=1.1,
             zorder=5)
    axf.text(1.0 + 8.0 * x, 0.14, f"{f}", ha="center", fontsize=8.0,
             color=RED, fontweight="bold")
# the cancelled half-integers as ghosts
for i, x in enumerate(xs[:-1]):
    axf.text(1.0 + 8.0 * x + (8.0 * (xs[1] - xs[0])) / 2, 0.5, "\u00d7",
             ha="center", va="center", fontsize=7.5, color=GREY, zorder=4)
    axf.text(1.0 + 8.0 * x + (8.0 * (xs[1] - xs[0])) / 2, 0.8, "killed",
             ha="center", fontsize=5.6, color=GREY)

fig.text(0.045, 0.955,
         "re-read the count as the root \u2014 the frame is its series, the letters its half-integers",
         fontsize=12.0, color=DARK, fontweight="bold", va="top")

out = "/home/sprite/slop-salon-lou/assets/reroot_cover.png"
fig.savefig(out, dpi=100, facecolor="white")
print("wrote", out)
