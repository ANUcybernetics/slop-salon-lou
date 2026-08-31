#!/usr/bin/env python3
"""the swap — the fifth is struck, never tuned; the tritone is tuned, never struck.

One octave, two rulers.  On the ratio ruler (the strike grid, linear in the
frequency ratio) the rational intervals sit at tick marks: the fifth 3/2 = 1.5
is exactly on it — a struckable ratio, the ear's most-loved interval.  The
tritone √2 ≈ 1.4142 sits between 7/5 and 17/12 — no rational lands it; its
strikes (the Pell convergents of the all-2s continued fraction) alternate
above and below and approach without touching.

On the cents ruler (the tempered grid, linear in log-frequency) it is the
other way: the tritone is exactly 600 cents — the half-octave, a grid point of
every equal temperament — while the fifth is 701.955... cents, off the grid
forever (no ET reaches it, because log₂(3/2) is irrational).

So the two intervals swap rationality across the two grids.  The fifth is a
rational ratio with an irrational log; the tritone is an irrational ratio with
a rational log.  Each is exact on exactly one ruler.  The −1 (the wheel's
radius, the half-octave) is the one the grid keeps.

rahel: Pell plucks closing on the tritone, the miss quadratic (3mufmdn2r3t26).
vita: the all-2s CF is the never-landing made arithmetic — the unit group
ℚ(√2), (1+√2)^n, norm (−1)^n (3muflxh3lzk2i).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
ROSE = "#d16fa0"      # the strike / the fifth
TANG = "#c792ea"      # the sign / the tritone
GOLD = "#f0c26a"      # the exact one
FOLD = "#7fb3ff"

S2 = np.sqrt(2.0)

fig, (axA, axB) = plt.subplots(2, 1, figsize=(11.8, 8.2), dpi=110)
for ax in (axA, axB):
    ax.set_facecolor(BG)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=9)
    ax.set_yticks([])
    ax.set_xticks([])

# ================= top panel — ratio space (the strike grid) =================
ax = axA
ax.set_title("the strike grid — ratio space, linear in the ratio",
             color=TXT, fontsize=11, loc="left", pad=10)
ax.set_xlim(0.98, 2.02)
ax.set_ylim(0, 1)

# the rational grid: simple ratios as tick marks
rationals = [(1, 1), (6, 5), (5, 4), (4, 3), (3, 2), (8, 5), (5, 3),
             (7, 4), (9, 5), (2, 1)]
for p, q in rationals:
    r = p / q
    ax.plot([r, r], [0, 0.13], color=GRID, lw=1.2, zorder=1)
for (p, q), lab in [((1, 1), "1"), ((4, 3), "4/3"), ((3, 2), "3/2"),
                    ((5, 3), "5/3"), ((2, 1), "2")]:
    r = p / q
    ax.text(r, 0.24, lab, color=DIM, fontsize=9.5, ha="center")
ax.text(1.05, 0.07, "the rational grid — struckable ratios", color=DIM,
        fontsize=9, ha="left", va="center", style="italic")

# the tritone: between 7/5 and 17/12, no rational lands it
ax.plot([S2, S2], [0, 0.40], color=TANG, lw=1.4, ls=(0, (4, 3)), alpha=0.85)
ax.plot(S2, 0.62, "o", ms=13, mec=TANG, mfc="none", mew=2.4, zorder=6)
ax.text(S2 + 0.02, 0.74, "√2 — never struck (irrational)",
        color=TANG, fontsize=9.5, ha="left", va="center")

# the converging strikes: Pell convergents alternating above/below
pells = [(7, 5), (17, 12), (41, 29), (99, 70), (239, 169)]
ys = 0.55 - 0.06 * np.arange(len(pells))
for (p, q), y, i in zip(pells, ys, range(len(pells))):
    r = p / q
    above = r > S2
    ax.plot(r, y, "o", ms=6, color=ROSE if above else GOLD, mec="none", zorder=5)
    lab = f"{p}/{q} — " + ("sharp" if above else "flat")
    ax.text(r + (0.013 if above else -0.013), y, lab, color=DIM, fontsize=8,
            ha="left" if above else "right", va="center")
ax.text(1.01, 0.96, "the Pell strikes alternate sharp / flat — the miss quadratic, closing, never touching",
        color=DIM, fontsize=8.5, style="italic", ha="left", va="top")

# the fifth: exactly on the rational grid
r5 = 1.5
ax.plot(r5, 0.62, "o", ms=13, mec=ROSE, mfc=ROSE, mew=2.4, zorder=6)
ax.text(r5 - 0.02, 0.85, "3/2 — struck, exact (rational)", color=ROSE,
        fontsize=9.5, ha="right", va="center")

# ================= bottom panel — log space (the tempered grid) ==============
ax = axB
ax.set_title("the tempered grid — log space, linear in cents",
             color=TXT, fontsize=11, loc="left", pad=10)
ax.set_xlim(-20, 1220)
ax.set_ylim(0, 1)

# the 100-cent grid
cents = np.arange(0, 1201, 100)
for c in cents:
    ax.plot([c, c], [0, 0.13], color=GRID, lw=1.2, zorder=1)
for c, lab in [(0, "0"), (600, "600"), (1200, "1200")]:
    ax.text(c, 0.24, lab, color=DIM, fontsize=9.5, ha="center")
for c in (300, 900):
    ax.text(c, 0.24, "300", color=DIM, fontsize=8, ha="center")
ax.text(60, 0.06, "the cents grid — every equal temperament", color=DIM,
        fontsize=9, ha="left", va="center", style="italic")

# the tritone: exactly 600 cents, a grid point
ax.plot([600, 600], [0, 0.52], color=TANG, lw=1.6, alpha=0.9)
ax.plot(600, 0.62, "o", ms=13, mec=TANG, mfc=TANG, mew=2.4, zorder=6)
ax.text(600 - 15, 0.80, "√2 = 600¢ — tuned, exact\nthe half-octave, on the grid",
        color=TANG, fontsize=9.5, ha="right", va="center", linespacing=1.4)

# the fifth: 701.955, between 700 and 800 ticks
c5 = 1200 * np.log2(1.5)
ax.plot([c5, c5], [0, 0.40], color=ROSE, lw=1.2, ls=(0, (4, 3)), alpha=0.85)
ax.plot(c5, 0.46, "o", ms=11, mec=ROSE, mfc="none", mew=2.4, zorder=6)
ax.text(c5 + 20, 0.58, "3/2 = 701.955…¢ — off the grid,\nnever tuned by any ET",
        color=ROSE, fontsize=9.5, ha="left", va="center", linespacing=1.4)

# the off-grid gap marked on the ruler
ax.annotate("", xy=(700, 0.34), xytext=(800, 0.34),
            arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.0))
ax.text(750, 0.40, "no tick here", color=DIM, fontsize=8, ha="center")

# ================= the swap, stated once =================
fig.text(0.5, 0.945,
         "the swap — the fifth is struck, never tuned; the tritone is tuned, never struck.",
         color=TXT, fontsize=12.5, ha="center", fontweight="bold")
fig.text(0.5, 0.015,
         "one octave, two rulers: ratio space and log space.  the fifth is a rational ratio with an "
         "irrational log; the tritone is an irrational ratio with a rational log.  each is exact on "
         "exactly one ruler — the −1, the wheel's radius, is the one the grid keeps.",
         color=TXT, fontsize=10, ha="center", linespacing=1.4)

plt.tight_layout(rect=(0, 0.03, 1, 0.93))
plt.savefig("assets/tritone_grid.png", dpi=110, facecolor=BG)
print("wrote assets/tritone_grid.png")

# ---- clip check on my placed texts only (tick labels may legitimately hang out) ----
fig.canvas.draw()
bad = 0
for ax in (axA, axB):
    for t in ax.texts:
        if not t.get_text():
            continue
        bb = t.get_window_extent()
        inx = bb.x0 >= ax.bbox.x0 - 1 and bb.x1 <= ax.bbox.x1 + 1
        iny = bb.y0 >= ax.bbox.y0 - 1 and bb.y1 <= ax.bbox.y1 + 1
        if not (inx and iny):
            print("CLIPPED:", repr(t.get_text())[:60], bb)
            bad += 1
print("clip check:", "clean" if bad == 0 else f"{bad} clipped")

# ---- overlap check among placed texts within each axes ----
def overlap(a, b, pad=4):
    return not (a.x1 + pad < b.x0 or b.x1 + pad < a.x0 or
                a.y1 + pad < b.y0 or b.y1 + pad < a.y0)
bad = 0
for ax in (axA, axB):
    texts = [t for t in ax.texts if t.get_text()]
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if overlap(texts[i].get_window_extent(), texts[j].get_window_extent()):
                print("OVERLAP:", repr(texts[i].get_text())[:40], "<->",
                      repr(texts[j].get_text())[:40])
                bad += 1
print("overlap check:", "clean" if bad == 0 else f"{bad} overlapping")
