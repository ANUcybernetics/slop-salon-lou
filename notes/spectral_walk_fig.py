#!/usr/bin/env python3
"""two spectra, one mirror — still for the video.

Left: the involution, discrete. M = P − R, M² = I, σ(M) = {+1, −1}. The sign
flips and returns — a closed two-point loop.

Right: the glide, continuous. M(x) = 2⌊x⌋ − x, two folds a translation M² = T₋₂.
The walk is free, absolutely continuous — a tone crossing the drone at 110 and
leaving it. No point spectrum; the whole circle, no dots.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0c0c10")

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
DRONE = "#e05252"
SIGN = "#7fb3ff"
FREE = "#e0b45c"

# ---------------- left: the involution, discrete ----------------
axL.set_facecolor(BG)
axL.axhline(0, color=GRID, lw=1.0)
axL.axhline(1, color=GRID, lw=0.8)
axL.axhline(-1, color=GRID, lw=0.8)
# the two eigenvalues
axL.plot([0], [1], "o", color=SIGN, ms=14, zorder=5)
axL.plot([0], [-1], "o", color=SIGN, ms=14, zorder=5)
axL.text(0.14, 1.06, "+1", color=SIGN, fontsize=15, va="center")
axL.text(0.14, -1.06, "−1", color=SIGN, fontsize=15, va="center")
# the bounce loop: the sign flips and returns
theta = np.linspace(0, 2 * np.pi, 200)
bounce = 0.75 * np.cos(theta)
axL.plot(np.sin(theta) * 0.5, bounce, color=SIGN, lw=1.8, alpha=0.9)
axL.annotate("", xy=(0.0, 1.0), xytext=(0.45, 0.3),
             arrowprops=dict(arrowstyle="-|>", color=SIGN, lw=1.4))
axL.annotate("", xy=(0.0, -1.0), xytext=(-0.45, -0.3),
             arrowprops=dict(arrowstyle="-|>", color=SIGN, lw=1.4))
axL.text(0.0, 0.0, "flips", color=DIM, fontsize=11, ha="center", style="italic")
axL.text(0.0, -1.75, "and returns", color=DIM, fontsize=11, ha="center", style="italic")

axL.set_xlim(-1.2, 1.4)
axL.set_ylim(-2.3, 1.9)
axL.set_xticks([]); axL.set_yticks([])
for s in ("top", "right", "left", "bottom"):
    axL.spines[s].set_visible(False)
axL.set_title("the involution — discrete", color=TXT, fontsize=16, loc="left")
axL.text(0.0, 1.72, "M = P − R,  M² = I", color=TXT, fontsize=13, ha="left")
axL.text(0.0, 1.45, "σ(M) = {+1, −1}   ·   the sign returns", color=SIGN, fontsize=12, ha="left")

# ---------------- right: the glide, continuous ----------------
axR.set_facecolor(BG)
f_grid = [220.0, 110.0, 55.0, 27.5]
for f in f_grid:
    col = DRONE if f == 110.0 else GRID
    axR.axhline(np.log2(f / 110.0), color=col, lw=2.0 if f == 110.0 else 1.0,
                alpha=0.95 if f == 110.0 else 1.0)
    axR.text(0.02, np.log2(f / 110.0) + 0.06, f"{f:g}",
             color=DRONE if f == 110.0 else DIM, fontsize=11, va="bottom")
# the descent: 220 → 27.5, crossing the drone, continuing
tt = np.linspace(0, 1, 300)
f = 220.0 * 2.0 ** (-3.0 * tt)
y = np.log2(f / 110.0)
axR.plot(tt, y, color=FREE, lw=2.4, zorder=4)
# mark the crossing of the drone
tc = 1.0 / 3.0
axR.plot(tc, 0.0, "o", color=DRONE, ms=9, zorder=5)
axR.annotate("the seal = the crossing", xy=(tc, 0.0), xytext=(0.52, -1.3),
             color=DRONE, fontsize=11, arrowprops=dict(arrowstyle="->", color=DRONE, lw=1.2))
# the arrow keeps going, out of frame
axR.annotate("", xy=(1.0, np.log2(27.5 / 110.0)), xytext=(0.85, np.log2(34.0 / 110.0)),
             arrowprops=dict(arrowstyle="-|>", color=FREE, lw=1.6))
# the free spectrum: the whole circle, a smear with no dots
xs = np.linspace(1.03, 1.3, 50)
ys = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(xs, ys)
sm = 0.55 * np.exp(-0.5 * ((Y / 0.55) ** 2)) * (1 - np.abs(X - 1.165) / 0.12)
sm = np.clip(sm, 0, None)
axR.imshow(sm, extent=(1.03, 1.3, -1.5, 1.5), origin="lower", aspect="auto",
           cmap="inferno", alpha=0.45, zorder=0)
axR.text(1.29, 0.0, "the whole\ncircle", color=FREE, fontsize=10, ha="center", va="center", alpha=0.9)
axR.text(1.29, -0.55, "no dots", color=DIM, fontsize=10, ha="center", va="center", style="italic")

axR.set_xlim(-0.02, 1.32)
axR.set_ylim(-2.2, 2.1)
axR.set_xticks([]); axR.set_yticks([])
for s in ("top", "right", "left", "bottom"):
    axR.spines[s].set_visible(False)
axR.set_title("the glide — continuous", color=TXT, fontsize=16, loc="left")
axR.text(-0.0, 1.85, "M(x) = 2⌊x⌋ − x,  M² = T₋₂", color=TXT, fontsize=13, ha="left")
axR.text(-0.0, 1.58, "free — no point spectrum   ·   the sign never returns",
         color=FREE, fontsize=12, ha="left")

plt.tight_layout()
plt.savefig("assets/spectral_walk.png", dpi=100, facecolor=BG)
print("wrote assets/spectral_walk.png")
