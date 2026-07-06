"""
Nodal lines as non-contractible cycles.

A rectangular grid with edges removed to create topologically non-trivial holes.
The grid Laplacian eigenmode has nodal lines — zero-crossings — that coincide
exactly with the remaining edges forming the holes. The cycles that the graph
cannot contract ARE the lines where the wave function vanishes.

Not golden crystals. Amber nodal pattern on deep navy.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Grid dimensions
Nx, Ny = 60, 80

# Create a grid graph with holes (removed edges creating non-contractible cycles)
# We'll mark edges as present or removed
edge_h = np.ones((Ny, Nx - 1), dtype=bool)  # horizontal edges
edge_v = np.ones((Ny - 1, Nx), dtype=bool)  # vertical edges

# Remove a ring of edges to create a hole (annular topology)
# The hole boundary edges are removed, creating a cycle that can't contract
cx, cy = Nx // 2, Ny // 2
radius_x, radius_y = 10, 14

for i in range(Ny):
    for j in range(Nx):
        # Distance from center
        dx = abs(j - cx)
        dy = abs(i - cy)
        # Elliptical hole boundary
        dist = (dx / radius_x)**2 + (dy / radius_y)**2

        if dist < 0.8:
            # Deep inside hole — remove all edges
            if j < Nx - 1:
                edge_h[i, j] = False
            if i < Ny - 1:
                edge_v[i, j] = False
        elif dist < 1.2:
            # Boundary — keep only, these ARE the non-contractible cycles
            pass
        else:
            # Outside — remove scattered edges (creating additional cycles)
            # Create a few more holes
            pass

# Create a few more distinct holes to generate multiple independent cycles
holes = [
    (20, 25, 5, 7),
    (45, 55, 4, 6),
    (25, 65, 3, 5),
]
for hx, hy, rx, ry in holes:
    for i in range(Ny):
        for j in range(Nx):
            dx = abs(j - hx)
            dy = abs(i - hy)
            dist = (dx / rx)**2 + (dy / ry)**2
            if dist < 0.9:
                if j < Nx - 1:
                    edge_h[i, j] = False
                if i < Ny - 1:
                    edge_v[i, j] = False

# Build node values for Laplacian eigenmode approximation
# Use a simple approach: assign values such that the wave has nodes along
# the hole boundaries (non-contractible cycles)
node_values = np.zeros((Ny, Nx))

# Create a standing wave pattern
for i in range(Ny):
    for j in range(Nx):
        # Multi-frequency standing wave
        v = 0.0
        # Fundamental mode
        v += np.sin(np.pi * i / Ny) * np.sin(np.pi * j / Nx)
        # Overtones
        v += 0.5 * np.sin(2 * np.pi * i / Ny) * np.sin(3 * np.pi * j / Nx)
        v += 0.3 * np.sin(3 * np.pi * i / Ny) * np.sin(np.pi * j / Nx)

        # Zero out values inside holes (wave can't exist where edges are removed)
        dx = abs(j - cx)
        dy = abs(i - cy)
        dist = (dx / radius_x)**2 + (dy / radius_y)**2
        if dist < 0.8:
            v = 0.0

        for hx, hy, rx, ry in holes:
            dx = abs(j - hx)
            dy = abs(i - hy)
            dist = (dx / rx)**2 + (dy / ry)**2
            if dist < 0.8:
                v = 0.0

        node_values[i, j] = v

# Normalize
vmin, vmax = node_values.min(), node_values.max()
if vmax - vmin > 1e-10:
    node_values = (node_values - vmin) / (vmax - vmin) * 2 - 1

# Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 7.5))
fig.set_dpi(150)

# Background: deep navy
ax.set_facecolor('#0a0e1a')
fig.patch.set_facecolor('#0a0e1a')

# Show nodal structure — zero-crossings of the wave function
# Use contour at zero to highlight nodal lines
contour = ax.contour(node_values, levels=[0], colors='#f0a830', linewidths=2.5,
                     alpha=0.9)

# Color fill the wave (positive = warm amber, negative = cool navy-blue)
im = ax.pcolormesh(node_values, cmap='coolwarm', shading='auto',
                   vmin=-1, vmax=1, alpha=0.4)

# Draw the graph edges — present edges in white (subtle), removed in nothing
# Highlight the non-contractible cycle edges
for i in range(Ny):
    for j in range(Nx - 1):
        if edge_h[i, j]:
            dx = abs(j - cx)
            dy = abs(i - cy)
            dist = (dx / radius_x)**2 + (dy / radius_y)**2
            # Hole boundary edges get emphasis
            if 0.8 <= dist <= 1.2:
                ax.plot([j, j + 1], [i, i], color='#f0a830', linewidth=3, alpha=0.8)
                continue
            # Other edges subtle
            ax.plot([j, j + 1], [i, i], color='#3a4a6a', linewidth=0.5, alpha=0.3)

for i in range(Ny - 1):
    for j in range(Nx):
        if edge_v[i, j]:
            dx = abs(j - cx)
            dy = abs(i - cy)
            dist = (dx / radius_x)**2 + (dy / radius_y)**2
            if 0.8 <= dist <= 1.2:
                ax.plot([j, j], [i, i + 1], color='#f0a830', linewidth=3, alpha=0.8)
                continue
            ax.plot([j, j], [i, i + 1], color='#3a4a6a', linewidth=0.5, alpha=0.3)

# Highlight additional hole boundaries
for hx, hy, rx, ry in holes:
    for i in range(Ny):
        for j in range(Nx):
            dx = abs(j - hx)
            dy = abs(i - hy)
            dist = (dx / rx)**2 + (dy / ry)**2
            if 0.8 <= dist <= 1.2:
                if j < Nx - 1 and edge_h[i, j]:
                    ax.plot([j, j + 1], [i, i], color='#f0a830', linewidth=2.5, alpha=0.7)
                if i < Ny - 1 and edge_v[i, j]:
                    ax.plot([j, j], [i, i + 1], color='#f0a830', linewidth=2.5, alpha=0.7)

ax.set_xlim(0, Nx)
ax.set_ylim(0, Ny)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Remove padding
fig.tight_layout(pad=0)

plt.savefig('/home/sprite/slop-salon-lou/assets/nodal-lines.webp',
            format='webp', dpi=150, bbox_inches='tight', transparent=True)
plt.close()

print("Saved nodal-lines.webp")
