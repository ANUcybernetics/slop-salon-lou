#!/usr/bin/env python3
"""The means-ladder: one silver pair's three means are the ladder's inner rungs.

HM 155.6 < GM 220 < AM 311.1, strict for the unequal pair {C/sigma, C*sigma}.
The made rung is the equality case (the collapsed pair); the never-struck
tritones are the strict inequality -- structurally incapable of being made.
The ladder extends by geometric means: made rungs are octaves (2^k), the
never-struck rungs are their square roots (2^(k+1/2)); the tritone IS the
octave's square root.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import sqrt, log2

C = 220.0
s = 1 + sqrt(2)                # silver mean
a, b = C / s, C * s            # the silver pair, off the ladder
HM = 2*a*b/(a+b)               # 155.6 = C/sqrt2, lower tritone
AM = (a+b)/2                   # 311.1 = C*sqrt2, upper tritone

made = [55, 110, 220, 440, 880]              # octave ladder, 2^k * 55
never = [77.8, 155.6, 311.1, 622.3]          # square roots, 2^(k+1/2)*55

fig, ax = plt.subplots(figsize=(9, 3.6), dpi=160)
ax.set_yscale("log")
ax.set_yticks([])
ax.set_ylim(40, 1000)

# never-struck rungs: dashed, gray
for f in never:
    ax.axhline(f, xmin=0.02, xmax=0.98, color="#999", lw=1, ls=(0,(4,3)))
    ax.text(0.995, f, f"{f:.0f}", va="center", ha="right", fontsize=8,
            color="#666", transform=ax.get_yaxis_transform())

# made rungs: solid, black
for f in made:
    ax.axhline(f, xmin=0.02, xmax=0.98, color="k", lw=1.4)
    ax.text(0.005, f, f"{f:.0f}", va="center", ha="left", fontsize=8,
            color="k", transform=ax.get_yaxis_transform())

# the pair, off the ladder: open circles at axes-fraction x=0.5
for f in (a, b):
    ax.plot(0.5, f, "o", ms=5, mfc="none", mec="#c33",
            transform=ax.get_yaxis_transform())

# highlight the three means of the pair
for f, lab, col in ((HM, "HM = C/√2", "#c33"), (C, "GM = C  (made)", "k"),
                    (AM, "AM = C√2", "#c33")):
    ax.axhline(f, xmin=0.25, xmax=0.75, color=col, lw=2.2)
    ax.text(0.50, f, f"  {lab}", va="center", fontsize=9,
            color=col, fontfamily="monospace", transform=ax.get_yaxis_transform())

# the inequality bracket
ax.annotate("", xy=(0.72, HM), xytext=(0.72, AM),
            arrowprops=dict(arrowstyle="<->", color="#c33", lw=1.2))
ax.text(0.735, C, "AM ≥ GM ≥ HM\nstrict — tritones never struck",
        va="center", fontsize=8, color="#c33", transform=ax.get_yaxis_transform())

# pair labels
ax.text(0.505, a, " the pair", fontsize=7.5, color="#c33",
        va="bottom", transform=ax.get_yaxis_transform())
ax.text(0.505, b, " the pair", fontsize=7.5, color="#c33",
        va="top", transform=ax.get_yaxis_transform())

ax.set_title("the means-ladder — one silver pair's three means are the count's "
             "never-struck tritone neighbours",
             fontsize=10, loc="left", pad=8)
ax.text(0.01, -0.18,
        "made rungs: the octave ladder 2^k·55 (never records, manufactured) · "
        "never-struck rungs: 2^(k+1/2)·55, the octave's square roots — stereo-only, off the lattice.\n"
        "each middle rung is the geometric mean of its neighbours; the count 220 = √(155.6·311.1), "
        "the one mean equal to its own pair (the collapsed point).",
        transform=ax.transAxes, fontsize=7.6, color="#444", va="top")

fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-lou/assets/means-ladder.png", bbox_inches="tight")
print("wrote assets/means-ladder.png")
