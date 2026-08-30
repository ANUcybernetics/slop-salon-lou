#!/usr/bin/env python3
"""the kiss — still for the video.

Left: the geometry. Over the octave 55–220 the fold M(x)=2⌊x⌋−x and the mirror
N(x)=12100/x kiss at (110,110): same value, same slope −1. On the count's cell
the fold IS the line 220−x; the mirror is tangent to it — the shared slope is
the sign. They agree to first order and peel to second order.

Right: the time diagram — what the ear hears. Two voices read the same
descending x: the fold falls 220→55 (on the grid, kinked), the mirror rises
55→220 (smooth). They kiss at the count at t=38 — the beat dies, the deepest
wait — then peel: the fold walks on below, the mirror returns above. The two
absences are exchanged — one transposition.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=100)
BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
DRONE = "#e05252"
FOLD = "#7fb3ff"     # the fold, on the grid
MIRR = "#e0b45c"     # the mirror, smooth
TANG = "#c792ea"     # the shared tangent — the sign

for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=10)

# ---------------- left: the kiss in the octave ----------------
axL.set_title("they agree because they kiss", color=TXT, fontsize=16, loc="left")
axL.text(55, 224, "fold  M(x)=2⌊x⌋−x   ·   mirror  N(x)=12100/x",
         color=DIM, fontsize=11)

xx = np.linspace(55, 220, 2000)
mirr = 12100.0 / xx
axL.plot(xx, mirr, color=MIRR, lw=2.4, zorder=3, label="mirror  12100/x")
# the fold: 2⌊x⌋−x — on each integer cell a line of slope −1
for k in range(55, 220):
    xs = np.linspace(k, k + 1, 2)
    axL.plot(xs, 2 * k - xs, color=FOLD, lw=1.1, alpha=0.85, zorder=2,
             solid_capstyle="butt")
# the count's cell, where the fold IS the tangent line
xs = np.linspace(110, 111, 2)
axL.plot(xs, 220 - xs, color=FOLD, lw=3.2, zorder=4)
# the shared tangent: slope −1 through (110,110) — extended a little
xt = np.linspace(96, 124, 2)
axL.plot(xt, 220 - xt, color=TANG, lw=1.6, ls="--", zorder=5)
axL.annotate("the shared slope = −1\n(the sign)", xy=(124, 96),
             xytext=(140, 84), color=TANG, fontsize=11,
             arrowprops=dict(arrowstyle="->", color=TANG, lw=1.2))

# the drone and the two absences
for f in (55.0, 110.0, 220.0):
    c = DRONE if f == 110.0 else GRID
    axL.axhline(f, color=c, lw=2.2 if f == 110.0 else 1.0, zorder=1,
                alpha=0.95 if f == 110.0 else 1.0)
    axL.text(55.5, f + 3, f"{f:g}", color=DRONE if f == 110.0 else DIM,
             fontsize=11, va="bottom")
axL.text(55.5, 55 - 12, "55", color=DIM, fontsize=11)

# the kiss point
axL.plot(110, 110, "o", color=TANG, ms=11, zorder=6, mec="none")
axL.annotate("the kiss\n(110, 110)", xy=(110, 110), xytext=(128, 150),
             color=TANG, fontsize=12, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TANG, lw=1.4))

axL.set_xlim(55, 220)
axL.set_ylim(30, 235)
axL.set_xlabel("x (the shared descent)", color=DIM)
axL.set_ylabel("reading (Hz)", color=DIM)

# ---------------- right: the time diagram — what the ear hears ----------------
axR.set_title("the two readings — one kiss, one swap", color=TXT, fontsize=16, loc="left")

TA = 38.0
TOTAL = 72.0
SR = 44100
NA = int(TA * SR)
tA = np.arange(NA) / SR
delta = 110.0 * (1.0 - tA / TA) ** 1.5
xA = 110.0 + delta
NB = int((TOTAL - TA) * SR)
tB = np.arange(NB) / SR
xB = 110.0 - 55.0 * (tB / (TOTAL - TA)) ** 0.75
x = np.concatenate([xA, xB])
tT = np.concatenate([tA, tA[-1] + 1.0 / SR + tB])
fL = 2.0 * np.floor(x) - x
fR = 12100.0 / x

# drone line and the two absences
for f in (55.0, 110.0, 220.0):
    c = DRONE if f == 110.0 else GRID
    axR.axhline(f, color=c, lw=2.2 if f == 110.0 else 1.0, zorder=1,
                alpha=0.95 if f == 110.0 else 1.0)
    axR.text(1.2, f + 3, f"{f:g}", color=DRONE if f == 110.0 else DIM,
             fontsize=11, va="bottom")

# thin-down for plotting
step = max(1, len(fL) // 1200)
axR.plot(tT[::step], fL[::step], color=FOLD, lw=2.2, zorder=3, label="the fold — falls")
axR.plot(tT[::step], fR[::step], color=MIRR, lw=2.2, zorder=3, label="the mirror — rises")

# the kiss
axR.plot(TA, 110, "o", color=TANG, ms=11, zorder=6, mec="none")
axR.annotate("the kiss\nthe beat dies", xy=(TA, 110), xytext=(TA + 4, 150),
             color=TANG, fontsize=12, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TANG, lw=1.4))
axR.annotate("", xy=(71, 57), xytext=(63, 110),
             arrowprops=dict(arrowstyle="-|>", color=FOLD, lw=1.6))
axR.annotate("", xy=(71, 217), xytext=(63, 110),
             arrowprops=dict(arrowstyle="-|>", color=MIRR, lw=1.6))
axR.text(70, 45, "the fold walks\n(one-way in time)", color=FOLD, fontsize=10,
         ha="right")
axR.text(70, 226, "the mirror returns\n(exact)", color=MIRR, fontsize=10, ha="right")
axR.text(62, 78, "the swap — the\nsign is the exchange", color=DIM, fontsize=10,
         ha="right", style="italic")

axR.set_xlim(0, TOTAL)
axR.set_ylim(30, 235)
axR.set_xlabel("time (s)", color=DIM)
axR.set_ylabel("reading (Hz)", color=DIM)

fig.text(0.5, 0.015, "the sign is the shared slope — agree to first order, peel to second: δ²/110",
         color=TXT, fontsize=12, ha="center")

plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig("assets/kiss_readings.png", dpi=100, facecolor=BG)
print("wrote assets/kiss_readings.png")
