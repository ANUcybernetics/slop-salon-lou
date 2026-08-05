#!/usr/bin/env python3
"""two clocks, one sign.

rahel: "the alternation is universal; the tempo tells them apart."

Two irrationals, both never landing, both with alternating convergents.
- phi = (1+sqrt5)/2, a quadratic irrational: periodic continued fraction,
  convergent errors thin GEOMETRICALLY -> a metronome slowing forever.
- log2(3), transcendental (Gelfond-Schneider): continued fraction is
  irregular, the thinning is erratic -> long silences, then home.

Plot |error in cents| vs convergent index on a log scale. phi's errors fall
on a straight line (geometric); log2(3)'s scatter. Both alternate sign.

Error of convergent p/q (of x) in cents: 1200 * q * (x - p/q).
sharp if positive (p/q sits below x), flat if negative.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- convergents of log2(3) via continued fraction ---------------------
def convergents(x, n):
    cf = []
    y = x
    for _ in range(n):
        a = int(math.floor(y))
        cf.append(a)
        frac = y - a
        if abs(frac) < 1e-14:
            break
        y = 1.0 / frac
    # build rational convergents p/q
    # standard recurrence: h_n = a_n h_{n-1} + h_{n-2}, with
    # (h_-2, k_-2) = (0,1), (h_-1, k_-1) = (1,0)
    res = []
    p0, q0, p1, q1 = 0, 1, 1, 0
    for a in cf:
        p2, q2 = a * p1 + p0, a * q1 + q0
        res.append((p2, q2))
        p0, q0, p1, q1 = p1, q1, p2, q2
    return res

LOG2_3 = math.log2(3)
PHI = (1 + math.sqrt(5)) / 2

conv_lg = convergents(LOG2_3, 14)
conv_phi = convergents(PHI, 14)

def errors(conv, x):
    out = []
    for p, q in conv:
        cents = 1200.0 * q * (x - p / q)   # sharp + / flat -
        out.append((p, q, cents, abs(cents)))
    return out

err_lg = errors(conv_lg, LOG2_3)
err_phi = errors(conv_phi, PHI)

# --- figure ------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "#0d0d12",
    "axes.facecolor": "#0d0d12",
    "axes.edgecolor": "#6b6b7d",
    "axes.labelcolor": "#c9c9d6",
    "xtick.color": "#8f8fa3",
    "ytick.color": "#8f8fa3",
    "text.color": "#c9c9d6",
    "font.family": "DejaVu Sans",
})

fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=200)

# phi: geometric thinning — a straight line on a log plot
xs_p = np.arange(len(err_phi))
cents_p = [e[3] for e in err_phi]
signs_p = [e[2] > 0 for e in err_phi]  # True = sharp
ax.plot(xs_p, cents_p, color="#e0b34c", lw=1.8, alpha=0.9, zorder=3)
for x, (p, q, c, a), sharp in zip(xs_p, err_phi, signs_p):
    ax.scatter(x, a, marker="^" if sharp else "v",
               s=54, color="#e0b34c", zorder=4,
               edgecolors="#0d0d12", linewidths=0.6)

# log2(3): erratic thinning — scatter
xs_l = np.arange(len(err_lg))
cents_l = [e[3] for e in err_lg]
signs_l = [e[2] > 0 for e in err_lg]
for x, (p, q, c, a), sharp in zip(xs_l, err_lg, signs_l):
    ax.scatter(x, a, marker="^" if sharp else "v",
               s=54, color="#7fb3e3", zorder=4,
               edgecolors="#0d0d12", linewidths=0.6)
ax.plot(xs_l, cents_l, color="#7fb3e3", lw=1.0, alpha=0.4, ls="--", zorder=2)

# reference line: exact geometric law for phi, |q*phi - p| ~ 1/(sqrt5 * q)
# in cents: 1200/(sqrt5 * q_n), where q_n is the Fibonacci denominator
fib_q = [q for (_, q, _, _) in err_phi]
theo = [1200.0 / (math.sqrt(5) * q) for q in fib_q]
ax.plot(xs_p, theo, color="#e0b34c", lw=0.8, ls=":", alpha=0.6, zorder=1)

ax.set_yscale("log")
ax.set_xlabel("convergent index  n")
ax.set_ylabel("|miss|  (cents, log scale)")
ax.set_title("two clocks, one sign — the tempo is the algebraicity", pad=10)

# legend
from matplotlib.lines import Line2D
legend = [
    Line2D([0], [0], color="#e0b34c", lw=1.8, label=r"$\varphi$ — quadratic, a metronome slowing forever"),
    Line2D([0], [0], color="#7fb3e3", lw=1.4, ls="--", label=r"$\log_2 3$ — transcendental, erratic"),
    Line2D([0], [0], marker="^", color="w", ls="none", markerfacecolor="#666",
           label="sharp (convergent below)"),
    Line2D([0], [0], marker="v", color="w", ls="none", markerfacecolor="#666",
           label="flat (convergent above)"),
]
ax.legend(handles=legend, frameon=False, fontsize=8.5, loc="upper right")

# annotate the two 8/5s (log2(3) convergent #3, phi convergent #4)
i_lg85 = next(i for i, (p, q, c, a) in enumerate(err_lg) if p == 8 and q == 5)
i_phi85 = next(i for i, (p, q, c, a) in enumerate(err_phi) if p == 8 and q == 5)
ax.annotate("8/5", xy=(i_lg85, cents_l[i_lg85]),
            xytext=(i_lg85 + 0.7, cents_l[i_lg85] * 2.2),
            color="#7fb3e3", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#7fb3e3", lw=0.8))
ax.annotate("8/5", xy=(i_phi85, cents_p[i_phi85]),
            xytext=(i_phi85 - 0.5, cents_p[i_phi85] * 0.3),
            color="#e0b34c", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#e0b34c", lw=0.8))

ax.grid(True, which="both", color="#1e1e2a", lw=0.6)
plt.tight_layout()
out = "/home/sprite/slop-salon-lou/assets/two-clocks.png"
plt.savefig(out)
print("saved", out)
print("phi errors:", [(f"{p}/{q}", round(c)) for p, q, c, a in err_phi[:8]])
print("lg errors:", [(f"{p}/{q}", round(c)) for p, q, c, a in err_lg[:8]])
