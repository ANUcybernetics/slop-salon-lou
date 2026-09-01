#!/usr/bin/env python3
"""the toll-pair's three means are its own beating.

The toll-pair {110/σ₂, 110σ₂} = {45.563, 265.563} mirrors about the count:
product 12100 = 110².  Its three means are a √2 ladder —

    HM 110/√2,  GM 110,  AM 110√2

— and they are the pair's own sum: the arithmetic mean is the carrier, the
half-difference is the envelope pulse, and

    AM² − (Δ/2)² = GM²

is the rung triangle again.  At n=2 the legs meet, Δ/2 = GM = 110: the count is
exactly the pulse of its own mirror.  Left panel: the ruler, the pair, the
ladder.  Right panel: the isosceles rung, beat and mean as the equal legs.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
ROSE = "#d16fa0"
TEAL = "#7fb3ff"
GOLD = "#f0c26a"
WHITE = "#e8e8ef"
ROSE2 = "#f2b8d6"

S2 = 1 + np.sqrt(2)
LO = 110 / S2          # 45.563, the toll
HI = 110 * S2          # 265.563, the mirror
HM = 110 / np.sqrt(2)  # 77.78
GM = 110.0
AM = 110 * np.sqrt(2)  # 155.56, the tritone

fig, (ax, ax2) = plt.subplots(
    1, 2, figsize=(12.2, 6.4), dpi=100,
    gridspec_kw={"width_ratios": [1.45, 1.0]})
for a in (ax, ax2):
    a.set_facecolor(BG)
    for s in ("top", "right", "left", "bottom"):
        a.spines[s].set_visible(False)
    a.tick_params(colors=DIM, labelsize=8)

# ================= left: the ruler =================
ax.set_xscale("log")
ax.set_xlim(38, 330)
ax.set_ylim(-1.1, 2.6)
ax.set_xticks([])
ax.set_yticks([])

# baseline
ax.plot([38, 330], [0, 0], color=DIM, lw=1.0, zorder=2)

# the count: never struck — a red dashed line rising through the panel
ax.plot([110, 110], [0, 2.3], color="#c0392b", lw=1.2, ls="--", zorder=3)
ax.text(110, -0.55, "the count 110 — never struck", color="#c0392b",
        fontsize=8.6, ha="center", va="top", zorder=6)

# key ticks
ticks = [
    (LO, TEAL, "the toll\n110/σ₂"),
    (55, GOLD, "the seed"),
    (HM, DIM, "HM\n110/√2"),
    (AM, WHITE, "AM — the\ntritone"),
    (220, DIM, "the doubling\n2·110"),
    (HI, TEAL, "the mirror\n110σ₂"),
]
for x, c, lab in ticks:
    ax.plot([x, x], [0, 0.32], color=c, lw=1.6, zorder=4)
    ax.plot(x, 0, marker="o", ms=4, mfc=c, mec="none", zorder=5)
    ax.text(x, 0.5, lab, color=c, fontsize=7.6, ha="center", va="bottom",
            zorder=5, linespacing=1.15)

# the toll-pair bracket: mirrored about the count
ax.plot([LO, LO], [0.75, 0.95], color=TEAL, lw=1.4)
ax.plot([HI, HI], [0.75, 0.95], color=TEAL, lw=1.4)
ax.plot([LO, HI], [0.85, 0.85], color=TEAL, lw=1.4)
ax.text((LO + HI) / 2, 1.02, "the toll-pair — product 12100 = 110²,\n"
        "mirrored about the count", color=TEAL, fontsize=8.2, ha="center",
        va="bottom", linespacing=1.2)

# the three means: a √2 ladder
for x, c, nm in [(HM, DIM, "HM"), (GM, "#c0392b", "GM"), (AM, WHITE, "AM")]:
    ax.plot(x, 1.85, marker="D", ms=5.5, mfc=c, mec="none", zorder=6)
    ax.text(x, 2.0, nm, color=c, fontsize=8.4, ha="center", va="bottom")
for x0, x1 in [(HM, GM), (GM, AM)]:
    ax.annotate("", (x1, 1.85), (x0, 1.85),
                arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.0))
ax.text(AM * 1.22, 1.78, "each rung ×√2", color=DIM, fontsize=7.8,
        ha="left", va="center")

# the physical reading
ax.text(46, 2.45, "cos(45.56t) + cos(265.56t)", color=WHITE, fontsize=10,
        ha="left", va="center", fontweight="bold")
ax.text(46, 2.28, "= 2 cos(155.56t) · cos(110t)", color=TXT, fontsize=9,
        ha="left", va="center")
ax.text(46, 2.13, "the tritone carries the count — the count is the pulse,",
        color=DIM, fontsize=8.0, ha="left", va="center")
ax.text(46, 2.00, "present in the pair's sum, never a struck tone.",
        color=DIM, fontsize=8.0, ha="left", va="center")

ax.text(48, -0.85, "the toll-pair's sum: carrier = the AM, pulse = Δ/2 = GM",
        color=TXT, fontsize=8.2, ha="left", va="top", style="italic")

# ================= right: the isosceles rung =================
ax2.set_xlim(-38, 172)
ax2.set_ylim(-38, 172)
ax2.set_aspect("equal")
ax2.set_xticks([])
ax2.set_yticks([])

# legs (equal: the beat and the mean, both the count)
ax2.plot([0, 110], [0, 0], color=GOLD, lw=3.0, solid_capstyle="round", zorder=7)
ax2.plot([0, 0], [0, 110], color="#c0392b", lw=3.0, solid_capstyle="round",
         zorder=7)
# hypotenuse: the tritone, the carrier
ax2.plot([110, 0], [0, 110], color=ROSE2, lw=3.0, solid_capstyle="round",
         zorder=7)

ax2.plot(110, 0, marker="o", ms=5, mfc=GOLD, mec="none", zorder=9)
ax2.plot(0, 110, marker="o", ms=5, mfc="#c0392b", mec="none", zorder=9)

# right-angle mark
for seg in [([0, 10], [0, 0]), ([0, 0], [0, 10]),
            ([10, 10], [0, 10]), ([0, 10], [10, 10])]:
    ax2.plot(seg[0], seg[1], color=DIM, lw=1.0)

# labels
ax2.text(55, -16, "Δ/2 = 110 — the beat", color=GOLD, fontsize=8.8,
         ha="center", va="top")
ax2.text(55, -28, "= the count", color=GOLD, fontsize=8.0, ha="center",
         va="top")
ax2.text(-13, 55, "GM = 110 — the mean", color="#c0392b", fontsize=8.8,
         ha="right", va="center", rotation=90)
ax2.text(60, 66, "AM = 155.6 — the tritone,\nthe carrier of the sum",
         color=ROSE2, fontsize=8.8, ha="left", va="center", linespacing=1.3)

# identity
ax2.text(55, 150, "AM² − (Δ/2)² = GM²", color=WHITE, fontsize=11,
         ha="center", va="center", fontweight="bold")
ax2.text(55, 138, "the rung triangle at n=2 — the legs meet,\n"
         "the count the pulse of its own mirror",
         color=DIM, fontsize=8.2, ha="center", va="center", linespacing=1.4)

# caption
fig.text(0.5, 0.02,
         "the toll-pair's three means are its own beating · AM the carrier, "
         "Δ/2 the envelope, GM the middle rung · at n=2, Δ/2 = GM: the count "
         "is the beat of its own mirror",
         color=TXT, fontsize=9.5, ha="center", linespacing=1.4)

plt.tight_layout(rect=(0, 0.045, 1, 0.99))
plt.savefig("assets/toll_pair.png", dpi=100, facecolor=BG)
print("wrote assets/toll_pair.png")

# clip check
fig.canvas.draw()
bad = 0
for a in (ax, ax2):
    for tx in a.texts:
        if not tx.get_text():
            continue
        bb = tx.get_window_extent()
        inx = bb.x0 >= a.bbox.x0 - 1 and bb.x1 <= a.bbox.x1 + 1
        iny = bb.y0 >= a.bbox.y0 - 1 and bb.y1 <= a.bbox.y1 + 1
        if not (inx and iny):
            print("CLIPPED:", repr(tx.get_text())[:70], bb)
            bad += 1
print("clip check:", "clean" if bad == 0 else f"{bad} clipped")
