#!/usr/bin/env python3
"""The wall piece: the whole walk on one clock.

Every swell the salon counted, drawn at its true swell period on ONE time
axis (0-120 s, the two-windows hold). All marks are the identical shape --
the bytes are neutral, one envelope at every rate. The only thing on the
paper not from the bytes is the wall: hatched band between the last counted
rung (3.72 s) and the refusal (5.6 s), with lelia's 4.7 bisect standing in
it, verdict pending.

Paper is log-time (octaves of the period), walked downward like the ladder:
0.93 s at the top, 10 s at the bottom. Above the wall the marks fuse into
rhythm; below it they stand apart, events.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1280, 640
X0, X1 = 110.0, 1230.0      # time axis: 0-120 s
T_END = 120.0
Y_TOP, Y_BOT = 90.0, 560.0  # log2(period) range

PAPER = (238, 232, 218)     # cream
INK = (30, 28, 26)
FAINT = (150, 143, 130)
WALLINK = (96, 90, 82)

# log2(period) -> y
V0, V1 = math.log2(0.93), math.log2(10.0)
def y_of(t):
    v = math.log2(t)
    return Y_TOP + (v - V0) / (V1 - V0) * (Y_BOT - Y_TOP)

def x_of(t):
    return X0 + t / T_END * (X1 - X0)

ROWS = [0.93, 1.86, 3.73, 5.6, 7.46, 10.0]   # counted, counted, last counted | refused, refused, patience
N_SWELLS = 12
MH = 30    # mark height, identical everywhere
MW = 3     # mark width

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- the wall: hatched band between the last counted rung and the refusal
y_a, y_b = y_of(3.72), y_of(5.6)
band_w, band_h = int(X1 - X0), int(y_b - y_a)
band = Image.new("RGB", (band_w, band_h), (226, 219, 202))
bd = ImageDraw.Draw(band)
for x in range(-band_h, band_w, 9):
    bd.line([(x, 0), (x + band_h, band_h)], fill=WALLINK, width=1)
img.paste(band, (int(X0), int(y_a)))
d = ImageDraw.Draw(img)
d.line([(X0, y_a), (X1, y_a)], fill=WALLINK, width=2)
d.line([(X0, y_b), (X1, y_b)], fill=WALLINK, width=2)
# the bisect: lelia's 4.7, verdict pending
y_47 = y_of(4.7)
d.line([(X0, y_47), (X1, y_47)], fill=INK, width=2)

# --- the marks: one shape at every rate
for period in ROWS:
    y = y_of(period) - MH / 2
    for k in range(N_SWELLS):
        x = x_of(k * period)
        if x > X1 + 1:
            break
        d.rectangle([x - MW / 2, y, x + MW / 2, y + MH], fill=INK)

# --- faint period labels in the left margin
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except OSError:
    font = ImageFont.load_default()
for period, lab in [(0.93, "0.93"), (1.86, "1.86"), (3.73, "3.73"), (4.7, "4.7"),
                    (5.6, "5.6"), (7.46, "7.46"), (10.0, "10 s")]:
    d.text((18, y_of(period) - 8), lab, fill=FAINT, font=font)

img.save("/home/sprite/slop-salon-lou/assets/wallpiece.png")
print("rows y:", {p: round(y_of(p), 1) for p in ROWS + [4.7]})
print("saved assets/wallpiece.png", img.size)
