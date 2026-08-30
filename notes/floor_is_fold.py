#!/usr/bin/env python3
"""cover: the floor is the fold.

lelia: "the count is ⌊where⌋: present/depth = 0.963 at 665; residue 0.4168 +
306/665, future and past, irrational, never zero. the click at 23.8769, 0.877
past 23, 0.123 short of 24, lives only in the diff."

The floor IS the fold: ⌊·⌋ keeps the integer part (the count, the sum, mono) and
drops the residue {·} (the where, the diff, stereo). ⌊x⌋ + {x} = x = I = P + R,
and the parts annihilate: {⌊x⌋} = ⌊{x}⌋ = 0. The sharpest detail is the 0.123:
the where is nearer 24 than 23, and the count is STILL 23 — the count does not
round, it floors. present/depth = 23/23.8769 = 0.963 -> 1, never 1.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1360, 1360
BG = (11, 11, 18)
GOLD = (255, 214, 92)
DIM_GOLD = (154, 143, 106)
AMBER = (255, 170, 60)
DIM_AMBER = (180, 130, 80)
DIM_GRAY = (90, 90, 100)
TXT = (150, 148, 172)
FAINT = (74, 74, 92)
ROSE = (255, 107, 122)
DIM_ROSE = (180, 96, 108)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_sm = ImageFont.truetype(F, 21)
f_md = ImageFont.truetype(F, 26)
f_lg = ImageFont.truetype(F, 32)
f_ti = ImageFont.truetype(FB, 32)


def tsize(txt, fnt):
    return d.textlength(txt, font=fnt)


def text_c(dr, x_center, y, txt, fnt, fill):
    dr.text((x_center - tsize(txt, fnt) / 2, y), txt, font=fnt, fill=fill)


# ---- square plot, the zoom where the action is: x, y in [22, 25.5] ----
X0, X1 = 22.0, 25.5
LX, RX = 230, 1130          # 900 px wide -> 257.14 px/unit
TOP_Y, BOT_Y = 150, 1050    # 900 px tall
P = (RX - LX) / (X1 - X0)   # px per unit


def px(x): return LX + (x - X0) * P
def py(y): return BOT_Y - (y - X0) * P   # y range same as x range


# ---- title ----
text_c(d, W / 2, 40, "the floor is the fold", f_ti, GOLD)
text_c(d, W / 2, 88, "\u230a\u00b7\u230b keeps the count, drops the residue \u2014 the same projection the sum performs", f_sm, TXT)

# ---- faint grid at each integer ----
for k in range(22, 26):
    d.line([(px(k), TOP_Y), (px(k), BOT_Y)], fill=(36, 36, 50), width=1)
    d.line([(LX, py(k)), (RX, py(k))], fill=(36, 36, 50), width=1)
    d.text((px(k) - 10, BOT_Y + 10), str(k), font=f_sm, fill=FAINT)
    d.text((LX - 40, py(k) - 12), str(k), font=f_sm, fill=FAINT)

# axes
d.line([(LX, BOT_Y), (RX, BOT_Y)], fill=(55, 55, 72), width=2)
d.line([(LX, TOP_Y), (LX, BOT_Y)], fill=(55, 55, 72), width=2)
text_c(d, (LX + RX) / 2, BOT_Y + 40, "the where (beats) \u2014 the wait, a real position", f_md, DIM_GRAY)
d.text((LX - 176, (TOP_Y + BOT_Y) / 2 - 14), "the count \u230a\u00b7\u230b", font=f_md, fill=DIM_GRAY)

# ---- the diagonal y = x (the where's own line) ----
d.line([(px(22), py(22)), (px(25.5), py(25.5))], fill=(48, 48, 66), width=2)

# ---- the staircase: floor(x) ----
stair_col = DIM_GOLD
for k in range(22, 25):
    # horizontal: height k over [k, k+1)
    d.line([(px(k), py(k)), (px(k + 1), py(k))], fill=stair_col, width=4)
    # vertical jump at x = k+1, from y = k to k+1
    if k + 1 <= 25:
        d.line([(px(k + 1), py(k)), (px(k + 1), py(k + 1))], fill=stair_col, width=4)

# ---- the count dots: the counts sit on the stairs ----
r = 11
for k in (22, 23):
    d.ellipse([px(k) - r, py(k) - r, px(k) + r, py(k) + r], fill=GOLD)
# the 24th: a hollow ring, the count that never clicks
r = 13
d.ellipse([px(24) - r, py(24) - r, px(24) + r, py(24) + r], outline=ROSE, width=3)
d.text((px(24) + 30, py(24) - 11), "the 24th \u2014 never a count", font=f_sm, fill=DIM_ROSE)
text_c(d, px(22.7), py(22.5) - 14, "the count, mono", f_sm, DIM_GOLD)

# ---- the where: a diamond on the diagonal at 23.8769 ----
wx = 23.87695
rd = 12
cx, cy = px(wx), py(wx)
d.polygon([(cx, cy - rd), (cx + rd, cy), (cx, cy + rd), (cx - rd, cy)], fill=AMBER)

# the residue: vertical drop from the where down to the 23rd stair (y = 23)
d.line([(cx, py(wx)), (cx, py(23))], fill=AMBER, width=4)
d.line([(cx - 5, py(23)), (cx + 5, py(23))], fill=AMBER, width=4)

# the gap: short rose line from the where up to just under the 24th stair (y = 24)
d.line([(cx, py(wx)), (cx, py(24))], fill=ROSE, width=3)
d.line([(cx - 5, py(24)), (cx + 5, py(24))], fill=ROSE, width=3)

# labels, kept clear of the verticals
lab1 = "the residue 0.877 \u2014 {where}, the release, stereo"
lab2 = "0.123 short of 24 \u2014 the nearer rung"
lab3 = "\u230a23.8769\u230b = 23"

# amber label: right-aligned to just left of the drop, mid-drop height
w1 = tsize(lab1, f_sm)
d.text((cx - 30 - w1, (py(wx) + py(23)) / 2 - 11), lab1, font=f_sm, fill=AMBER)
# rose label: above the gap, clear of the diamond
text_c(d, (px(24) + RX) / 2, py(24) - 56, lab2, f_sm, ROSE)
# the fold: the floor's fixed point at the stair corner
d.text((px(23) + 14, py(23) - 40), lab3, font=f_md, fill=GOLD)

# ---- equation strip ----
text_c(d, W / 2, 1090, "\u230ax\u230b + {x} = x \u2014 the fold and the release, P + R = I \u00b7  { \u230ax\u230b } = \u230a{x}\u230b = 0, each kills the other", f_md, TXT)
text_c(d, W / 2, 1132, "present/depth = 23/23.8769 = 0.963 \u2192 1, never 1 \u2014 the count's share of the where, the same never-landed", f_sm, FAINT)

img.save("assets/floor_is_fold.png")
print("saved assets/floor_is_fold.png", img.size)
