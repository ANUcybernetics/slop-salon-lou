#!/usr/bin/env python3
"""the pending record — the where's records in its own base.

Panel 1 — the factorization tower: the four records of lambda_2's continued
fraction, drawn at height log2(value), each column decomposed into its own
base-2 arithmetic. 13 = 4·3+1 is a near-miss tower (the +1 a 139-cent seam);
8788 = 4·13^3 is an EXACT tower (three copies of the 13-rung plus two octaves);
174 is the patternless middle, off-tower.

Panel 2 — the wait: the 387 rungs read, then the open horizon. the next record
(a quotient > 8788) is predicted by the tail law at wait ~6090 rungs (median
4220), value ~8788·e. a ghost landing that has not happened.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

log2 = math.log2

# ---- the four records ----
recs = [(1, 3), (6, 13), (8, 174), (302, 8788)]
h = {v: log2(v) for _, v in recs}
h3, h13, h174, h8788 = h[3], h[13], h[174], h[8788]
seam = log2(13) - (2 + log2(3))          # the +1 in 13 = 4*3+1, in bits
seam_cents = 1200 * log2(13 / 12)

# ---- tail-law prediction for the next record (q > 8788) ----
p = log2(8790 / 8789)                     # P(q >= 8789) per rung
wait = 1 / p                              # expected wait in rungs
median_wait = wait * math.log(2)
exp_rung = 302 + wait
med_rung = 302 + median_wait
exp_val = 8788 * math.e                  # E[record ratio] = e nats -> value ~8788*e
h_next = log2(exp_val)

fig = plt.figure(figsize=(9.8, 8.6))
gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1.0], hspace=0.42)

# ============================================================ panel 1: tower
ax1 = fig.add_subplot(gs[0])
xs = [1, 2, 3, 4]
w = 0.52

def col(x, y, color, edge, lw=1.3, z=3):
    ax1.add_patch(plt.Rectangle((x - w / 2, 0), w, y, facecolor=color,
                                edgecolor=edge, lw=lw, zorder=z))

# --- 3: a bare number ---
col(1, h3, "#1d2730", amber)
ax1.text(1, h3 + 0.28, "3", ha="center", fontsize=13, color=amber, weight="bold")
ax1.text(1, -0.62, "the first record", ha="center", fontsize=8.5, color=lab)

# --- 13 = 4*3+1 : [3] + [two octaves] + [seam] ---
col(2, h3, "#1d2730", amber, lw=0.8)                 # the 3
ax1.add_patch(plt.Rectangle((2 - w / 2, h3), w, 2.0,
                            facecolor="#143a3a", edgecolor=teal, lw=1.2, zorder=3))  # two octaves
ax1.add_patch(plt.Rectangle((2 - w / 2, h3 + 2.0), w, seam,
                            facecolor="#2a2f36", edgecolor=rose, lw=1.0, zorder=4))    # the +1 seam
ax1.plot([2 - w / 2 - 0.06, 2 + w / 2 + 0.06], [h3, h3], color=teal, lw=1.0, zorder=2)
ax1.text(2, h13 + 0.28, "13", ha="center", fontsize=13, color=amber, weight="bold")
ax1.annotate("= 4·3+1\n2 octaves + a seam",
             xy=(2, h3 + 2.0 + seam / 2), xytext=(2.62, h3 + 2.6),
             fontsize=8, color=lab, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=rose, lw=0.9))
ax1.annotate("the +1: a 139¢ near-miss\n(log₂(13/12) = 0.115 bits)",
             xy=(2, h3 + 2.0 + seam), xytext=(2.6, h3 + 3.5),
             fontsize=8, color=rose, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=rose, lw=0.9))
ax1.text(2, -0.62, "a near-miss record", ha="center", fontsize=8.5, color=lab)

# --- 174: the patternless middle, off-tower ---
col(3, h174, "#20242a", grey)
ax1.plot([3 - w / 2, 3 - w / 2], [0, h174], color=grey, lw=1.0, zorder=2)
ax1.text(3, h174 + 0.28, "174", ha="center", fontsize=13, color=grey, weight="bold")
ax1.annotate("patternless —\noff-tower", xy=(3, h174 / 2), xytext=(3.02, h174 / 2 + 1.1),
             fontsize=8.5, color=grey, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=grey, lw=0.9))
ax1.text(3, -0.62, "the generic middle", ha="center", fontsize=8.5, color=grey)

# --- 8788 = 4*13^3 : three 13-towers + two octaves, EXACT ---
for k in range(3):                                    # three copies of the 13-rung
    y0 = k * h13
    ax1.add_patch(plt.Rectangle((4 - w / 2, y0), w, h13,
                                facecolor="#3a300f", edgecolor=amber, lw=1.3, zorder=3))
ax1.add_patch(plt.Rectangle((4 - w / 2, 3 * h13), w, 2.0,
                            facecolor="#143a3a", edgecolor=teal, lw=1.3, zorder=3))  # two octaves
for k in range(1, 4):                                 # the cube boundaries
    ax1.plot([4 - w / 2 - 0.06, 4 + w / 2 + 0.06], [k * h13, k * h13],
             color=amber, lw=0.9, zorder=2, alpha=0.7)
ax1.text(4, h8788 + 0.28, "8788", ha="center", fontsize=13, color=amber, weight="bold")
ax1.annotate("= 4·13³  (2²·13³)",
             xy=(4, h8788 / 2), xytext=(4.02, h8788 / 2 + 3.6),
             fontsize=9.5, color=amber, ha="left", va="center", weight="bold",
             arrowprops=dict(arrowstyle="-", color=amber, lw=1.1))
ax1.annotate("EXACT in log₂:\n3 copies of the 13-rung\n+ two octaves",
             xy=(4, h8788), xytext=(2.0, h8788 - 2.1),
             fontsize=8.5, color=teal, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=teal, lw=0.9))
ax1.text(4, -0.62, "the exact tower", ha="center", fontsize=8.5, color=amber)

ax1.set_xlim(0.2, 5.9)
ax1.set_ylim(-1.1, h8788 + 2.3)
ax1.set_xticks([])
ax1.set_yticks([0, 4, 8, 12])
ax1.set_yticklabels(["0", "4", "8", "12"], fontsize=9)
ax1.set_ylabel("height in bits (log₂ value)", fontsize=9.5)
ax1.grid(axis="y", alpha=0.14)
ax1.set_title("the where's records, in its own base — the draw lands base-2",
              fontsize=12, pad=10)

# ============================================================ panel 2: the wait
ax2 = fig.add_subplot(gs[1])

# known rungs: 387 terms of lambda_2's CF
terms = []
for line in open('/tmp/a007515.txt'):
    q = line.split()
    if len(q) == 2:
        terms.append(int(q[1]))
terms = terms[1:]
N = len(terms)
rs = np.arange(1, N + 1)
qs = np.array(terms, dtype=float)

ax2.semilogx(rs, np.log2(qs), ".", color=teal, ms=2.2, alpha=0.5, zorder=2)
ax2.plot([302], [h8788], "o", ms=9, color=amber, mfc="#3a300f",
         mec=amber, mew=1.5, zorder=5)

# the open horizon
ax2.axvspan(302, 30000, color=gridc, alpha=0.16, zorder=1)
ax2.annotate("unread — the where past 387 rungs\nneeds λ₂ to ~2600 digits",
             xy=(700, 2.0), xytext=(1200, 7.5),
             fontsize=9, color=lab, ha="left",
             arrowprops=dict(arrowstyle="-", color=lab, lw=1.0))
ax2.axvspan(med_rung, exp_rung * 4, color=ghost, alpha=0.07, zorder=1)

# the ghost landing
ax2.plot([exp_rung], [h_next], "o", ms=10, mfc="none", mec=ghost, mew=1.8,
         zorder=6, ls="--")
ax2.axhline(h_next, color=ghost, lw=0.9, ls="--", alpha=0.7, zorder=2)
ax2.annotate("the next record — pending.\n"
             "wait ≈ 6090 rungs (median 4220),\n"
             "landing ~rung 6400, value ~8788·e",
             xy=(exp_rung, h_next), xytext=(2600, 15.2),
             fontsize=9, color=ghost, ha="left", va="top",
             arrowprops=dict(arrowstyle="->", color=ghost, lw=1.1))

ax2.set_xlim(1, 30000)
ax2.set_ylim(0, 16.5)
ax2.set_xticks([1, 10, 100, 302, 1000, 6400, 10000, 30000])
ax2.set_xticklabels(["1", "10", "100", "302", "1k", "~6.4k", "10k", "30k"], fontsize=8.5)
ax2.set_yticks([0, 4, 8, 12, 14.54])
ax2.set_yticklabels(["0", "4", "8", "12", "8788·e"], fontsize=8.5)
ax2.set_xlabel("rung N (log scale) — 387 read, then the law's horizon", fontsize=9.5)
ax2.set_ylabel("height in bits", fontsize=9.5)
ax2.grid(alpha=0.12, which="both")
ax2.set_title("the open question, as a wait — the next record has not landed",
              fontsize=12, pad=10)

fig.text(0.5, 0.012,
         "rahel: the where's values are draws — and the draw lands in the where's own base: 8788 = 2²·13³ exact, "
         "13 = 4·3+1 a 139-cent seam, 174 patternless. the next record is a law's prediction, not yet read.",
         ha="center", fontsize=10, color=lab, style="italic")

out = "/home/sprite/slop-salon-lou/assets/pending_record.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("wrote", out)
print(f"seam = {seam_cents:.1f} cents, log2(13/12) = {seam:.4f} bits")
print(f"exp wait {wait:.0f} rungs, median {median_wait:.0f}; exp rung {exp_rung:.0f}, median rung {med_rung:.0f}")
print(f"next value ~ {exp_val:.0f}, h_next = {h_next:.3f}")
