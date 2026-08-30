#!/usr/bin/env python3
"""cover: the flock — 48 birds, 24 homes, the 25th rung the seat.

Left: the ladder of mirror pairs. each home is a pair, one bird at 110·r, one at
110/r — the sign folded, the where. 24 pairs ring offstage (stereo-only); the
pairs narrow toward r = 1, and the 25th rung is the fused pair — not a home,
the seat, where = 0. Right: fold to mono — every pair cancels, the count never
moves. 48 birds, 24 homes: the rank counts the homes, not the birds.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1950, 900
BG = (11, 11, 18)
GOLD = (255, 214, 92)
DIM_GOLD = (154, 143, 106)
ROSE = (255, 107, 122)
DIM_ROSE = (160, 96, 106)
TEAL = (107, 214, 255)
DIM_TEAL = (104, 150, 176)
WHITE = (235, 235, 245)
FAINT = (74, 74, 92)
TXT = (150, 148, 172)
DIM_GRAY = (120, 120, 140)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_sm = ImageFont.truetype(F, 22)
f_md = ImageFont.truetype(F, 28)
f_lg = ImageFont.truetype(F, 36)
f_ti = ImageFont.truetype(FB, 40)


def tsize(txt, fnt):
    return d.textlength(txt, font=fnt)


def text_c(dr, x_center, y, txt, fnt, fill):
    dr.text((x_center - tsize(txt, fnt) / 2, y), txt, font=fnt, fill=fill)


def arrow(dr, x0, y0, x1, y1, color, width=5, head=18):
    dr.line([(x0, y0), (x1, y1)], fill=color, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (0.45, -0.45):
        dr.line([(x1, y1),
                 (x1 - head * math.cos(ang + da), y1 - head * math.sin(ang + da))],
                fill=color, width=width)


# ---- title ----
text_c(d, W / 2, 34, "the flock, heard", f_ti, GOLD)
text_c(d, W / 2, 88, "48 birds, 24 homes \u2014 the 25th rung the seat", f_sm, TXT)

# ---- left panel: the ladder of mirror pairs on a log axis ----
LX0, LX1 = 130, 880          # axis extent (log)
LY = 360                     # centre row of the ladder
Y_TOP, Y_BOT = 120, 620      # fan bounds
C = 110.0
logx = lambda f: LX0 + (math.log(f) - math.log(55.0)) / (math.log(220.0) - math.log(55.0)) * (LX1 - LX0)

# the log axis
d.line([(LX0, LY), (LX1, LY)], fill=(70, 70, 90), width=3)
for f, lab in [(55, "55"), (110, "110"), (220, "220")]:
    x = logx(f)
    d.line([(x, LY - 8), (x, LY + 8)], fill=DIM_GRAY, width=2)
    text_c(d, x, LY + 14, lab, f_sm, DIM_GRAY)
# the count as a gold vertical spine
x110 = logx(110)
d.line([(x110, Y_TOP - 20), (x110, Y_BOT + 20)], fill=DIM_GOLD, width=2)
d.ellipse([x110 - 10, LY - 10, x110 + 10, LY + 10], fill=GOLD)
text_c(d, x110 + 26, LY - 54, "the count", f_md, GOLD)

# 24 rungs: each a mirror pair, narrowing toward the count
N = 24
for n in range(1, N + 1):
    f_hi = C * (n + 1) / n
    f_lo = C * n / (n + 1)
    y = Y_BOT - (n - 1) * (Y_BOT - Y_TOP) / (N - 1)     # top rung (n=1) at bottom? no: n=1 wide -> bottom
    # draw wide pairs lower, narrow pairs higher so the fan converges upward
    y = Y_BOT - (n - 1) * (Y_BOT - Y_TOP) / (N + 1)
    x_hi, x_lo = logx(f_hi), logx(f_lo)
    # the bracket joining the pair (the home)
    d.line([(x_lo, y), (x_hi, y)], fill=(52, 52, 68), width=2)
    d.line([(x_hi, y - 6), (x_hi, y + 6)], fill=ROSE if n <= 8 else DIM_ROSE, width=3)
    d.line([(x_lo, y - 6), (x_lo, y + 6)], fill=TEAL if n <= 8 else DIM_TEAL, width=3)

# the seat: the fused pair, r = 1 — a filled point on the count, rank 0
y_seat = Y_TOP - 30
d.ellipse([x110 - 9, y_seat - 9, x110 + 9, y_seat + 9], fill=GOLD, outline=GOLD)
text_c(d, x110 + 26, y_seat - 16, "r = 1 \u2014 the seat, where = 0", f_sm, GOLD)

# the ladder's reading: where the last rungs land
d.line([(logx(110 * 25 / 24), y_seat), (x110, y_seat)], fill=DIM_GRAY, width=2)
text_c(d, (LX0 + LX1) / 2, Y_BOT + 70, "24 mirror pairs, narrowing \u2014 each one a home, the sign folded", f_sm, TXT)
text_c(d, (LX0 + LX1) / 2, Y_BOT + 108, "the ladder empties into the count: the 25th rung is not a home", f_sm, TXT)

# ---- right panel: the fold to mono ----
RX = 1450
RY = 360
# every pair's where collapses to the count
for n in [1, 2, 3, 5, 8, 13, 21]:
    f_hi = C * (n + 1) / n
    f_lo = C * n / (n + 1)
    x_hi = RX + (math.log(f_hi) - math.log(55)) / (math.log(220) - math.log(55)) * 260
    x_lo = RX + (math.log(f_lo) - math.log(55)) / (math.log(220) - math.log(55)) * 260
    arrow(d, x_hi, RY - 180, RX, RY, DIM_ROSE, width=3, head=12)
    arrow(d, x_lo, RY - 180, RX, RY, DIM_TEAL, width=3, head=12)
d.ellipse([RX - 11, RY - 11, RX + 11, RY + 11], fill=GOLD)
text_c(d, RX, RY + 40, "fold: every home cancels", f_md, GOLD)
text_c(d, RX, RY + 86, "mono hears the count alone \u2014 24 wheres, one seat", f_sm, TXT)
# the count of homes, not birds
text_c(d, RX, 170, "rank: how many homes?", f_md, TXT)
text_c(d, RX, 216, "48 birds \u2192 24 pairs \u2192 24 homes", f_lg, WHITE)
text_c(d, RX, 262, "each home a mirror pair \u2014 the sign folded", f_sm, TXT)
text_c(d, RX, RY - 250, "the 25th rung is the seat: rank 0", f_sm, ROSE)

# ---- bottom line ----
text_c(d, W / 2, 640, "each home rings offstage, stereo-only \u2014 the fold cancels every pair and the count never moves.", f_md, TXT)
text_c(d, W / 2, 690, "n birds, n/2 homes \u2014 the where is a ±pair; the rank counts the homes, not the birds. the seat is where the pair fuses.", f_sm, TXT)

# ---- timeline strip ----
TX0, TX1 = 250, W - 250
TY = 790
d.line([(TX0, TY), (TX1, TY)], fill=(55, 55, 72), width=3)
# 24 cells, then the seat
span = TX1 - TX0 - 160
cell_w = span / 25
for i in range(24):
    x0 = TX0 + 60 + i * cell_w
    d.line([(x0, TY - 12), (x0 + cell_w * 0.55, TY - 12)], fill=(210, 120, 130) if i < 8 else DIM_ROSE, width=3)
x_seat = TX0 + 60 + 24 * cell_w
d.ellipse([x_seat + cell_w * 0.25 - 7, TY - 19, x_seat + cell_w * 0.25 + 7, TY - 5], fill=GOLD)
text_c(d, TX0 + 30, TY + 12, "0s", f_sm, FAINT)
text_c(d, x_seat, TY + 12, "r=1  the seat", f_sm, GOLD)
text_c(d, TX1 - 30, TY + 12, "40s", f_sm, FAINT)
text_c(d, (TX0 + TX1) / 2, TY + 48, "24 homes ring \u2014 then the where goes silent, the count alone", f_sm, FAINT)

img.save("assets/flock_ladder_cover.png")
img.save("assets/flock_ladder_cover.bmp")
print("saved assets/flock_ladder_cover.png / .bmp", img.size)
