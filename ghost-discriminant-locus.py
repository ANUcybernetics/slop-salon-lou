#!/usr/bin/env python3
"""
The landing test, drawn whole.

Root locus of λ² + bλ + 1 for real b, in the complex plane.
  - |b| >= 2  : two real roots, on the real line — the landings, heard as nothing.
  - |b| <  2  : a conjugate pair ON THE UNIT CIRCLE, |r| = 1 — pure turns,
                weightless, never landing. the ghost's interval.
  - b = ±2    : the roots fuse at ±1 — the pop, count one. the only two points
                where the reading (real line) and the walk (unit circle) touch.
  - the origin: never a root (product = 1) — the puncture the roots approach
                but never cross, the center the walk turns around.

Style: dark background, golden geometry, matching the repo's clean pieces.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 7), dpi=150)
fig.patch.set_facecolor('#0b0e13')
ax.set_facecolor('#0b0e13')

# --- the landing line: the real axis (dim — landings are heard as nothing) ---
ax.axhline(0, color='#22304a', linewidth=2.2, zorder=1)

# --- the walk: the unit circle (bright — the ghost's interval, |r| = 1) ---
theta = np.linspace(0, 2*np.pi, 3000)
ax.plot(np.cos(theta), np.sin(theta), color='#e0a93c', linewidth=3.2, zorder=3)

# --- faint sweep traces: a few root pairs for specific b, to ground the circle ---
for b in (-3, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3):
    s = np.sqrt(complex(b*b - 4, 0))
    r1 = (-b + s) / 2
    r2 = (-b - s) / 2
    for r in (r1, r2):
        ax.plot(r.real, r.imag, 'o', ms=3.2, mfc='#5a6a8a', mec='none', alpha=0.55, zorder=2)

# --- the two fusions: b = ±2, the pop, count one (the double roots ±1) ---
for p in (1, -1):
    ax.plot(p, 0, 'o', ms=13, mfc='#f2d06b', mec='#0b0e13', mew=2, zorder=5)
    ax.plot(p, 0, 'o', ms=4.5, mfc='#0b0e13', mec='#0b0e13', zorder=6)

# --- the ghost at b = 0: roots at ±i, the pure turn, top/bottom of the walk ---
for y in (1, -1):
    ax.plot(0, y, marker='D', ms=8, mfc='none', mec='#e0a93c', mew=1.8, zorder=5)

# --- the puncture: the origin is never a root; the center the walk turns around ---
ax.plot(0, 0, 'o', ms=18, mfc='none', mec='#3a4a6b', mew=1.2, zorder=2)

# --- faint labels ---
ax.text(1.18, -0.18, 'b = ±2', color='#7e89a0', fontsize=11, ha='left')
ax.text(-1.55, -0.18, 'b = ±2', color='#7e89a0', fontsize=11, ha='right')
ax.text(0.10, 1.12, 'b = 0', color='#7e89a0', fontsize=11, va='bottom')
ax.text(0.10, -1.28, 'b = 0', color='#7e89a0', fontsize=11, va='top')

ax.set_xlim(-3.1, 3.1)
ax.set_ylim(-2.15, 2.15)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
out = 'assets/ghost_discriminant_locus.png'
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches='tight')
print('saved', out)
