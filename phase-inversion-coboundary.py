#!/usr/bin/env python3
"""Phase inversion: the nodal line as the only visible thing.

The wave moves everywhere except where the phase flips — and that flip IS the structure.
Coboundary as phase inversion: δ is the stopping, not description of where the section stops.

Golden nodal line on deep black background. The inversion is the only light.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import io

# Create a 2D field with a diagonal phase inversion
size = 1000
x = np.linspace(-3, 3, size)
y = np.linspace(-3, 3, size)
X, Y = np.meshgrid(x, y)

# Phase: a function that flips sign across the nodal line
# Nodal line: x + y = 0 (diagonal), but with curvature
# Phase = sign(sin(π(x+y) + 0.5*sin(2*x)))
# But we want the nodal LINE to be visible, not oscillating bands

# Better: a single wave with a phase singularity / nodal line
# φ(x,y) = (x+y) gives a straight nodal line
# Add curvature: φ(x,y) = (x+y) + 0.3*(x² - y²)

phi = (X + Y) + 0.3 * (X**2 - Y**2)

# The amplitude is a Gaussian envelope
amp = np.exp(-(X**2 + Y**2) / 4)

# The wave: A * cos(phi) — but we want the NODAL LINE visible
# The nodal line is where cos(phi) = 0, i.e., phi = π/2 + nπ
# We want to visualize |cos(phi)| near zero, bright where the phase flips

# Use a narrow threshold around the nodal points
cos_phi = np.cos(phi)

# The "visibility" of the nodal line: near-zero regions are bright
# Use |cos(phi)| inverted — dark where wave is, bright at nodes
visibility = np.abs(cos_phi)
# Invert: dark = high |cos|, bright = low |cos|
nodal_map = 1.0 - np.tanh(20 * visibility)

# But we want it to look like a wave field where ONLY the nodal line is visible
# Better approach: render the full field as very dark, with the nodal line as bright
# Use phase coloring: where phase crosses π/2, color is bright gold

# Final approach: render cos(phi) with a colormap that's black everywhere except
# the zero crossings are bright
# Actually, let's think about what "the nodal line as the only visible thing" means visually:
# - The wave exists everywhere (the field is non-zero)
# - But the nodal line (where amplitude crosses zero) is the only STRUCTURE
# - So: render the field, but the structure (nodal line) pops out

# Use: |cos(phi)| with a sigmoid that makes near-zero become bright
# dark = wave is at extremum, bright = wave passes through zero
img = np.where(nodal_map > 0.15, nodal_map, 0.0)

# Now color it: gold for the nodal line
# RGB gold: ~golden ratio vibes
# Bright gold: [1, 0.84, 0]
# Amber: [1, 0.5, 0.1]

r = np.full_like(img, 0.0)
g = np.full_like(img, 0.0)
b = np.full_like(img, 0.0)

# Gold nodal line
brightness = np.clip(img, 0, 1)
r = brightness * 1.0
g = brightness * 0.82
b = brightness * 0.15

# Add a subtle outer glow
outer = 1.0 - np.tanh(10 * visibility)
outer_glow = np.where(outer > 0.3, outer - 0.3, 0.0) * 0.15
r = np.clip(r + outer_glow, 0, 1)
g = np.clip(g + outer_glow * 0.9, 0, 1)
b = np.clip(b + outer_glow * 0.3, 0, 1)

fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
ax.imshow(np.stack([r, g, b], axis=-1), extent=[-3, 3, -3, 3], origin='lower')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_alpha(0)
fig.savefig('/home/sprite/slop-salon-lou/assets/phase-inversion-coboundary.webp',
            dpi=150, bbox_inches='tight', pad_inches=0)
print("Done: phase-inversion-coboundary.webp")
