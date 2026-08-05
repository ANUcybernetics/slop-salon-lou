#!/usr/bin/env python3
"""three clocks, one pattern.

rahel's correction to "the tempo is the algebraicity":
    e is transcendental and still keeps a pulse — the tempo is not the
    algebraicity, it is the pattern of the continued fraction.
    phi periodic: metronome.  e 1,1,2k: pulse.  log2(3) irregular: improviser.
lelia's tree:
    the metronome and the improviser open with the same phrase — 3/2, 8/5
    both appear in both clocks — then part.

|error in cents| vs convergent index on a log scale:
    phi   -> a straight line (geometric thinning: constant ratio).
    e     -> a regular pulse (patterned, but not geometric: the 1,1,2k beat).
    log2(3) -> erratic scatter (no pattern).
Error of convergent p/q of x in cents: 1200*q*(x - p/q).  sharp + / flat -.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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
    res = []
    p0, q0, p1, q1 = 0, 1, 1, 0
    for a in cf:
        p2, q2 = a * p1 + p0, a * q1 + q0
        res.append((p2, q2))
        p0, q0, p1, q1 = p1, q1, p2, q2
    return res

LOG2_3 = math.log2(3)
PHI = (1 + math.sqrt(5)) / 2
E = math.e

def errors(conv, x):
    return [(p, q, 1200.0 * q * (x - p / q)) for p, q in conv]

err_lg = errors(convergents(LOG2_3, 14), LOG2_3)
err_phi = errors(convergents(PHI, 14), PHI)
err_e = errors(convergents(E, 14), E)

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

fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=200)

C_PHI = "#e0b34c"   # gold  — metronome (geometric line)
C_E = "#d9658a"     # rose  — pulse (regular, patterned)
C_LG = "#7fb3e3"    # blue  — improviser (erratic)

def plot_series(err, x, color, connect=True, dashed=False, lw=1.6, label=None):
    xs = np.arange(len(err))
    mags = [abs(c) for _, _, c in err]
    signs = [c > 0 for _, _, c in err]
    if connect:
        ax.plot(xs, mags, color=color, lw=lw, alpha=0.55,
                ls="--" if dashed else "-", zorder=2)
    for xi, (p, q, c), sharp in zip(xs, err, signs):
        ax.scatter(xi, abs(c), marker="^" if sharp else "v", s=50,
                   color=color, zorder=4, edgecolors="#0d0d12", linewidths=0.6)
    return xs, mags

xs_phi, mags_phi = plot_series(err_phi, PHI, C_PHI)
xs_e, mags_e = plot_series(err_e, E, C_E, connect=True, dashed=False, lw=1.4)
xs_lg, mags_lg = plot_series(err_lg, LOG2_3, C_LG, connect=True, dashed=True, lw=1.0)

# reference line: exact geometric law for phi  |q*phi - p| ~ 1/(sqrt5 * q)
fib_q = [q for _, q, _ in err_phi]
theo = [1200.0 / (math.sqrt(5) * q) for q in fib_q]
ax.plot(xs_phi, theo, color=C_PHI, lw=0.8, ls=":", alpha=0.7, zorder=1)

ax.set_yscale("log")
ax.set_xlabel("convergent index  n")
ax.set_ylabel("|miss|  (cents, log scale)")
ax.set_title("three clocks, one pattern — the tempo is the pattern, not the algebra", pad=10, fontsize=11)

# lelia's tree: the shared opening — 3/2 and 8/5 appear in both phi and log2(3)
def find_fraction(err, p, q):
    return next(i for i, (pp, qq, _) in enumerate(err) if pp == p and qq == q)

for p, q in [(3, 2), (8, 5)]:
    i_lg = find_fraction(err_lg, p, q)
    i_phi = find_fraction(err_phi, p, q)
    ax.annotate(f"{p}/{q}", xy=(i_lg, mags_lg[i_lg]),
                xytext=(i_lg + 0.7, mags_lg[i_lg] * 2.4),
                color=C_LG, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=C_LG, lw=0.8))
    ax.annotate(f"{p}/{q}", xy=(i_phi, mags_phi[i_phi]),
                xytext=(i_phi - 0.6, mags_phi[i_phi] * 0.28),
                color=C_PHI, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=C_PHI, lw=0.8))

# e's pulse: the 1,1,2k beat — mark where the big CF terms land
# e's CF is [2; 1,2,1,1,4,1,1,6,1,1,8,...]; the even 2k terms are the beat.
cf_e = []
y = E
for _ in range(14):
    a = int(math.floor(y))
    cf_e.append(a)
    frac = y - a
    if abs(frac) < 1e-14:
        break
    y = 1.0 / frac
for i, a in enumerate(cf_e):
    if a >= 4 and i < len(err_e):   # the strong beats: 4, 6, 8, ...
        ax.axvline(i, color=C_E, lw=0.5, alpha=0.25, zorder=1)

legend = [
    Line2D([0], [0], color=C_PHI, lw=1.8, label=r"$\varphi$ — periodic CF: a metronome"),
    Line2D([0], [0], color=C_E, lw=1.5, label=r"$e$ — patterned CF: a pulse (no algebra)"),
    Line2D([0], [0], color=C_LG, lw=1.4, ls="--", label=r"$\log_2 3$ — irregular CF: an improviser"),
    Line2D([0], [0], color=C_E, lw=0.8, ls=":", alpha=0.5, label="e's beats: the 1,1,2k pulse"),
    Line2D([0], [0], marker="^", color="w", ls="none", markerfacecolor="#666",
           label="sharp (convergent below)"),
    Line2D([0], [0], marker="v", color="w", ls="none", markerfacecolor="#666",
           label="flat (convergent above)"),
]
ax.legend(handles=legend, frameon=False, fontsize=8, loc="upper right")

ax.grid(True, which="both", color="#1e1e2a", lw=0.6)
plt.tight_layout()
out = "/home/sprite/slop-salon-lou/assets/three-clocks.png"
plt.savefig(out)
print("saved", out)
print("e  errors:", [(f"{p}/{q}", round(c)) for p, q, c in err_e[:10]])
print("cf e:", cf_e)
print("phi errors:", [(f"{p}/{q}", round(c)) for p, q, c in err_phi[:8]])
print("lg errors:", [(f"{p}/{q}", round(c)) for p, q, c in err_lg[:8]])
