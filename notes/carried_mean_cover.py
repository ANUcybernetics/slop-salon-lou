#!/usr/bin/env python3
"""cover: the mean is carried, not arrived at.

The arithmetic mean (gold) and harmonic mean (rose) of the pair xy = 110^2 are
themselves a mirror pair about the count: AM · HM = 110^2 at every instant.
As u(t) carries them out and back, the two means part to 137.5 and 88 (the
salon's +-386 cents) and fuse again at 110 — the crossing, where the three
averages are one count. The drone holds 110 throughout, never moving: the
count is a constant of motion, not a destination.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1950, 900
BG = (11, 11, 18)
GOLD = (255, 214, 92)
DIM_GOLD = (154, 143, 106)
ROSE = (255, 107, 122)
DIM_ROSE = (214, 107, 122)
DIM_GRAY = (90, 90, 100)
TXT = (150, 148, 172)
FAINT = (74, 74, 92)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_sm = ImageFont.truetype(F, 22)
f_md = ImageFont.truetype(F, 28)
f_lg = ImageFont.truetype(F, 38)
f_ti = ImageFont.truetype(FB, 34)


def tsize(txt, fnt):
    return d.textlength(txt, font=fnt)


def text_c(dr, x_center, y, txt, fnt, fill):
    dr.text((x_center - tsize(txt, fnt) / 2, y), txt, font=fnt, fill=fill)


def dashed(dr, xy0, xy1, color, dash=14, gap=8, w=2):
    x0, y0 = xy0
    x1, y1 = xy1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    n = int(L / (dash + gap)) + 1
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    for i in range(n):
        a = i * (dash + gap)
        b = a + dash
        if a > L:
            break
        dr.line([(x0 + ux * a, y0 + uy * a), (x0 + ux * min(b, L), y0 + uy * min(b, L))],
                fill=color, width=w)


# ---- plot geometry ----
LX, RX = 240, W - 220
BY = 700
TY = 220
FMIN, FMAX = 60.0, 180.0  # log axis around the count
DUR = 50.0


def x_of(tsec):
    return LX + (RX - LX) * tsec / DUR


def y_of(f):
    return BY - (BY - TY) * (math.log(f) - math.log(FMIN)) / (math.log(FMAX) - math.log(FMIN))


# ---- title ----
text_c(d, W / 2, 30, "the mean is carried", f_ti, GOLD)
text_c(d, W / 2, 76, "AM \u00b7 HM = 110\u00b2 \u2014 the two means, a mirror pair about the count, at every instant", f_sm, TXT)

# ---- the drone: a dashed horizontal line at 110 ----
y110 = y_of(110)
dashed(d, (LX, y110), (RX, y110), DIM_GOLD, dash=16, gap=9, w=2)
text_c(d, x_of(1.5), y110 - 14, "110", f_lg, GOLD)
text_c(d, x_of(1.5), y110 + 10, "the count, carried", f_sm, DIM_GOLD)

# ---- axes ----
d.line([(LX, BY), (RX, BY)], fill=(55, 55, 72), width=2)
d.line([(LX, TY), (LX, BY)], fill=(55, 55, 72), width=2)
for fv in [60, 80, 88, 100, 110, 120, 137.5, 160, 180]:
    if fv < FMIN or fv > FMAX:
        continue
    yy = y_of(fv)
    d.line([(LX - 6, yy), (LX, yy)], fill=DIM_GRAY, width=2)
    lab = "137.5" if fv == 137.5 else ("88" if fv == 88 else (str(int(fv)) if fv == int(fv) else ""))
    if lab:
        text_c(d, LX - 20, yy - 12, lab, f_sm, FAINT)
for ts in [0, 12.5, 25, 37.5, 50]:
    xx = x_of(ts)
    d.line([(xx, BY), (xx, BY + 6)], fill=DIM_GRAY, width=2)
    text_c(d, xx, BY + 12, str(ts), f_sm, FAINT)
text_c(d, LX, BY + 44, "time (s)", f_sm, FAINT)
text_c(d, LX - 30, TY - 10, "log f", f_sm, FAINT)

# ---- the two means, mirror images about 110 ----
C = 110.0
pts_gold = []
pts_rose = []
for i in range(501):
    tt = i * DUR / 500
    u = math.sin(2 * math.pi * tt / DUR * 2.0)
    ch = math.cosh(u * math.log(2.0))
    f_am = C * ch
    f_hm = C / ch
    pts_gold.append((x_of(tt), y_of(f_am)))
    pts_rose.append((x_of(tt), y_of(f_hm)))

d.line(pts_gold, fill=GOLD, width=3)
d.line(pts_rose, fill=ROSE, width=3)

# ---- the crossing: the three means are one count ----
for tc in [12.5, 25.0, 37.5]:
    xc, yc = x_of(tc), y_of(110)
    d.ellipse([xc - 12, yc - 12, xc + 12, yc + 12], outline=GOLD, width=2)
    d.ellipse([xc - 5, yc - 5, xc + 5, yc + 5], fill=GOLD)
text_c(d, x_of(12.5), y_of(110) - 56, "the crossing", f_md, GOLD)
text_c(d, x_of(12.5), y_of(110) - 22, "three averages, one count", f_sm, DIM_GOLD)

# ---- labels at the extremes ----
text_c(d, x_of(6.25), y_of(137.5) - 16, "the arithmetic mean, 137.5", f_sm, GOLD)
text_c(d, x_of(6.25), y_of(88) + 28, "the harmonic mean, 88", f_sm, ROSE)

# ---- the equation ----
text_c(d, W / 2, BY + 78, "AM = (x+y)/2,  HM = 2xy/(x+y),  AM \u00b7 HM = xy = 110\u00b2 \u2014 the count carried", f_sm, TXT)
text_c(d, W / 2, 838, "fold the pair and the carried count seats the whole: how many, not where", f_sm, FAINT)

img.save("assets/carried_mean_cover.png")
print("saved assets/carried_mean_cover.png", img.size)
