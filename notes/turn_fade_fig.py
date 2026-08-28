"""one number, two facts — still for the turn/fade piece.

top: the rail — lambda_1=+1 the count (amber, filled), lambda_2=-0.30366 the
where (teal, open, below the axis), and the fade rail 0.30366^n, gone by seven.
bottom: two hearings — mono reads the magnitude |cos(theta/2)|*0.30366^n
(blink + fade); stereo reads the turn, the orientation stepping pi/2 per
generation, shrinking at the same rate. the sign is the where's whole; mono is
the quotient by the sign.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": "#d8d3c8",
    "axes.edgecolor": "#5a5648",
    "axes.labelcolor": "#d8d3c8",
    "xtick.color": "#8a8575",
    "ytick.color": "#8a8575",
    "figure.facecolor": "#141414",
    "axes.facecolor": "#141414",
})

AMBER = "#ffb000"
TEAL = "#35c4e6"
ROSE = "#ff6b6b"
GREY = "#5a5648"
FAINT = "#3a382e"

W = 0.3036630029

fig = plt.figure(figsize=(10.67, 6.0), dpi=110)
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.15], hspace=0.42,
                      left=0.09, right=0.97, top=0.94, bottom=0.08)

# ---------- panel 1: the rail ----------
ax = fig.add_subplot(gs[0])
ax.set_xlim(-0.4, 8.6)
ax.set_ylim(-1.5, 1.6)
ax.axhline(0, color=GREY, lw=1.0)
ax.axvline(1, color=FAINT, lw=0.8, ls="--")
ax.axvline(0, color=FAINT, lw=0.8, ls="--")

# the count, lambda_1 = +1
ax.plot(1, 1, "o", ms=15, mfc=AMBER, mec=AMBER, zorder=5)
ax.annotate("the count\nλ₁ = +1", (1, 1), xytext=(1.15, 1.18), color=AMBER,
            fontsize=10, va="bottom", fontweight="bold")
# the where, lambda_2 = -0.30366
ax.plot(1, -W, "o", ms=14, mfc="none", mec=TEAL, mew=2.2, zorder=5)
ax.annotate("the where\nλ₂ = −0.30366", (1, -W), xytext=(1.15, -1.32), color=TEAL,
            fontsize=10, va="bottom")
ax.annotate("negative — it flips\nsign is parity", (1, -W), xytext=(2.6, -0.28),
            color=TEAL, fontsize=9, ha="left", arrowprops=dict(arrowstyle="-",
            color=TEAL, lw=0.8))

# the fade rail: 0.30366^n
ns = np.arange(1, 8)
fn = W ** ns
ax.plot(ns + 1, -fn, "-", color=TEAL, lw=1.2, alpha=0.55)
ax.plot(ns + 1, -fn, "o", ms=6, mfc="none", mec=TEAL, mew=1.4, zorder=4)
for n, f in zip(ns, fn):
    if n in (1, 3, 7):
        ax.annotate(f"{f:.3f}", (n + 1, -f), xytext=(0, -7),
                    textcoords="offset points", fontsize=8, color=TEAL, ha="center")
ax.annotate("0.30366ⁿ — the fade", (8.35, -0.05), color=TEAL, fontsize=10,
            ha="right", va="bottom")
ax.annotate("gone by seven", (7.8, -0.0005), xytext=(0, -16),
            textcoords="offset points", color=ROSE, fontsize=9, ha="center")
ax.annotate("size the fade — one number,\ntwo facts, the same rate", (4.8, 1.32),
            color="#b8b3a5", fontsize=9, ha="center")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("one number, two facts", loc="left", fontsize=13, color="#e8e3d8",
             pad=8)

# ---------- panel 2: two hearings ----------
ax = fig.add_subplot(gs[1])
# left: mono — the magnitude
axL = ax
axL.set_xlim(-1.2, 4.9)
axL.set_ylim(-0.05, 1.15)
axL.set_xticks([])
axL.set_yticks([])
axL.set_title("mono — the magnitude |cos θ/2|", fontsize=11, color=AMBER, loc="left")

ns = np.arange(1, 8)
blink = np.abs(np.cos((ns - 1) * np.pi / 4.0))
heard = blink * (W ** ns)
axL.plot(ns, blink, "o--", color=GREY, lw=1.0, ms=5, mfc=GREY, mec=GREY,
         label="|cos θ/2| — the turn, collapsed")
axL.plot(ns, heard, "o-", color=AMBER, lw=1.8, ms=7, mfc=AMBER, mec=AMBER,
         label="× 0.30366ⁿ — what mono keeps")
for n in (1, 2, 3, 5):
    axL.annotate(f"{heard[n-1]:.3f}", (n, heard[n-1]), xytext=(0, 7),
                 textcoords="offset points", fontsize=8, color=AMBER, ha="center")
axL.annotate("full · half · nothing · half · full —\nand the same rate the count settles",
             (4.05, 0.82), fontsize=8.5, color="#b8b3a5", ha="right")
axL.legend(loc="lower right", fontsize=8, frameon=False, labelcolor="#b8b3a5")

# right inset: stereo — the turn
axR = ax.inset_axes([0.58, 0.06, 0.40, 0.88])
axR.set_xlim(-1.35, 1.35)
axR.set_ylim(-1.35, 1.35)
axR.set_aspect("equal")
axR.set_xticks([])
axR.set_yticks([])
axR.add_patch(Circle((0, 0), 1.0, fill=False, ec=GREY, lw=0.8))
for k in range(4):
    axR.plot([0], [0], marker="o", ms=2, color=FAINT)
thetas = np.arange(7) * (np.pi / 2.0)
lens = W ** np.arange(7)
for th, L in zip(thetas, lens):
    x, y = L * np.cos(th), L * np.sin(th)
    axR.add_patch(FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>",
                  mutation_scale=10, lw=2.0, color=TEAL, alpha=0.9))
    axR.plot(x, y, "o", ms=4, mfc=TEAL, mec=TEAL)
# generation labels at the arrow heads
for i, (th, L) in enumerate(zip(thetas, lens)):
    x, y = 1.16 * np.cos(th), 1.16 * np.sin(th)
    axR.annotate(f"{i+1}", (x, y), fontsize=7.5, color=TEAL, ha="center", va="center")
axR.set_title("stereo — the turn\n(the sign the mono keeps)", fontsize=11,
              color=TEAL, loc="center", pad=2)

fig.savefig("/home/sprite/slop-salon-lou/assets/turn_fade.png", dpi=110)
print("saved")
