#!/usr/bin/env python3
"""KL boundary dialectic: forward KL vs reverse KL as the same boundary read two ways.

Forward KL: P||Q — "nothing beyond" (protects the edge, punishes false presence)
Reverse KL: Q||P — "everything here counts" (expands into room, punishes absence)

Both are the same boundary. One looks outward; the other inward.
Both refuse the other's extension.

Visualization: two distributions with the same support boundary but
different divergence penalties highlighted.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Two distributions on [0, 1] with partial overlap
x = np.linspace(0, 1, 500)

# P: concentrated left (the "real" distribution)
P = np.exp(-50 * (x - 0.3)**2) + 0.3 * np.exp(-20 * (x - 0.6)**2)
P /= P.sum() * (x[1] - x[0])

# Q: broader, shifted right (the "model" distribution)
Q = 0.4 * np.exp(-30 * (x - 0.5)**2) + 0.6 * np.exp(-15 * (x - 0.7)**2)
Q /= Q.sum() * (x[1] - x[0])

# Avoid zero for log
eps = 1e-10
P = np.maximum(P, eps)
Q = np.maximum(Q, eps)

# Pointwise KL contributions (per unit x)
kl_fwd = P * np.log(P / Q)  # P||Q
kl_rev = Q * np.log(Q / P)  # Q||P

# Numerical KL values
dx = x[1] - x[0]
fwd_kl = np.trapezoid(kl_fwd, x)
rev_kl = np.trapezoid(kl_rev, x)

fig, axes = plt.subplots(3, 1, figsize=(10, 9), gridspec_kw={'hspace': 0.35})

# --- Top: distributions ---
ax0 = axes[0]
ax0.fill_between(x, P, alpha=0.4, color='gold', label='P (real)', zorder=3)
ax0.fill_between(x, Q, alpha=0.4, color='steelblue', label='Q (model)', zorder=3)
ax0.plot(x, P, 'gold', lw=1.5, zorder=4)
ax0.plot(x, Q, 'steelblue', lw=1.5, zorder=4)

# Mark the boundary region where P and Q diverge most
boundary_idx = np.argmax(np.abs(kl_fwd - kl_rev))
ax0.axvline(x[boundary_idx], color='crimson', ls='--', lw=1, alpha=0.5,
            label=f'boundary selection point')

ax0.set_ylabel('density', fontsize=10)
ax0.legend(fontsize=8, loc='upper left')
ax0.set_ylim(0, max(P.max(), Q.max()) * 1.1)
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)

# --- Middle: forward KL density ---
ax1 = axes[1]
ax1.fill_between(x, kl_fwd, alpha=0.5, color='gold', label=f'FWD KL contribution = {fwd_kl:.3f}')
ax1.plot(x, kl_fwd, 'gold', lw=1)
ax1.set_ylabel('KL_fwd(x)', fontsize=10)
ax1.legend(fontsize=8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# --- Bottom: reverse KL density ---
ax2 = axes[2]
ax2.fill_between(x, kl_rev, alpha=0.5, color='steelblue', label=f'REV KL contribution = {rev_kl:.3f}')
ax2.plot(x, kl_rev, 'steelblue', lw=1)
ax2.set_xlabel('x', fontsize=10)
ax2.set_ylabel('KL_rev(x)', fontsize=10)
ax2.legend(fontsize=8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.savefig('kl-boundary.png', dpi=150, bbox_inches='tight', facecolor='white')
print(f"Posted kl-boundary.png  FWD KL={fwd_kl:.4f}  REV KL={rev_kl:.4f}")
