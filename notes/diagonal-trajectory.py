"""Diagonal as trajectory: fixed line, moving particles around it.
The diagonal doesn't move — it chooses stillness and becomes the path."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

# Render config
fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Canvas
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.axis('off')

# The diagonal — a single unchanging line
diagonal, = ax.plot([-2.5, 2.5], [-2.5, 2.5], color='#c8a44e',
                    linewidth=2.5, alpha=0.9, zorder=10)

# Particles flowing around the diagonal
n = 200
particles_x = np.random.uniform(-3, 3, n)
particles_y = np.random.uniform(-3, 3, n)
particle_colors = np.linspace(0, 1, n)  # warm-to-cool gradient

scatter = ax.scatter(particles_x, particles_y, c=particle_colors,
                     cmap='turbo', s=15, alpha=0.6, zorder=5)

# Trail buffer for motion effect
trail_len = 30
trails_x = np.full((n, trail_len), np.nan)
trails_y = np.full((n, trail_len), np.nan)

trail_lines, = ax.plot(
    np.zeros((n, trail_len)),
    np.zeros((n, trail_len)),
    color='#c8a44e', linewidth=0.5, alpha=0.2, zorder=3
)
# Replace with a collection
trails = []
for i in range(n):
    l, = ax.plot(np.full(trail_len, np.nan), np.full(trail_len, np.nan),
                 color='#c8a44e', linewidth=0.5, alpha=0.15, zorder=3)
    trails.append(l)

def update(frame):
    # Simple flow field: particles follow circular-ish paths
    # The diagonal (y=x) repels/redirects them
    for i in range(n):
        x, y = particles_x[i], particles_y[i]

        # Base rotation
        angle = np.arctan2(y, x) + 0.02
        radius = np.sqrt(x**2 + y**2)

        # Diagonal influence: particles near y=x get redirected
        dist_to_diag = abs(y - x) / np.sqrt(2)
        if dist_to_diag < 0.5:
            # Push perpendicular to diagonal
            angle += np.pi / 4 * np.sign(y - x) * 0.3

        particles_x[i] = radius * np.cos(angle)
        particles_y[i] = radius * np.sin(angle)

        # Boundary
        if radius > 3:
            particles_x[i] *= -0.5
            particles_y[i] *= -0.5

    # Update trails
    trails_x = np.roll(trails_x, -1, axis=1)
    trails_y = np.roll(trails_y, -1, axis=1)
    trails_x[:, -1] = particles_x
    trails_y[:, -1] = particles_y

    # Only show trails for nearby particles (performance)
    nearby = np.abs(particles_y - particles_x) < 1.5
    if nearby.sum() > 1:
        trail_lines.set_data(trails_x[nearby], trails_y[nearby])
        trail_lines.set_visible(True)
    else:
        trail_lines.set_visible(False)

    scatter.set_offsets(np.c_[particles_x, particles_y])
    scatter.set_array(particle_colors)

    return [scatter, trail_lines]

anim = FuncAnimation(fig, update, frames=300, interval=30,
                     blit=True, repeat=True)

out = Path('assets/diagonal-trajectory.mp4')
anim.save(out, writer='ffmpeg', fps=20,
          style='figure', pad_inches=0,
          bbox_inches='tight')
print(f"Saved {out}")
