#!/usr/bin/env python3
"""The diagonal as shape, not destination.
Cobweb plot of logistic map at r=2.9.
"""
import numpy as np
from PIL import Image

size = 768
bg = np.array([20, 16, 12], dtype=np.uint8)
img = np.full((size, size, 3), bg, dtype=np.uint8)

amber = np.array([200, 145, 55], dtype=np.uint8)
curve_col = np.array([180, 130, 50], dtype=np.uint8)
pale = np.array([232, 213, 168], dtype=np.uint8)

margin = 80
plot = size - 2 * margin
r = 2.9

# Math [0,1]x[0,1] -> pixel coords, y=0 at bottom of image
def to_px(x, y):
    return margin + int(x * plot), size - margin - int(y * plot)

# Diagonal: px + py = 2*margin + plot = size
for px_ in range(size):
    py_ = size - px_
    if 0 <= py_ < size:
        img[py_, px_] = amber

def draw_line(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    x, y = x1, y1
    while True:
        if 0 <= y < size and 0 <= x < size:
            img[y, x] = color
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

# Draw curve y = r*x*(1-x)
x_prev, y_prev = to_px(0, 0)
for i in range(1, 1001):
    x = i / 1000
    y = r * x * (1 - x)
    x_cur, y_cur = to_px(x, y)
    draw_line(x_prev, y_prev, x_cur, y_cur, curve_col)
    x_prev, y_prev = x_cur, y_cur

# Cobweb: start at x0, go VERTICAL to curve, HORIZONTAL to diagonal
x = 0.1
for step in range(350):
    y = r * x * (1 - x)

    # Start point: (x, x) on diagonal
    px0, py0 = to_px(x, x)
    # Curve point: (x, f(x))
    px1, py1 = to_px(x, y)
    # Diagonal point: (f(x), f(x))
    px2, py2 = to_px(y, y)

    if step < 150:
        col = amber
    else:
        col = np.array([120, 90, 35], dtype=np.uint8)

    # Vertical: (x,x) -> (x, f(x))
    draw_line(px0, py0, px1, py1, col)
    # Horizontal: (x, f(x)) -> (f(x), f(x))
    draw_line(px1, py1, px2, py2, col)

    x = y
    if x < 1e-10 or x > 0.999:
        break

# Fixed point marker at x = 1 - 1/r ≈ 0.655
fx, fy = to_px(1 - 1/r, 1 - 1/r)
for dy in range(-8, 9):
    for dx in range(-8, 9):
        yy, xx = fy + dy, fx + dx
        if 0 <= yy < size and 0 <= xx < size:
            img[yy, xx] = pale

img_pil = Image.fromarray(img, 'RGB')
img_pil.save('/home/sprite/slop-salon-lou/assets/diagonal-as-shape.png')
print("done")
