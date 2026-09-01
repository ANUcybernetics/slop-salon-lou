#!/usr/bin/env python3
"""Animated cover for the root's metronome: a log-frequency field with
horizontal lines at the octaves; the count 110 is a clean bright line that
never receives a mark; the seed 55 line collects sixteen irregular ticks;
the one-time great records flash faintly once each high above.
A cursor sweeps left to right. 150 s @ 10 fps = 1500 frames.
"""
import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 576
FPS = 10
DUR = 150.0
NF = int(DUR * FPS)

# ---- the event data (mirrors the audio script) ----
seed_times = [0.0, 2.0, 11.5, 22.2, 34.5, 47.8, 52.7, 70.4, 74.0, 92.7,
              98.0, 101.2, 102.6, 106.8, 117.6, 143.4]
records = [(2.85, 107), (2.91, 227), (3.40, 309), (4.38, 342), (15.4, 390),
           (23.1, 463), (93.2, 666), (107.6, 897)]

# ---- geometry ----
LM, RM, TM, BM = 70, 40, 50, 60
def x_of(t): return LM + (W - LM - RM) * t / DUR
def y_of(f):
    lo, hi = 45.0, 920.0
    return TM + (H - TM - BM) * (1 - (np.log(f) - np.log(lo)) / (np.log(hi) - np.log(lo)))

BG = (9, 12, 18)
GRID = (36, 46, 62)
COUNT = (198, 164, 106)      # the count line: gold, clean, never marked
SEED = (214, 96, 88)         # the seed: warm
TICK = (238, 214, 170)
REC = (130, 150, 190)

# static background with grid + lines
bg = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(bg)
for f, c, w in [(55, SEED, 2), (110, COUNT, 3), (220, GRID, 1), (440, GRID, 1), (880, GRID, 1)]:
    y = y_of(f)
    d.line([(LM, y), (W - RM, y)], fill=c, width=w)
# faint octave labels as tiny ticks on the left margin
for f in [55, 110, 220, 440, 880]:
    y = y_of(f)
    d.line([(LM - 8, y), (LM, y)], fill=(70, 80, 100), width=1)
bg = bg.convert("RGBA")

pre = np.array(bg)

for i in range(NF):
    cur = float(i) / FPS
    frame = pre.copy()
    d = ImageDraw.Draw(Image.fromarray(frame, "RGBA"))
    cx = x_of(cur)
    # cursor
    d.line([(cx, TM - 8), (cx, H - BM)], fill=(70, 80, 100), width=1)
    # seed ticks already struck
    for tm in seed_times:
        if tm <= cur:
            x = x_of(tm); y = y_of(55)
            r = 5 + 2 * (1 - min(1.0, (cur - tm) / 2.0))  # recent ticks glow bigger
            glow = int(40 * max(0, 1 - (cur - tm) / 3.0))
            if glow > 0:
                d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=(214, 96, 88, glow))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(238, 214, 170, 230))
    # record pings, faint once
    for tm, f in records:
        if tm <= cur:
            x = x_of(tm); y = y_of(f)
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(130, 150, 190, 120))
    out = Image.fromarray(frame, "RGBA").convert("RGB")
    out.save(f"/home/sprite/slop-salon-lou/assets/seed_frames/f_{i:04d}.png")

print("wrote", NF, "frames")
