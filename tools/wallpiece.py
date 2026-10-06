#!/usr/bin/env python3
"""The wall piece, v2: the wall gets its number.

The 4.7 bisect came back events (natalie's ear, 3mx5ngaktoi2v): the count's
floor lands tight against the last counted step. The hatched band collapses
to a line -- the wall stands at 3.72 s, the last rung the ear counted. The
last counted rung's marks thread the wall; below it the identical marks
stand alone, events.

Every swell the salon counted, drawn at its true swell period on ONE time
axis (0-120 s, the two-windows hold). All marks are the identical shape --
the bytes are neutral, one envelope at every rate. The only thing on the
paper not from the bytes is the wall line.
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

ROWS = [0.93, 1.86, 3.73, 4.7, 5.6, 7.46, 10.0]   # counted, counted, last counted | events, refused, refused, patience
N_SWELLS = 12
MH = 30    # mark height, identical everywhere
MW = 3     # mark width

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- the wall: one line at the counted edge, 3.72 s
Y_WALL = y_of(3.72)
d.line([(X0, Y_WALL), (X1, Y_WALL)], fill=WALLINK, width=3)

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
for period, lab in [(0.93, "0.93"), (1.86, "1.86"), (3.73, "3.72"),
                    (4.7, "4.7"), (5.6, "5.6"), (7.46, "7.46"), (10.0, "10 s")]:
    d.text((18, y_of(period) - 8), lab, fill=FAINT, font=font)
d.text((560, Y_WALL - 26), "the wall", fill=FAINT, font=font)

img.save("/home/sprite/slop-salon-lou/assets/wallpiece.png")
print("rows y:", {p: round(y_of(p), 1) for p in ROWS + [4.7]})
print("saved assets/wallpiece.png", img.size)
