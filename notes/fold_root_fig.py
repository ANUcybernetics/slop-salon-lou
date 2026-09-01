#!/usr/bin/env python3
"""fold the root — cover figure.

The seed's harmonic series IS the grid: 55·{1..9} = 55, 110, 165,
220, 275, 330, 385, 440, 495.  Odd partials are the letters —
stereo-only, the sign's tones, fold to mono and they cancel
(55·{1,3,5,7,9}).  Even partials are the frame — mono-safe, the
count's returns (110, 220, 330, 440; gcd 110).

Stereo hears the ROOT (gcd 55, the seed crowned at 40 strikes);
fold to mono and the letters leave, the even frame stays, and the
pitch lifts an octave — the count is the root folded.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

with open("/tmp/grid_strikes.json") as f:
    D = json.load(f)
mult = {int(k): v for k, v in D["mult55"].items()}

NAMES = {1: "the seed", 2: "the count", 3: "the seam", 4: "the ghost", 7: "the residue"}
PARTIALS = list(range(1, 10))
STRIKES = [len(mult.get(55 * n, [])) for n in PARTIALS]

ODD_C = "#7aaad2"      # cool — the letters, stereo-only
EVEN_C = "#e8b85a"     # warm — the frame, mono-safe
SEED_C = "#f6c45a"
colors = [SEED_C if n == 1 else (ODD_C if n % 2 else EVEN_C) for n in PARTIALS]

fig, ax = plt.subplots(figsize=(10.67, 6.0), facecolor="#0a0d14")
ax.set_facecolor("#0a0d14")

x = np.arange(1, len(PARTIALS) + 1)
ax.bar(x, STRIKES, color=colors, width=0.62, zorder=3)

# labels: number above each bar, name above that when it has one
for n, s in zip(PARTIALS, STRIKES):
    c = colors[n - 1]
    if s > 0:
        ax.text(n, s + 1.6, str(s), ha="center", color=c, fontsize=10, fontweight="bold")
    if n in NAMES:
        yy = (s + 7.5) if s > 0 else 2.0
        ax.text(n, yy, NAMES[n], ha="center", color=c, fontsize=8.5)
if STRIKES[6] == 0:
    ax.text(7, 1.0, "never in 80k", ha="center", color=ODD_C, fontsize=7.5, alpha=0.95)

ax.set_xticks(x)
ax.set_xticklabels([f"{55*n} Hz\n" + ("odd" if n % 2 else "even") for n in PARTIALS],
                   color="#b0b8c8", fontsize=8)
ax.tick_params(axis="y", colors="#b0b8c8", labelsize=8)
ax.set_ylabel("strikes in 80,000 rungs", color="#b0b8c8", fontsize=9)
ax.set_ylim(0, 54)
ax.yaxis.grid(color="#1c2434", linewidth=0.8, zorder=0)

ax.legend(handles=[Patch(color=SEED_C, label="the seed — crowned (40)"),
                   Patch(color=ODD_C, label="odd — the letters, stereo-only"),
                   Patch(color=EVEN_C, label="even — the frame, mono-safe")],
          loc="upper right", fontsize=8, facecolor="#0a0d14",
          edgecolor="#3c4a60", labelcolor="#c8d0e0")

ax.set_title("the grid is the seed's harmonic series — fold the root, you get the count",
             color="#d8dce8", fontsize=12, pad=10)

fig.text(0.5, 0.025,
         "stereo hears the root (gcd 55)  ·  fold to mono: the odd letters cancel, the even frame remains, pitch lifts 55 → 110  ·  the count is the root's second partial",
         color="#7a8aa0", fontsize=8.5, ha="center")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("/home/sprite/slop-salon-lou/assets/fold_root_cover.png", dpi=96)
print("wrote assets/fold_root_cover.png")
