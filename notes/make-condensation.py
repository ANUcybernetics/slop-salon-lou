#!/usr/bin/env python3
"""
Condensation as surface becoming legible.
Droplets nucleate and coalesce. Each surviving drop is a region of
closest approach — the canvas shows which drop owns each pixel.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    N = 512
    rng = np.random.RandomState(42)

    # --- Step 1: nucleate ---
    n_drops = int(N * N / 150)
    drops_x = rng.rand(n_drops) * N
    drops_y = rng.rand(n_drops) * N
    drops_r = (np.random.rand(n_drops) ** 1.5) * 10 + 2

    # --- Step 2: coalescence ---
    order = np.argsort(-drops_r)
    x = drops_x[order].copy()
    y = drops_y[order].copy()
    r = drops_r[order].copy()
    alive = np.ones(len(x), dtype=bool)
    alive[0] = True

    for i in range(len(x)):
        if not alive[i]:
            continue
        for j in range(i + 1, len(x)):
            if not alive[j]:
                continue
            dx = x[i] - x[j]
            dy = y[i] - y[j]
            dist = np.hypot(dx, dy)
            merge_r = (r[i] ** 2 + r[j] ** 2) ** 0.5
            if dist < merge_r * 2:
                new_x = (r[i]**2 * x[i] + r[j]**2 * x[j]) / (r[i]**2 + r[j]**2)
                new_y = (r[i]**2 * y[i] + r[j]**2 * y[j]) / (r[i]**2 + r[j]**2)
                x[i] = new_x
                y[i] = new_y
                r[i] = merge_r
                alive[j] = False

    surv = np.where(alive)[0]
    sx, sy, sr = x[surv], y[surv], r[surv]
    ns = len(sx)
    print(f"{ns} drops survived from {n_drops} initial")

    # --- Step 3: render ---
    # For each pixel, find the closest drop center (by distance / radius ratio)
    # This creates natural boundaries between adjacent drops
    yg, xg = np.mgrid[0:N, 0:N]

    canvas = np.zeros((N, N), dtype=np.float64)
    highlight = np.zeros((N, N), dtype=np.float64)

    for i in range(ns):
        cx, cy, cr = sx[i], sy[i], sr[i]
        rr = max(int(cr) + 3, 3)
        y0 = max(0, int(cy) - rr)
        y1 = min(N, int(cy) + rr + 1)
        x0 = max(0, int(cx) - rr)
        x1 = min(N, int(cx) + rr + 1)

        dy = yg[y0:y1, x0:x1] - cy
        dx = xg[y0:y1, x0:x1] - cx
        d = np.hypot(dx, dy) / (cr + 1e-10)

        # Smooth circular mask
        mask = np.exp(-d**2 * 2)

        # Brightness: drop interior with gradient
        brightness = 0.3 + 0.5 * np.exp(-d**2 * 3)

        # Bright rim
        rim = np.exp(-((d - 1.0) ** 2) / 0.015) * 0.6

        # Specular highlight (offset toward upper-left)
        hx = cx - cr * 0.25
        hy = cy - cr * 0.35
        hxg = xg[y0:y1, x0:x1] - hx
        hyg = yg[y0:y1, x0:x1] - hy
        sd = np.hypot(hxg, hyg) / max(cr * 0.15, 1)
        spec = np.exp(-sd**2) * 0.7

        # Only keep where this drop is the "closest" relative to its radius
        # Simple approach: multiply by mask^0.5 (fade at edges)
        fade = np.exp(-d**2 * 4)

        canvas[y0:y1, x0:x1] += (brightness + rim + spec) * fade
        highlight[y0:y1, x0:x1] += fade

    canvas = np.clip(canvas / (highlight + 0.001), 0, 1)
    canvas = np.clip(canvas, 0, 1)

    # Contrast stretch
    p95 = np.percentile(canvas, 95)
    canvas = np.clip(canvas / p95, 0, 1)
    canvas = canvas ** 0.9

    # --- Render ---
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_facecolor('#060608')

    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(canvas, extent=[0, N, N, 0], origin='upper',
               cmap='Greys_r', vmin=0, vmax=1)

    ax1.set_xlim(0, N)
    ax1.set_ylim(N, 0)
    ax1.set_aspect('equal')
    ax1.set_title('condensation — surface becoming legible', fontsize=11,
                  fontweight='bold', pad=10)
    ax1.axis('off')

    plt.tight_layout(pad=0.2)
    outpath = '/home/sprite/slop-salon-lou/assets/condensation.png'
    plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

    print(f"Saved to {outpath}")

if __name__ == '__main__':
    main()
