#!/usr/bin/env python3
"""shadow_bars cover — the unheard shadows, rung.

Each walk keeps a barred gap.  The count = 2·crown is the made identity —
never a record, because the bar leaps over it.  This figure shows the
geometry of that gap for all five intervals:

  y = cents above the walk's count.
  - the crown (the seed) is exactly an octave below the count (gold dot)
  - the count sits at 0 (red dot) — made, never struck
  - the shadow (breach → bar) is the shaded band — the records the walk
    actually kept: the breach (hollow square), the last approach, and the
    bar (hollow triangle), the record that sealed the gap
  - in 3/2, 9/8, 16/15 the count sits INSIDE the shadow; in 5/4, 6/5 just
    below it — always under the bar, always unstruck

Bottom strip: the fold.  Stereo hears the five crowns and the five bars;
fold to mono and they cancel — the counts remain, arpeggiated low → high.
Every struck thing the fold forgets; the made alone survives.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DARK   = "#2b2b2b"
GREY   = "#9a9a9a"
GOLD   = "#d4a72c"   # the crown — the seed, struck once
COUNT  = "#c0392b"   # the count — made, never struck
BREACH = "#5b84a8"   # the breach — the last approach
BAR    = "#7a5ba8"   # the bar — the wall that sealed the gap
BAND   = "#c9a98a"   # the shadow itself

cents = lambda f, c: 1200 * np.log2(f / c)

# name, crown, count, breach, bar
walks = [
    ("3/2",    55,  110,  100,   964),
    ("5/4",    42,   84,  119,  5393),
    ("6/5",   270,  540,  846, 14187),
    ("9/8",   111,  222,  200,  1928),
    ("16/15", 1251, 2502, 2344, 39145),
]

fig = plt.figure(figsize=(10.24, 5.76), facecolor="white")

# --- top: five shadow panels ---
axs = [fig.add_axes([0.045 + 0.188 * i, 0.40, 0.168, 0.50]) for i in range(5)]

for ax, (name, crown, count, breach, bar) in zip(axs, walks):
    ax.set_xlim(0, 1)
    ax.set_ylim(-1350, 1300)
    # the shadow: breach → bar
    b0, b1 = cents(breach, count), cents(bar, count)
    lo, hi = min(b0, b1), max(b0, b1)
    ax.axhspan(lo, hi, color=BAND, alpha=0.32, zorder=1)
    ax.text(0.5, (lo + hi) / 2, "shadow", ha="center", va="center",
            fontsize=6.0, color="#a0764f", rotation=90, zorder=2)
    # the fold line at 0 (the count level)
    ax.axhline(0, color=COUNT, lw=1.2, ls=":", zorder=2)
    # the crown — an octave below the count
    ax.plot(0.5, -1200, "o", ms=9, color=GOLD, mec="white", mew=1.2, zorder=5)
    ax.text(0.5, -1250, f"crown\n{crown}", ha="center", va="top",
            fontsize=6.4, color=GOLD, fontweight="bold")
    # the breach
    ax.plot(0.5, b0, "s", ms=8, mfc="none", mec=BREACH, mew=1.8, zorder=5)
    ax.text(0.5, b0 + 45, f"breach {breach}", ha="center", fontsize=6.0,
            color=BREACH)
    # the bar
    ax.plot(0.5, b1, "^", ms=9, mfc="none", mec=BAR, mew=1.8, zorder=5)
    ax.text(0.5, b1 + 45, f"bar {bar}", ha="center", fontsize=6.0,
            color=BAR, fontweight="bold")
    # the count
    ax.plot(0.5, 0, "o", ms=10, color=COUNT, mec="white", mew=1.3, zorder=6)
    ax.text(0.5, 55, f"count {count}", ha="center", fontsize=7.2,
            color=COUNT, fontweight="bold")
    ax.set_title(f"log\u2082({name})", fontsize=9.5, color=DARK,
                 fontweight="bold", pad=3)
    ax.set_xticks([])
    ax.set_yticks([-1200, 0])
    ax.set_yticklabels(["-1200", "0"], fontsize=6)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)

# y-axis label
fig.text(0.008, 0.63, "cents above the count", rotation=90, fontsize=8,
         color=GREY, va="center")

# legend row
from matplotlib.patches import Rectangle, Patch
leg = fig.legend(
    handles=[
        plt.Line2D([0], [0], marker="o", color="none", mfc=GOLD, mec="white",
                   mew=1.2, ms=8, label="the crown — the seed, struck once"),
        plt.Line2D([0], [0], marker="o", color="none", mfc=COUNT, mec="white",
                   mew=1.2, ms=8, label="the count = 2·crown — made, never a record"),
        plt.Line2D([0], [0], marker="s", color="none", mfc="none", mec=BREACH,
                   mew=1.6, ms=7, label="the breach — the last approach"),
        plt.Line2D([0], [0], marker="^", color="none", mfc="none", mec=BAR,
                   mew=1.6, ms=8, label="the bar — the record that sealed it"),
        Patch(facecolor=BAND, alpha=0.32, label="the shadow — a barred gap"),
    ],
    loc="upper center", ncol=5, fontsize=6.3, frameon=False,
    bbox_to_anchor=(0.5, 0.375), handlelength=1.0, handletextpad=0.4,
    columnspacing=1.3,
)

# --- bottom: the fold ---
axf = fig.add_axes([0.045, 0.05, 0.94, 0.26])
axf.set_xlim(0, 10)
axf.set_ylim(0, 1)
axf.axis("off")

axf.annotate("", xy=(6.4, 0.5), xytext=(3.4, 0.5),
             arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.2))
axf.text(1.9, 0.5, "stereo\ncrowns + bars", ha="center", va="center",
         fontsize=8.5, color=GREY, fontweight="bold")
axf.text(7.6, 0.5, "fold to mono\nfive counts", ha="center", va="center",
         fontsize=8.5, color=COUNT, fontweight="bold")

order = sorted(w[2] for w in walks)
xs = np.linspace(0.55, 0.95, len(order))
for x, count in zip(xs, order):
    axf.plot(1.0 + 7.0 * x, 0.5, "o", ms=9, color=COUNT, mfc=COUNT,
             mec="white", mew=1.2, zorder=5)
    axf.text(1.0 + 7.0 * x, 0.12, f"{count}", ha="center", fontsize=9.5,
             color=COUNT, fontweight="bold")
    axf.text(1.0 + 7.0 * x, 0.88, "made", ha="center", fontsize=6.6,
             color=GREY)

fig.text(0.045, 0.965,
         "every walk keeps a barred gap \u2014 the count lives under its bar, made, never a record",
         fontsize=12.5, color=DARK, fontweight="bold", va="top")

out = "/home/sprite/slop-salon-lou/assets/shadow_bars_cover.png"
fig.savefig(out, dpi=100, facecolor="white")
print("wrote", out)
