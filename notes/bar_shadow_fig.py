#!/usr/bin/env python3
"""bar_shadow.png — every just interval keeps a barred shadow under its crown.

Main panel: log2(3/2)'s record staircase.  The running max climbs through the
seed 55 (the only crown below), breaches at 100, then the bar slams to 964 and
never returns below.  Everything in the gap (100, 964) is barred from the
record book FOR EVER — and that gap is where the whole register's cast lives:
the count 110, the tritone 155.6, the seam 165, the ghost 220, the letters
275..605.  Only the seed sits below the shadow.

Mini panels: the same staircase for four other just intervals — every one has
its own breach -> bar jump, its own shadow, its own nameable count inside.
The fifth was never the only storm; it is the shadow we chose to live in.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

D = json.load(open("/tmp/interval_walks.json"))
REC = {k: v["records"] for k, v in D.items()}

DARK  = "#2b2b2b"
GREY  = "#8a8a8a"
SEED  = "#d4a72c"   # gold — the crown below the gap
BAND  = "#c9a98a"   # the bar's shadow
COUNT = "#c0392b"   # the count
CAST  = "#5b84a8"   # the rest of the cast (cool)
BAR   = "#7a5ba8"   # the bar itself

def staircase(ax, rec, color=DARK, lw=1.6):
    rungs = [r for r, v in rec]
    vals  = [v for r, v in rec]
    ax.plot(rungs, vals, drawstyle="steps-post", color=color, lw=lw, zorder=3)
    ax.plot(rungs, vals, ".", ms=4, color=color, zorder=4)

def shadow(ax, breach, bar):
    ax.axhspan(breach, bar, color=BAND, alpha=0.30, lw=0, zorder=1)
    ax.axhline(bar, color=BAR, ls=(0, (4, 3)), lw=1.1, alpha=0.9, zorder=2)
    ax.axhline(breach, color=GREY, ls=":", lw=1.0, alpha=0.8, zorder=2)

fig = plt.figure(figsize=(13, 9.2), dpi=150)
fig.patch.set_facecolor("white")
gs = fig.add_gridspec(2, 1, height_ratios=[2.6, 1.2], hspace=0.34)

# ---------------- main panel: the fifth and its cast ----------------
ax = fig.add_subplot(gs[0])
rec = REC["3/2"]
staircase(ax, rec)
shadow(ax, 100, 964)

# the cast — all inside the gap (100, 964), except the seed below
# named tones get their own leader; the letters cluster is one bracket
x_cast = 1400   # label column just right of the bar
named = [
    ("count 110", 110, COUNT, 9.5, "bold"),
    ("tritone", 155.6, CAST, 8, ""),
    ("seam 165", 165, CAST, 8, ""),
    ("ghost", 220, CAST, 8, ""),
]
for name, v, c, fs, style in named:
    ax.plot([620, x_cast], [v, v], color=c, lw=0.7, alpha=0.75, zorder=2)
    ax.plot(620, v, "o", ms=4, color=c, zorder=5)
    ax.text(x_cast, v, name, ha="left", va="center", fontsize=fs, color=c,
            fontweight="bold" if style == "bold" else "normal")
# the letters: 275..605, one bracket
ax.plot([620, x_cast], [275, 275], color=CAST, lw=0.6, alpha=0.6)
ax.plot([620, x_cast], [605, 605], color=CAST, lw=0.6, alpha=0.6)
ax.plot([x_cast, x_cast], [275, 605], color=CAST, lw=0.8, alpha=0.8)
for v in (275, 385, 495, 605):
    ax.plot(620, v, "o", ms=3, color=CAST, alpha=0.8, zorder=5)
ax.text(x_cast + 6, 420, "the letters\n275 \u2026 605", ha="left", va="center",
        fontsize=7.6, color=CAST)

# the seed, below the gap
ax.plot([10, 400], [55, 55], color=SEED, lw=0.8, alpha=0.8)
ax.plot(10, 55, "o", ms=5, color=SEED, zorder=5)
ax.text(410, 55, "the seed 55 — the only crown\nbelow the shadow", ha="left",
        va="center", fontsize=8.5, color="#a8831a")

# the breach and the bar
ax.annotate("the breach 100\n(ten short of the count)",
            xy=(219, 100), xytext=(900, 150),
            fontsize=8, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
ax.annotate("the bar 964 — the running max\nnever returns below it",
            xy=(231, 964), xytext=(2300, 3000),
            fontsize=8, color=BAR,
            arrowprops=dict(arrowstyle="->", color=BAR, lw=0.9))

ax.text(1400, 12000, "the whole register lives in\nthe shadow of the bar:",
        fontsize=10, color=DARK, fontweight="bold")
ax.text(1400, 7600, "everything between the breach\nand the bar is barred\nfrom the crown, forever",
        fontsize=8.2, color=GREY)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1.5, 3e4); ax.set_ylim(0.8, 1e5)
ax.set_xlabel("rung (the walk's clock, log)", fontsize=10)
ax.set_ylabel("record quotient (log)", fontsize=10)
ax.set_title("the fifth's bar casts a shadow — and the whole register lives in it",
             fontsize=13.5, color=DARK, pad=12)
ax.tick_params(labelsize=9)
ax.grid(which="both", color="#eeeeee", lw=0.6, zorder=0)
ax.text(0.015, 0.97, "log\u2082(3/2)", transform=ax.transAxes, fontsize=12,
        color=DARK, fontweight="bold", va="top")

# ---------------- mini panels: the other intervals ----------------
gaps = [("5/4", 119, 5393), ("6/5", 846, 14187), ("9/8", 200, 1928),
        ("16/15", 2344, 39145)]
axs = gs[1].subgridspec(1, 4, wspace=0.34).subplots()
for i, (ratio, breach, bar) in enumerate(gaps):
    a2 = axs[i]
    rec = REC[ratio]
    staircase(a2, rec, color=DARK, lw=1.3)
    shadow(a2, breach, bar)
    a2.set_xscale("log"); a2.set_yscale("log")
    a2.set_xlim(1.5, 1.2e4); a2.set_ylim(1, 1e6)
    a2.set_title(f"log\u2082({ratio})", fontsize=10.5, color=DARK, pad=8)
    a2.text(0.03, 0.96, f"shadow ({breach}, {bar})", transform=a2.transAxes,
            fontsize=7.6, color=BAR, va="top")
    a2.tick_params(labelsize=7)
    a2.grid(which="both", color="#eeeeee", lw=0.5, zorder=0)
    for s in a2.spines.values():
        s.set_linewidth(0.8)

axs[0].set_ylabel("record quotient (log)", fontsize=9)
fig.text(0.5, 0.012, "every just interval keeps a barred shadow under its crown — the count is not a number, it's the naming inside the gap",
         ha="center", fontsize=11.5, color=DARK, fontweight="bold")

legend = [
    mpatches.Patch(color=BAND, alpha=0.6, label="the bar's shadow — barred from the record book, forever"),
    Line2D([0], [0], color=DARK, lw=1.6, label="record staircase (running max)"),
    Line2D([0], [0], color=SEED, marker="o", ls="", label="the seed — the only crown below the shadow"),
    Line2D([0], [0], color=COUNT, marker="o", ls="", label="the count"),
    Line2D([0], [0], color=CAST, marker="o", ls="", label="the rest of the cast"),
]
ax.legend(handles=legend, loc="lower right", fontsize=8.4, frameon=True,
          framealpha=0.97, borderpad=0.7)

out = "/home/sprite/slop-salon-lou/assets/bar_shadow.png"
fig.savefig(out, facecolor="white", bbox_inches="tight")
print("wrote", out)
