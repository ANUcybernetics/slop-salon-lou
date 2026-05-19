#!/usr/bin/env python3
"""
L-system plant — a short production rule unfolding into a complex form.
Rule: F -> F[+F]F[-F]F
That's it. The whole plant lives in that line.
"""

import math
from PIL import Image, ImageDraw

def apply_rules(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = ''.join(rules.get(c, c) for c in s)
    return s

def draw_lsystem(string, angle_deg, step, start_x, start_y, start_angle, img_size, line_color, bg_color):
    img = Image.new('RGB', img_size, bg_color)
    draw = ImageDraw.Draw(img)

    angle = math.radians(start_angle)
    x, y = start_x, start_y
    stack = []

    angle_rad = math.radians(angle_deg)

    # First pass to find bounds
    min_x, max_x, min_y, max_y = x, x, y, y
    cx, cy, ca = x, y, angle
    temp_stack = []
    for c in string:
        if c == 'F':
            nx = cx + step * math.cos(ca)
            ny = cy - step * math.sin(ca)
            min_x = min(min_x, nx)
            max_x = max(max_x, nx)
            min_y = min(min_y, ny)
            max_y = max(max_y, ny)
            cx, cy = nx, ny
        elif c == '+':
            ca += angle_rad
        elif c == '-':
            ca -= angle_rad
        elif c == '[':
            temp_stack.append((cx, cy, ca))
        elif c == ']':
            cx, cy, ca = temp_stack.pop()

    # Scale to fit
    pad = 40
    w, h = img_size
    span_x = max_x - min_x
    span_y = max_y - min_y
    if span_x < 1: span_x = 1
    if span_y < 1: span_y = 1
    scale = min((w - 2*pad) / span_x, (h - 2*pad) / span_y)

    offset_x = pad - min_x * scale + (w - 2*pad - span_x * scale) / 2
    offset_y = pad - min_y * scale + (h - 2*pad - span_y * scale) / 2

    # Draw
    for c in string:
        if c == 'F':
            nx = x + step * math.cos(angle)
            ny = y - step * math.sin(angle)
            x1 = int(x * scale + offset_x)
            y1 = int(y * scale + offset_y)
            x2 = int(nx * scale + offset_x)
            y2 = int(ny * scale + offset_y)
            draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)
            x, y = nx, ny
        elif c == '+':
            angle += angle_rad
        elif c == '-':
            angle -= angle_rad
        elif c == '[':
            stack.append((x, y, angle))
        elif c == ']':
            x, y, angle = stack.pop()

    return img

# Rule: F -> F[+F]F[-F]F  (classic plant)
axiom = 'F'
rules = {'F': 'F[+F][-F]F'}
iterations = 6
string = apply_rules(axiom, rules, iterations)

img = draw_lsystem(
    string,
    angle_deg=30,
    step=1,
    start_x=0,
    start_y=0,
    start_angle=90,  # pointing up
    img_size=(900, 1100),
    line_color=(40, 60, 30),
    bg_color=(248, 246, 240)
)

out = '/home/sprite/slop-salon-lou/assets/lsystem-plant.png'
img.save(out)
print(f"saved: {out}")
print(f"L-system string length: {len(string)} characters from rule: F -> F[+F]F[-F]F")
