#!/usr/bin/env python3
"""the grid's one crown — strike table for the seed's grid in 80,000 rungs.

Only the seed (55) ever leads: it is the one multiple of 55 that becomes a
record.  Every higher rung of the grid — count 110, seam 165, ghost 220,
the residue 385 — is struck late or not at all, and never a record: the bar
(964 @ rung 231) closes the window, and all their strikes come after.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

with open("/tmp/grid_strikes.json") as f:
    D = json.load(f)
mult = {int(k): v for k, v in D["mult55"].items()}
records = {int(k): v for k, v in D["records"].items()}
N = D["N"]

from math import log2 as mlog2


def gk(k):
    return N * (mlog2(1 + 1.0 / (k * (k + 2))))


fig, ax = plt.subplots(figsize=(11.5, 6.6), facecolor="#0a0d14")
ax.set_facecolor("#0a0d14")

ms = list(range(1, 17))
vals = [55 * m for m in ms]
strikes = [len(mult.get(v, [])) for v in vals]
gkexp = [gk(v) for v in vals]

x = np.arange(len(ms))
colors = []
for v, s in zip(vals, strikes):
    if v == 55:
        colors.append("#f6c45a")          # the crown — gold
    elif v == 165:
        colors.append("#7aaad2")          # the seam — cool, the one landing
    else:
        colors.append("#3c4a60")          # the rest of the grid — mute
bars = ax.bar(x, strikes, color=colors, width=0.72, zorder=3)
bars[0].set_edgecolor("#f6c45a"); bars[0].set_linewidth(1.5)
bars[1].set_edgecolor("#c8a84c")
bars[2].set_edgecolor("#a9d0ef"); bars[2].set_linewidth(1.5)

# GK expected: faint dashed ticks
ax.scatter(x, gkexp, marker="_", s=300, linewidths=1.2, color="#5a6a80",
           label="Gauss–Kuzmin expected", zorder=4)

# annotations
ax.text(0, strikes[0] + 1.6, "40\n— the crown", color="#f6c45a", ha="center",
        fontsize=10, fontweight="bold")
ax.text(2, strikes[2] + 1.6, "1\n— once", color="#a9d0ef", ha="center",
        fontsize=10, fontweight="bold")
ax.text(1, strikes[1] + 0.6, "5", color="#c8a84c", ha="center", fontsize=9)
for i in [3, 4, 5, 7, 8, 9, 15]:
    if strikes[i] > 0:
        ax.text(i, strikes[i] + 0.3, str(strikes[i]), color="#7a8aa0", ha="center", fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels([f"55·{m}" if m in (1, 2, 3, 7) else f"{v}" for m, v in zip(ms, vals)],
                   color="#b0b8c8", fontsize=8)
ax.tick_params(axis="y", colors="#b0b8c8", labelsize=8)
ax.set_ylabel("strikes in 80,000 rungs", color="#b0b8c8", fontsize=10)
ax.set_ylim(0, max(strikes) * 1.18)
ax.yaxis.grid(color="#1c2434", linewidth=0.8, zorder=0)

# the bar: a horizontal dashed line at the record level, marking the cutoff
ax.axhline(0, color="#f6c45a", linewidth=1.2, alpha=0.9)
# annotate the record cutoff with an arrow
ax.annotate("the bar — 964 @ rung 231\ncloses the record book",
            xy=(1, 0.0), xytext=(4.2, strikes[0] * 0.55),
            color="#8a92b0", fontsize=9, ha="left",
            arrowprops=dict(arrowstyle="->", color="#8a92b0", lw=1.2))

ax.set_title("the grid's one crown — only the seed ever leads",
             color="#d8dce8", fontsize=13, pad=12)
ax.legend(loc="upper right", fontsize=8, facecolor="#0a0d14", edgecolor="#3c4a60",
          labelcolor="#b0b8c8")

fig.text(0.02, 0.02, "struck exactly once: 165 @ rung 27,378 · never struck in 80k: 385, 550, 605, …",
         color="#5a6a80", fontsize=8)
fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-lou/assets/once_fig.png", dpi=170)
print("wrote assets/once_fig.png")
