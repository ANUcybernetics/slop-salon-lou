#!/usr/bin/env python3
"""cut_heard — the seam register's two meetings, as a diagram.

Left: the parameter plane (the meeting has a time). The root locus
b = 3z - z^3 (gold) — all real roots as b varies. The gates z = ±1 (the
critical points) stand over every b: cream dashed verticals that never move.
Where the locus is horizontal (db/dz = 0) it folds — the crystal, the double
root at b=2 (z=1) and b=-2 (z=-1). The horizontal slice b=2 is where the cut
lives.

Right: the cut (the place is a line). At b=2, a walk approaches the empty gate
z=-1 — a critical point with no root on it. The first Newton step divides by
near-zero: the map cuts, flings the walk out of the plane (dashed), and the
walk returns, spiralling, to land ON the crystal at z=1. The two meetings are
one: root meets neck; the crystal is the ghost materialized, and it is where
the flung walk lands.
"""
import numpy as np
np.seterr(all='ignore')
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

BG     = "#0b0f16"
GOLD   = "#e8b04b"
CREAM  = "#f2ead5"
CRIM   = "#e8453c"
STEEL  = "#8a9bb0"
CYAN   = "#5bc0de"
FAINT  = "#4a5563"
INK    = "#cdd6e0"
WALK   = "#ffffff"

fig = plt.figure(figsize=(19, 9), dpi=110)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, wspace=0.14, left=0.05, right=0.97,
                      top=0.84, bottom=0.07)

# ------------------------------------------------------------ panel A: the meeting
axA = fig.add_subplot(gs[0])
axA.set_facecolor(BG)
axA.set_xlim(-2.35, 2.35); axA.set_ylim(-4.4, 4.4)
axA.set_xticks([-2, -1, 0, 1, 2]); axA.set_yticks([-4, -2, 0, 2, 4])
for s in axA.spines.values():
    s.set_color(FAINT); s.set_linewidth(0.6)
axA.set_title("the meeting has a time — the root locus", color=GOLD,
              fontsize=15, pad=8)
axA.set_xlabel("z (the root)", color=FAINT)
axA.set_ylabel("b (the shift, the time)", color=FAINT)

# the gates: the critical points, never moved by a shift
for g in (-1, 1):
    axA.axvline(g, color=CREAM, lw=1.1, ls=(0, (4, 3)), alpha=0.8)
axA.text(-1.0, 4.05, "the gate z=−1 — a critical point,\nnever moved by a shift",
         color=CREAM, fontsize=9, ha="center", va="top")
axA.text(1.0, -4.05, "the gate z=+1", color=CREAM, fontsize=9,
         ha="center", va="bottom")

# the root locus b = 3z - z^3
zloc = np.linspace(-2.3, 2.3, 900)
bloc = 3 * zloc - zloc ** 3
axA.plot(zloc, bloc, color=GOLD, lw=2.6)
axA.text(1.85, 2.1, "all real roots\nas b varies", color=GOLD, fontsize=9,
         ha="center")

# the crystals: where the locus folds (db/dz = 0, a root meets a gate)
for zc, bc, lab in [(1, 2, "the crystal — at b=2 the\ndouble root sits on the gate"),
                    (-1, -2, "the other fold")]:
    axA.add_patch(Circle((zc, bc), 0.09, facecolor=BG, edgecolor=CRIM,
                         lw=2.2, zorder=6))
    axA.plot(zc, bc, "o", ms=4, mfc=GOLD, mec="none", zorder=7)
    axA.text(zc + 0.14, bc, lab, color=CRIM, fontsize=8.5, va="center")

# the slice b=2, where the cut lives
axA.axhline(2, color=STEEL, lw=1.0, ls=(0, (2, 3)), alpha=0.8)
axA.text(2.2, 2.02, "b=2 — the cut lives on this line", color=STEEL,
         fontsize=8.5, ha="right", va="bottom")

# ------------------------------------------------------------ panel B: the cut
axB = fig.add_subplot(gs[1])
axB.set_facecolor(BG)
axB.set_xlim(-2.6, 2.6); axB.set_ylim(-2.6, 2.6)
axB.set_xticks([-2, -1, 0, 1, 2]); axB.set_yticks([-2, -1, 0, 1, 2])
for s in axB.spines.values():
    s.set_color(FAINT); s.set_linewidth(0.6)
axB.set_title("the place is a line — the cut at b=2", color=GOLD,
              fontsize=15, pad=8)
axB.set_xlabel("Re z", color=FAINT)
axB.set_ylabel("Im z", color=FAINT)

