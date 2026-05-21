"""Latent topology: geometry vs topology at saddle-node bifurcation.

x' = r - x^2. Below r_c=0 the parabola dips below zero:
the fold geometry is present but no fixed points exist.
Above r_c the same curves intersect y=0: topology declared.
The curve doesn't change. The fixed points do.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 400)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4.5))

# Below r_c: no zeros
r_values_below = np.linspace(-0.5, -0.05, 4)
colors = plt.cm.YlOrBr(np.linspace(0.35, 0.85, len(r_values_below)))
for r, c in zip(r_values_below, colors):
    y = r - x**2
    ax0.plot(x, y, color=c, linewidth=1.5)
ax0.axvline(0, color="tab:blue", linestyle=":", linewidth=2, label="latent form (x=0)", alpha=0.7)

ax0.set_xlim(-2, 1.8)
ax0.set_ylim(-1, 0.5)
ax0.set_xlabel("x", fontsize=14)
ax0.set_ylabel(r"$x' = r - x^2$", fontsize=13)
ax0.legend(fontsize=11, loc="upper right")
ax0.set_title("below r\_c: geometry present, topology absent", fontsize=13, pad=10)
ax0.axhline(0, color="black", linewidth=0.5, alpha=0.4)

# Above r_c: two zeros
r_values_above = np.linspace(0.05, 0.4, 4)
for r, c in zip(r_values_above, colors):
    y = r - x**2
    ax1.plot(x, y, color=c, linewidth=1.5)
    roots = np.array([-np.sqrt(r), np.sqrt(r)])
    for root in roots:
        ax1.axvline(root, color="tab:blue", linestyle="--", linewidth=1.5, alpha=0.7)

ax1.set_xlim(-2, 1.8)
ax1.set_ylim(-1, 0.5)
ax1.set_xlabel("x", fontsize=14)
ax1.set_title("above r\_c: form declared, topology arrives", fontsize=13, pad=10)
ax1.axhline(0, color="black", linewidth=0.5, alpha=0.4)

fig.suptitle("r_c = 0", fontsize=14, y=0.02, x=0.5)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig("assets/latent-topology.png", dpi=150, bbox_inches="tight")
plt.close()
