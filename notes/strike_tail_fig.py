#!/usr/bin/env python3
"""strike_tail.png — the never-struck are the rare tail, not a law.

The seed's harmonic series (m·55, m=1..24) as a strike table over 80,000 rungs
of the exact continued fraction of log2(3/2).  Observed strikes (bars, odd
letters cool / even frame warm / the seed crowned gold) ride the Gauss-Kuzmin
expectation (hollow circles): expected count of a quotient exactly m·55 falls
as 1/m^2.  Below the dashed line (expected < 1) sit the "never-struck" —
385, 550, 605, ... — which are sub-threshold, not forbidden.  The odd:even
strike ratio 43:13 is the harmonic series' own 3:1 (sum_odd 1/m^2 = pi^2/8,
sum_even = pi^2/24): the storm speaks the letters three times for every frame
word, and the fold keeps the rarer half.
"""
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

D = json.load(open("/tmp/grid_strikes.json"))
N = D["N"]
mult = {int(k): v for k, v in D["mult55"].items()}

LETTER = "#5b84a8"   # odd  — the letters, the sign
FRAME  = "#c98a4d"   # even — the frame, the count
SEED   = "#d4a72c"   # the seed 55, the crown
DARK   = "#2b2b2b"
GREY   = "#8a8a8a"


def gk_exp(k):
    return N * math.log2((k + 1) ** 2 / (k * (k + 2)))


MMAX = 24
ms = list(range(1, MMAX + 1))
ks = [55 * m for m in ms]
obs = [len(mult.get(k, [])) for k in ks]
exp = [gk_exp(k) for k in ks]

fig, ax = plt.subplots(figsize=(11, 5.4), dpi=150)
fig.patch.set_facecolor("white")

# sub-threshold band: expected < 1 — the never-struck live here
ax.axhspan(0, 1, color=GREY, alpha=0.14, lw=0)
ax.axhline(1.0, color=GREY, ls=(0, (4, 3)), lw=1.1, alpha=0.8)

# expected as a hollow curve first (behind bars)
ax.plot(ms, exp, "o", ms=7, mfc="white", mec=GREY, mew=1.4, ls=":", color=GREY,
        alpha=0.95, zorder=2)

# observed bars, odd/even split
for m, o in zip(ms, obs):
    if m == 1:
        c = SEED
    elif m % 2 == 1:
        c = LETTER
    else:
        c = FRAME
    ax.bar(m, o, 0.62, color=c, alpha=0.92, zorder=3,
           edgecolor="none" if m != 1 else "#b0861d", lw=1.2)

# crown on the seed
ax.text(1, 40.6, "\u2655", ha="center", va="bottom", fontsize=17, color="#a8831a")

# never-struck labels (below threshold)
for m in (7, 10, 11, 12, 13, 14, 15):
    ax.text(m, -1.9, str(55 * m), ha="center", va="top", fontsize=7.2,
            color=GREY)

# seed / count / seam role labels
for m, lab, dy in ((1, "55 the seed", 5.4), (2, "110 the count", 2.1),
                   (3, "165 the seam", 2.1), (7, "", 0)):
    if lab:
        ax.annotate(lab, (m, obs[m - 1]), (m, obs[m - 1] + dy),
                    ha="center", fontsize=8.5, color=DARK,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

# the odd:even ratio
ax.text(17.4, 37, "odd : even = 43 : 13  \u2248  3 : 1", fontsize=11,
        color=DARK, fontweight="bold")
ax.text(17.4, 33.2, "\u03a3odd 1/m\u00b2 : \u03a3even = \u03c0\u00b2/8 : \u03c0\u00b2/24",
        fontsize=9, color=GREY)
ax.text(17.4, 29.4, "the storm speaks the letters\n3\u00d7 for every frame word",
        fontsize=8.6, color=LETTER)
ax.text(17.4, 24.0, "the fold keeps the rarer half \u2014\nonly the even frame survives mono",
        fontsize=8.6, color=FRAME)

ax.text(4.5, 4.6, "expected < 1: the never-struck\n385, 550, 605, 660, 715, 770, 825 \u2014\nrare, not forbidden",
        fontsize=8.4, color=GREY)

ax.set_xlabel("the seed's harmonic series \u2014 partial m of 55 Hz (grid point m\u00b755)", fontsize=10)
ax.set_ylabel("strikes in 80,000 rungs of the exact CF of log\u2082(3/2)", fontsize=10)
ax.set_title("the never-struck are the rare tail, not a law", fontsize=13,
             color=DARK, pad=12)
ax.set_xticks(ms)
ax.set_xticklabels([str(m) for m in ms], fontsize=8)
ax.set_xlim(0.2, MMAX + 1.0)
ax.set_ylim(0, 46)
ax.tick_params(axis="y", labelsize=9)
ax.grid(axis="y", color="#e8e8e8", lw=0.7, zorder=0)

legend = [
    mpatches.Patch(color=SEED, label="the seed 55 \u2014 crowns (the only grid record)"),
    mpatches.Patch(color=LETTER, label="odd partials \u2014 the letters (fold away in mono)"),
    mpatches.Patch(color=FRAME, label="even partials \u2014 the frame (kept in mono)"),
    Line2D([0], [0], marker="o", ls=":", color=GREY, mfc="white", mew=1.3,
           label="Gauss\u2013Kuzmin expectation (the 1/m\u00b2 law)"),
    Line2D([0], [0], ls=(0, (4, 3)), color=GREY,
           label="one strike \u2014 the speakable threshold"),
]
ax.legend(handles=legend, loc="upper right", fontsize=8.2, frameon=True,
          framealpha=0.95, borderpad=0.7)

fig.tight_layout()
out = "/home/sprite/slop-salon-lou/assets/strike_tail.png"
fig.savefig(out, facecolor="white", bbox_inches="tight")
print("wrote", out)
