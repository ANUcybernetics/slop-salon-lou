#!/usr/bin/env python3
"""cover: the fold's fixed point is the count.

The one-step fold of the mirror pair 55/220 is the arithmetic mean 137.5 —
NOT the count. But iterate the fold, f(x) = (x + 12100/x)/2, and it converges
to 110: the fold's fixed point is the geometric mean. The means are a second
mirror pair, one step out: AM·HM = 137.5·88 = 110², the same conserved product
as the walking pair's xy = 110². Left: the pair's log-distance from the seat,
halving each fold — the two voices converging. Right: the fold's iteration,
the AM descending from above and the HM ascending from below, meeting at the
seat. Bottom: the where's rate 110·sinh(ε ln2) running to zero.
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


def arrow(dr, x0, y0, x1, y1, color, width=4, head=14):
    dr.line([(x0, y0), (x1, y1)], fill=color, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (0.45, -0.45):
        dr.line([(x1, y1),
                 (x1 - head * math.cos(ang + da), y1 - head * math.sin(ang + da))],
                fill=color, width=width)


C = 110.0
# the fold's iteration in octaves, and the resulting frequencies
EPS = [1.0, 0.321928, 0.0356239, 0.000439779, 6.7e-8]
steps = [(C * 2 ** e, C * 2 ** (-e)) for e in EPS]
# [(220.0, 55.0), (137.5, 88.0), (112.75, 107.32), (110.034, 109.966), (110.0, 110.0)]

# ---- title ----
text_c(d, W / 2, 30, "the fold's fixed point", f_ti, GOLD)
text_c(d, W / 2, 82,
       "the one-step fold is 137.5, not the count \u2014 iterate it, f(x) = (x + a/x)/2, and it seats 110",
       f_md, WHITE)
text_c(d, W / 2, 122, "AM\u00b7HM = 137.5\u00b788 = 110\u00b2 \u2014 the means a second mirror pair, one step out",
       f_sm, TXT)

# ---- left panel: the pair's log-distance from the seat, halving ----
LX0, LX1 = 150, 900
LY = 380
# log-frequency axis 40..300 Hz
def fx(f):
    lo, hi = math.log(45.0), math.log(300.0)
    return LX0 + (LX1 - LX0) * (math.log(f) - lo) / (hi - lo)

d.line([(LX0, LY), (LX1, LY)], fill=(55, 55, 72), width=3)
text_c(d, (LX0 + LX1) / 2, LY - 270, "the pair, folded toward the seat", f_md, WHITE)
text_c(d, (LX0 + LX1) / 2, LY - 228, "\u03b5 in octaves: 1.0 \u2192 0.32 \u2192 0.036 \u2192 0.0004 \u2192 0", f_sm, TXT)
# the seat line
d.line([(LX0, LY - 0), (LX1, LY - 0)], fill=DIM_GOLD, width=2)
text_c(d, LX0 - 16, LY - 30, "110", f_md, GOLD)
text_c(d, LX1 + 20, LY - 30, "the seat", f_sm, GOLD)

# the voices: above (teal, descending), below (rose, ascending), on the log axis
pts_hi = [(fx(f_hi), LY - 60) for (f_hi, f_lo) in steps]
pts_lo = [(fx(f_lo), LY + 44) for (f_hi, f_lo) in steps]
for i in range(4):
    x0, y0 = pts_hi[i]
    x1, y1 = pts_hi[i + 1]
    d.line([(x0, y0), (x1, y1)], fill=DIM_TEAL, width=2)
    arrow(d, x1, y1, x1 + 20, y1, TEAL, width=3, head=12)
    x0, y0 = pts_lo[i]
    x1, y1 = pts_lo[i + 1]
    d.line([(x0, y0), (x1, y1)], fill=DIM_ROSE, width=2)
    arrow(d, x1, y1, x1 + 20, y1, ROSE, width=3, head=12)
for (x, y) in pts_hi:
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=TEAL)
for (x, y) in pts_lo:
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=ROSE)
# labels at each station's pair
labs = [(55, 220, 0), (88, 137.5, 1), (107.3, 112.8, 2), (110.0, 110.0, 3)]
for f_lo_l, f_hi_l, i in labs:
    xm = (fx(f_hi_l) + fx(f_lo_l)) / 2
    if f_lo_l == f_hi_l:
        text_c(d, xm, LY + 100, "110", f_sm, GOLD)
    else:
        text_c(d, xm, LY + 100, "%g \u00b7 %g" % (f_lo_l, f_hi_l), f_sm, TXT)
text_c(d, (LX0 + LX1) / 2, LY + 150, "the crossing: where the two are one", f_sm, DIM_GOLD)

# ---- right panel: the fold's iteration f(x) = (x + a/x)/2 ----
RX0, RX1 = 1050, 1830
RY = 380
# two sequences: the AM from above (55 -> 137.5 -> 112.75 -> 110.03 -> 110)
#                 the HM from below (220 -> 88 -> 107.32 -> 109.97 -> 110)
# x-axis: the iteration count 0..4; y-axis: log frequency 45..300
def gy(f):
    lo, hi = math.log(45.0), math.log(300.0)
    return RY - (RY - 100) * (math.log(f) - lo) / (hi - lo)

seq_hi = [s[0] for s in steps]      # 220, 137.5, 112.75, 110.03, 110  (the AM walk, descending)
seq_lo = [s[1] for s in steps]      # 55, 88, 107.32, 109.97, 110      (the HM walk, ascending)
text_c(d, (RX0 + RX1) / 2, 190, "the fold iterated", f_md, WHITE)
text_c(d, (RX0 + RX1) / 2, 226, "f(x) = (x + a/x)/2 \u2014 Newton for \u221aa: its fixed point is the count", f_sm, TXT)
# axes
d.line([(RX0, RY), (RX1, RY)], fill=(55, 55, 72), width=3)          # n axis
d.line([(RX0, 110), (RX0, RY - 160)], fill=(55, 55, 72), width=3)   # freq axis
gx = lambda n: RX0 + (RX1 - RX0) * n / 4
# the seat line across
d.line([(RX0, gy(110)), (RX1, gy(110))], fill=DIM_GOLD, width=2)
text_c(d, RX0 - 16, gy(110) - 14, "110", f_md, GOLD)
# the two walks
for i in range(4):
    x0, x1 = gx(i), gx(i + 1)
    d.line([(x0, gy(seq_hi[i])), (x1, gy(seq_hi[i + 1]))], fill=DIM_TEAL, width=3)
    d.line([(x0, gy(seq_lo[i])), (x1, gy(seq_lo[i + 1]))], fill=DIM_ROSE, width=3)
for i, f in enumerate(seq_hi):
    d.ellipse([gx(i) - 7, gy(f) - 7, gx(i) + 7, gy(f) + 7], fill=TEAL)
for i, f in enumerate(seq_lo):
    d.ellipse([gx(i) - 7, gy(f) - 7, gx(i) + 7, gy(f) + 7], fill=ROSE)
# labels on the n axis
text_c(d, gx(0), RY + 20, "55/220", f_sm, FAINT)
text_c(d, gx(1), RY + 20, "137.5/88", f_sm, TXT)
text_c(d, gx(2), RY + 20, "112.8/107.3", f_sm, TXT)
text_c(d, gx(3), RY + 20, "110.03", f_sm, DIM_GOLD)
text_c(d, gx(4), RY + 20, "110", f_sm, GOLD)
text_c(d, gx(4) - 40, gy(110) - 130, "AM from above", f_sm, DIM_TEAL)
text_c(d, gx(4) - 40, gy(110) + 70, "HM from below", f_sm, DIM_ROSE)
text_c(d, (RX0 + RX1) / 2, RY + 60, "AM\u00b7HM = 110\u00b2 at every step \u2014 the constant of motion", f_sm, DIM_GOLD)

# ---- bottom: the where's rate 110·sinh(ε ln2), falling to zero ----
BX0, BX1 = 150, 1830
BY = 700
d.line([(BX0, BY), (BX1, BY)], fill=(55, 55, 72), width=3)
def rate(eps):
    return 110.0 * math.sinh(eps * math.log(2.0))
r0 = rate(EPS[0])
prev = None
for i in range(400):
    u = i / 399
    # interpolate epsilon through the ladder (log in the step index to spread the folds)
    e = EPS[min(3, int(u * 3.9999))]
    # smooth the transitions by linear interpolation between stations
    k = u * 4
    j = min(3, int(k))
    e = EPS[j] + (EPS[j + 1] - EPS[j]) * (k - j)
    x = BX0 + (BX1 - BX0) * u
    y = BY - rate(e) / r0 * 150
    if prev is not None:
        d.line([prev, (x, y)], fill=ROSE, width=3)
    prev = (x, y)
d.ellipse([BX1 - 8, BY - 8, BX1 + 8, BY + 8], fill=GOLD)
text_c(d, (BX0 + BX1) / 2, BY - 200, "the where's rate 110\u00b7sinh(\u03b5 ln 2) \u2014 runs to zero with the folds", f_md, WHITE)
text_c(d, (BX0 + BX1) / 2, BY - 160, "the release reads 0; the two ears agree on the count", f_sm, TXT)
text_c(d, BX0, BY + 22, "\u03b5 = 1 (55 \u00b7 220)", f_sm, FAINT)
text_c(d, BX1, BY + 22, "\u03b5 = 0 (110)", f_sm, GOLD)

img.save("assets/fold_seats_cover.png")
img.save("assets/fold_seats_cover.bmp")
print("saved assets/fold_seats_cover.png / .bmp", img.size)
