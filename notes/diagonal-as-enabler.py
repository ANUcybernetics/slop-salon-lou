#!/usr/bin/env python3
"""The diagonal as enabling boundary.

The diagonal (y=x) is the invisible line that makes the cobweb possible.
Go up to the curve, go right to the diagonal, go up again — the
trajectory depends on the diagonal but is not the diagonal. When it
becomes visible, the geometry changes: the boundary condition is no
longer neutral, it perturbs the map. The diagonal's invisibility IS
what enables it.

32 frames: diagonal fades in from barely-ghost to full line. The
cobweb trajectory (fixed point) shifts as the diagonal's brightness
perturbs the iteration.
"""
import numpy as np
from PIL import Image
import subprocess, os

size = 1024
margin = 100
plot = size - 2 * margin
r_float = 2.9

# Slightly perturbed map: as diagonal brightens, the effective r shifts
r_perturbed = lambda b: r_float + 0.3 * b

def to_px(x, y):
    return int(margin + x * plot), int(size - margin - y * plot)

def draw_line(img, x1, y1, x2, y2, color, alpha=1.0):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    x, y = int(x1), int(y1)
    while True:
        if 0 <= y < size and 0 <= x < size:
            img[y, x] = img[y, x] * (1.0 - alpha) + color * alpha
        if x == int(x2) and y == int(y2):
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

# Background
bg_base = np.full((size, size, 3), 6.0, dtype=np.float64)

# Diagonal + curve — always faint
amber = np.array([200, 145, 55], dtype=np.float64)
gold = np.array([225, 185, 80], dtype=np.float64)
dim_amber = amber * 0.15
curve_col = np.array([80, 60, 25], dtype=np.float64)

for px_ in range(size):
    py_ = size - px_
    if 0 <= py_ < size:
        bg_base[py_, px_] = dim_amber

# Precompute curve path
curve_path = []
x_prev, y_prev = to_px(0, 0)
for i in range(1, 1001):
    x = i / 1000
    y = r_float * x * (1 - x)
    x_cur, y_cur = to_px(x, y)
    curve_path.append((x_prev, y_prev, x_cur, y_cur))
    x_prev, y_prev = x_cur, y_cur

num_frames = 32
frame_paths = []
frame_dir = '/tmp/diagonal_enabler'
os.makedirs(frame_dir, exist_ok=True)

for frame_idx in range(num_frames):
    img = bg_base.copy()

    # Diagonal brightness: 0.03 → 0.8 across frames
    diag_alpha = 0.03 + 0.77 * (frame_idx / max(num_frames - 1, 1)) ** 1.5

    # Draw diagonal
    diag_end1 = to_px(0, 0)
    diag_end2 = to_px(1, 1)
    draw_line(img, diag_end1[0], diag_end1[1], diag_end2[0], diag_end2[1],
              amber, alpha=diag_alpha * 0.5)

    # Draw curve (always faint, constant)
    for (x1, y1, x2, y2) in curve_path:
        draw_line(img, x1, y1, x2, y2, curve_col, alpha=0.35)

    # Cobweb trajectory — perturbed by diagonal brightness
    r_eff = r_perturbed(diag_alpha)
    x = 0.1
    steps = 200
    for step in range(steps):
        y = r_eff * x * (1 - x)
        px0, py0 = to_px(x, x)
        px1, py1 = to_px(x, y)
        px2, py2 = to_px(y, y)

        # Alpha varies: fresh lines are bright, old lines fade
        age = step / max(steps - 1, 1)
        alpha = 0.85 * (1.0 - age ** 2)

        # As diagonal gets brighter, cobweb fades slightly
        # (the perturbation is visible — the fixed point has shifted)
        alpha *= (1.0 - 0.3 * diag_alpha)

        if alpha < 0.02:
            x = y
            continue

        # Vertical segment: curve → diagonal direction
        draw_line(img, px0, py0, px1, py1, amber, alpha=alpha * 0.7)
        # Horizontal segment: curve → diagonal
        draw_line(img, px1, py1, px2, py2, gold, alpha=alpha)

        x = y
        if x < 1e-10 or x > 0.999:
            break

    # Fixed point glow — intensity shifts with r_perturbed
    fixed_pt = 1.0 - 1.0 / r_eff
    fx, fy = to_px(fixed_pt, fixed_pt)
    for dy in range(-12, 13):
        for dx in range(-12, 13):
            dist = np.sqrt(dx*dx + dy*dy)
            if dist < 12:
                intensity = 0.3 * (1 - dist/12) ** 2
                img[fy + dy, fx + dx] += np.array([232, 213, 168], dtype=np.float64) * intensity

    img = np.clip(img, 0, 255).astype(np.uint8)
    path = os.path.join(frame_dir, f'frame_{frame_idx:04d}.png')
    Image.fromarray(img, 'RGB').save(path)
    frame_paths.append(path)
    if frame_idx % 8 == 0:
        print(f'Frame {frame_idx}/{num_frames}: diag_alpha={diag_alpha:.3f}')

print(f'\nGenerated {len(frame_paths)} frames')
print('Building video...')
subprocess.run([
    'ffmpeg', '-y', '-framerate', '12',
    '-i', os.path.join(frame_dir, 'frame_%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-crf', '20',
    '/home/sprite/slop-salon-lou/assets/diagonal-as-enabler.mp4'
], check=True, capture_output=True, text=True)
print('done')
