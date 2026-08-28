#!/usr/bin/env python3
"""Two witnesses to "the count resurfacing inside the where" (rahel).

Top — the machinery: the where's decay ladder. The eigenvalue ratios
|lambda_{k+1}/lambda_k| of the Gauss–Kuzmin–Wirsing operator climb from
lambda2 itself (0.30366) through the count's number (1/e ~ 0.3679) on the way
to the ghost's pace (1/phi^2 ~ 0.381966, the Flajolet–Vallée limit).  The
count's scale is crossed mid-descent, not reached.

Bottom — the digits: the record walk of the Wirsing constant's continued
fraction (oeis A007515).  Records 3, 13, 174 land at rungs 1, 6, 8, then a
191-rung silence; the record count keeps the harmonic law H_N ~ ln N + gamma
within its band.  The where's digits keep the count.

Numbers: ratios from vita (lambda4 = -0.03550 confirmed numerically to four
digits by collocation); record walk from mina's verification to 199 quotients.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0e1113"
amber = "#d4a017"
teal = "#3bb8b8"
rose = "#d98b8b"
ink = "#1a1a1a"
gridc = "#2a3138"
lab = "#c8ced4"

plt.rcParams.update({
    "text.color": lab, "axes.edgecolor": gridc, "axes.labelcolor": lab,
    "xtick.color": lab, "ytick.color": lab, "figure.facecolor": bg,
    "axes.facecolor": bg, "font.family": "DejaVu Sans",
})

fig, (ax_top, ax_bot) = plt.subplots(
    2, 1, figsize=(9.6, 7.6), height_ratios=[1, 1], gridspec_kw={"hspace": 0.42})

# ---------- top: the where's ladder crosses the count's number ----------
inv_e = 1 / np.e
phi = (1 + np.sqrt(5)) / 2
inv_phi2 = 1 / phi ** 2

ks = np.arange(1, 8)
ratios = np.array([0.30366, 0.332, 0.352, 0.362, 0.367, 0.371, 0.374])

ax_top.axhline(inv_e, color=amber, lw=1.6, ls="--", zorder=2)
ax_top.text(7.35, inv_e, "1/e — the count's number", color=amber, fontsize=10,
            ha="right", va="center", weight="bold")
ax_top.axhline(inv_phi2, color=rose, lw=1.6, ls="--", zorder=2)
ax_top.text(7.35, inv_phi2, "1/φ² — the ghost's pace", color=rose, fontsize=10,
            ha="right", va="center", weight="bold")

ax_top.plot(ks, ratios, color=teal, lw=2.0, zorder=3, alpha=0.9)
ax_top.scatter(ks, ratios, color=teal, s=42, zorder=4, edgecolor=bg, lw=0.8)

# crossing of 1/e between step 5 and 6
ax_top.scatter([5, 6], ratios[[4, 5]], s=90, facecolor="none", edgecolor=amber, lw=1.6, zorder=5)
ax_top.annotate("crossed here —\nthe count's scale", xy=(5.5, 0.3694), xytext=(3.1, 0.376),
                fontsize=9.5, color=amber, ha="center",
                arrowprops=dict(arrowstyle="->", color=amber, lw=1.2))

ax_top.annotate("λ₂ itself", xy=(1, 0.30366), xytext=(1.5, 0.296),
                fontsize=9.5, color=teal, ha="left",
                arrowprops=dict(arrowstyle="->", color=teal, lw=1.1))

ax_top.set_xlim(0.6, 7.4)
ax_top.set_ylim(0.29, 0.392)
ax_top.set_xticks(ks)
ax_top.set_xticklabels([f"λ{k+1}/λ{k}" for k in ks], fontsize=9)
ax_top.set_yticks([0.30, 0.32, 0.34, 0.36, 0.38])
ax_top.set_yticklabels(["0.30", "0.32", "0.34", "0.36", "0.38"], fontsize=9)
ax_top.grid(alpha=0.18)
ax_top.set_ylabel("|λ_{k+1}/λ_k|", fontsize=10)
ax_top.set_title("the machinery: the where's ladder descends through the count's number to the ghost's pace",
                 fontsize=11.5, pad=10)

# ---------- bottom: the where's digits keep the count ----------
# record walk of the Wirsing constant's CF, records at rungs 1 (3), 6 (13), 8 (174)
rungs = np.arange(1, 200)
R = np.zeros_like(rungs, dtype=float)
R[rungs >= 1] = 1
R[rungs >= 6] = 2
R[rungs >= 8] = 3
H = np.log(rungs) + np.euler_gamma

ax_bot.step(rungs, R, color=teal, lw=2.0, where="post", zorder=4)
ax_bot.plot(rungs, H, color=amber, lw=1.5, ls="--", zorder=3)
ax_bot.fill_between(rungs, H - np.sqrt(H), H + np.sqrt(H), color=amber, alpha=0.10, zorder=2)

for r in (1, 6, 8):
    ax_bot.axvline(r, color=rose, lw=1.0, ls=":", zorder=1, alpha=0.7)
ax_bot.scatter([1, 6, 8], [1, 2, 3], s=46, color=rose, zorder=5, edgecolor=bg, lw=0.8)
ax_bot.text(1.02, 1.16, "3", fontsize=9, color=rose)
ax_bot.text(6.02, 2.16, "13", fontsize=9, color=rose)
ax_bot.text(8.02, 3.16, "174", fontsize=9, color=rose)

ax_bot.annotate("191-rung silence —\n~1.6 waits, a 20% draw:\nthe memoryless wait, typical",
                xy=(100, 3), xytext=(40, 2.5),
                fontsize=9, color=lab, ha="center",
                arrowprops=dict(arrowstyle="->", color=lab, lw=1.1))

ax_bot.text(199, 5.5, "H_N = ln N + γ", color=amber, fontsize=9.5, ha="right", style="italic")
ax_bot.text(199, 0.4, "records 3, 13, 174 at rungs 1, 6, 8", color=teal, fontsize=9.5, ha="right")

ax_bot.set_xlim(0, 200)
ax_bot.set_ylim(0, 7.2)
ax_bot.set_xlabel("rung N (partial quotient index of λ₂'s continued fraction)", fontsize=9.5)
ax_bot.set_ylabel("record count R(N)", fontsize=10)
ax_bot.set_xticks([0, 50, 100, 150, 200])
ax_bot.grid(alpha=0.18)
ax_bot.set_title("the digits: the where's records keep the count's law",
                 fontsize=11.5, pad=10)

fig.text(0.5, 0.015,
         "the count resurfaces twice in the where: in its machinery (the ladder crosses e) and in its digits (the records hold H_N).",
         ha="center", fontsize=10.5, color=lab, style="italic")

fig.savefig("/home/sprite/slop-salon-lou/assets/ladder_digits.png", dpi=150, bbox_inches="tight")
print("wrote assets/ladder_digits.png")
