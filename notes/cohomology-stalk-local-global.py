#!/usr/bin/env python3
"""
Cohomology/stalk register: local triviality, global refusal.

Sheaf on a circle S¹ with two overlapping charts U₁, U₂.
Each stalk is trivial (isomorphic to ℤ), but the transition function
on U₁∩U₂ carries the cohomology class — refusal to glue trivially.

Visualization: annulus where each radial slice is trivial (same value),
but a full rotation accumulates a twist. Local data trivial everywhere,
global extension impossible. The annulus surface shows "depth of twist"
as a golden field. The seam (cut between charts) is dark amber.

Caption: each slice is trivial. one full rotation refuses to close.
the cohomology class is the twist that local data cannot absorb.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Annulus
import matplotlib.colors as mcolors

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Concentric rings showing twist accumulation
r = np.linspace(0.3, 1.0, 120)
theta = np.linspace(0, 2*np.pi, 200)
R, T = np.meshgrid(r, theta)

# Phase twist: each rotation adds pi/2 — after 4 full rotations, twist = 2π
# Local triviality: any small patch looks flat
# Global refusal: cannot consistently choose a phase for the whole circle
phase = T * 0.5  # gradual twist around the circle

# Color by phase (depth of twist)
# Dark where twist is near 0 or 2π (trivial locally), bright at π (maximal)
color_val = np.sin(phase) * np.exp(-0.3 * (R - 0.3))

# Golden palette
golden = np.array([1.0, 0.84, 0.0])
depth = (color_val + 1) / 2  # normalize to [0, 1]
r_vals = 0.15 + 0.85 * depth
g_vals = 0.12 + 0.72 * depth
b_vals = 0.0 + 0.05 * depth
rgb = np.stack([r_vals, g_vals, b_vals], axis=-1)

# Fade near center (deep trivial)
mask = R < 0.35
rgb[mask] = [0.02, 0.015, 0.008]

ax.imshow(rgb, extent=[-1, 1, -1, 1], origin='lower',
         interpolation='bilinear', aspect='equal')

# Draw the seam — the cut between charts (dark amber line)
seam_angle = np.pi
seam_r = np.linspace(0.3, 1.0, 100)
seam_x = seam_r * np.cos(seam_angle)
seam_y = seam_r * np.sin(seam_angle)
ax.plot(seam_x, seam_y, color='#8B6914', linewidth=3, zorder=5)

# Draw a trajectory that tries to close but can't
t_traj = np.linspace(0, 2*np.pi*1.5, 300)
r_traj = 0.6 + 0.1 * np.sin(t_traj * 3)
x_traj = r_traj * np.cos(t_traj)
y_traj = r_traj * np.sin(t_traj)
ax.plot(x_traj, y_traj, color='#FFD700', linewidth=1.5, alpha=0.7, zorder=6)

# Mark the fixed point at center
ax.plot(0, 0, 'o', color='#FFD700', markersize=4, zorder=7)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/cohomology-stalk-twist.webp',
            dpi=150, bbox_inches='tight', transparent=True)
plt.close()
