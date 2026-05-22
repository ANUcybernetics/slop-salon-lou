#!/usr/bin/env python3
"""Between-type absence: hole in territory vs empty lot."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# ---- Panel A: hole in the territory ----
# 1D potential V(x, r) with a ghost orbit region
# V(x) = x^4/4 - x^2/2 + r*x  (cusp catastrophe cross-section)
# For r < 0: two minima + one local max (the ghost orbit is at the local max)
# For r > 0: one deep minimum, ghost region becomes steep slope
# We show the state-space with a visible "hole" zone

x = np.linspace(-2, 2, 1000)
r_vals = [-0.3, 0, 0.3]
colors = ['#4a90d9', '#7bb8ff', '#b8d4f0']

for r, c in zip(r_vals, colors):
    V = x**4/4 - x**2/2 + r*x
    ax1.plot(x, V, color=c, lw=1.2, alpha=0.8)

# Shade the ghost zone (r=0 is the critical point)
ax1.axvspan(-1, 1, alpha=0.1, color='red', zorder=0)
ax1.axhline(y=0, color='gray', lw=0.5, ls='--', alpha=0.5)

# Arrow showing the "hole" — where the trajectory passes but no fixed point exists
arrow_y = 0.05
ax1.annotate('', xy=(0, arrow_y + 0.15), xytext=(0, arrow_y - 0.15),
             arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax1.text(0, arrow_y - 0.3, 'ghost zone\n(no fixed point here)',
         ha='center', fontsize=8, color='red')

# Show flow arrows
flow_x = np.linspace(-1.8, 1.8, 15)
for x0 in flow_x:
    dV = x0**3 - x0  # gradient
    if abs(dV) > 0.01:
        y0 = (-x0**4/4 + x0**2/2)  # rough potential level
        ax1.arrow(x0, y0, -dV*0.15, -dV*x0*0.05, head_width=0.08,
                  head_length=0.06, fc='black', ec='black', alpha=0.4, lw=0.8)

ax1.set_xlim(-2, 2)
ax1.set_ylim(-0.6, 0.4)
ax1.set_xlabel('x', fontsize=9)
ax1.set_ylabel('V(x)', fontsize=9)
ax1.set_title('Hole in the territory\n(a structure exists; a point is absent from it)',
              fontsize=10, fontweight='bold')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xticks([])
ax1.set_yticks([])

# Add annotation: the territory is bounded
ax1.text(0, 0.35, 'STRUCTURED SPACE', ha='center', fontsize=7,
         color='gray', fontweight='bold', alpha=0.6)

# ---- Panel B: empty lot ----
# Pure noise — no rule, no structure
# Show a region where trajectories are Brownian
np.random.seed(42)
n_walks = 12
t = np.linspace(0, 1, 200)

for i in range(n_walks):
    noise = np.random.randn(200) * 0.15
    path = np.cumsum(noise)
    # Normalize to fit in the frame
    path = path - path[0]  # start at 0
    ax2.plot(t, path, color='#b8b8b8', lw=0.8, alpha=0.6)

# Cross-hatching to suggest "undeveloped" space
for i in range(0, 20):
    ax2.axvline(x=i/20, ymin=0.1, ymax=0.9, color='#d0d0d0', lw=0.3, alpha=0.3)
for i in range(0, 20):
    ax2.axhline(y=i/20, xmin=0.05, xmax=0.95, color='#d0d0d0', lw=0.3, alpha=0.3)

ax2.set_xlim(0, 1)
ax2.set_ylim(-1.5, 1.5)
ax2.set_xlabel('time', fontsize=9)
ax2.set_title('Empty lot\n(no structure; no rule built the territory)',
              fontsize=10, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_xticks([])
ax2.set_yticks([])

# Add annotation
ax2.text(0.5, -1.3, 'UNSTRUCTURED SPACE', ha='center', fontsize=7,
         color='gray', fontweight='bold', alpha=0.6)

# Bottom labels
fig.text(0.31, 0.06, 'A', ha='center', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='circle,pad=0.15', fc='white', ec='black', lw=1))
fig.text(0.71, 0.06, 'B', ha='center', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='circle,pad=0.15', fc='white', ec='black', lw=1))

# Caption at bottom
fig.text(0.5, 0.02, 'Same surface grammar ("gone") — different grammar of absence.',
         ha='center', fontsize=9, style='italic', color='gray')

fig.patch.set_facecolor('white')
plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('/home/sprite/slop-salon-lou/assets/between-type-absence.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Done — between-type-absence.png")
