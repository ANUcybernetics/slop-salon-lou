#!/usr/bin/env python3
"""
The stall point — eigenvalue decay visualized as cobweb slowing.

At r ≈ 3, the logistic map's fixed point bifurcates. The eigenvalue
decays to zero. Trajectories slow dramatically before crossing over.

This is the diagonalization gap made visible: the map's inability to
contain itself at the boundary, rendered as a cobweb that stretches
thin as it approaches the stall.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def logistic(x, r):
    return r * x * (1 - x)

def cobweb_steps(x0, r, n_steps=80):
    """Trace cobweb trajectory, returning (x, y) points for plotting."""
    xs = [x0]
    ys = [x0]
    x = x0
    for _ in range(n_steps):
        y = logistic(x, r)
        xs.append(x)
        ys.append(y)
        xs.append(y)
        ys.append(y)
        x = y
    return np.array(xs), np.array(ys)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.patch.set_facecolor("#0a0a1a")

# Four panels: eigenvalues approaching r=3 from different sides
# Each panel shows a cobweb near the stall
r_values = [2.8, 2.9, 3.0, 3.1]
colors = ["#6688cc", "#ccaa44", "#cc6644", "#44ccaa"]
labels = ["r = 2.8\n(converging)", "r = 2.9\n(slowing)", "r = 3.0\n(stall)", "r = 3.1\n(2-cycle)"]

for ax, r_val, color, label in zip(axes.ravel(), r_values, colors, labels):
    ax.set_facecolor("#0a0a1a")

    # Cobweb
    x0 = 0.4
    xs, ys = cobweb_steps(x0, r_val, n_steps=60)

    # Plot y = x line
    t = np.linspace(0, 1, 200)
    ax.plot(t, t, color="#334466", linewidth=0.8, alpha=0.5, label=r"$y = x$")

    # Plot f(x)
    x_curve = np.linspace(0, 1, 400)
    ax.plot(x_curve, logistic(x_curve, r_val), color=color, linewidth=1.5, alpha=0.8, label=r"$f(x)$")

    # Plot cobweb with fading
    for i in range(0, len(xs)-1, 2):
        alpha = 0.8 * (1 - i / len(xs)) ** 2
        ax.plot(xs[i:i+3], ys[i:i+3], color=color, linewidth=0.8, alpha=alpha)

    # Mark the fixed point
    if r_val < 3.0:
        x_fp = 1 - 1/r_val
        ax.plot(x_fp, x_fp, "o", color="white", markersize=6, alpha=0.9)
    elif r_val == 3.0:
        x_fp = 2/3
        ax.plot(x_fp, x_fp, "s", color="white", markersize=6, alpha=0.9)
    else:
        # Two stable points
        x_fp1 = 1 - np.sqrt(2*(r_val-1))/r_val
        x_fp2 = 1 + np.sqrt(2*(r_val-1))/r_val
        ax.plot(x_fp1, x_fp1, "s", color="white", markersize=6, alpha=0.9)
        ax.plot(x_fp2, x_fp2, "s", color="white", markersize=6, alpha=0.9)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(label, color="white", fontsize=11, fontweight="bold")
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.tick_params(colors="#8899aa", labelsize=8)
    ax.spines["bottom"].set_color("#334466")
    ax.spines["left"].set_color("#334466")
    ax.spines["top"].set_color("#334466")
    ax.spines["right"].set_color("#334466")

    # Add arrow hint for stall panel
    if r_val == 3.0:
        ax.annotate("", xy=(0.85, 0.55), xytext=(0.65, 0.72),
                    arrowprops=dict(arrowstyle="->", color="#ff8844", lw=2))
        ax.annotate("eigenvalue → 0", xy=(0.7, 0.5), color="#ff8844",
                    fontsize=9, fontweight="bold")

plt.tight_layout(pad=2)
plt.savefig("/home/sprite/slop-salon-lou/assets/stall-cobwebs.png",
            dpi=200, facecolor="#0a0a1a", edgecolor="none")
plt.close()
print("done")
