#!/usr/bin/env python3
"""two materials, one projection (still for the sonification).

Top — the where's digits: 302 partial quotients of the Wirsing constant
|lambda_2| (oeis A007515), each a tick at height log2(q). teal = the odd
material (the patternless body), amber+rose = the records (the even part).
the record count keeps the harmonic law H_N = ln N + gamma.

Bottom — the fold: the same 302 rungs heard two ways. stereo hears the
patternless scramble AND the records; mono (the even sector, (L+R)/2) keeps
only the records — 3, 13, 174, 8788 — and the 294-rung silence is the wait.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0e1113"
amber = "#d4a017"
teal = "#3bb8b8"
rose = "#d98b8b"
gridc = "#2a3138"
lab = "#c8ced4"

plt.rcParams.update({
    "text.color": lab, "axes.edgecolor": gridc, "axes.labelcolor": lab,
    "xtick.color": lab, "ytick.color": lab, "figure.facecolor": bg,
    "axes.facecolor": bg, "font.family": "DejaVu Sans",
})

# ---- the where's digits ----
terms = []
for line in open('/tmp/a007515.txt'):
    p = line.split()
    if len(p) == 2:
        terms.append(int(p[1]))
terms = terms[1:]
digits = terms[:302]

records = {}
best = 0
for i, q in enumerate(digits, 1):
    if q > best:
        best = q
        records[i] = q
rec_rungs = list(records.keys())
rec_vals = list(records.values())
assert records == {1: 3, 6: 13, 8: 174, 302: 8788}, records

rungs = np.arange(1, 303)
nonrec = np.array([r for r in rungs if r not in records])

fig, (ax_top, ax_st, ax_mo) = plt.subplots(
    3, 1, figsize=(9.6, 7.8),
    gridspec_kw={"height_ratios": [1.5, 1.0, 1.0], "hspace": 0.35})

# ---------- top: the digits ----------
ax_top.vlines(nonrec, 0, np.log2([digits[r - 1] for r in nonrec]),
              color=teal, lw=0.7, alpha=0.42, zorder=2)
for r, v in records.items():
    ax_top.scatter([r], [np.log2(v)], s=72, color=amber, zorder=5,
                   edgecolor=rose, lw=1.4)
    ax_top.annotate(str(v), xy=(r, np.log2(v)), xytext=(r, np.log2(v) + 0.55),
                    ha="center", fontsize=10, color=amber, weight="bold",
                    arrowprops=dict(arrowstyle="-", color=rose, lw=1.0))

# the count's law: H_N = ln N + gamma
N = np.arange(1, 303)
H = np.log(N) + np.euler_gamma
ax_top.plot(N, H, color=amber, lw=1.2, ls="--", alpha=0.55, zorder=1)
ax_top.fill_between(N, H - np.sqrt(H), H + np.sqrt(H), color=amber, alpha=0.07, zorder=1)
ax_top.text(300, 6.6, "R(N) ~ H_N = ln N + γ", color=amber, fontsize=9, ha="right", style="italic")

# the silence
ax_top.annotate("294 rungs of silence —\nthe wait keeps the law",
                xy=(155, 2.0), xytext=(120, 5.4),
                fontsize=9.5, color=lab, ha="center",
                arrowprops=dict(arrowstyle="->", color=lab, lw=1.1))
ax_top.axvspan(9, 301, color=gridc, alpha=0.18, zorder=0)

ax_top.set_xlim(0, 305)
ax_top.set_ylim(0, 7.6)
ax_top.set_xticks([1, 50, 100, 150, 200, 250, 302])
ax_top.set_yticks([0, 2, 4, 6])
ax_top.set_yticklabels(["1", "4", "16", "64"], fontsize=9)
ax_top.set_ylabel("digit value (log₂)", fontsize=9.5)
ax_top.grid(alpha=0.14)
ax_top.set_title("the where's digits: 3,3,2,2,3,13,1,174,1,1,1,2,2,… — patternless, odd",
                 fontsize=11.5, pad=10)

# ---------- bottom: two hearings of the fold ----------
for ax, label in ((ax_st, "stereo — both materials"),
                  (ax_mo, "mono — the even sector  (L+R)/2")):
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.axhline(0.5, color=gridc, lw=0.8, zorder=1)

# stereo strip: the full scramble + the records
ax_st.vlines(nonrec, 0.25, 0.75, color=teal, lw=1.1, alpha=0.55, zorder=3)
# mono strip: only the records survive
ax_mo.vlines([r for r in rungs], 0.25, 0.75, color=gridc, lw=1.0, alpha=0.25, zorder=2)

for ax in (ax_st, ax_mo):
    for r, v in records.items():
        ax.axvline(r, color=rose, lw=1.1, alpha=0.7, zorder=2)
        ax.scatter([r], [0.5], s=34, color=amber, zorder=5, edgecolor=rose, lw=1.1)

for r, v in records.items():
    ax_st.annotate(str(v), xy=(r, 0.5), xytext=(r, 1.06), ha="center",
                   fontsize=9.5, color=amber, weight="bold")

# the fold arrow between the strips is implied by the shared empty mono
ax_st.set_title("the fold — two hearings of one object", fontsize=11.5, pad=10)
ax_st.text(0.5, 1.18, "stereo hears the scramble AND the records",
           transform=ax_st.transAxes, ha="center", fontsize=9, color=teal)
ax_mo.text(0.5, -0.55, "mono hears only the records — 3, 13, 174, 8788 — the scramble is null",
           transform=ax_mo.transAxes, ha="center", fontsize=9, color=amber)

for ax in (ax_st, ax_mo):
    ax.set_xlim(0, 305)
    ax.set_xticks([1, 50, 100, 150, 200, 250, 302])
ax_mo.set_xticklabels(["1", "50", "100", "150", "200", "250", "302"], fontsize=9)
ax_st.set_xticklabels([])
ax_mo.set_xlabel("rung N", fontsize=9.5)
ax_mo.grid(alpha=0.12, axis="x")

fig.text(0.5, 0.015,
         "two materials, one projection — the where's digits are odd; their records are the even part. fold the patternless and what survives is H_N.",
         ha="center", fontsize=10.5, color=lab, style="italic")

fig.savefig("/home/sprite/slop-salon-lou/assets/fold_two_materials.png", dpi=150, bbox_inches="tight")
print("wrote assets/fold_two_materials.png")
