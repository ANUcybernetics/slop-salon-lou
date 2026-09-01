#!/usr/bin/env python3
"""Figure: the tail is one law; the records are five signatures.

Reads /tmp/grid_tail.json (walks of five intervals, N=50000).
Top: strike counts of every quotient ride the single Gauss-Kuzmin curve —
     the seed 55 is just a point on everyone's tail.
Bottom: each interval's record ladder is its own — crown, breach, bar (the
     first >=8x jump, the slam), and the shadow gap (breach, bar) that bars
     every grid point above the seed.
"""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

N = 50000
data = json.load(open("/tmp/grid_tail.json"))
intervals = ["3/2", "5/4", "6/5", "9/8", "16/15"]
colors = {"3/2": "#b0413e", "5/4": "#e0a458", "6/5": "#5e7c6c",
          "9/8": "#7d6b91", "16/15": "#4a7fa5"}

def gk(k):
    return math.log2((k + 1) ** 2 / (k * (k + 2)))

def slam(rec):
    """Find crown, breach, bar: the first record >= 8x the previous is the
    bar; the record before it is the breach; the one before that the crown."""
    vals = [v for (r, v) in rec]
    for j in range(1, len(vals)):
        if vals[j] >= 8 * vals[j - 1]:
            return {"crown": vals[j - 2] if j >= 2 else vals[0],
                    "breach": vals[j - 1], "bar": vals[j]}
    return {"crown": vals[-2] if len(vals) > 1 else vals[0],
            "breach": vals[-2] if len(vals) > 1 else vals[0],
            "bar": vals[-1]}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9),
                               gridspec_kw={"height_ratios": [1.15, 1]})

# ---- top: the universal tail ----
ks = np.arange(1, 501)
ax1.plot(ks, N * np.array([gk(k) for k in ks]), color="black", lw=1.8,
         label="Gauss–Kuzmin tail  N·log₂((k+1)²/k(k+2))")
for iv in intervals:
    st = data[iv]["strikes"]
    x, y = [], []
    for k in ks:
        v = st.get(str(int(k)), 0)
        if v > 0:
            x.append(k); y.append(v)
    ax1.scatter(x, y, s=13, color=colors[iv], alpha=0.5, label=iv, zorder=3)
ax1.axvline(55, color="gray", ls=":", lw=1)
ax1.text(55, N * gk(55) * 2.5, "the seed 55\nis just a point\non the tail",
         ha="center", fontsize=8, color="dimgray")
ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlabel("quotient k")
ax1.set_ylabel("strikes in 50,000 rungs")
ax1.set_title("every integer is a quotient — the tail is one law, everyone's",
              fontsize=12)
ax1.legend(fontsize=8, ncol=3, loc="upper right")
ax1.set_xlim(0.9, 600)
ax1.set_ylim(0.7, 50000)

# ---- bottom: the record ladders ----
for i, iv in enumerate(intervals):
    rec = data[iv]["records"]
    vals = [v for (r, v) in rec]
    S = slam(rec)
    base = 4.5 - i
    ax2.plot(vals, [base] * len(vals), color=colors[iv], lw=1.1, alpha=0.7)
    ax2.scatter(vals, [base] * len(vals), s=26, color=colors[iv], zorder=4)
    # shadow gap (breach, bar)
    ax2.axvspan(S["breach"], S["bar"], color=colors[iv], alpha=0.12, zorder=1)
    # crown marker
    ax2.scatter([S["crown"]], [base], s=80, color=colors[iv], zorder=5,
                edgecolor="white", linewidths=1.0)
    # label: crown + bar
    ax2.annotate(f"{iv}   crown {S['crown']}   bar {S['bar']}",
                 xy=(S["crown"], base), xytext=(max(S["crown"] * 1.9, 3), base),
                 fontsize=8.5, va="center", color=colors[iv])
ax2.axvline(55, color="gray", ls=":", lw=1)
ax2.text(55, 5.15, "55 — the A1 convention", fontsize=8, ha="center",
         color="dimgray")
ax2.set_yticks([])
ax2.set_ylim(-0.2, 5.6)
ax2.set_xlim(1.5, 600000)
ax2.set_xscale("log")
ax2.set_xlabel("record quotient (log)")
ax2.set_title("the records are the only thing each walk keeps for itself —\n"
              "crown (·) · breach · bar · the shadow the bar casts",
              fontsize=12)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-lou/assets/grid_tail.png", dpi=150)
print("saved assets/grid_tail.png")
