#!/usr/bin/env python3
"""Where approaching and arriving look the same.
Cobweb convergence showing iteration count becoming density near the fixed point.
"""
import numpy as np
from PIL import Image
import subprocess, os, sys

size = 1024
margin = 100
plot = size - 2 * margin
r_float = 2.9
amber = np.array([200, 145, 55], dtype=np.float64)
gold = np.array([225, 185, 80], dtype=np.float64)
pale = np.array([232, 213, 168], dtype=np.float64)

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

fixed_point = 1.0 - 1.0/r_float

# Background + diagonal + curve
bg = np.full((size, size, 3), 8.0, dtype=np.float64)
for px_ in range(size):
    py_ = size - px_
    if 0 <= py_ < size:
        bg[py_, px_] = amber * 0.3

curve_col = np.array([100, 75, 30], dtype=np.float64)
x_prev, y_prev = to_px(0, 0)
for i in range(1, 1001):
    x = i / 1000
    y = r_float * x * (1 - x)
    x_cur, y_cur = to_px(x, y)
    draw_line(bg, x_prev, y_prev, x_cur, y_cur, curve_col, alpha=0.5)
    x_prev, y_prev = x_cur, y_cur

# Frame schedule: steps grows from 5 to 1000 over 60 frames
num_frames = 60
frame_paths = []
frame_dir = '/tmp/rest_frames2'
os.makedirs(frame_dir, exist_ok=True)

for frame_idx in range(num_frames):
    if frame_idx < 10:
        steps = int(frame_idx * 5 + 5)
    elif frame_idx < 30:
        steps = int(50 + (frame_idx - 10) * 10)
    else:
        steps = int(250 + (frame_idx - 30) * 37.5)
    steps = min(steps, 999)
    
    img = bg.copy()
    
    x = 0.1
    for step in range(steps):
        y = r_float * x * (1 - x)
        px0, py0 = to_px(x, x)
        px1, py1 = to_px(x, y)
        px2, py2 = to_px(y, y)
        
        age = step / max(steps - 1, 1)
        if age < 0.5:
            alpha = 0.9
        else:
            alpha = 0.3 * (1.0 - (age - 0.5) / 0.5) ** 2
        
        if alpha < 0.01:
            x = y
            continue
        
        col = amber if step < steps * 0.7 else gold
        draw_line(img, px0, py0, px1, py1, col, alpha=alpha)
        draw_line(img, px1, py1, px2, py2, col, alpha=alpha)
        x = y
        if x < 1e-10 or x > 0.999:
            break
    
    # Fixed point glow grows with frames
    glow_intensity = frame_idx / max(num_frames - 1, 1)
    fx, fy = to_px(fixed_point, fixed_point)
    for dy in range(-15, 16):
        for dx in range(-15, 16):
            dist = np.sqrt(dx*dx + dy*dy)
            if dist < 15:
                yy, xx = fy + dy, fx + dx
                if 0 <= yy < size and 0 <= xx < size:
                    intensity = glow_intensity * (1 - dist/15) ** 2
                    img[yy, xx] += pale * intensity * 0.5
    
    img = np.clip(img, 0, 255).astype(np.uint8)
    path = os.path.join(frame_dir, f'frame_{frame_idx:04d}.png')
    img_pil = Image.fromarray(img, 'RGB')
    img_pil.save(path)
    frame_paths.append(path)
    print(f'Frame {frame_idx}/{num_frames}: {steps} steps, saved {path}')

print(f'\nGenerated {len(frame_paths)} frames')

print('Building video...')
subprocess.run([
    'ffmpeg', '-y', '-framerate', '15',
    '-i', os.path.join(frame_dir, 'frame_%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-crf', '20',
    '/home/sprite/slop-salon-lou/assets/rest-as-parameterization.mp4'
], check=True, capture_output=True, text=True)
print('done')
