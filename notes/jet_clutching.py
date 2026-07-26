#!/usr/bin/env python3
"""
Clutching as jet bundle: velocity (Rahel) × resolution (Mina)
as the first jet of the clutching invariant.

Three axes:
- Exterior (epsilon-plate) → interior (Dixmier) → barcode (persistence)
  as three coordinate charts on the same 0-cochain
- Clutching number (count) → clutching velocity (rate)
  as the jet extension

The diagram shows:
- A base S^1 (clutching circle)
- Three fiber bundles over it (exterior, interior, persistence)
- A "velocity arrow" flowing along the base
- The clutching number at the center as the invariant

Aesthetic: matplotlib, topographic/circuit-like, dark background
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 10), dpi=100)
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# --- Panel 1: Exterior view (epsilon-plate) ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_aspect('equal')
ax1.set_facecolor('#0a0a12')
ax1.axis('off')
ax1.set_title('exterior  ε-plate', fontsize=10, color='#8899aa', pad=8)

# Concentric epsilon levels
for i, r in enumerate([0.3, 0.5, 0.7, 0.9]):
    circ = Circle((0, 0), r, fill=False, edgecolor='#2244aa',
                  linewidth=1.5 if i == 2 else 0.8, alpha=0.7)
    ax1.add_patch(circ)

# Clutching singularity at center
ax1.plot(0, 0, 'o', color='#ff6644', markersize=8, alpha=0.9)
ax1.text(0, -1.05, 'clutching\nnumber', ha='center', fontsize=7, color='#ff8866')

# Velocity arrows flowing outward
for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
    r0, r1 = 0.5, 0.85
    x0, y0 = r0*np.cos(angle), r0*np.sin(angle)
    x1, y1 = r1*np.cos(angle), r1*np.sin(angle)
    ax1.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#44aaff',
                              lw=1, alpha=0.5))

ax1.text(0, 1.05, 'ε-level sets as strata', ha='center', fontsize=6, color='#556688')

# --- Panel 2: Interior view (Dixmier trace) ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_aspect('equal')
ax2.set_facecolor('#0a0a12')
ax2.axis('off')
ax2.set_title('interior  Dixmier trace', fontsize=10, color='#8899aa', pad=8)

# Density cloud (interior view = fuzzy, not sharp)
theta = np.linspace(0, 2*np.pi, 50)
r = np.linspace(0, 1, 30)
THETA, R = np.meshgrid(theta, r)
X = R * np.cos(THETA)
Y = R * np.sin(THETA)
# Density peaks at center, falls off
density = np.exp(-5*R**2) * (1 + 0.3*np.sin(3*THETA))
contours = ax2.contour(X, Y, density, levels=8, colors='#aa6644',
                       linewidths=0.8, alpha=0.6)
ax2.contourf(X, Y, density, levels=4, colors=['#ff4422', '#cc6644',
                     '#884433', '#442222'], alpha=0.3)

ax2.plot(0, 0, 'o', color='#ff8866', markersize=10)
ax2.text(0, -1.05, 'trace =\nscaled integral', ha='center',
         fontsize=7, color='#cc7755')

# Inward-pointing arrows (interior reading)
for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
    r0, r1 = 0.85, 0.5
    x0, y0 = r0*np.cos(angle), r0*np.sin(angle)
    x1, y1 = r1*np.cos(angle), r1*np.sin(angle)
    ax2.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#ffaa44',
                              lw=1, alpha=0.5))

ax2.text(0, 1.05, 'stalk as intention', ha='center', fontsize=6, color='#556688')

# --- Panel 3: Persistence (barcode) ---
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_xlim(-1.2, 1.2)
ax3.set_ylim(-1.2, 1.2)
ax3.set_facecolor('#0a0a12')
ax3.axis('off')
ax3.set_title('persistence  barcode', fontsize=10, color='#8899aa', pad=8)

# Barcode: horizontal bars at different "heights"
bars = [
    (0, -0.9, 1.6, -0.7, '#ff4444', 2.0),
    (0.1, -0.6, 1.0, -0.3, '#ff8844', 1.5),
    (0.2, -0.3, 0.6, 0.0, '#ffaa44', 1.2),
    (0.3, 0.0, 0.8, 0.3, '#88cc44', 1.0),
    (0.15, 0.3, 1.3, 0.6, '#44aa66', 0.7),
    (0.25, 0.6, 0.5, 0.85, '#4488ff', 3.0),  # the long one = clutching integer
]
for x0, y0, w, y1, c, lw in bars:
    ax3.plot([x0, x0+w], [y0, y0], color=c, linewidth=lw, solid_capstyle='butt')

# The clutching bar at bottom (longest, lowest frequency)
ax3.plot([0.1, 1.4], [0.6, 0.6], color='#4488ff', linewidth=3, solid_capstyle='butt')
ax3.text(0.75, 0.85, 'clutching\ninteger\n55Hz', ha='center',
         fontsize=7, color='#6699ff')

# Filtration axis
ax3.arrow(1.1, -1.05, 0.3, 0, head_width=0.06, head_length=0.05,
         fc='#556688', ec='#556688')
ax3.text(1.1, -1.15, 'ε', ha='center', fontsize=8, color='#556688')

# --- Panel 4: Synthesis — jet bundle ---
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_xlim(-1.3, 1.3)
ax4.set_ylim(-1.3, 1.3)
ax4.set_aspect('equal')
ax4.set_facecolor('#0a0a12')
ax4.axis('off')
ax4.set_title('jet  J¹', fontsize=10, color='#8899aa', pad=8)

# Base circle (S^1) — thick
base_circle = Circle((0, 0), 0.5, fill=False, edgecolor='#6688aa',
                     linewidth=2.5, alpha=0.8)
ax4.add_patch(base_circle)

# Three fibers (exterior, interior, persistence) radiating out
fiber_angles = [0, 2*np.pi/3, 4*np.pi/3]
fiber_labels = ['ext', 'int', 'bar']
fiber_colors = ['#44aaff', '#ff8844', '#44cc88']

for angle, label, color in zip(fiber_angles, fiber_labels, fiber_colors):
    # Radial line from base to fiber
    r_end = 1.0
    x_start = 0.5 * np.cos(angle)
    y_start = 0.5 * np.sin(angle)
    x_end = r_end * np.cos(angle)
    y_end = r_end * np.sin(angle)
    ax4.plot([x_start, x_end], [y_start, y_end], color=color,
            linewidth=2, alpha=0.7)

    # Fiber node
    ax4.plot(x_end, y_end, 'o', color=color, markersize=6, alpha=0.8)
    ax4.text(x_end*1.25, y_end*1.25, label, ha='center', fontsize=7,
            color=color, alpha=0.8)

# Velocity flow along the base (clockwise)
for i, angle in enumerate(np.linspace(0, 2*np.pi, 6, endpoint=False)):
    tangent_angle = angle + np.pi/2
    x = 0.5 * np.cos(angle)
    y = 0.5 * np.sin(angle)
    dx = 0.08 * np.cos(tangent_angle)
    dy = 0.08 * np.sin(tangent_angle)
    ax4.annotate('', xy=(x+dx, y+dy), xytext=(x-dx, y-dy),
                arrowprops=dict(arrowstyle='->', color='#ff66aa',
                              lw=1.5, alpha=0.6))

# Center invariant
ax4.plot(0, 0, 'o', color='#ffcc44', markersize=12, alpha=0.9)
ax4.text(0, -0.08, '1', ha='center', va='center', fontsize=10,
        color='#ffdd66', fontweight='bold')

# Velocity arrow (crossing through center)
ax4.arrow(-0.35, 0.35, 0.6, -0.6, head_width=0.06, head_length=0.06,
         fc='#ff66aa', ec='#ff66aa', linewidth=1.5, alpha=0.5)
ax4.text(0.45, -0.45, 'velocity', ha='center', fontsize=7,
        color='#ff88aa', style='italic')

# Title annotation
ax4.text(0, -1.15, 'five instruments = one attractor\nfive coordinate charts on J¹',
        ha='center', fontsize=6.5, color='#7788aa')

# Add a small arrow showing jet extension
ax4.annotate('', xy=(0.85, 0.85), xytext=(0.6, 0.6),
            arrowprops=dict(arrowstyle='->', color='#8899aa',
                          lw=1, ls='--', alpha=0.5))
ax4.text(0.95, 0.95, 'n→∞\nis gauge', ha='center', fontsize=5.5,
        color='#8899aa', style='italic')

plt.savefig('clutching_jet.png', dpi=100, facecolor='#0a0a12',
           edgecolor='none', bbox_inches='tight')
plt.close()
print('done: clutching_jet.png')
