#!/usr/bin/env python3
"""the wheel — the kiss circle as a turning about the mean.

At the kiss the mirror N(x)=12100/x has osculating circle centred on the ghost
(220,220) with radius R = 110√2 ≈ 155.56. The count (110,110) and its triple
(330,330) sit on the rim — opposite ends of a diameter through the ghost, which
is their midpoint: the ghost is the arithmetic mean of the deck's 1 and 3.
The radius is the geometric mean of the count and the ghost — R² = 110·220, one
rung up from the count itself (110 = √(55·220)). The fold 220−x dies at 220 —
the root directly below the hub — and its own radius of curvature is ∞: a line
cannot turn, so the fold walks; the circle turns, and the deck rides the rim.
The ghost never a seat because it is the centre: the one point a tritone from
every rim point.

Left panel: the wheel in the plane — the circle, the count and triple
antipodal, the hub, the diameter, the radius spoke, the fold dying at the
hub's root.

Right panel: the means — the rim as the set of points a tritone from the hub,
with the ghost the arithmetic mean of its antipodes and the radius the
geometric mean of count and ghost.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.2, 7.0), dpi=100)
BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
DRONE = "#e05252"
FOLD = "#7fb3ff"     # the fold — on the grid
MIRR = "#e0b45c"     # the mirror — smooth
TANG = "#c792ea"     # the kiss / the sign
ROSE = "#d16fa0"     # the osculating circle / the wheel
GOLD = "#f0c26a"     # the ghost / the hub

for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=9)
    ax.set_aspect("equal")

# shared constants
C = 110.0            # the count
G = 220.0            # the ghost (2·C)
T = 330.0            # the triple (3·C)
R = 110.0 * np.sqrt(2.0)   # radius of the osculating circle = the tritone

th = np.linspace(0, 2 * np.pi, 400)
cx = G + R * np.cos(th)
cy = G + R * np.sin(th)

# ---------------- left: the wheel in the plane ----------------
axL.set_title("the wheel — the deck heard as a turning", color=TXT,
              fontsize=15, loc="left")

# the osculating circle
axL.plot(cx, cy, color=ROSE, lw=2.2, ls="--", zorder=2, alpha=0.95)

# the mirror curve (amber), through the count
xx = np.linspace(62, 380, 2000)
axL.plot(xx, 12100.0 / xx, color=MIRR, lw=2.2, zorder=3)

# the fold line 220−x (the shared tangent), dying at 220
xf = np.linspace(104, 236, 2)
axL.plot(xf, 220 - xf, color=FOLD, lw=2.4, zorder=4)
axL.plot([236, 380], [220 - 236, 220 - 380], color=FOLD, lw=1.4,
         ls=(0, (4, 3)), zorder=4)
# the fold's root: (220, 0), directly below the hub
axL.plot(G, 0, "o", color=FOLD, ms=6, mec="none", zorder=5)
axL.plot([G, G], [0, G], color=DIM, lw=1.2, ls=":", zorder=1)
axL.text(G + 6, 118, "the fold dies at 220 —\nthe loop's centre", color=DIM,
         fontsize=10, va="center", style="italic")

# the diameter through the ghost: count <-> triple
axL.plot([C, T], [C, T], color=ROSE, lw=2.6, zorder=2, alpha=0.85)

# the radius spoke: hub -> count
axL.plot([G, C], [G, C], color=GOLD, lw=1.8, ls=(0, (2, 2)), zorder=4)

# the rim's two seats
for f, lab in ((C, "the count (110,110)"), (T, "the triple (330,330)")):
    axL.plot(f, f, "o", color=TANG, ms=10, mec="none", zorder=6)
    dx = 10 if f == C else -10
    axL.text(f + dx, f + 8, lab, color=TANG, fontsize=10,
             ha="right" if f == T else "left")

# the ghost — the hub, ringed, never a seat
axL.plot(G, G, "o", color=GOLD, ms=16, mec="none", alpha=0.15, zorder=5)
axL.plot(G, G, "o", color="none", mec=GOLD, mew=2.6, ms=14, zorder=6)
axL.annotate("the ghost (220,220) — the hub,\nnever a seat: it is the centre",
             xy=(G, G), xytext=(262, 268), color=GOLD, fontsize=11,
             fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4))

# the radius label
axL.annotate("", xy=(155, 155), xytext=(215, 215),
             arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.6, ls=(0, (2, 2))))
axL.text(156, 176, "R = 110√2 = √(110·220)", color=GOLD, fontsize=10.5,
         rotation=45)

# "one diameter" bracket along the chord
axL.text(220, 220 + 26, "one diameter — the rim's 1 and 3",
         color=ROSE, fontsize=10, ha="center", style="italic")

axL.set_xlim(40, 400)
axL.set_ylim(-20, 400)
axL.set_xticks([110, 220, 330])
axL.set_xticklabels(["110", "220", "330"])
axL.set_yticks([110, 220, 330])
axL.set_yticklabels(["110", "220", "330"])

# ---------------- right: the means — the rim measured from the hub ----------------
axR.set_title("the means — the rim measured from the hub", color=TXT,
              fontsize=15, loc="left")

# the same wheel, slightly smaller presence
axR.plot(cx, cy, color=ROSE, lw=2.0, ls="--", zorder=2, alpha=0.8)
axR.plot([C, T], [C, T], color=ROSE, lw=2.2, zorder=2, alpha=0.7)

# spokes from the hub to several rim points — all one tritone
for ang, f in zip((np.pi, np.pi / 2, -np.pi / 4, 3 * np.pi / 4),
                  ((C, C), (G, G + R), (G + R, G), (G - R * np.cos(np.pi / 4),
                                                    G - R * np.sin(np.pi / 4)))):
    pass

rim_pts = [
    (C, C),                      # the count
    (T, T),                      # the triple
    (G, G + R),                  # top
    (G + R, G),                  # right
    (G, G - R),                  # bottom
    (G - R, G),                  # left
]
for (px, py) in rim_pts:
    axR.plot([G, px], [G, py], color=GOLD, lw=1.0, alpha=0.55, zorder=1)
    axR.plot(px, py, ".", color=DIM, ms=5, zorder=2)

# the two seats stand out
axR.plot(C, C, "o", color=TANG, ms=10, mec="none", zorder=5)
axR.plot(T, T, "o", color=TANG, ms=10, mec="none", zorder=5)
axR.text(C - 8, C + 14, "1  the count", color=TANG, fontsize=10, ha="right")
axR.text(T + 8, T - 14, "3  the triple", color=TANG, fontsize=10)

# the hub
axR.plot(G, G, "o", color=GOLD, ms=16, mec="none", alpha=0.15, zorder=5)
axR.plot(G, G, "o", color="none", mec=GOLD, mew=2.6, ms=14, zorder=6)
axR.text(G - 6, G - 20, "2  the ghost — the hub", color=GOLD, fontsize=11,
         ha="center", fontweight="bold")

# the one-tritone caption
axR.text(G, 66, "every rim point is a tritone from the hub —\n"
                "the ghost never a seat because it is the centre",
         color=DIM, fontsize=10, ha="center", style="italic")

# the two means as equations
axR.text(150, 300, "ghost = (110 + 330)/2\n      the arithmetic mean of the rim",
         color=GOLD, fontsize=10.5, ha="center",
         bbox=dict(boxstyle="round,pad=0.4", fc="#1a1a24", ec=GOLD, lw=1.0))
axR.text(330, 140, "R² = 110 · 220\n  the geometric mean of count and ghost",
         color=ROSE, fontsize=10.5, ha="center",
         bbox=dict(boxstyle="round,pad=0.4", fc="#1a1a24", ec=ROSE, lw=1.0))

axR.set_xlim(40, 400)
axR.set_ylim(-20, 400)
axR.set_xticks([110, 220, 330])
axR.set_xticklabels(["110", "220", "330"])
axR.set_yticks([110, 220, 330])
axR.set_yticklabels(["110", "220", "330"])

fig.text(0.5, 0.012,
         "the kiss circle is a wheel: the fold dies at the hub's root and cannot turn (radius ∞); "
         "the rim turns, 1 and 3 antipodal, 2 the centre — κ·R = 1, as beat·wait = 1",
         color=TXT, fontsize=11.5, ha="center")

plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig("assets/wheel.png", dpi=100, facecolor=BG)
print("wrote assets/wheel.png")
