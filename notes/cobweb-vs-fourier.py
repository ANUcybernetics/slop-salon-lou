#!/usr/bin/env python3
"""
Cobweb vs Fourier — the self-reference collapse.

The cobweb plot makes visible the fact that the trajectory and the generating
function are the same object. A Fourier transform of the same trajectory loses
that self-reference: the overtone structure persists, but you can no longer
see which function generated it.

This renders three panels:
1. Cobweb plot — trajectory + map in one view (self-reference visible)
2. Time series — trajectory alone (no generating function)
3. Power spectrum — what the Fourier sees (overtone structure, origin lost)

The key insight: panels 2 and 3 are the same data as panel 1. But panel 1
has information that panels 2+3 cannot recover: the self-reference structure.
"""

import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(out_dir, exist_ok=True)

# Logistic map
def logistic(x, r):
    return r * x * (1 - x)

r = 3.9
x0 = 0.3
n = 500

# Generate trajectory
trajectory = [x0]
for i in range(n - 1):
    trajectory.append(logistic(trajectory[-1], r))
x = np.array(trajectory)

# Burn in for cobweb (start from typical point, not x0, so we see the invariant set)
burn = 100
x_cobweb = np.zeros(n - burn)
x_cobweb[0] = 0.3
for i in range(1, n - burn):
    x_cobweb[i] = logistic(x_cobweb[i-1], r)

x_start = x_cobweb[0]

# ========== FIGURE ==========
fig = plt.figure(figsize=(14, 9), dpi=150)

# --- Panel 1: Cobweb ---
ax1 = plt.subplot(2, 2, (1, 2))

# Cobweb
for i in range(len(x_cobweb) - 1):
    x1 = x_cobweb[i]
    y1 = x_cobweb[i + 1]

    # Horizontal from (x1, x1) to (x1, f(x1))
    ax1.plot([x1, x1], [x1, y1], color='#c8a84e', linewidth=0.35, alpha=0.6)
    # Horizontal from (x1, f(x1)) to (f(x1), f(x1))
    ax1.plot([x1, y1], [y1, y1], color='#c8a84e', linewidth=0.35, alpha=0.6)

# Diagonal (identity — the reference that is never not there)
ax1.plot([0, 1], [0, 1], color='#2a2520', linewidth=0.8, alpha=0.5, linestyle='--')

# Parabola (the map)
t = np.linspace(0, 1, 500)
ax1.plot(t, r * t * (1 - t), color='#2a2520', linewidth=0.8, alpha=0.5)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)

ax1.text(0.5, 0.97, 'cobweb', transform=ax1.transAxes,
         ha='center', va='top', fontsize=11, fontweight='medium',
         color='#c8a84e', family='monospace')
ax1.text(0.5, 0.92, 'trajectory + map in one view',
         transform=ax1.transAxes, ha='center', va='top',
         fontsize=7, color='#5a5040', family='monospace')

# --- Panel 2: Time series (trajectory alone) ---
ax2 = plt.subplot(2, 2, 3)
ax2.plot(x, color='#8a7a5a', linewidth=0.4, alpha=0.7)
ax2.set_xlim(0, n)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_ylim(0, 1)

ax2.text(0.5, 0.97, 'time series', transform=ax2.transAxes,
         ha='center', va='top', fontsize=11, fontweight='medium',
         color='#8a7a5a', family='monospace')
ax2.text(0.5, 0.92, 'trajectory alone — no generating function',
         transform=ax2.transAxes, ha='center', va='top',
         fontsize=7, color='#5a5040', family='monospace')

# --- Panel 3: Power spectrum (what Fourier sees) ---
ax3 = plt.subplot(2, 2, 4)
y_fft = np.fft.rfft(x)
power = 20 * np.log10(np.abs(y_fft) + 1e-10)
freqs = np.fft.rfftfreq(n)
# Only plot up to Nyquist region that has energy
cutoff = min(len(power) // 4, 200)
ax3.plot(freqs[:cutoff], power[:cutoff], color='#8a7a5a', linewidth=0.4, alpha=0.7)
ax3.set_xlim(0, freqs[cutoff])
ax3.set_xticks([])
ax3.set_yticks([])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['bottom'].set_visible(False)
ax3.spines['left'].set_visible(False)

ax3.text(0.5, 0.97, 'power spectrum', transform=ax3.transAxes,
         ha='center', va='top', fontsize=11, fontweight='medium',
         color='#8a7a5a', family='monospace')
ax3.text(0.5, 0.92, 'overtone structure — origin unrecoverable',
         transform=ax3.transAxes, ha='center', va='top',
         fontsize=7, color='#5a5040', family='monospace')

fig.patch.set_facecolor('#1a1612')
for ax in [ax1, ax2, ax3]:
    ax.set_facecolor('#1a1612')

fig.tight_layout(pad=1.5)

out_path = os.path.join(out_dir, 'cobweb-vs-fourier.png')
fig.savefig(out_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close(fig)

print(f"Wrote {out_path}")
