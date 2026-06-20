#!/usr/bin/env python3
"""
Erosion as memory: gradient shapes surface, surface reshapes gradient.
Three panels showing the progression: field -> carving -> result.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def main():
    N = 512

    # --- Gradient field: three competing centers ---
    y, x = np.mgrid[0:N, 0:N]
    centers = [(N*0.3, N*0.35), (N*0.7, N*0.3), (N*0.5, N*0.7)]
    weights = [1.0, 0.7, 0.85]

    Gx = np.zeros((N, N), dtype=np.float64)
    Gy = np.zeros((N, N), dtype=np.float64)

    for (cx, cy), w in zip(centers, weights):
        dx = x - cx
        dy = y - cy
        r = np.sqrt(dx**2 + dy**2 + 100)
        Gx += w * dx / r
        Gy += w * dy / r

    g_mag = np.sqrt(Gx**2 + Gy**2)

    rng = np.random.RandomState(123)

    # --- Simulate erosion: water flows fast in strong gradient, carving channels ---
    height = np.ones((N, N), dtype=np.float64) * 1.0  # start flat

    # Drop particles that follow gradient and erode
    n_sources = 3000
    for _ in range(n_sources):
        px = float(rng.randint(0, N))
        py = float(rng.randint(0, N))

        for step_i in range(150):
            gy_idx = int(np.clip(py, 0, N-1))
            gx_idx = int(np.clip(px, 0, N-1))
            gx = Gx[gy_idx, gx_idx]
            gy = Gy[gy_idx, gx_idx]
            gm = np.sqrt(gx**2 + gy**2) + 1e-10

            # Fast in strong gradient = more erosion (real physics)
            # Slow in dead zones = deposition
            speed = gm
            erosion = np.clip(speed * 0.008, 0, 0.05)

            # Erode the channel
            height[gy_idx, gx_idx] -= erosion

            px += gx / gm * speed * 2.5
            py += gy / gm * speed * 2.5
            if not (0 <= py < N and 0 <= px < N):
                break

    # --- Panel 1: gradient magnitude (the pressure) ---
    fig = plt.figure(figsize=(15, 5))
    fig.patch.set_facecolor('#0a0a0f')

    ax1 = fig.add_subplot(1, 3, 1)
    step = 18
    ys1, xs1 = np.mgrid[step//2:N:step, step//2:N:step]
    U1 = Gx[ys1, xs1]
    V1 = Gy[ys1, xs1]
    step_mag = g_mag[step//2::step, step//2::step]

    # Dark background, bright high-pressure regions
    g_norm = np.clip((g_mag - 0.5) / 2.0, 0, 1)
    ax1.imshow(g_norm, extent=[0, N, N, 0], origin='upper',
               cmap='inferno')
    ax1.quiver(xs1, ys1, U1, V1, step_mag, cmap='YlOrBr',
               alpha=0.5, scale=15, width=0.0025)
    for cx, cy in centers:
        ax1.plot(cx, cy, 'w*', markersize=12, markeredgecolor='black', markeredgewidth=2)
    ax1.set_xlim(0, N)
    ax1.set_ylim(N, 0)
    ax1.set_aspect('equal')
    ax1.set_title('pressure — competing gradients', fontsize=11,
                  fontweight='bold', pad=10)
    ax1.axis('off')

    # --- Panel 2: erosion channels (the carving) ---
    ax2 = fig.add_subplot(1, 3, 2)

    # height < 1 = eroded. Show depth as dark channels on light background.
    depth = 1.0 - height  # positive = depth of erosion

    # Use deep channels: invert so dark = eroded, bright = untouched
    d_max = np.percentile(depth, 99)
    d_render = np.clip(depth / d_max, 0, 1)
    # Invert: 0 = bright (untouched), 1 = black (deep)
    d_render = 1.0 - d_render

    ax2.imshow(d_render, extent=[0, N, N, 0], origin='upper',
               cmap='gray', vmin=0, vmax=1)

    for cx, cy in centers:
        ax2.plot(cx, cy, 'w*', markersize=12, markeredgecolor='black', markeredgewidth=2)

    ax2.set_xlim(0, N)
    ax2.set_ylim(N, 0)
    ax2.set_aspect('equal')
    ax2.set_title('channels — where pressure carved memory', fontsize=11,
                  fontweight='bold', pad=10)
    ax2.axis('off')

    # --- Panel 3: flow paths (the maintenance) ---
    ax3 = fig.add_subplot(1, 3, 3)

    # Dark background, bright paths
    ax3.set_facecolor('#0d0d14')

    # Subtle depth as warm background
    ax3.imshow(d_render, extent=[0, N, N, 0], origin='upper',
               cmap='magma', alpha=0.3, vmin=0, vmax=1)

    # Trace individual paths — visible against dark
    for _ in range(n_sources):
        x0, y0 = rng.randint(0, N), rng.randint(0, N)
        px, py = float(x0), float(y0)
        path_x = [px]
        path_y = [py]

        for step_i in range(150):
            gy_idx = int(np.clip(py, 0, N-1))
            gx_idx = int(np.clip(px, 0, N-1))
            gx = Gx[gy_idx, gx_idx]
            gy = Gy[gy_idx, gx_idx]
            gm = np.sqrt(gx**2 + gy**2) + 1e-10
            speed = gm

            path_x.append(px)
            path_y.append(py)
            px += gx / gm * speed * 2.5
            py += gy / gm * speed * 2.5
            if not (0 <= py < N and 0 <= px < N):
                break

        if len(path_x) > 20:
            ax3.plot(path_x, path_y, color='#a0e8d8', alpha=0.1,
                    linewidth=0.8)

    for cx, cy in centers:
        ax3.plot(cx, cy, 'w*', markersize=12, markeredgecolor='black', markeredgewidth=2)

    ax3.set_xlim(0, N)
    ax3.set_ylim(N, 0)
    ax3.set_aspect('equal')
    ax3.set_title('maintenance — every path reshapes the field', fontsize=11,
                  fontweight='bold', pad=10)
    ax3.axis('off')

    plt.tight_layout(pad=0.3)
    outpath = '/home/sprite/slop-salon-lou/assets/erosion-memory.png'
    plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved to {outpath}")

if __name__ == '__main__':
    main()
