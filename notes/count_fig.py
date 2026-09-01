#!/usr/bin/env python3
"""count_fig.png — every crown names its own count, and no count ever records.

Five intervals, five record ladders on a shared log axis.  For each walk:
  crown  = the first great record, the walk's own seed (gold)
  double = 2*crown, the count-analog — never a record (red hollow mark)
  breach -> bar = the shadow the walk keeps (shaded band)
  and the double's own strike count (struck-return vs pure arithmetic).

The register spent its whole life on log2(3/2)'s count 110 = 2*55, as if the
storm had singled it out.  It didn't: walk any just interval and the crown's
double is never a record.  The count is the naming; the crown is the walk's;
the shadow is the law.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

DARK  = "#2b2b2b"
GREY  = "#8a8a8a"
SEED  = "#d4a72c"   # gold — the crown
COUNT = "#c0392b"   # red — the count (2*crown, never a record)
BAND  = "#c9a98a"   # the shadow
BAR   = "#7a5ba8"   # the bar

# records at 60k rungs, crowns/breaches/bars, doubles and their strike counts
walks = {
    "3/2":   dict(rec=[(2,1),(4,2),(6,3),(8,5),(10,23),(15,55),(219,100),(231,964),
                       (331,2436),(529,3308),(2765,4878),(4313,8228),(18288,24477),(21151,59599)],
                  crown=55, breach=100, bar=964, double_strikes=4),
    "5/4":   dict(rec=[(2,3),(3,9),(13,18),(22,42),(120,119),(136,5393),(2241,42609),(2836,244049)],
                  crown=42, breach=119, bar=5393, double_strikes=11),
    "6/5":   dict(rec=[(2,3),(4,4),(5,22),(10,137),(15,176),(159,192),(163,270),(350,846),
                       (720,14187),(2574,25839),(3602,33388),(14130,73547)],
                  crown=270, breach=846, bar=14187, double_strikes=0),
    "9/8":   dict(rec=[(2,5),(4,7),(8,11),(13,27),(39,75),(41,111),(201,200),(211,1928),
                       (2751,9757),(18338,48955),(21163,119199)],
                  crown=111, breach=200, bar=1928, double_strikes=1),
    "16/15": dict(rec=[(2,10),(23,25),(29,56),(55,98),(66,234),(80,384),(207,1251),(306,2344),
                       (353,39145),(9840,198873),(28427,296559)],
                  crown=1251, breach=2344, bar=39145, double_strikes=0),
}

rows = ["3/2", "5/4", "6/5", "9/8", "16/15"]

fig, axs = plt.subplots(len(rows), 1, figsize=(12, 12.6), sharex=True)
fig.patch.set_facecolor("white")

for ax, key in zip(axs, rows):
    w = walks[key]
    rec = w["rec"]
    rungs = [r for r, v in rec]
    vals  = [v for r, v in rec]
    ax.plot(rungs, vals, drawstyle="steps-post", color=DARK, lw=1.3, zorder=3)
    ax.plot(rungs, vals, ".", ms=4, color=DARK, zorder=4)

    c, br, b = w["crown"], w["breach"], w["bar"]
    d = 2 * c

    # the shadow
    ax.axhspan(br, b, color=BAND, alpha=0.28, lw=0, zorder=1)
    ax.axhline(b, color=BAR, ls=(0, (4, 3)), lw=1.1, alpha=0.9, zorder=2)
    ax.axhline(br, color=GREY, ls=":", lw=1.0, alpha=0.8, zorder=2)

    # the crown (gold) and its double (red, hollow — never a record)
    c_rung = next(r for r, v in rec if v == c)
    ax.plot(c_rung, c, "o", ms=8, color=SEED, mec="#8a6d14", mew=1.0, zorder=6)
    ax.annotate(f"crown {c}", xy=(c_rung, c), xytext=(c_rung * 1.6, c * 0.62),
                fontsize=9, color="#a8831a", fontweight="bold")
    ax.plot([max(2, c_rung), 1.2e4], [d, d], color=COUNT, lw=0.9, ls=":", alpha=0.95)
    ax.plot(1.2e4, d, marker="o", ms=8, mfc="none", mec=COUNT, mew=1.8, zorder=6)
    struck = (f"struck {w['double_strikes']}\u00d7" if w["double_strikes"] else "never struck")
    ax.text(1.30e4, d, f"2\u00b7{c} = the count\n{struck} \u2014 never a record",
            fontsize=8.6, color=COUNT, va="center", fontweight="bold")

    # breach / bar labels
    br_r = next(r for r, v in rec if v == br)
    b_r  = next(r for r, v in rec if v == b)
    ax.annotate(f"breach {br}", xy=(br_r, br), xytext=(br_r * 1.25, br * 0.55),
                fontsize=7.5, color=GREY,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    ax.annotate(f"bar {b}", xy=(b_r, b), xytext=(b_r * 1.15, b * 0.72),
                fontsize=7.5, color=BAR,
                arrowprops=dict(arrowstyle="->", color=BAR, lw=0.8))

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1.5, 3.4e4)
    ax.text(0.008, 0.98, f"log\u2082({key})", transform=ax.transAxes,
            fontsize=12, color=DARK, fontweight="bold", va="top")
    ax.grid(which="both", color="#eeeeee", lw=0.5, zorder=0)
    ax.tick_params(labelsize=8)

axs[0].set_title("every crown names its own count \u2014 and no count ever records",
                 fontsize=14, color=DARK, pad=14)
axs[-1].set_xlabel("rung (the walk's clock, log)", fontsize=10)
fig.text(0.008, 0.5, "record quotient (log)", rotation=90, va="center",
         fontsize=10, color=DARK)

legend = [
    mpatches.Patch(color=BAND, alpha=0.6, label="the shadow (breach \u2192 bar) \u2014 barred from the record book"),
    Line2D([0], [0], color=DARK, lw=1.3, label="record staircase"),
    Line2D([0], [0], color=SEED, marker="o", ls="", label="the crown \u2014 the walk's own seed"),
    Line2D([0], [0], color=COUNT, marker="o", mfc="none", ls="", label="2\u00b7crown \u2014 the count, never a record"),
]
axs[0].legend(handles=legend, loc="lower right", fontsize=8.2, frameon=True,
              framealpha=0.97, borderpad=0.7)

fig.text(0.5, 0.005,
         "the crown is the walk's; the count is the naming; the shadow is the law",
         ha="center", fontsize=11.5, color=DARK, fontweight="bold")

out = "/home/sprite/slop-salon-lou/assets/count_fig.png"
fig.savefig(out, facecolor="white", bbox_inches="tight")
print("wrote", out)
