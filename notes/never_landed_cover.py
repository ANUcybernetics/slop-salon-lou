#!/usr/bin/env python3
"""cover for never_landed: the ladder walks in, then the same distances walk out.

a cents axis, the drone at 0 as a solid line (0¢ is not a distance, it is the
drone), the signed near-misses as points, the walk-in converging (solid path)
and the walk-out diverging (dashed path) — the same points twice. the pivot
near the centre is where the ladder becomes the drone.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ladder = [+204.0, -90.0, +23.5, -19.8, +3.6, -1.8, +0.076]

fig, ax = plt.subplots(figsize=(10.24, 5.76), dpi=100)
fig.patch.set_facecolor("#0b0e13")
ax.set_facecolor("#0b0e13")

# ---- the drone: a solid line at 0, the origin that never clicks ----
ax.axvline(0.0, color="#e8b84b", lw=2.5, alpha=0.95, zorder=5)
ax.text(0.0, 1.02, "0¢ — the drone, not a distance", color="#e8b84b",
        fontsize=11, ha="center", va="bottom", alpha=0.95)

# ---- the walk-in: the ladder converging on the centre ----
xin = np.array(ladder)
yin = np.linspace(0.86, 0.14, len(ladder))     # descending (approaching)
ax.plot(xin, yin, color="#e8b84b", lw=1.2, alpha=0.75, zorder=3)
ax.scatter(xin, yin, s=[60 * (0.3 + 0.7 * abs(m) / 204) for m in ladder],
           color="#e8b84b", alpha=0.9, edgecolors="none", zorder=4)

# ---- the walk-out: the same points, reversed, diverging ----
xout = np.array(ladder[-2::-1])                # -1.8, +3.6, -19.8, +23.5, -90, +204
yout = np.linspace(0.14, 0.86, len(xout))
ax.plot(xout, yout, color="#7fb0d8", lw=1.8, ls="--", alpha=0.9, zorder=3)
ax.scatter(xout, yout, s=[110 * (0.3 + 0.7 * abs(m) / 204) for m in xout],
           color="#7fb0d8", alpha=0.85, edgecolors="none", zorder=4)

# ---- the pivot: the deepest near-miss is the drone itself ----
ax.plot([0.076], [0.14], "o", ms=13, color="#e8b84b", alpha=0.35, zorder=2)
ax.annotate("", xy=(0, 0.14), xytext=(0.076, 0.14),
            arrowprops=dict(arrowstyle="-", color="#e8b84b", alpha=0.9, lw=1.6))
ax.text(6, 0.12, "the deepest miss", color="#7fb0d8", fontsize=9,
        ha="left", va="top", alpha=0.8)

# labels at the ends
ax.text(204, 0.14, "+204", color="#e8b84b", fontsize=9, ha="left", va="center", alpha=0.9)
ax.text(-90, 0.14, "−90", color="#7fb0d8", fontsize=9, ha="right", va="center", alpha=0.9)

ax.text(0.5, -0.12, "the same distances twice — walk in (solid), walk out (dashed)",
        color="#8a93a3", fontsize=9, transform=ax.transAxes, ha="center")

ax.set_xlim(-225, 230)
ax.set_ylim(-0.05, 1.12)
ax.set_yticks([])
ax.set_xticks([-200, -100, 0, 100, 200])
ax.set_xticklabels(["-200", "-100", "0", "+100", "+200"], color="#8a93a3", fontsize=9)
for s in ax.spines.values():
    s.set_color("#232a36")
ax.tick_params(colors="#8a93a3")
ax.set_xlabel("cents from 110", color="#8a93a3", fontsize=10)

fig.tight_layout()
fig.savefig("assets/never_landed_cover.png", dpi=100, facecolor=fig.get_facecolor())
print("wrote assets/never_landed_cover.png")
