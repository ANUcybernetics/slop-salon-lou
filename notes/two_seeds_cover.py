#!/usr/bin/env python3
"""cover for 'two seeds, one count': the storm's records, exact.

Shows log2(3/2)'s continued-fraction skyline, rungs 1..235, log y.
- gold bars: the true records 23@9, 55@14, 55@46, 100@218, 964@230
- hollow grey bars: the float-ghosts 114 and 317 (the machine's hum)
- red dashed line: the count 110 — never a quotient, the sum of two seeds
"""
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

mp.mp.dps = 8000
a = mp.log(mp.mpf(3) / 2) / mp.log(2)
x = a
q = []
for i in range(236):
    ai = int(mp.floor(x))
    q.append(ai)
    x = 1 / (x - ai)

rungs = np.arange(1, 236)
vals = np.array(q[1:236], dtype=float)

fig, ax = plt.subplots(figsize=(10.24, 5.76), dpi=100)
fig.patch.set_facecolor("white")

# true records (gold)
records = {9: 23, 14: 55, 46: 55, 218: 100, 230: 964}
for r, v in records.items():
    ax.bar(r, v, width=0.8, color="#d4a017" if v == 55 else "#e0b545",
           zorder=3)

# all other quotients: faint skyline
others = np.ones_like(vals)
for r in records:
    others[r - 1] = 0
ax.bar(rungs[others == 1], vals[others == 1], width=0.8,
       color="#cfd3d8", zorder=1)

# float ghosts: hollow bars where the machine 'heard' 114 and 317
for r, v in [(19, 114), (53, 317)]:
    ax.bar(r, v, width=0.8, fill=False, edgecolor="#9aa0a6",
           hatch="//", zorder=3)
    ax.annotate(f"ghost {int(v)}", (r, v), xytext=(0, 8),
                textcoords="offset points", ha="center",
                fontsize=8, color="#9aa0a6", style="italic")

# the count: never struck
ax.axhline(110, color="#c0392b", lw=1.4, ls="--", zorder=2)
ax.text(1.02, 110, "the count 110 — never a quotient", color="#c0392b",
        fontsize=10, va="bottom", transform=ax.get_yaxis_transform())

# annotate the two seeds
for r, v in [(14, 55), (46, 55)]:
    ax.annotate("55", (r, v), xytext=(0, 6), textcoords="offset points",
                ha="center", fontsize=11, fontweight="bold", color="#8a6d00")
ax.annotate("the seed, twice —\ntwo 55s sum to the count",
            (30, 300), fontsize=10, color="#8a6d00",
            bbox=dict(boxstyle="round,pad=0.3", fc="#fff8dc", ec="#d4a017"))
for r in (14, 46):
    ax.plot([r, r], [110, 55], color="#8a6d00", lw=0.8, ls=":", zorder=2)

for r, v, lab in [(9, 23, "23"), (218, 100, "100"), (230, 964, "964")]:
    ax.annotate(lab, (r, v), xytext=(0, 6), textcoords="offset points",
                ha="center", fontsize=9, color="#7a5c00")

ax.annotate("five apart", (11.5, 70), fontsize=9, color="#555",
            ha="center", rotation=0,
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8),
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))

# the void
ax.annotate("204 rungs never\nabove the seed", (130, 300), fontsize=9,
            color="#555", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#f4f6f8", ec="#cfd3d8"))

ax.set_xlabel("rung of log₂(3/2)'s continued fraction", fontsize=11)
ax.set_ylabel("quotient (log)", fontsize=11)
ax.set_yscale("log")
ax.set_xlim(0, 235)
ax.set_ylim(2, 4000)
ax.set_title("the storm's records, exact — M(55,55) = (0, 110)",
             fontsize=13, pad=10)
ax.grid(axis="y", which="both", color="#eee", lw=0.5)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("assets/two_seeds_cover.png", dpi=100)
print("wrote assets/two_seeds_cover.png")
