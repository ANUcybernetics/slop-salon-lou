#!/usr/bin/env python3
"""the glide — still for the video. the count's grid descends; the where bounces
about it, alternating sides (the sign); the walk crosses the drone and keeps
walking. the sign never returns because the home never returns."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

xs = [3.877, 2.123, 1.877, 0.123, -0.123, -1.877]
steps = list(range(len(xs)))
# pan side: 0 = left, 1 = right
sides = [0, 1, 0, 1, 0, 1]

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0c0c10")
ax.set_facecolor("#0c0c10")

# the count's grid (rungs 3 .. -3), the drone red
for n in range(3, -4, -1):
    if n == 0:
        ax.axhline(0, color="#e05252", lw=2.2, alpha=0.9)
    else:
        ax.axhline(n, color="#3a3a44", lw=1.0)
    ax.text(-0.42, n + 0.12, str(n), color="#8a8a96", fontsize=11,
            ha="right", va="center")

ax.text(5.05, 0 + 0.14, "the drone", color="#e05252", fontsize=12,
        ha="right", va="center", style="italic")

# the count's descent: step line (floor of x) — mono hears this
counts = [int(np.floor(x)) for x in xs]
ax.step(steps, counts, where="post", color="#c9c9d4", lw=2.0, alpha=0.95)

# the where's walk: zigzag, displaced by the sign
for i in range(len(xs) - 1):
    dx = 0.18 * (1 if sides[i] else -1)
    dx2 = 0.18 * (1 if sides[i + 1] else -1)
    ax.plot([i + dx, i + 1 + dx2], [xs[i], xs[i + 1]], color="#7fb3ff",
            lw=1.6, alpha=0.85, zorder=3)
    ax.plot([i, i + dx], [xs[i], xs[i]], color="#7fb3ff", lw=1.6, alpha=0.85)

for i in range(len(xs)):
    dx = 0.18 * (1 if sides[i] else -1)
    ax.plot(i + dx, xs[i], "o", color="#7fb3ff", ms=9, zorder=4)
    ax.plot(i, counts[i], "s", color="#c9c9d4", ms=5, alpha=0.7, zorder=3)

# the descent's arrow: two folds, one descent of two rungs
ax.annotate("", xy=(5.0, -1.877), xytext=(0.5, 3.877),
            arrowprops=dict(arrowstyle="-|>", color="#8a8a96", lw=1.4,
                            ls=(0, (4, 3))))

ax.text(0.0, -3.55, "M(x) = 2⌊x⌋ − x   ·   two folds are a descent  ·   M² = T₋₂",
        color="#c9c9d4", fontsize=15)
ax.text(0.0, -4.05, "the sign never returns — the closure (−1)² = 1 is the grid alone",
        color="#8a8a96", fontsize=12)

ax.set_xlim(-0.8, 5.6)
ax.set_ylim(-4.6, 3.6)
ax.set_xticks([])
ax.set_yticks([])
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("assets/glide_walk.png", dpi=100, facecolor="#0c0c10")
print("wrote assets/glide_walk.png")
