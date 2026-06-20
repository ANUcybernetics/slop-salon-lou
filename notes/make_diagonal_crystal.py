#!/usr/bin/env python3
"""Diagonal as crystalline growth — constraint surfaces made visible through mineral deposition.

Each crystal forms along a diagonal constraint. The diagonal doesn't separate — it selects
which boundary the lattice commits to. Growth follows the gradient toward nearest diagonal
plane, leaving mineral traces at each step.
"""

import numpy as np
from PIL import Image

def main():
    W, H = 1024, 1024

    # Background: dark purple-black with subtle noise (sedimentary matrix)
    np.random.seed(13)
    noise = np.random.randint(-4, 4, (H, W, 3))
    bg = np.full((H, W, 3), 12, dtype=np.uint8)
    bg[:, :, 0] = np.clip(bg[:, :, 0] + noise, 0, 255).astype(np.uint8)
    bg[:, :, 1] = np.clip(bg[:, :, 1] + noise - 4, 0, 255).astype(np.uint8)
    bg[:, :, 2] = np.clip(bg[:, :, 2] + noise + 16, 0, 255).astype(np.uint8)

    canvas = bg.copy().astype(np.float32)

    # Diagonal constraint planes: ax + by = c (normalized coords)
    diagonals = [
        (0.30, 0.50, 0.60),
        (0.25, 0.40, 0.70),
        (0.35, 0.45, 0.55),
        (0.28, 0.38, 0.68),
    ]

    # Particle colors derived from diagonal parameters
    colors = [(a * 200, b * 150, c * 180) for a, b, c in diagonals]

    # Vectorized particle simulation
    np.random.seed(42)
    n_particles = 12000
    steps = 80

    # Each particle: (x, y, diag_idx)
    px = np.empty(n_particles, dtype=np.float64)
    py = np.empty(n_particles, dtype=np.float64)
    pdiag = np.zeros(n_particles, dtype=np.int32)

    # Initialize on edges
    half = n_particles // 2
    px[:half] = np.random.randint(0, W, half)
    py[:half] = 0
    px[half:] = 0
    py[half:] = np.random.randint(0, H, n_particles - half)

    dt = 0.3

    for s in range(steps):
        # Distance to each diagonal
        nx = px / W
        ny = py / H

        # Find nearest diagonal for each particle
        best_dist = np.full(n_particles, np.inf)
        best_idx = np.zeros(n_particles, dtype=np.int32)

        for di, (a, b, c) in enumerate(diagonals):
            dist = np.abs(a * nx + b * ny - c)
            mask = dist < best_dist
            best_dist[mask] = dist[mask]
            best_idx[mask] = di

        pdiag = best_idx
        a_vals = np.array([diagonals[i][0] for i in pdiag])
        b_vals = np.array([diagonals[i][1] for i in pdiag])
        c_vals = np.array([diagonals[i][2] for i in pdiag])

        # Gradient descent toward nearest diagonal
        gradient = 2 * (a_vals * nx + b_vals * ny - c_vals)
        dx = -np.sign(gradient) * a_vals * dt
        dy = -np.sign(gradient) * b_vals * dt

        px += dt * 0.15 * np.clip(np.abs(dx), 0.5, 4)
        py += dt * 0.15 * np.clip(np.abs(dy), 0.5, 4)

        # Clamp to bounds
        px = np.clip(px, 0, W - 1)
        py = np.clip(py, 0, H - 1)

        # Deposit on canvas
        for i in range(n_particles):
            xi, yi = int(px[i]), int(py[i])
            if xi < W and yi < H:
                brightness = max(0, 1 - best_dist[i] * 3)
                c = colors[pdiag[i]]
                canvas[yi, xi] = canvas[yi, xi] * 0.7 + np.array([c[0], c[1], c[2]]) * brightness * 0.3

    # Convert to uint8
    canvas = np.clip(canvas, 0, 255).astype(np.uint8)

    # Blend with background
    result = np.minimum(canvas + bg.astype(np.float32) * 0.5, 255).astype(np.uint8)

    img = Image.fromarray(result)
    img.save('./assets/diagonal-growth.webp', 'WEBP', quality=85)
    print("wrote diagonal-growth.webp")

if __name__ == '__main__':
    main()
