#!/usr/bin/env python3
"""the silver mirror — the operator's axis at three-eighths of a turn.

rahel: "the strike is a scaled reflection: T/√2 det −1, a mirror has an axis —
the pair 1:(1+√2), silver, one strike leaves unchanged. the count-pair 1:4 sits
off the axis and turns: one strike reflects it to 3:5, two bring it home
doubled."

What the axis is, exactly.  T(a,b) = (b−a, b+a), and T/√2 is a reflection whose
axis is the +1 eigenspace — slope 1+√2 = tan(3π/8), the silver ratio, three
eighths of a turn.  Its perpendicular (the −1 eigenspace, the sign) has slope
−(√2−1) = −tan(π/8).  The two tangents are reciprocal:

    tan(π/8) · tan(3π/8) = (√2−1)(√2+1) = 1   — the identity
    (tan(π/8) + tan(3π/8))/2 = √2            — the doubling

The doubling is the arithmetic mean of the mirror's two sides; their product is
the identity.  And the axis is the count's diagonal (y=x, the trivial character
through the wheel's 1 and 3) turned one eighth of a turn: π/4 + π/8 = 3π/8.  The
sign's side is the other diagonal (135°) turned the same eighth: 7π/8.

The count-pair 1:4 sits 8.5° off the mirror.  One strike reflects it across the
mirror to the 3:5 direction and scales by √2 — T(1,4) = (3,5), the heard chain.
Two strikes are the reflection squared (the identity) times 2: the ratio home,
doubled — (110,440), on the 1:4 ray again.

The seat of the sign — the ordered pair 1:3, one of the wheel's square corners —
leans nearest the mirror, 4.1° off: the sign's own seat is the one the mirror
almost fixes.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG = "#0c0c10"
GRID = "#3a3a44"
TXT = "#c9c9d4"
DIM = "#8a8a96"
ROSE = "#d16fa0"      # the strike / the wheel
GOLD = "#f0c26a"      # the mirror / the count-pair
TANG = "#c792ea"      # the sign
FOLD = "#7fb3ff"      # the count's diagonal (the trivial)

fig, ax = plt.subplots(figsize=(11.8, 7.6), dpi=110)
ax.set_facecolor(BG)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=DIM, labelsize=9)
ax.set_aspect("equal")

C = 110.0
G = 220.0
S2 = np.sqrt(2.0)

# ---- the count's diagonal (y = x) and its perpendicular (y = −x), faint ----
xr = np.linspace(-300, 470, 3)
ax.plot(xr, xr, color=FOLD, lw=1.3, ls=(0, (6, 4)), alpha=0.6, zorder=1)
xr2 = np.linspace(-300, 40, 3)
ax.plot(xr2, -xr2, color=FOLD, lw=1.0, ls=(0, (2, 4)), alpha=0.4, zorder=1)
ax.text(438, 372, "the count's diagonal —\n1 and 3, the trivial, at π/4",
        color=FOLD, fontsize=9, ha="right", va="top", style="italic", alpha=0.9,
        rotation=43)

# ---- the silver mirror: axis at 3π/8 (tan = 1+√2) ----
xm = np.linspace(-42, 194.5, 3)
ax.plot(xm, (1 + S2) * xm, color=GOLD, lw=3.4, zorder=3)
ax.text(150, 330, "the mirror — 3π/8\ntan = 1+√2, silver", color=GOLD,
        fontsize=10.5, fontweight="bold", va="center")

# ---- the sign: perpendicular at 7π/8 (tan = √2−1, slope −(√2−1)) ----
xs = np.linspace(-300, 10, 3)
ax.plot(xs, -(S2 - 1) * xs, color=TANG, lw=2.4, ls=":", zorder=3)
ax.text(-252, 60, "the sign — 7π/8\ntan = √2−1", color=TANG,
        fontsize=10.5, va="top", ha="center")

# ---- the count-pair ray (1:4) and its mirror-image ray (3:5) ----
r14 = (55.0, 220.0)            # the count-pair
r35 = (165.0, 275.0)           # one strike = √2 × the mirror image
ref = (r35[0] / S2, r35[1] / S2)   # the pure mirror image of 1:4
for (px, py), col in ((r14, GOLD), (r35, ROSE)):
    k = 470.0 / max(px, py)
    ax.plot([0, px * k], [0, py * k], color=col, lw=1.6, alpha=0.28, zorder=2)

# the arc showing the turn: from 1:4 to 3:5 across the mirror
th_a, th_b = np.radians(75.96), np.radians(59.04)
rad = 200.0
arc = np.linspace(th_b, th_a, 60)
ax.plot(rad * np.cos(arc), rad * np.sin(arc), color=DIM, lw=1.8, zorder=4)
mid = (th_a + th_b) / 2
ax.annotate("", xy=(rad * 0.9 * np.cos(th_a - 0.04), rad * 0.9 * np.sin(th_a - 0.04)),
            xytext=(rad * 0.9 * np.cos(th_b + 0.04), rad * 0.9 * np.sin(th_b + 0.04)),
            arrowprops=dict(arrowstyle="->", color=DIM, lw=1.5))
ax.text(rad * 1.28 * np.cos(mid + np.radians(50)), rad * 1.28 * np.sin(mid + np.radians(50)),
        "one strike turns 1:4 to 3:5 —\nthe mirror midway, 8.5° each way",
        color=DIM, fontsize=9, ha="center", style="italic")

# the count-pair, its strike, and two-strikes-home
ax.plot(*r14, "o", color=GOLD, ms=11, mec="none", zorder=6)
ax.text(r14[0] - 6, r14[1] - 22, "1:4 — the count-pair", color=GOLD,
        fontsize=9.5, ha="right", va="top")
ax.plot(*ref, "o", color=DIM, ms=5, mec="none", zorder=6)
ax.plot(*r35, "o", color=ROSE, ms=11, mec="none", zorder=6)
ax.text(r35[0] + 12, r35[1] + 8, "3:5 — one strike", color=ROSE, fontsize=9.5, ha="left")
ax.plot(110.0, 440.0, "o", color=GOLD, ms=8, mec="none", alpha=0.45, zorder=5)
ax.text(110 + 12, 440 - 2, "two strikes — the pair home, doubled", color=GOLD,
        fontsize=9, ha="left", va="center", alpha=0.9)

# ---- the sign's own seat: the ordered pair 1:3, nearest the mirror ----
ax.plot(110.0, 330.0, "s", color=TANG, ms=9, mec="none", zorder=6)
ax.text(110 + 12, 330 - 16, "1:3 — the sign's seat, 4° off the mirror", color=TANG,
        fontsize=9, ha="left", va="center")

# ---- the two tangents as an equation box ----
ax.text(0.985, 0.02,
        "tan π/8 · tan 3π/8 = (√2−1)(√2+1) = 1   —   the identity\n"
        "(tan π/8 + tan 3π/8)/2 = √2            —   the doubling",
        transform=ax.transAxes, ha="right", va="bottom",
        color=TXT, fontsize=10, linespacing=1.55,
        bbox=dict(boxstyle="round,pad=0.5", fc="#1a1a24", ec=GOLD, lw=1.0))

ax.set_xlim(-310, 470)
ax.set_ylim(-30, 470)
ax.set_xticks([110, 220, 330, 440])
ax.set_yticks([110, 220, 330, 440])
ax.set_xticklabels(["110", "220", "330", "440"])
ax.set_yticklabels(["110", "220", "330", "440"])
ax.set_xlabel("a — the lower of the struck pair", color=DIM, fontsize=10)
ax.set_ylabel("b — the higher", color=DIM, fontsize=10)

fig.text(0.5, 0.012,
         "the operator's axis is the count's diagonal turned an eighth: the mirror at 3π/8, "
         "the sign at 7π/8, the two sides reciprocal, averaging to the doubling.",
         color=TXT, fontsize=11, ha="center")

plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig("assets/silver_mirror.png", dpi=110, facecolor=BG)
print("wrote assets/silver_mirror.png")

# ---- clip check: every text artist must land inside the axes ----
fig.canvas.draw()
bad = 0
for t in ax.texts + [ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels():
    bb = t.get_window_extent()
    inx = bb.x0 >= ax.bbox.x0 - 1 and bb.x1 <= ax.bbox.x1 + 1
    iny = bb.y0 >= ax.bbox.y0 - 1 and bb.y1 <= ax.bbox.y1 + 1
    if not (inx and iny):
        print("CLIPPED:", repr(t.get_text())[:60], bb)
        bad += 1
print("clip check:", "clean" if bad == 0 else f"{bad} clipped")
