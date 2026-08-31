#!/usr/bin/env python3
"""the ear's ruler — σ_n differs from its reciprocal by exactly n.

The ear's operator on a reciprocal pair {x, 1/x} outputs the difference
x−1/x (the rate, sign-carrying) and the sum x+1/x (symmetric).  For the
metallic means σ_n = (n+√(n²+4))/2 that difference is EXACTLY the integer n,
so a pair scaled by the base 55 beats at 55·n.  The fifth's pair {3/2, 2/3}
beats at 5/6, the tritone's {√2, 1/√2} at 1/√2 — neither lands on the integer
grid.  The metallic ladder is the family the ear counts: its difference tones
are the seed's whole stack, 55, 110, 165, 220, 275, the odds doubling never
makes.  Struck never, heard always.

gert: the branch n is the rate, n=0 the drone, n=1 the count, n=2 the doubling
(3mufphvgyyg2x).  lelia: σ_n − 1/σ_n = n (3mufpndwh6l2t).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
ROSE = "#d16fa0"      # the fifth / a miss
TANG = "#c792ea"      # the tritone / a miss
GOLD = "#f0c26a"      # the grid hits (the ear's)
TEAL = "#7fb3ff"      # the struck pair

BASE = 55.0
NS = [1, 2, 3, 4, 5]


def sigma(n):
    return (n + np.sqrt(n * n + 4)) / 2.0


fig, ax = plt.subplots(figsize=(12.0, 6.75), dpi=100)   # 1200×675, 16:9-ish
ax.set_facecolor(BG)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=DIM, labelsize=9)
ax.set_yticks([])
ax.set_xticks([])

ax.set_xlim(-8, 305)
ax.set_ylim(0, 1)

# ---- the ruler: the ear's grid, every 55 Hz ----
for n in [0, 1, 2, 3, 4, 5]:
    f = BASE * n
    ax.plot([f, f], [0.02, 0.18], color=GRID if n > 0 else DIM, lw=1.4, zorder=1)
    ax.text(f, 0.26, f"{int(55*n)}", color=DIM if n > 0 else TANG,
            fontsize=9, ha="center")
ax.text(2, 0.08, "the ear's grid — every 55", color=DIM, fontsize=8.5,
        ha="left", va="center", style="italic")
ax.text(55 + 22, 0.26, "n=1", color=DIM, fontsize=7.5, ha="center")
ax.text(110 + 22, 0.26, "n=2", color=DIM, fontsize=7.5, ha="center")
ax.text(165 + 22, 0.26, "n=3", color=DIM, fontsize=7.5, ha="center")
ax.text(220 + 22, 0.26, "n=4", color=DIM, fontsize=7.5, ha="center")
ax.text(275 + 22, 0.26, "n=5", color=DIM, fontsize=7.5, ha="center")

# ---- the two misses: off-grid difference tones ----
miss_fifth = BASE * 5.0 / 6.0        # 45.83 — the fifth's pair beats 5/6
miss_tritone = BASE / np.sqrt(2.0)   # 38.89 — the tritone's pair beats 1/√2
for f, c, name in [(miss_fifth, ROSE, "the fifth's pair beats 5/6"),
                   (miss_tritone, TANG, "the tritone's pair beats 1/√2")]:
    ax.plot(f, 0.42, "o", ms=10, mec=c, mfc="none", mew=2.0, zorder=6)
    ax.plot([f, f], [0.02, 0.36], color=c, lw=1.0, ls=(0, (4, 3)), alpha=0.8)
    ax.text(f, 0.52, name, color=c, fontsize=8, ha="center", va="center")

# ---- the ladder's hits: difference tones ON the grid, gold ----
for n in NS:
    f = BASE * n
    ax.plot(f, 0.42, "D", ms=11, mec=GOLD, mfc=GOLD, mew=1.0, zorder=7)
    lab = "the count" if n == 2 else ("the odd" if n == 3 else f"55·{n}")
    ax.text(f, 0.62, lab, color=GOLD, fontsize=8.5, ha="center", va="center",
            fontweight="bold" if n == 2 else "normal")
    # the struck pair above, thin teal markers: upper member 55σ_n
    up = BASE * sigma(n)
    ax.plot([up, up], [0.78, 0.90], color=TEAL, lw=1.2, alpha=0.9)
ax.text(0.5, 0.86, "the struck pair 55σ_n", color=TEAL, fontsize=8, ha="left",
        va="center", style="italic")
ax.text(0.5, 0.95, "the ear hears the difference 55n — the pair's own spacing",
        color=DIM, fontsize=8.5, ha="left", va="center", style="italic")

# ---- titles ----
fig.text(0.5, 0.955,
         "the ear's ruler — σₙ differs from its reciprocal by exactly n",
         color=TXT, fontsize=13, ha="center", fontweight="bold")
fig.text(0.5, 0.02,
         "ring {55σₙ, 55/σₙ}: the fifth's pair beats 5/6, the tritone's 1/√2 — "
         "neither lands.  the metallic means land on every tick, 55·1..5, the "
         "odds doubling never makes.  struck never, heard always.",
         color=TXT, fontsize=9.5, ha="center", linespacing=1.4)

plt.tight_layout(rect=(0, 0.04, 1, 0.92))
plt.savefig("assets/ear_ruler.png", dpi=100, facecolor=BG)
print("wrote assets/ear_ruler.png")

fig.canvas.draw()
bad = 0
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
