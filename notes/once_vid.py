#!/usr/bin/env python3
"""Animated cover for 'once': the seed's grid, log-frequency field.

  - the seed 55 line collects its 40 ticks, the first (t=4s) the crown —
    gold, the grid's one record; the far-side returns fainter.
  - the count 110 line collects its 5 ticks, small, on the far side.
  - the seam 165 line receives exactly ONE tick (t=65.4s) — a single bright
    flash, the odd sector's one landing, in a cooler tone.
  - at t=14s the bar flashes — a vertical line that closes the window:
    everything above the seed is locked out of the record book.
  - a cursor sweeps left to right. 165 s @ 10 fps = 1650 frames.
"""
import json
import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 576
FPS = 10
DUR = 165.0
NF = int(DUR * FPS)

with open("/tmp/grid_strikes.json") as f:
    D = json.load(f)
mult = {int(k): v for k, v in D["mult55"].items()}
N_RUNGS = D["N"]
BAR = 231


def rung_time(r):
    if r <= 15:
        return 4.0 * r / 15
    if r <= 47:
        return 4.0 + 4.0 * (r - 15) / (47 - 15)
    if r <= BAR:
        return 8.0 + 6.0 * (r - 47) / (BAR - 47)
    return 14.0 + (r - BAR) * (151.0 / (N_RUNGS - BAR))


seed_times = [rung_time(r) for r in mult[55]]
count_times = [rung_time(r) for r in mult[110]]
seam_times = [rung_time(r) for r in mult[165]]
bar_time = rung_time(BAR)

# ---- geometry ----
LM, RM, TM, BM = 70, 40, 50, 60


def x_of(t):
    return LM + (W - LM - RM) * t / DUR


def y_of(f):
    lo, hi = 45.0, 920.0
    return TM + (H - TM - BM) * (1 - (np.log(f) - np.log(lo)) / (np.log(hi) - np.log(lo)))


BG = (9, 12, 18)
GRID = (36, 46, 62)
SEED = (214, 96, 88)          # warm — the root
SEED_TICK = (238, 214, 170)
COUNT = (198, 164, 106)       # gold — the count line
SEAM = (122, 170, 210)        # cool — the odd sector
SEAM_TICK = (170, 210, 250)
BAR = (150, 150, 190)

# static background
bg = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(bg)
for f, c, w in [(55, SEED, 2), (110, COUNT, 3), (165, SEAM, 2),
                (220, GRID, 1), (440, GRID, 1), (880, GRID, 1)]:
    y = y_of(f)
    d.line([(LM, y), (W - RM, y)], fill=c, width=w)
for f in [55, 110, 165, 220, 440, 880]:
    y = y_of(f)
    d.line([(LM - 8, y), (LM, y)], fill=(70, 80, 100), width=1)
    d.text((LM - 44, y - 7), str(f), fill=(90, 100, 120))
# faint vertical "bar" guide at t=14s
bx = x_of(bar_time)
d.line([(bx, TM), (bx, H - BM)], fill=(150, 150, 190, 90), width=1)
bg = bg.convert("RGBA")
pre = np.array(bg)

for i in range(NF):
    cur = float(i) / FPS
    frame = pre.copy()
    d = ImageDraw.Draw(Image.fromarray(frame, "RGBA"))
    cx = x_of(cur)
    # cursor
    d.line([(cx, TM - 8), (cx, H - BM)], fill=(70, 80, 100), width=1)
    # seed ticks (crown = big gold)
    for j, tm in enumerate(seed_times):
        if tm <= cur:
            x = x_of(tm); y = y_of(55)
            if j == 0:
                r = 9 + 2 * (1 - min(1.0, (cur - tm) / 2.0))
                glow = int(70 * max(0, 1 - (cur - tm) / 3.0))
                d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=(214, 96, 88, glow))
                d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 226, 160, 255))
            else:
                r = 5 + 2 * (1 - min(1.0, (cur - tm) / 2.0))
                glow = int(30 * max(0, 1 - (cur - tm) / 3.0))
                if glow > 0:
                    d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=(214, 96, 88, glow))
                d.ellipse([x - r, y - r, x + r, y + r], fill=(238, 214, 170, 200))
    # count ticks: small gold, far side
    for tm in count_times:
        if tm <= cur:
            x = x_of(tm); y = y_of(110)
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(198, 164, 106, 200))
    # seam: ONE tick, bright cool flash
    for tm in seam_times:
        if tm <= cur:
            x = x_of(tm); y = y_of(165)
            glow = int(110 * max(0, 1 - (cur - tm) / 2.5))
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(122, 170, 210, glow))
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(190, 224, 255, 255))
    # the bar flash: at t=14 the window closes
    if 0 <= (cur - bar_time) < 2.5:
        a = int(140 * (1 - (cur - bar_time) / 2.5))
        bx = x_of(bar_time)
        d.line([(bx, TM), (bx, H - BM)], fill=(150, 150, 190, a), width=3)
    out = Image.fromarray(frame, "RGBA").convert("RGB")
    out.save(f"/home/sprite/slop-salon-lou/assets/once_frames/f_{i:04d}.png")

print("wrote", NF, "frames")
