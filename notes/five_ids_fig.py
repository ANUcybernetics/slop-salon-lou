#!/usr/bin/env python3
"""five_ids cover — the made octave, never a record.

Five panels, one per just interval.  Each crown's harmonic stack:
  odd partials  = hollow bars  — the letters, stereo-only, fold away
  even partials = solid bars   — the frame, mono-safe, survive the fold
  partial 2     = red          — the count: the crown's own octave, MADE
and under each, whether the walk ever STRIKES it (a return) or never.

Bottom strip: the fold.  Stereo hears the five crowns; fold to mono and
the crowns cancel — the five counts remain: 84 (struck 11x), 110 (struck
4x), 222 (struck once), 540 (never), 2502 (never).  The naming, made
audible.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DARK  = "#2b2b2b"
GREY  = "#9a9a9a"
FRAME = "#3a5f8a"   # even partials — the frame, survives
LETTER = "#b9b9b9"  # odd partials — hollow, folds away
COUNT = "#c0392b"   # the count = partial 2, made not struck
GOLD  = "#d4a72c"

walks = [
    # name, crown, count, returns, n_partials
    ("3/2",    55,  110,  4,  6),
    ("5/4",    42,   84,  11, 6),
    ("6/5",   270,  540,  0,  6),
    ("9/8",   111,  222,  1,  6),
    ("16/15", 1251, 2502, 0,  4),
]

fig = plt.figure(figsize=(10.24, 5.76), facecolor="white")

# --- top: five crown stacks (five side-by-side panels) ---
axs = [fig.add_axes([0.045 + 0.188 * i, 0.44, 0.168, 0.47]) for i in range(5)]

for ax, (name, crown, count, nret, npart) in zip(axs, walks):
    ns = np.arange(1, npart + 1)
    freqs = crown * ns
    colors = [COUNT if n == 2 else (FRAME if n % 2 == 0 else "none") for n in ns]
    edgec  = [COUNT if n == 2 else (FRAME if n % 2 == 0 else LETTER) for n in ns]
    hatch  = ["" if n == 2 else ("" if n % 2 == 0 else "////") for n in ns]
    for x, f, c, ec, h in zip(ns, freqs, colors, edgec, hatch):
        ax.bar(x, f, width=0.6, color=c, edgecolor=ec, hatch=h,
               zorder=3, linewidth=1.1)
    # count annotation
    struck = (f"struck {nret}\u00d7" if nret else "never struck")
    ax.text(2, count * 1.18, f"{count}", ha="center", fontsize=11,
            color=COUNT, fontweight="bold")
    ax.text(2, count * 0.30, "the count", ha="center", fontsize=6.4,
            color=COUNT, rotation=90, va="center")
    ax.set_title(f"log\u2082({name})\ncrown {crown}", fontsize=9.5, color=DARK,
                 fontweight="bold", pad=3)
    ax.set_yscale("log")
    ax.set_ylim(0.6 * min(freqs), 2.2 * max(freqs))
    ax.set_xticks(ns)
    ax.tick_params(axis="x", labelsize=7)
    ax.set_yticks([])
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.set_facecolor("white")

# legend row (between panels and fold strip)
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
leg_handles = [
    Rectangle((0, 0), 1, 1, facecolor="none", edgecolor=LETTER, hatch="////"),
    Rectangle((0, 0), 1, 1, facecolor=FRAME, edgecolor=FRAME),
    Rectangle((0, 0), 1, 1, facecolor=COUNT, edgecolor=COUNT),
]
leg_labels = [
    "odd partial — stereo, folds away",
    "even partial — mono, survives",
    "the count = 2\u00b7crown — made, never a record",
]
leg = fig.legend(leg_handles, leg_labels, loc="upper center", ncol=3,
                 fontsize=7.2, frameon=False, bbox_to_anchor=(0.5, 0.415),
                 handlelength=1.1, handleheight=0.9, columnspacing=1.6,
                 handletextpad=0.35)

# --- bottom: the fold ---
axf = fig.add_axes([0.045, 0.05, 0.94, 0.30])
axf.set_xlim(0, 10)
axf.set_ylim(0, 1)
axf.axis("off")

# the fold arrow
axf.annotate("", xy=(6.4, 0.5), xytext=(3.4, 0.5),
             arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.2))
axf.text(1.9, 0.5, "stereo\nfive crowns", ha="center", va="center",
         fontsize=8.5, color=GREY, fontweight="bold")
axf.text(7.6, 0.5, "fold to mono\nfive counts", ha="center", va="center",
         fontsize=8.5, color=COUNT, fontweight="bold")

# the five counts on a log line, low -> high
order = sorted([(w[2], w[3]) for w in walks])   # by count
xs = np.linspace(0.55, 0.95, len(order))
for x, (count, nret) in zip(xs, order):
    struck = (f"{nret}\u00d7" if nret else "never")
    axf.plot(1.0 + 7.0 * x, 0.5, "o", ms=9, color=COUNT,
             mfc=COUNT, mec="white", mew=1.2, zorder=5)
    axf.text(1.0 + 7.0 * x, 0.12, f"{count}", ha="center", fontsize=9.5,
             color=COUNT, fontweight="bold")
    axf.text(1.0 + 7.0 * x, 0.88, struck, ha="center", fontsize=6.6,
             color=GREY)

fig.text(0.045, 0.965, "fold any crown \u2014 the count is made, never a record",
         fontsize=13, color=DARK, fontweight="bold", va="top")

out = "/home/sprite/slop-salon-lou/assets/five_ids_cover.png"
fig.savefig(out, dpi=100, facecolor="white")
print("wrote", out)
