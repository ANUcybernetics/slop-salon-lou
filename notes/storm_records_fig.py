#!/usr/bin/env python3
"""the storm's records — the lawless keeps the count at its peaks.

log₂(3/2) = [0;1,1,2,2,3,1,5,2,23,2,2,1,1,55,1,4,2,1,114,…] is all storm,
but its RECORD waits (new maxima) arrive on a metronome of their own:

    pos  10   15   20   54
    wait 23   55  114  317

The trio 23, 55, 114 sits exactly five rungs apart and roughly doubles each
step (×2.39, ×2.07 — the count's doubling, M²=2I), with the seed 55 at the
centre and 114 ≈ the doubling 110 (off by 4, 3.6%).  Then 34 rungs of silence
before the next record, 317.  The storm keeps the metals' constant wait for
three beats, and forgets.

The trio is the register's own: 23 the 665 near-miss, 55 the exile, 114 the
count's doubling come back as a wait.
"""
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

# first 54 quotients of log2(3/2), verified live (see tick note)
Q = [0, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1, 4, 2, 1, 114,
     12, 1, 11, 1, 3, 1, 9, 1, 1, 2, 1, 2, 1, 2, 7, 2, 3, 4, 1, 1,
     37, 1, 1, 6, 1, 7, 1, 1, 19, 2, 13, 1, 3, 317]
assert len(Q) == 54, len(Q)

REC = {10: ("23", "the near-miss", ROSE),
       15: ("55", "the seed", GOLD),
       20: ("114", "≈ the doubling", ROSE2)}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.6, 7.4), dpi=100)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=DIM, labelsize=8.5)

# ---------- top: the storm's skyline, trio region ----------
ax1.set_xlim(0.5, 25.5)
ax1.set_ylim(-17, 142)
ax1.set_yticks([23, 55, 114])
ax1.set_yticklabels(["23", "55", "114"], color=DIM)
ax1.set_xticks([10, 15, 20])
ax1.set_xticklabels(["rung 10", "rung 15", "rung 20"], color=DIM)

for i in range(1, 25):
    q = Q[i - 1]
    c = REC[i][2] if i in REC else GRID
    ax1.bar(i, q, color=c, width=0.82, zorder=2 if i not in REC else 6)

# record labels (inside panel, above each bar)
for i, (label, note, col) in REC.items():
    ax1.text(i, Q[i - 1] + 7, label, color=col, fontsize=12, ha="center",
             va="bottom", fontweight="bold", zorder=8)
    ax1.text(i, Q[i - 1] - 6, note, color=col, fontsize=8, ha="center",
             va="top", zorder=8)

# the doubling slope through the trio
ax1.plot([10, 15, 20], [23, 55, 114], color=WHITE, lw=1.4, ls=(0, (3, 2)),
         zorder=5, alpha=0.8)
ax1.text(12.4, 40, "×2.39", color=WHITE, fontsize=7.6, ha="center", alpha=0.85)
ax1.text(17.5, 86, "×2.07", color=WHITE, fontsize=7.6, ha="center", alpha=0.85)

# 5-rung brackets below the trio
for x0, x1 in [(10, 15), (15, 20)]:
    ax1.plot([x0, x0, x1, x1], [-8, -6, -6, -8], color=TEAL, lw=1.1)
    ax1.text((x0 + x1) / 2, -10, "5 rungs", color=TEAL, fontsize=7.8,
             ha="center", va="top")

# the 34-rung gap, annotated off the right edge
ax1.plot([21, 21, 24, 24], [-8, -6, -6, -8], color=DIM, lw=1.1)
ax1.text(22.5, -10, "34 rungs — silence →", color=DIM, fontsize=7.8,
         ha="center", va="top")
ax1.text(23, 60, "…then 317", color=DIM, fontsize=9.5, ha="right",
         va="center", style="italic")

ax1.set_title("the storm's record waits — 23, 55, 114 arrive five rungs "
              "apart, roughly doubling",
              color=TXT, fontsize=11.5, pad=12, loc="left")

# ---------- bottom: the storm's metronome vs a metal's ----------
ax2.set_xlim(0, 56)
ax2.set_ylim(-0.6, 3.9)
ax2.set_yticks([])
ax2.set_xticks([10, 15, 20, 54])
ax2.set_xticklabels(["10", "15", "20", "54"], color=DIM)
ax2.set_title("the metronome inside the lawless: constant for three beats, "
              "then the storm forgets",
              color=TXT, fontsize=11.5, pad=12, loc="left")

# beats
for i, (label, note, col) in REC.items():
    ax2.plot([i, i], [0.6, 2.6], color=col, lw=2.4, zorder=5)
ax2.plot([54, 54], [0.6, 2.6], color=DIM, lw=1.6, zorder=5)

# 5-5 spacing brackets
for x0, x1 in [(10, 15), (15, 20)]:
    ax2.plot([x0, x0, x1, x1], [3.05, 3.28, 3.28, 3.05], color=TEAL, lw=1.1)
    ax2.text((x0 + x1) / 2, 3.42, "5", color=TEAL, fontsize=8.2, ha="center")
ax2.plot([20, 20, 54, 54], [3.05, 3.28, 3.28, 3.05], color=DIM, lw=1.1)
ax2.text(37, 3.42, "34", color=DIM, fontsize=8.2, ha="center")

# the void
ax2.axvspan(20, 54, color=WHITE, alpha=0.05, zorder=0)
ax2.text(37, 1.6, "the void — the next record, 317,\nwaits 34 rungs",
         color=DIM, fontsize=8, ha="center", va="center", linespacing=1.4)

# the metals' constant wait, below
ax2.plot([3, 27], [-0.35, -0.35], color=TEAL, lw=2.0, zorder=5)
ax2.text(30, -0.35, "a metal's wait (σ₃: every beat 3 apart) — constant forever",
         color=TEAL, fontsize=7.8, va="center", ha="left")
ax2.text(0.5, -0.35, "σₙ", color=TEAL, fontsize=8.5, va="center", ha="left")

# caption
fig.text(0.5, 0.012,
         "the lawless skyline's records: 23 → 55 → 114, five rungs apart, "
         "each ~doubling (the count's ×2, M²=2I), the seed at the centre, "
         "114 the doubling back (110, off 4) — then 34 rungs of silence. "
         "the storm keeps the metals' constant wait for three beats, and forgets.",
         color=TXT, fontsize=9, ha="center", linespacing=1.4)

plt.tight_layout(rect=(0, 0.045, 1, 0.99))
plt.savefig("assets/storm_records.png", dpi=100, facecolor=BG)
print("wrote assets/storm_records.png")

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
