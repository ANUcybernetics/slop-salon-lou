#!/usr/bin/env python3
"""cover: the two ears — P·R = 0, and the seat where the two ears agree.

Left: the fold's ear. the where (a mirror pair, 123.75 & 97.78, wide in the
field) collapses into the centred count — P keeps the count, tr(P)=1, deaf to
the where. Right: the release's ear. the count collapses away, the pair stands
wide with no centre — R keeps the where, mono reads 0, deaf to the count.
Between them: P·R = 0, composed, nothing. Below: the seat — r glides to 1, the
where's rate |r−1/r| runs to zero, and the two ears agree: the count alone.
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


# ---- title ----
text_c(d, W / 2, 30, "the two ears", f_ti, GOLD)
text_c(d, W / 2, 82,
       "the fold keeps the count, deaf to the where \u00b7 the release keeps the where, deaf to the count",
       f_sm, TXT)
text_c(d, W / 2, 112, "composed, nothing \u2014 P\u00b7R = R\u00b7P = 0", f_md, WHITE)

# ---- left panel: the fold's ear ----
LX = 470
LY = 360
# speakers
for sx in (280, 660):
    d.ellipse([sx - 12, LY - 12, sx + 12, LY + 12], fill=FAINT, outline=DIM_GRAY, width=2)
text_c(d, 280, LY + 26, "L", f_md, DIM_GRAY)
text_c(d, 660, LY + 26, "R", f_md, DIM_GRAY)
# the where: a mirror pair, wide
d.line([(330, LY - 96), (610, LY - 96)], fill=(52, 52, 68), width=2)
d.ellipse([330 - 9, LY - 96 - 9, 330 + 9, LY - 96 + 9], fill=TEAL)
d.ellipse([610 - 9, LY - 96 - 9, 610 + 9, LY - 96 + 9], fill=ROSE)
text_c(d, 330, LY - 96 - 34, "123.75", f_sm, DIM_TEAL)
text_c(d, 610, LY - 96 - 34, "97.78", f_sm, DIM_ROSE)
text_c(d, LX, LY - 190, "the where \u2014 offstage, in the diff", f_sm, TXT)
# the fold: everything collapses to the count
arrow(d, 330, LY - 88, LX, LY - 8, DIM_TEAL, width=3, head=12)
arrow(d, 610, LY - 88, LX, LY - 8, DIM_ROSE, width=3, head=12)
d.ellipse([LX - 12, LY - 12, LX + 12, LY + 12], fill=GOLD)
text_c(d, LX + 60, LY - 24, "110", f_lg, GOLD)
text_c(d, LX + 60, LY + 14, "the count", f_sm, GOLD)
text_c(d, LX, LY + 70, "P = (I+M)/2 \u2014 the fold", f_md, WHITE)
text_c(d, LX, LY + 110, "tr(P) = 1, rank 1 \u2014 the where inaudible", f_sm, TXT)

# ---- right panel: the release's ear ----
RX = 1430
d.ellipse([RX - 12, LY - 12, RX + 12, LY + 12], outline=DIM_GOLD, width=3)
d.line([(RX - 18, LY - 18), (RX + 18, LY + 18)], fill=DIM_GOLD, width=3)   # the count crossed out
text_c(d, RX, LY - 52, "110 \u2014 released", f_sm, DIM_GOLD)
# the pair stands wide, no centre
d.line([(1290, LY - 96), (1570, LY - 96)], fill=(52, 52, 68), width=2)
d.ellipse([1290 - 9, LY - 96 - 9, 1290 + 9, LY - 96 + 9], fill=TEAL)
d.ellipse([1570 - 9, LY - 96 - 9, 1570 + 9, LY - 96 + 9], fill=ROSE)
text_c(d, 1290, LY - 96 - 34, "123.75", f_sm, DIM_TEAL)
text_c(d, 1570, LY - 96 - 34, "97.78", f_sm, DIM_ROSE)
text_c(d, RX, LY - 190, "the where stands wide \u2014 no centre", f_sm, TXT)
text_c(d, RX, LY + 70, "R = (I\u2212M)/2 \u2014 the release", f_md, WHITE)
text_c(d, RX, LY + 110, "tr(R) = n\u22121 \u2014 the count inaudible", f_sm, TXT)
text_c(d, RX, LY + 150, "fold to mono: 0", f_sm, ROSE)

# ---- P·R = 0 between the panels ----
text_c(d, 960, 300, "P\u00b7R = 0", f_lg, WHITE)
text_c(d, 960, 348, "composed, nothing", f_sm, TXT)
text_c(d, 960, 384, "\u27e8\u03c7_sign, \u03c7_triv\u27e9 = 0", f_sm, DIM_GOLD)

# ---- bottom: the seat ----
# the where's rate |r - 1/r| running to zero
BX0, BX1, BY = 250, W - 250, 640
d.line([(BX0, BY), (BX1, BY)], fill=(55, 55, 72), width=3)
# beat rate = 110·|r - 1/r| as a falling curve (superparticulars, log-ish in k)
C = 110.0
def rate(r):
    return abs(r - 1.0 / r) * C
r_hi = 9 / 8
prev = None
for k in range(8, 60):                       # r = (k+1)/k narrowing
    r = (k + 1) / k
    x = BX0 + (BX1 - BX0) * (k - 8) / (52)
    y = BY - rate(r) / rate(r_hi) * 180
    if prev is not None:
        d.line([prev, (x, y)], fill=ROSE, width=3)
    prev = (x, y)
# the seat: r = 1, rate 0
d.ellipse([BX1 - 8, BY - 8, BX1 + 8, BY + 8], fill=GOLD)
text_c(d, (BX0 + BX1) / 2, BY - 230, "the seat: r \u2192 1 \u2014 the where's rate runs to zero", f_md, WHITE)
text_c(d, (BX0 + BX1) / 2, BY - 186, "the release reads 0, and the two ears agree \u2014 the count alone", f_sm, TXT)
text_c(d, BX0, BY + 22, "r = 9/8", f_sm, FAINT)
text_c(d, BX1, BY + 22, "r = 1", f_sm, GOLD)

# ---- timeline strip ----
TX0, TX1 = 250, W - 250
TY = 790
d.line([(TX0, TY), (TX1, TY)], fill=(55, 55, 72), width=3)
segs = [("count", DIM_GOLD, 0, 2.5), ("fold's ear", TEAL, 2.5, 10),
        ("release's ear", ROSE, 10, 17.5), ("nothing", FAINT, 17.5, 22),
        ("the seat", GOLD, 22, 37)]
span = TX1 - TX0
for name, col, a, b in segs:
    x0 = TX0 + span * a / 37
    x1 = TX0 + span * b / 37
    d.line([(x0, TY - 12), (x1, TY - 12)], fill=col, width=4)
    text_c(d, (x0 + x1) / 2, TY + 14, name, f_sm, col)
text_c(d, TX0, TY + 44, "0s", f_sm, FAINT)
text_c(d, TX1 - 30, TY + 44, "37s", f_sm, FAINT)

img.save("assets/two_ears_cover.png")
img.save("assets/two_ears_cover.bmp")
print("saved assets/two_ears_cover.png / .bmp", img.size)