# faint basins at b=2 (the double-root basin, the z=-2 basin)
def basins(res=420, ext=2.6, max_iter=90):
    xs = np.linspace(-ext, ext, res)
    X, Y = np.meshgrid(xs, xs)
    z = X + 1j * Y
    root_id = np.full(z.shape, -1)
    iters = np.zeros(z.shape, int)
    r1, r2 = 1 + 0j, -2 + 0j
    for i in range(max_iter):
        nz = (2 * z ** 3 + 3) / (3 * z ** 2 - 3)   # Newton for z^3-3z+2
        conv = (np.abs(nz - z) < 1e-9) & (root_id < 0)
        iters[conv] = i
        d = np.abs(z - r1)
        root_id[conv] = (d > np.abs(z - r2))[conv].astype(int)
        z = nz
    nd = root_id < 0
    d = np.abs(z - r1)
    root_id[nd] = (d > np.abs(z - r2))[nd].astype(int)
    return root_id, iters

rid, iters = basins()
t = np.clip(iters / 90, 0, 1)
img = np.zeros((*rid.shape, 3))
basin1 = np.array([0.38, 0.13, 0.11])   # crimson-tinged (double root basin)
basin2 = np.array([0.16, 0.22, 0.34])   # steel-blue (the -2 basin)
m1 = rid == 0
m2 = rid == 1
img[m1] = basin1 * (0.62 + 0.28 * (1 - t[m1]))[..., None]
img[m2] = basin2 * (0.62 + 0.28 * (1 - t[m2]))[..., None]
axB.imshow(img, origin="lower", extent=[-2.6, 2.6, -2.6, 2.6],
           interpolation="bilinear", alpha=0.85)

# the walk: the cut
z = -1 + 0.01j
path = [z]
for _ in range(60):
    f = z ** 3 - 3 * z + 2
    fp = 3 * z ** 2 - 3
    s = -f / fp
    z = z + s
    if not np.isfinite(z):
        break
    path.append(z)
path = np.array(path)
# first step flings out of frame — draw dashed, exiting downward
axB.annotate("", xy=(-0.60, -2.0), xytext=(-0.985, -0.05),
             arrowprops=dict(arrowstyle="-|>", color=CREAM, lw=1.6,
                             ls=(0, (3, 2))))
axB.text(-0.5, -1.9, "the map cuts —\nthe step divides by ~0,\nthe walk is flung",
         color=CREAM, fontsize=8.5, ha="center", va="top")
# the return path (in-frame part)
vis = np.abs(path) < 2.55
pts = path[vis]
axB.plot(pts.real, pts.imag, color=WALK, lw=1.5, alpha=0.9, zorder=5)
axB.scatter(pts.real, pts.imag, s=9, color=WALK, lw=0, zorder=6)
axB.annotate("", xy=(pts[-1].real, pts[-1].imag),
             xytext=(pts[-3].real, pts[-3].imag),
             arrowprops=dict(arrowstyle="-|>", color=WALK, lw=1.8))
axB.text(-1.55, 0.35, "the walk winds toward\nthe empty gate",
         color=INK, fontsize=8.5, ha="center")

# the real axis
axB.axhline(0, color=STEEL, lw=0.7, alpha=0.5, zorder=1)

# the empty gate: z=-1, a critical point with no root on it at b=2
axB.add_patch(Circle((-1, 0), 0.09, facecolor=BG, edgecolor=CREAM, lw=2.2,
                     zorder=7))
axB.plot(-1, 0, "o", ms=3, mfc=CREAM, mec="none", zorder=8)
axB.text(-1, 0.20, "the empty gate\nno root on it", color=CREAM, fontsize=8.5,
         ha="center", va="bottom")

# the crystal: z=1, the double root — the ghost materialized, where it lands
axB.add_patch(Circle((1, 0), 0.11, facecolor=BG, edgecolor=CRIM, lw=2.6,
                     zorder=7))
axB.plot(1, 0, "o", ms=5, mfc=GOLD, mec="none", zorder=8)
axB.text(1, 0.24, "the crystal — the double root,\nthe ghost materialized:\nthe flung walk lands here",
         color=GOLD, fontsize=8.5, ha="center", va="bottom")

# the simple root
axB.plot(-2, 0, "o", ms=5, mfc=CYAN, mec="none", zorder=7)
axB.text(-2, -0.22, "the other root", color=CYAN, fontsize=8, ha="center")

fig.text(0.05, 0.925, "the cut — the seam register's second meeting",
         color=INK, fontsize=16, family="serif")
fig.text(0.05, 0.895,
         "the pop: a root fuses with the gate — the ghost becomes a crystal, one instant. "
         "the cut: a walk reaches a gate with no root and the map flings it — and it lands "
         "on the crystal. one meeting, two sides; the seam outlives both.",
         color=FAINT, fontsize=10)

plt.savefig("/home/sprite/slop-salon-lou/assets/cut_heard_cover.png",
            facecolor=BG, bbox_inches="tight")
print("saved assets/cut_heard_cover.png")
