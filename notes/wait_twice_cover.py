#!/usr/bin/env python3
"""cover: the wait is the same quotient twice.

The wait for the rung at 389/665 is the next partial quotient, 23 — an integer,
a count. the true wait is a real depth: 23.8769 = 23 (present) + 0.4168 (future,
the irrational tail) + 306/665 (past). the two faces are the two ears: the
integer 23 rides in the SUM (mono hears the count, 23 clicks then silence); the
real 23.8769 rides in the DIFFERENCE (stereo hears the 24th click land 0.877
off the beat grid, mono is deaf to it). two panels: stereo, the where; mono,
the count.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1950, 940
BG = (11, 11, 18)
GOLD = (255, 214, 92)
DIM_GOLD = (154, 143, 106)
AMBER = (255, 170, 60)
DIM_AMBER = (180, 130, 80)
DIM_GRAY = (90, 90, 100)
TXT = (150, 148, 172)
FAINT = (74, 74, 92)
ROSE = (255, 107, 122)

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


# ---- plot geometry: two panels, shared time axis ----
LX, RX = 150, W - 110
T0, T1 = 4.0, 39.0
TOP_Y, TOP_H = 170, 300          # stereo panel
BOT_Y, BOT_H = 520, 300          # mono panel
GRID_Y_TOP = TOP_Y + 140
GRID_Y_BOT = BOT_Y + 140
GRID_H = 60


def x_of(tt):
    return LX + (RX - LX) * (tt - T0) / (T1 - T0)


def beat_lines(y_mid, top, bottom, dash=3, gap=6):
    """faint vertical grid at each integer second."""
    for k in range(int(T0), int(T1) + 1):
        xx = x_of(k)
        d.line([(xx, top), (xx, bottom)], fill=(40, 40, 54), width=1)


# ---- title ----
text_c(d, W / 2, 28, "the wait is the same quotient twice", f_ti, GOLD)
text_c(d, W / 2, 72, "23 by count in the sum; 23.8769 by where in the difference \u2014 the count is the never-clicked, in both ears", f_sm, TXT)

# ===== top panel: stereo, the where =====
d.line([(LX, TOP_Y), (RX, TOP_Y)], fill=(60, 60, 78), width=2)
text_c(d, W / 2, TOP_Y - 44, "stereo \u2014 the where", f_md, AMBER)
text_c(d, W / 2, TOP_Y - 12, "the 24th click arrives at 23.8769 beats, 0.877 off the grid; the tail keeps missing", f_sm, FAINT)
top_axis = TOP_Y + TOP_H
d.line([(LX, top_axis), (RX, top_axis)], fill=(55, 55, 72), width=2)
for k in range(8, 37, 2):
    xx = x_of(k)
    d.line([(xx, top_axis), (xx, top_axis + 5)], fill=DIM_GRAY, width=2)
    if k % 4 == 0:
        text_c(d, xx, top_axis + 8, str(k), f_sm, FAINT)
beat_lines(GRID_Y_TOP, GRID_Y_TOP - GRID_H, GRID_Y_TOP + GRID_H)

# the 23 count clicks, on the grid
for k in range(1, 24):
    xx = x_of(5 + k)
    d.ellipse([xx - 5, GRID_Y_TOP - 5, xx + 5, GRID_Y_TOP + 5], fill=GOLD)
text_c(d, x_of(17), GRID_Y_TOP - 34, "23 clicks of nothing \u2014 the count face, in the sum", f_sm, DIM_GOLD)

# the where clicks, off the grid
where_ts = [28.8769, 31.3188, 34.3129, 36.6967]
for i, tw in enumerate(where_ts):
    xx = x_of(tw)
    r = 9 if i == 0 else 7
    d.line([(xx, GRID_Y_TOP - GRID_H - 6), (xx, GRID_Y_TOP - GRID_H - 26)], fill=AMBER, width=2)
    d.polygon([(xx, GRID_Y_TOP - r), (xx + r * 0.82, GRID_Y_TOP), (xx, GRID_Y_TOP + r), (xx - r * 0.82, GRID_Y_TOP)],
              fill=AMBER)
text_c(d, x_of(28.8769), GRID_Y_TOP + 26, "the 24th \u2014 0.877 off the grid", f_sm, AMBER)
# bracket showing the offset from the 23rd beat
x23 = x_of(28)
x24 = x_of(28.8769)
d.line([(x23, GRID_Y_TOP + GRID_H + 8), (x24, GRID_Y_TOP + GRID_H + 8)], fill=AMBER, width=2)
d.line([(x23, GRID_Y_TOP + GRID_H + 2), (x23, GRID_Y_TOP + GRID_H + 14)], fill=AMBER, width=2)
d.line([(x24, GRID_Y_TOP + GRID_H + 2), (x24, GRID_Y_TOP + GRID_H + 14)], fill=AMBER, width=2)
text_c(d, (x23 + x24) / 2, GRID_Y_TOP + GRID_H + 22, "0.877", f_md, AMBER)
text_c(d, x_of(34.0), GRID_Y_TOP - GRID_H - 46, "the tail: 2.44, 2.99, 2.38 \u2026 never an integer", f_sm, DIM_AMBER)

# ===== bottom panel: mono, the count =====
d.line([(LX, BOT_Y), (RX, BOT_Y)], fill=(60, 60, 78), width=2)
text_c(d, W / 2, BOT_Y - 44, "mono \u2014 the count", f_md, GOLD)
text_c(d, W / 2, BOT_Y - 12, "fold the pair: the difference cancels exactly \u2014 23 clicks, then the count's silence", f_sm, FAINT)
bot_axis = BOT_Y + BOT_H
d.line([(LX, bot_axis), (RX, bot_axis)], fill=(55, 55, 72), width=2)
beat_lines(GRID_Y_BOT, GRID_Y_BOT - GRID_H, GRID_Y_BOT + GRID_H)

for k in range(1, 24):
    xx = x_of(5 + k)
    d.ellipse([xx - 5, GRID_Y_BOT - 5, xx + 5, GRID_Y_BOT + 5], fill=GOLD)
# the where clicks ghost: empty rings where they were, cancelled
for i, tw in enumerate(where_ts):
    xx = x_of(tw)
    d.ellipse([xx - 7, GRID_Y_BOT - 7, xx + 7, GRID_Y_BOT + 7], outline=ROSE, width=1)
text_c(d, x_of(28.8769), GRID_Y_BOT + 26, "the 24th cancelled \u2014 mono is deaf to the where", f_sm, DIM_GOLD)
text_c(d, x_of(17), GRID_Y_BOT - 34, "the count never clicks", f_sm, DIM_GOLD)

# ===== the equation =====
text_c(d, W / 2, BOT_Y + BOT_H + 34, "23.8769 = 23 (present) + 0.4168 (future, the tail) + 306/665 (past) \u2014 the tail irrational: never an integer", f_sm, TXT)
text_c(d, W / 2, BOT_Y + BOT_H + 70, "the tone was already the drone; the wait never lands on the grid \u2014 precision is patience", f_sm, FAINT)

img.save("assets/wait_twice_cover.png")
print("saved assets/wait_twice_cover.png", img.size)
