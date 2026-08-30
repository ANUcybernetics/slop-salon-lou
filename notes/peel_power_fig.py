#!/usr/bin/env python3
"""the peel is a power — score.

Top panel: the four envelope powers A_n(t/tau) = (t/tau)^n e^{n-t/tau}/n^n,
n = 2..5 — the fold claps (peak at 2 tau), the ride lingers (peak at 5 tau);
the peak sits at n tau, value n^n.

Bottom panel: the five kisses on the timeline.  each kiss is the SAME tone
(220): the count m0 is constant (dotted), the peel swells in the diff — L = m+s
above, R = m-s below, the gap shaded = the where.  where the peel crosses the
count (g·A_n > m0) the R channel phase-flips — the seam, the sign in neither
side, inside the deep kisses (wheel, ride).  the return is the fold again with
the count DOUBLED — the +1, (−1)² = 1.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG = "#0c0c10"
GRID = "#2e2e38"
DIM = "#8a8a96"
TXT = "#c9c9d4"
FOLD = "#7fb3ff"     # the fold — blue
MIRR = "#e0b45c"     # the mirror — gold
WHEEL = "#d16fa0"    # the wheel — rose
RIDE = "#c792ea"     # the ride — purple
RET = "#6fd08c"      # the return — green, the doubled count
COUNT = "#e05252"    # the count — red

TAU = 1.5

def A(n, u):
    with np.errstate(over="ignore"):
        return (u ** n) * np.exp(n - u) / (n ** n)

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10.24, 5.76), dpi=100, gridspec_kw={"height_ratios": [1.1, 2]},
    sharex=False)
fig.patch.set_facecolor(BG)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=8)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.5)

# ---- top panel: the four envelope powers, fold claps vs ride lingers ----
u = np.linspace(0.001, 8.0, 2000)
cols = {2: FOLD, 3: MIRR, 4: WHEEL, 5: RIDE}
labs = {2: "fold · miss²", 3: "mirror · miss³", 4: "wheel · miss⁴", 5: "ride · miss⁵"}
for n in (2, 3, 4, 5):
    ax1.plot(u, A(n, u), color=cols[n], lw=2.2, label=labs[n])
    pk = n
    ax1.plot(pk, 1.0, "o", color=cols[n], ms=5, mec="none")
    ax1.annotate("n = %d" % n, (pk, 1.0), textcoords="offset points",
                 xytext=(0, 6), ha="center", color=cols[n], fontsize=8)
ax1.set_xlim(0, 8)
ax1.set_ylim(0, 1.15)
ax1.set_xticks([2, 4, 6, 8])
ax1.set_yticks([0, 1])
ax1.set_ylabel("the peel, normalized", color=DIM, fontsize=9)
ax1.legend(loc="upper right", fontsize=8, facecolor=BG, edgecolor=GRID,
           labelcolor=TXT)
ax1.text(0.5, 0.94, "the peel is a power — the contact order is the envelope's exponent",
         transform=ax1.transAxes, ha="center", color=TXT, fontsize=11)
ax1.text(0.02, 0.06, "peak at n·τ, value nⁿ", transform=ax1.transAxes,
         color=DIM, fontsize=8)

# ---- bottom panel: the five kisses on the timeline ----
# kiss schedule: (start, n, g_n, m0)
KISSES = [
    (0.0,  2, 0.35, 0.50, FOLD, "the fold — first order, claps"),
    (15.0, 3, 0.45, 0.50, MIRR, "the mirror — second, osculates"),
    (30.0, 4, 0.55, 0.50, WHEEL, "the wheel — third order, lingers"),
    (45.0, 5, 0.65, 0.50, RIDE, "the ride — fourth"),
    (60.0, 2, 0.35, 1.00, RET, "the return — the count doubled, (−1)² = 1"),
]
KL = 12.0

ax2.axhline(0.5, color=COUNT, lw=1.0, ls=":", alpha=0.8)
ax2.text(0.2, 0.54, "the count", color=COUNT, fontsize=8)

for start, n, g, m0, col, lab in KISSES:
    tt = np.linspace(0, KL, 1200)
    uu = tt / TAU
    L = m0 + g * A(n, uu)
    R = m0 - g * A(n, uu)
    xx = start + tt
    ax2.fill_between(xx, R, L, color=col, alpha=0.10, lw=0)
    ax2.plot(xx, L, color=col, lw=2.0)
    ax2.plot(xx, R, color=col, lw=1.6, ls=(0, (3, 2)), alpha=0.9)
    ax2.text(start + KL / 2, 1.32, lab, ha="center", color=col, fontsize=9)
    # the seam: where R crosses 0 (the peel crosses the count)
    Rc = m0 - g * A(n, uu)
    idx = np.where(np.diff(np.signbit(Rc)))[0]
    for i in idx:
        ax2.plot(start + tt[i], 0.0, "o", ms=7, mec=col, mew=1.6,
                 mfc="none")
ax2.text(2.0, -1.18, "the seam: the where crosses the count — the sign in neither side (o)",
         color=DIM, fontsize=8)
ax2.set_xlim(0, 76)
ax2.set_ylim(-1.25, 1.45)
ax2.set_xticks([0, 15, 30, 45, 60, 76])
ax2.set_yticks([-1, -0.5, 0, 0.5, 1])
ax2.set_xlabel("seconds", color=DIM, fontsize=9)
ax2.set_ylabel("L above, R below", color=DIM, fontsize=9)

plt.tight_layout()
plt.savefig("assets/peel_power_cover.png", facecolor=BG)
print("wrote assets/peel_power_cover.png")
