#!/usr/bin/env python3
"""cover: the kernel is a plane, not a line.

Left: the where as a plane — two independent axes, 330 and 550, and the
diagonal that is both at once. Three releases, three directions, all offstage.
Right: fold to mono — every release collapses to the one gold point, the
count. The plane has a dimension; the count can't see it. n voices, n-1 homes.
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


def arrow(dr, x0, y0, x1, y1, color, width=5, head=20):
    dr.line([(x0, y0), (x1, y1)], fill=color, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (0.45, -0.45):
        dr.line([(x1, y1),
                 (x1 - head * math.cos(ang + da), y1 - head * math.sin(ang + da))],
                fill=color, width=width)


# ---- title ----
text_c(d, W / 2, 34, "the kernel is a plane", f_ti, GOLD)
text_c(d, W / 2, 88, "two releases, one count \u2014 how many, not where", f_sm, TXT)

# ---- left panel: the where, a plane ----
LX, LY = 500, 480          # the count sits at the origin of the plane
AX = 250                   # axis half-length
# faint axis lines
d.line([(LX - AX, LY), (LX + AX, LY)], fill=(52, 52, 68), width=2)
d.line([(LX, LY - AX), (LX, LY + AX)], fill=(52, 52, 68), width=2)
# grid dots at the cardinal points
for gx, gy, lab in [(LX + AX, LY, "330"), (LX, LY - AX, "550")]:
    d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=FAINT)
    text_c(d, gx, gy + 12, lab, f_sm, FAINT)
text_c(d, LX, LY + 34, "the count, 110", f_md, GOLD)
d.ellipse([LX - 9, LY - 9, LX + 9, LY + 9], fill=GOLD)

# the three release directions
arrow(d, LX, LY, LX + 160, LY, ROSE, width=6)                    # A: 330
arrow(d, LX, LY, LX, LY - 160, TEAL, width=6)                    # B: 550
arrow(d, LX, LY, LX + 108, LY - 108, WHITE, width=6)             # AB: both
text_c(d, LX + 160, LY - 14, "A", f_lg, ROSE)
text_c(d, LX - 16, LY - 160 - 26, "B", f_lg, TEAL)
text_c(d, LX + 118, LY - 128, "AB", f_lg, WHITE)
text_c(d, LX, LY - 250, "the where \u2014 three directions, one plane", f_md, TXT)

# ---- right panel: the fold to mono ----
RX, RY = 1450, 480
# converging faint trails from the three directions down to the count
arrow(d, RX - 150, RY, RX, RY, DIM_ROSE, width=4, head=14)
arrow(d, RX + 150, RY, RX, RY, DIM_TEAL, width=4, head=14)
arrow(d, RX, RY - 150, RX, RY, (170, 170, 180), width=4, head=14)
d.ellipse([RX - 9, RY - 9, RX + 9, RY + 9], fill=GOLD)
text_c(d, RX, RY + 34, "the mono \u2014 the count alone", f_md, GOLD)
text_c(d, RX, RY - 250, "fold: every release lands here", f_md, TXT)

# ---- bottom line ----
text_c(d, W / 2, 640, "release A along one axis, release B along the other, AB the diagonal \u2014 mono hears the same count through each and through all.", f_md, TXT)
text_c(d, W / 2, 690, "one release is a line. two releases, a plane. the where has a rank: n voices, n\u22121 homes.", f_sm, TXT)

# a small timeline strip
TX0, TX1 = 330, W - 330
TY = 790
d.line([(TX0, TY), (TX1, TY)], fill=(55, 55, 72), width=3)
for x, lab in [(TX0 + 110, "rest"), (TX0 + 300, "A"), (TX0 + 500, "B"), (TX0 + 700, "AB"), (TX1 - 110, "rest")]:
    d.line([(x, TY - 6), (x, TY + 6)], fill=DIM_GRAY, width=2)
    text_c(d, x, TY + 12, lab, f_sm, FAINT)
for x0, x1, col in [(TX0 + 210, TX0 + 400, ROSE), (TX0 + 410, TX0 + 600, TEAL), (TX0 + 610, TX0 + 800, WHITE)]:
    d.line([(x0, TY - 14), (x1, TY - 14)], fill=col, width=4)
text_c(d, W / 2, TY + 44, "0s           A: 330          B: 550          AB: both            20s", f_sm, FAINT)

img.save("assets/kernel_rank_cover.png")
img.save("assets/kernel_rank_cover.bmp")
print("saved assets/kernel_rank_cover.png / .bmp", img.size)
