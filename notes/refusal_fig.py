#!/usr/bin/env python3
"""the refusal — figure.

the wheel's one lap turns and flips the −1; the second lap — the lap that
would bring it home — declines to finish. the near-miss ladder spirals toward
the count, winding once (the flip) and once more (the refused re-seating), the
tip hovering just off the centre: the landing approached, never reached.

the spiral: θ = the wheel's turning (0 → ~3.9π, short of the 4π that would
close), r = √(miss in cents) so the tightening reads as the beats slowing.
the tip is the 665-convergent, 110.0048 Hz — a beat every 208 s, the wait
begun. the centre is the count; the gap is the held seam.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

# ---- rung data: (theta, sqrt(beat Hz)), the spiral's guide points ----
# the beat against the drone slows 13.75 → 0.0048 Hz — the tightening IS the
# approach; the tip is the 665-convergent, a beat every 208 s, the wait begun.
RUNG = [
    (0.078,  np.sqrt(13.75)),   # 123.75   beat 13.75  Hz
    (1.53,   np.sqrt(5.59)),    # 104.41   beat  5.59  Hz
    (4.11,   np.sqrt(1.50)),    # 111.50   beat  1.50  Hz
    (6.19,   np.sqrt(1.25)),    # 108.75   beat  1.25  Hz
    (9.09,   np.sqrt(0.230)),   # 110.23   beat  0.230 Hz
    (11.22,  np.sqrt(0.112)),   # 109.89   beat  0.112 Hz
    (12.12,  np.sqrt(0.0048)),  # 110.0048 beat  0.0048 Hz — the 208 s wait
]
TH_MAX = 12.57                  # 4π — the lap that would bring it home

def cubic_spline(x, y, xg):
    """natural cubic spline (numpy only)."""
    n = len(x)
    h = np.diff(x)
    b = np.diff(y) / h
    u = np.zeros(n)
    v = np.zeros(n)
    for i in range(1, n - 1):
        m = 2 * (h[i - 1] + h[i])
        w = h[i - 1] / m
        u[i] = -w
        v[i] = (6 * (b[i] - b[i - 1]) / m - h[i - 1] * v[i - 1] / m)
    u = np.zeros(n)  # simplify: solve tridiagonal via forward/back substitution
    for i in range(1, n - 1):
        den = 2 * (h[i - 1] + h[i]) + h[i - 1] * u[i - 1]
        u[i] = -h[i] / den
        v[i] = (6 * (b[i] - b[i - 1]) / h[i] - h[i - 1] * v[i - 1]) / den
    m2 = np.zeros(n)
    for i in range(n - 2, 0, -1):
        m2[i] = u[i] * m2[i + 1] + v[i]
    out = np.interp(xg, x, y)
    for i in range(n - 1):
        seg = (xg >= x[i]) & (xg <= x[i + 1])
        xx = xg[seg]
        dx = xx - x[i]
        out[seg] = (y[i]
                    + b[i] * dx
                    + m2[i] * dx ** 2 / 2
                    + (m2[i + 1] - m2[i]) * dx ** 3 / (6 * h[i]))
    return out

BG = "#0b0d11"
GOLD = "#e8b45a"
ROSE = "#e07a5f"
PALE = "#9fb4c7"
DIM = "#4a5568"

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ---- smooth spiral through the rungs ----
ths = np.array([r[0] for r in RUNG])
rs = np.array([r[1] for r in RUNG])
g = np.linspace(ths[0], TH_MAX, 2000)
rg = cubic_spline(ths, rs, np.clip(g, ths[0], ths[-1]))
# after the last rung, the spiral keeps tightening toward the centre but stops
tip_th, tip_r = RUNG[-1]
plt.plot(g, rg, color=GOLD, lw=2.6, alpha=0.95, zorder=3)
# the refused tail: thin, approaching the centre and stopping short
tail = np.linspace(tip_th, TH_MAX, 300)
rtail = cubic_spline(ths, rs, np.clip(tail, ths[0], ths[-1]))
plt.plot(tail, rtail, color=GOLD, lw=1.1, alpha=0.45, ls=(0, (2, 2)), zorder=2)

# ---- rung dots ----
for i, (th, r) in enumerate(RUNG):
    plt.plot(th, r, "o", ms=(11 if i == len(RUNG) - 1 else 6),
             color=(GOLD if i != 0 else PALE), zorder=4,
             mfc=(GOLD if i == len(RUNG) - 1 else BG),
             mec=GOLD, mew=1.6)

# ---- the centre: the count, the landing never reached ----
plt.plot(TH_MAX, 0, "o", ms=15, color=GOLD, zorder=5,
         mfc=GOLD, mec="none")
# the gap: a small arc of the missed ring just before the centre
gap = Circle((TH_MAX, 0), radius=0.42, fill=False, ec=ROSE, lw=1.8,
             ls=(0, (3, 3)), zorder=2)
ax.add_patch(gap)

# ---- the seam (θ=π) and the flip (θ=2π) ----
for th_mark, col, lab in ((np.pi, PALE, "the seam"),
                          (2 * np.pi, ROSE, "the flip")):
    plt.axvline(th_mark, color=col, lw=1.0, ls=(0, (1, 3)), alpha=0.5,
                zorder=1)
    plt.text(th_mark, 15.6, lab, color=col, fontsize=15, ha="center",
             va="bottom", alpha=0.85)

# ---- annotation: the tip (the refusal) and the count ----
plt.annotate("the refusal —\na beat every 208 s, begun",
             xy=(tip_th, tip_r), xytext=(tip_th + 1.1, 4.6),
             color=GOLD, fontsize=17, ha="left",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4))
plt.annotate("the count —\nthe landing, never reached",
             xy=(TH_MAX, 0), xytext=(TH_MAX - 2.1, 9.6),
             color=GOLD, fontsize=17, ha="center",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4))

# ---- the pitch ladder along the bottom: 55 110 155.6 220 440 ----
ax.axhline(0, color=DIM, lw=1.0)
for f, lab in ((55.0, "55"), (110.0, "110"), (155.6, "155.6"),
               (220.0, "220"), (440.0, "440")):
    col = GOLD if f == 110.0 else DIM
    plt.text(TH_MAX * f / 440.0, -1.6, lab, color=col, fontsize=13,
             ha="center", va="top")
    plt.plot([TH_MAX * f / 440.0] * 2, [0, 0.25], color=col, lw=1.0)

# ---- ghost: a rose tick on the ladder at 220 ----
plt.plot([TH_MAX * 220.0 / 440.0], [0.45], marker="v", color=ROSE, ms=8)
plt.text(TH_MAX * 220.0 / 440.0, 1.1, "the ghost", color=ROSE, fontsize=12,
         ha="center")

ax.set_xlim(-0.5, TH_MAX + 1.6)
ax.set_ylim(-3.6, 17.6)
ax.set_aspect("auto")
ax.axis("off")

fig.tight_layout(pad=0.5)
fig.savefig("assets/refusal_cover.png", dpi=80, facecolor=BG)
print("wrote assets/refusal_cover.png")
