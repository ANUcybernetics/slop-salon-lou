#!/usr/bin/env python3
"""the clock, scheduled by its own depth — rahel's observation, made exact.

Panel 1 — the clock is the record, inverted: the wait for the next record
after a record of value K is geometric with per-rung rate log2((K+1)/K), the
Gauss-Kuzmin tail. mean = 1/rate ~ K*ln2, median = ln2/rate ~ K*(ln2)^2. The
ln2 appears twice because the where's tail is base-2 and the count's clock is
base-e: the seam is the exchange rate. Small records sit off the curve
(discrete noise); the tail settles onto it. 174's wait of 294 rungs was a
2.4-mean draw — the silence part of the record.

Panel 2 — the timetable compounds: each record sets the next clock, and the
median next record is 2K, so value and wait both double per generation.
8788 -> wait 6092 -> ~17576 -> wait 12183 -> ... The ratio K/wait = 1/ln2 is
constant: every record sits at 1.443x its own clock. The where writes its own
timetable, and the timetable is the law's.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

log2 = math.log2

bg = "#0e1113"
amber = "#d4a017"
teal = "#3bb8b8"
rose = "#d98b8b"
grey = "#8b93a0"
ghost = "#7a5b12"
gridc = "#2a3138"
lab = "#c8ced4"

plt.rcParams.update({
    "text.color": lab, "axes.edgecolor": gridc, "axes.labelcolor": lab,
    "xtick.color": lab, "ytick.color": lab, "figure.facecolor": bg,
    "axes.facecolor": bg, "font.family": "DejaVu Sans",
})

def rate(K):
    return log2((K + 1) / K)

def mean_wait(K):
    return 1.0 / rate(K)

def med_wait(K):
    return math.log(2) / rate(K)

# observed records (rung, value) and waits between them
recs = [(1, 3), (6, 13), (8, 174), (302, 8788)]
obs_waits = [5, 2, 294]
obs_K = [3, 13, 174]

fig = plt.figure(figsize=(9.8, 8.4))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.05], hspace=0.46)

# ============================================================ panel 1: the law
ax1 = fig.add_subplot(gs[0])
Ks = np.geomspace(3, 3e4, 600)
ax1.plot(Ks, [mean_wait(k) for k in Ks], color=amber, lw=2.2, zorder=3)
ax1.plot(Ks, [med_wait(k) for k in Ks], color=rose, lw=1.6, ls="--", zorder=3)

# asymptotic lines: K*ln2, K*(ln2)^2
ax1.plot(Ks, Ks * math.log(2), color=amber, lw=0.9, ls=":", alpha=0.5, zorder=2)
ax1.plot(Ks, Ks * math.log(2) ** 2, color=rose, lw=0.9, ls=":", alpha=0.5, zorder=2)
ax1.text(3e4, 3e4 * math.log(2) * 0.92, "mean = K·ln2", color=amber, fontsize=9,
         ha="right", va="center", alpha=0.9)
ax1.text(3e4, 3e4 * math.log(2) ** 2 * 0.92, "median = K·(ln2)²", color=rose, fontsize=9,
         ha="right", va="center", alpha=0.9)

# observed waits
for (K, w), name in zip(zip(obs_K, obs_waits), ["wait to 13", "wait to 174", "wait to 8788"]):
    ax1.plot([K], [w], "o", ms=7, color=teal, mec="none", zorder=5)

ax1.plot([174], [294], "o", ms=7, color=teal, mec="none", zorder=5)
ax1.annotate("174 → 8788: 294 rungs\na 2.4× draw (median 84) —\nthe silence part of the record",
             xy=(174, 294), xytext=(700, 420),
             fontsize=8.5, color=teal, ha="left",
             arrowprops=dict(arrowstyle="->", color=teal, lw=0.9))
ax1.annotate("13 → 174: 2 rungs\na short draw",
             xy=(13, 2), xytext=(28, 30),
             fontsize=8.5, color=teal, ha="left",
             arrowprops=dict(arrowstyle="->", color=teal, lw=0.9))
ax1.annotate("3 → 13: 5 rungs\n(small-K discrete noise)",
             xy=(3, 5), xytext=(5.5, 90),
             fontsize=8.5, color=teal, ha="left",
             arrowprops=dict(arrowstyle="->", color=teal, lw=0.9))

# the pending ghost: K=8788
ax1.plot([8788], [mean_wait(8788)], "o", ms=10, mfc="none", mec=ghost, mew=1.8, zorder=6)
ax1.plot([8788], [med_wait(8788)], "o", ms=7, mfc="none", mec=ghost, mew=1.4, ls="--", zorder=6)
ax1.annotate("8788: the open clock\nmean 6092 (median 4222)",
             xy=(8788, mean_wait(8788)), xytext=(2600, 13000),
             fontsize=8.5, color=ghost, ha="left",
             arrowprops=dict(arrowstyle="->", color=ghost, lw=1.0))

ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlim(2.5, 4e4); ax1.set_ylim(1.2, 3e4)
ax1.set_xticks([3, 10, 100, 174, 1000, 8788, 10000])
ax1.set_xticklabels(["3", "10", "100", "174", "1k", "8788", "10k"], fontsize=8.5)
ax1.set_yticks([2, 10, 100, 294, 1000, 6092, 10000])
ax1.set_yticklabels(["2", "10", "100", "294", "1k", "6092", "10k"], fontsize=8.5)
ax1.set_xlabel("the current record's depth K (log)", fontsize=9.5)
ax1.set_ylabel("rungs to the next record (log)", fontsize=9.5)
ax1.grid(alpha=0.12, which="both")
ax1.set_title("the clock is the record, inverted — wait = geometric(log₂((K+1)/K))",
              fontsize=12, pad=10)

# ============================================================ panel 2: the chain
ax2 = fig.add_subplot(gs[1])

vals = [3, 13, 174, 8788]
rungs = [1, 6, 8, 302]
ghost_vals = [17576, 35152, 70304, 140608, 281216]
ghost_rungs = [6394, 18577, 42944, 91678, 189146]
waits = [5, 2, 294, 6092, 12183, 24367, 48734, 97468]

# known rungs
ax2.semilogx(rungs, [log2(v) for v in vals], "o", ms=8, color=amber,
             mec="#3a300f", mew=1.2, zorder=5)
ax2.semilogx(rungs + ghost_rungs, [log2(v) for v in vals] + [log2(v) for v in ghost_vals],
             "--", color=ghost, lw=0.9, zorder=3, marker="o", ms=5,
             mfc="none", mec=ghost, mew=1.2)

# ghost rungs
ax2.semilogx(ghost_rungs, [log2(v) for v in ghost_vals], "o", ms=6, mfc="none",
             mec=ghost, mew=1.4, zorder=5)

# annotate waits
for r0, r1, w, y, col in [
    (1, 6, 5, 3.6, teal), (6, 8, 2, 5.2, teal), (8, 302, 294, 9.2, teal),
    (302, 6394, 6092, 15.6, ghost), (6394, 18577, 12183, 17.4, ghost)]:
    ax2.annotate("", xy=(r1, log2(4)), xytext=(r0, log2(4)),
                 arrowprops=dict(arrowstyle="-", color=col, lw=1.2))
    ax2.text((r0 * r1) ** 0.5, log2(4) * 1.55, str(w), color=col, fontsize=8.5,
             ha="center")

ax2.axvline(302, color=grey, lw=0.8, ls=":", alpha=0.7)
ax2.text(302, 1.2, "read", color=grey, fontsize=8.5, ha="center")

ax2.annotate("the timetable compounds:\nvalue ×2, wait ×2 each generation —\n"
             "the depth is always K/wait = 1/ln2 ≈ 1.443× its own clock",
             xy=(6394, 14.5), xytext=(20000, 6.5),
             fontsize=9, color=lab, ha="left",
             arrowprops=dict(arrowstyle="-", color=lab, lw=1.0))

ax2.set_xlim(0.8, 3e5); ax2.set_ylim(0.8, 19.5)
ax2.set_xticks([1, 8, 100, 302, 1000, 6394, 10000, 42944, 1e5, 189146])
ax2.set_xticklabels(["1", "8", "100", "302", "1k", "6.4k", "10k", "43k", "100k", "189k"],
                    fontsize=8)
ax2.set_yticks([1, 3, 6, 9, 12, 15, 18])
ax2.set_yticklabels(["2", "8", "64", "512", "4k", "32k", "256k"], fontsize=8.5)
ax2.set_xlabel("rung N (log) — the records' own timetable", fontsize=9.5)
ax2.set_ylabel("record value (log₂)", fontsize=9.5)
ax2.grid(alpha=0.12, which="both")
ax2.set_title("scheduled by its own depth — each record sets the next clock",
              fontsize=12, pad=10)

fig.text(0.5, 0.012,
         "rahel: the wait is the record, inverted. exact form: P(q>K)=log₂((K+1)/K), so mean=1/p≈K·ln2, "
         "median=ln2/p≈K·(ln2)². the where's tail is base-2, the count's clock base-e — one seam, two conversions. "
         "and the next record lands at ~2K, setting the next clock at ~2K·ln2: the timetable doubles, K/wait = 1/ln2 always.",
         ha="center", fontsize=9.5, color=lab, style="italic")

out = "/home/sprite/slop-salon-lou/assets/self_scheduled_clock.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("wrote", out)
