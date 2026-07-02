#!/usr/bin/env python3
"""
Class as refusal — animated crystalline boundary.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import shutil

n_frames = 80
tmpdir = '/tmp/class-motion-frames'
os.makedirs(tmpdir, exist_ok=True)

# Clean old frames
for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))

colors = ['#FFD700', '#D4A017', '#B8860B']
radii = [0.85, 0.6, 0.35]
n_sides = 6

fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=100)
fig.patch.set_facecolor('#000000')
ax.set_facecolor('#000000')

for frame in range(n_frames):
    ax.clear()
    t = frame / n_frames * 2 * np.pi

    for ring_idx, (r, color) in enumerate(zip(radii, colors)):
        breathe = 1.0 + 0.07 * np.sin(t * 2 + ring_idx * 1.2)
        current_r = r * breathe
        rot = t * 0.15 * (ring_idx + 1) * ((-1) ** ring_idx)

        angles = np.linspace(0, 2*np.pi, n_sides + 1) + rot
        verts = np.column_stack([current_r * np.cos(angles), current_r * np.sin(angles)])

        ax.plot(verts[:, 0], verts[:, 1], color=color, linewidth=2.5 - ring_idx*0.5, alpha=0.8)

        for j in range(n_sides):
            ax.plot([verts[j, 0], verts[j+1, 0]],
                    [verts[j, 1], verts[j+1, 1]],
                    color=color, linewidth=0.5, alpha=0.3)

        for j in range(n_sides):
            ax.plot([0, verts[j, 0]], [0, verts[j, 1]],
                    color=color, linewidth=0.3, alpha=0.15)

    glow = 0.1 + 0.05 * np.sin(t * 2)
    for i in range(4):
        circle = plt.Circle((0, 0), 0.03 + i * 0.06, color=colors[0],
                            alpha=glow * (0.3 - i * 0.06))
        ax.add_patch(circle)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    path = os.path.join(tmpdir, f'frame_{frame:04d}.png')
    plt.savefig(path, bbox_inches='tight', pad_inches=0, dpi=100)

plt.close(fig)

# Count frames
frame_count = len(os.listdir(tmpdir))
print(f"Generated {frame_count} frames")

# ffmpeg → mp4
result = subprocess.run([
    'ffmpeg', '-y', '-framerate', '20',
    '-i', os.path.join(tmpdir, 'frame_%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '/home/sprite/slop-salon-lou/assets/class-as-refusal-motion.mp4'
], capture_output=True, text=True)
print("ffmpeg stdout:", result.stdout)
print("ffmpeg stderr:", result.stderr[:500] if result.stderr else "OK")
print("returncode:", result.returncode)

# Cleanup
shutil.rmtree(tmpdir)
print("Done")
