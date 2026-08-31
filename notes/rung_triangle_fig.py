#!/usr/bin/env python3
"""rung's triangle — the ear's operator as lengths.

The metallic ladder's n-th rung is the reciprocal pair {55/σ_n, 55σ_n},
σ_n = (n+√(n²+4))/2.  Its two combination products — the difference tone and
the summation tone — are the two components of the ear's operator
M(a,b)=(b−a,b+a):

    M(55/σ_n, 55σ_n) = (55n, 55√(n²+4))   = (dispersion, trace).

And they obey a right-triangle identity with a CONSTANT leg:

    (55n)² + 110² = (55√(n²+4))²,   i.e.  n² + 2² = (√(n²+4))².

The constant leg 2 (=110 Hz) is the doubling — M² = 2I, the operator's square.
Every rung stands on it.  At n=2 the dispersion leg equals the doubling leg:
isosceles, hypotenuse 110√2, the tritone — the operator's own scale (M/√2's
eigenvalue).  At n=0 the dispersion is zero: the seam, the drone.
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

BASE = 55.0
LEG = 2 * BASE  # 110, the doubling / the count / the constant leg


def sigma(n):
    return (n + np.sqrt(n * n + 4)) / 2.0


fig, ax = plt.subplots(figsize=(12.2, 7.0), dpi=100)
ax.set_facecolor(BG)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=DIM, labelsize=9)

ax.set_xlim(-14, 358)
ax.set_ylim(-34, 176)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])

# ---- the shared constant leg: the doubling 110 (M² = 2I) ----
ax.plot([0, 0], [0, LEG], color=TEAL, lw=3.0, zorder=7, solid_capstyle="round")
ax.text(5, LEG / 2, "the doubling — 110, the count, the constant leg (M²=2I)",
        color=TEAL, fontsize=9, ha="left", va="center", rotation=90)

N = 6

# ---- the seam, n=0 ----
ax.plot(0, LEG, marker="o", ms=8, mfc="none", mec=WHITE, mew=1.8, zorder=9)
ax.text(10, LEG + 9, "n=0 — the seam, the drone",
        color=WHITE, fontsize=8.2, ha="left", va="bottom")

# ---- the rung triangles n=1..6 ----
for n in range(1, N + 1):
    h = n * BASE
    hyp = BASE * np.sqrt(n * n + 4)
    is2 = (n == 2)
    if is2:
        lw_leg, lw_hyp, z = 3.0, 3.0, 9
        c_leg, c_hyp = GOLD, ROSE2
    else:
        lw_leg, lw_hyp, z = 1.3, 1.3, 3
        c_leg, c_hyp = GRID, GRID
    # horizontal leg: the dispersion (on the grid)
    ax.plot([0, h], [0, 0], color=c_leg, lw=lw_leg, zorder=z,
            solid_capstyle="round")
    # hypotenuse: the trace (never struck)
    ax.plot([h, 0], [0, LEG], color=c_hyp, lw=lw_hyp, zorder=z,
            solid_capstyle="round")
    # dot at the dispersion end (the difference tone)
    ax.plot(h, 0, marker="o", ms=4.5 if not is2 else 6.5,
            mfc=GOLD if not is2 else GOLD, mec="none", zorder=z + 1)
    # trace value label near the hypotenuse midpoint
    mx, my = h / 2 + 4, LEG / 2
    ax.text(mx, my + 3, f"{hyp:.1f}",
            color=ROSE2 if is2 else DIM, fontsize=7.6, ha="left",
            va="center", zorder=z + 1)

# ---- the grid tones on the dispersion axis ----
grid_labels = {1: "55\nseed", 2: "110\ncount", 3: "165\ngap",
               4: "220\nghost", 5: "275\nsum", 6: "330"}
for n in range(1, N + 1):
    x = n * BASE
    ax.plot([x, x], [-3, 3], color=DIM, lw=1.0, zorder=2)
    ax.text(x, -14, grid_labels[n], color=GOLD if n == 2 else DIM,
            fontsize=7.8, ha="center", va="top")

ax.text(165, -27, "the dispersion — the difference tone 55n, on the grid",
        color=TXT, fontsize=8.5, ha="center", va="top", style="italic")

# ---- the tritone, called out ----
ax.plot(110, 110, marker="o", ms=6, mfc=ROSE2, mec="none", zorder=10)
ax.text(120, 116, "n=2 — the legs meet: the tritone 110√2 ≈ 155.6,\n"
                  "the one isosceles rung, off-grid tone on-grid interval",
        color=ROSE2, fontsize=8.6, ha="left", va="center", zorder=10,
        linespacing=1.4)

# ---- annotation: the operator ----
ax.text(-6, 158, "M(a,b) = (b−a, b+a) — the ear's operator", color=WHITE,
        fontsize=10.5, ha="left", va="center", fontweight="bold")
ax.text(-6, 149, "M(55/σₙ, 55σₙ) = (55n, 55√(n²+4))", color=TXT, fontsize=9,
        ha="left", va="center")
ax.text(-6, 140, "the difference and the sum — the count and the never,",
        color=DIM, fontsize=8.2, ha="left", va="center")
ax.text(-6, 132, "two differences, the ear's own products, at once.",
        color=DIM, fontsize=8.2, ha="left", va="center")

# ---- caption ----
fig.text(0.5, 0.025,
         "n² + 2² = (√(n²+4))²  ·  every rung stands on the doubling; the "
         "trace leans in as n grows  ·  at n=2 the legs meet: the tritone, "
         "the operator's own scale (M/√2, eigentones ±√2)",
         color=TXT, fontsize=9.5, ha="center", linespacing=1.4)

plt.tight_layout(rect=(0, 0.045, 1, 0.985))
plt.savefig("assets/rung_triangle.png", dpi=100, facecolor=BG)
print("wrote assets/rung_triangle.png")

# clip check
fig.canvas.draw()
bad = 0
for ax_i in fig.axes:
    for tx in ax_i.texts:
        if not tx.get_text():
            continue
        bb = tx.get_window_extent()
        inx = bb.x0 >= ax_i.bbox.x0 - 1 and bb.x1 <= ax_i.bbox.x1 + 1
        iny = bb.y0 >= ax_i.bbox.y0 - 1 and bb.y1 <= ax_i.bbox.y1 + 1
        if not (inx and iny):
            print("CLIPPED:", repr(tx.get_text())[:60], bb)
            bad += 1
print("clip check:", "clean" if bad == 0 else f"{bad} clipped")
