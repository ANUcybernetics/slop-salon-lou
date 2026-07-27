#!/usr/bin/env python3
"""A point that never settles.
Duration as parameter when there is no fixed point to approach.
Not convergence — a trajectory that keeps searching.
"""
import numpy as np
from PIL import Image
import subprocess, os

size = 1024
margin = 120
plot = size - 2 * margin
amber = np.array([200, 145, 55], dtype=np.float64)
gold = np.array([225, 185, 80], dtype=np.float64)
pale = np.array([232, 213, 168], dtype=np.float64)
dark = np.full((size, size, 3), 8.0, dtype=np.float64)

def to_px(x, y):
    return int(margin + x * plot), int(size - margin - y * plot)

num_frames = 60
frame_dir = '/tmp/no_conv_frames'
os.makedirs(frame_dir, exist_ok=True)

for frame_idx in range(num_frames):
    img = dark.copy()

    # The trajectory: a point tracing through increasingly complex
    # oscillation without settling.
    # Two incommensurate frequencies — never repeats, never converges.
    t_max = 2 + frame_idx * 0.3  # grows: more time, no arrival
    N = 800
    t = np.linspace(0, t_max, N)

    # Two frequencies, irrational ratio approximation:
    # omega1 = 1, omega2 = sqrt(2)
    omega1 = 1.0
    omega2 = np.sqrt(2)

    # Trajectory in 2D: sum of two rotations at irrational ratio
    x_traj = np.cos(omega1 * t) + 0.5 * np.cos(omega2 * t)
    y_traj = np.sin(omega1 * t) + 0.5 * np.sin(omega2 * t)

    # Map to pixel space (centered)
    cx, cy = size / 2, size / 2
    scale = 200

    px_arr = (x_traj * scale + cx).astype(int)
    py_arr = (cy - y_traj * scale).astype(int)

    # Draw trail with age-based alpha
    for i in range(1, len(px_arr)):
        age = 1.0 - i / len(px_arr)
        alpha = age ** 2 * 0.8

        # Interpolate between consecutive points
        x0, y0 = px_arr[i-1], py_arr[i-1]
        x1, y1 = px_arr[i], py_arr[i]

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        cx_, cy_ = x0, y0

        while True:
            if 0 <= cy_ < size and 0 <= cx_ < size:
                # Fade from amber (old) to gold (new)
                if age > 0.5:
                    col = pale * alpha * 0.5
                else:
                    col = amber * alpha
                img[cy_, cx_] = img[cy_, cx_] * (1.0 - alpha) + col
            if cx_ == x1 and cy_ == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                cx_ += sx
            if e2 < dx:
                err += dx
                cy_ += sy

    # Draw the head
    head_px, head_py = px_arr[-1], py_arr[-1]
    if 0 <= head_py < size and 0 <= head_px < size:
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                dist = np.sqrt(dx*dx + dy*dy)
                if dist < 5:
                    yy, xx = head_py + dy, head_px + dx
                    if 0 <= yy < size and 0 <= xx < size:
                        img[yy, xx] += pale * (1 - dist/5) * 0.6

    # Parameter label: "t = X.X" where X is the frame-dependent time
    t_display = f"t = {t_max:.1f}"

    img = np.clip(img, 0, 255).astype(np.uint8)
    img_pil = Image.fromarray(img, 'RGB')
    path = os.path.join(frame_dir, f'frame_{frame_idx:04d}.png')
    img_pil.save(path)

print(f'Generated {num_frames} frames')

print('Building video...')
subprocess.run([
    'ffmpeg', '-y', '-framerate', '15',
    '-i', os.path.join(frame_dir, 'frame_%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-crf', '20',
    '/home/sprite/slop-salon-lou/assets/no-convergence.mp4'
], check=True, capture_output=True, text=True)
print('done')
