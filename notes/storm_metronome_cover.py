#!/usr/bin/env python3
"""cover still for the storm's metronome — the record beats on the time line."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
ROSE = "#d16fa0"
TEAL = "#7fb3ff"
GOLD = "#f0c26a"
WHITE = "#e8e8ef"
ROSE2 = "#f2b8d6"

fig, ax = plt.subplots(figsize=(10.24, 5.76), dpi=100)
ax.set_facecolor(BG)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=DIM, labelsize=9)

ax.set_xlim(0, 58)
ax.set_ylim(-0.6, 4.0)
ax.set_xticks([10, 15, 20, 54])
ax.set_xticklabels(["rung 10\nwait 23", "rung 15\nwait 55",
                    "rung 20\nwait 114", "rung 54\nwait 317"], color=DIM,
                   linespacing=1.4)
ax.set_yticks([])

# the void
ax.axvspan(20, 54, color=WHITE, alpha=0.06, zorder=0)

# the record beats
for i, col in [(10, ROSE), (15, GOLD), (20, ROSE2), (54, DIM)]:
    ax.plot([i, i], [0.6, 2.8], color=col, lw=3.0, zorder=5, alpha=0.95)

# 5-5 spacing brackets
for x0, x1 in [(10, 15), (15, 20)]:
    ax.plot([x0, x0, x1, x1], [3.15, 3.42, 3.42, 3.15], color=TEAL, lw=1.2)
    ax.text((x0 + x1) / 2, 3.6, "5 rungs", color=TEAL, fontsize=9, ha="center")
ax.plot([20, 20, 54, 54], [3.15, 3.42, 3.42, 3.15], color=DIM, lw=1.2)
ax.text(37, 3.6, "34 rungs of silence", color=DIM, fontsize=9, ha="center")

# labels
ax.text(10, 0.35, "23 — the near-miss", color=ROSE, fontsize=9.5,
        ha="center", va="top")
ax.text(15, 0.35, "55 — the seed", color=GOLD, fontsize=9.5, ha="center", va="top")
ax.text(20, 0.35, "114 — ≈ the doubling", color=ROSE2, fontsize=9.5,
        ha="center", va="top")
ax.text(54, 0.35, "317 — off the grid", color=DIM, fontsize=9.5,
        ha="center", va="top")

ax.text(37, 1.7, "five apart, roughly doubling —\nthen the storm forgets",
        color=DIM, fontsize=10, ha="center", va="center", linespacing=1.5,
        style="italic")

ax.text(29, -0.3, "the lawless keeps the metronome at its peaks",
        color=TXT, fontsize=12, ha="center", va="top")

plt.tight_layout(pad=0.4)
plt.savefig("assets/storm_metronome_cover.png", dpi=100, facecolor=BG)
print("wrote assets/storm_metronome_cover.png")
