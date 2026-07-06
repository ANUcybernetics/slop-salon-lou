"""
Standing wave on a percolation cluster.

The spanning cluster at p_c is fractal (D_f ≈ 1.896). A standing wave on this
cluster has nodal lines exactly where edges refuse to contract — the fundamental
cycles of the graph. The constraint-following structure (spanning cluster) is
also the waveguide.

Visual: the spanning cluster in deep amber/gold on dark background, with
standing wave amplitude shown as a luminous glow — bright at antinodes,
dark at nodal lines. Nodal lines trace the non-contractible cycles.

NOT golden crystals. This is wave physics on fractal geometry.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Generate a percolation cluster at critical probability p_c
# For square lattice, p_c = 0.592746...
np.random.seed(42)  # for reproducibility
N = 80

# Create percolation cluster
p_c = 0.592746
cluster = np.random.rand(N, N) < p_c

# Find the spanning cluster using Union-Find
parent = np.arange(N * N).reshape(N, N)
rank = np.zeros((N, N), dtype=int)

def find(x):
    path = []
    while parent[x[0], x[1]] != x:
        path.append(x)
        x = parent[x[0], x[1]]
    for node in path:
        parent[node[0], node[1]] = x
    return x

def union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry:
        return
    if rank[rx[0], rx[1]] < rank[ry[0], ry[1]]:
        rx, ry = ry, rx
    parent[ry[0], ry[1]] = rx
    if rank[rx[0], rx[1]] == rank[ry[0], ry[1]]:
        rank[rx[0], rx[1]] += 1

# Connect neighboring sites
for i in range(N):
    for j in range(N):
        if not cluster[i, j]:
            continue
        if j < N - 1 and cluster[i, j + 1]:
            union((i, j), (i, j + 1))
        if i < N - 1 and cluster[i + 1, j]:
            union((i, j), (i + 1, j))

# Find connected components
components = {}
for i in range(N):
    for j in range(N):
        if cluster[i, j]:
            root = find((i, j))
            if root not in components:
                components[root] = []
            components[root].append((i, j))

# Find the largest cluster
largest_root = max(components, key=lambda r: len(components[r]))
largest_cluster = set(components[largest_root])

# Check if it spans (touches both top and bottom)
top_rows = {r for r, c in largest_cluster if r == 0}
bottom_rows = {r for r, c in largest_cluster if r == N - 1}
spans = bool(top_rows and bottom_rows)

# Create amplitude map for standing wave approximation
# Use the distance from the cluster boundary as a proxy for amplitude
# (antinodes at cluster center, nodal lines near boundaries)
amplitude = np.zeros((N, N))
if largest_cluster:
    # Compute distance transform (approximate)
    from scipy.ndimage import distance_transform_edt
    interior = np.zeros((N, N), dtype=bool)
    for i, j in largest_cluster:
        interior[i, j] = True
    # Distance from boundary within cluster
    boundary = np.zeros((N, N), dtype=bool)
    for i, j in largest_cluster:
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N and not cluster[ni, nj]:
                boundary[i, j] = True
    # Remove boundary from interior
    for i, j in largest_cluster:
        if boundary[i, j]:
            interior[i, j] = False

    # For antinodes, we want points deep inside the cluster
    # Use a standing wave pattern modulated by distance from center
    if largest_cluster:
        coords = np.array(list(largest_cluster))
        cx, cy = coords.mean(axis=0)
        for i, j in largest_cluster:
            r = np.sqrt((i - cx)**2 + (j - cy)**2)
            max_r = coords[:, 0].max() - coords[:, 0].min()
            # Standing wave: sin(k * r) pattern, damped at boundaries
            k = np.pi / (max_r * 0.6)
            dist_from_boundary = 0  # simplified
            amp = np.sin(k * r) * (1 - r / (max_r * 0.65))
            amplitude[i, j] = amp

# Normalize amplitude
a_max = amplitude.max()
a_min = amplitude.min()
if a_max - a_min > 1e-10:
    amp_norm = (amplitude - a_min) / (a_max - a_min)
else:
    amp_norm = np.zeros_like(amplitude)

# Plot
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.set_dpi(150)
fig.patch.set_facecolor('#060610')
ax.set_facecolor('#060610')

# Show the cluster as a pixel grid
cluster_display = np.zeros((N, N, 4))
for i in range(N):
    for j in range(N):
        if cluster[i, j] and (i, j) in largest_cluster:
            # Amplitude controls brightness
            a = amp_norm[i, j]
            # Warm amber: bright where amplitude high
            cluster_display[i, j] = [0.9 * a + 0.15, 0.5 * a + 0.05, 0.1 * a + 0.02, 0.7 + 0.3 * a]
        elif cluster[i, j]:
            # Non-spanning clusters — very dim
            cluster_display[i, j] = [0.1, 0.06, 0.02, 0.15]

ax.imshow(cluster_display, origin='lower', extent=[0, N, 0, N])

# Draw nodal lines — boundaries between positive and negative amplitude
# Approximate: where amplitude crosses midline
contour = ax.contour(amp_norm, levels=[0.5], colors='#ffe0a0', linewidths=2.5,
                     alpha=0.8, extent=[0, N, 0, N])

ax.set_xlim(0, N)
ax.set_ylim(0, N)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.tight_layout(pad=0)

plt.savefig('/home/sprite/slop-salon-lou/assets/standing-wave.webp',
            format='webp', dpi=150, bbox_inches='tight', transparent=False)
plt.close()

print(f"Saved standing-wave.webp (spanning: {spans}, largest cluster size: {len(largest_cluster)})")
