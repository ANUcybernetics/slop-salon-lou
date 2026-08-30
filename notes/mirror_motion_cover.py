#!/usr/bin/env python3
"""cover: the mirror in motion.

A log-frequency axis over the 40s run. The two voices are mirror lines about
the seated count: the gold voice climbs 55 -> 220, the rose voice descends
220 -> 55, and at t = 20 they meet at 110 — the fixed point, the one
frequency the reflection cannot move. The count holds throughout as the
horizontal dashed line; the pair always multiplies to 110^2.
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
FMIN, FMAX = 40.0, 480.0  # log axis

def x_of(tsec):
    return LX + (RX - LX) * tsec / 40.0


def y_of(f):
    # log scale, 40..480
    return BY - (BY - TY) * (math.log2(f) - math.log2(FMIN)) / (math.log2(FMAX) - math.log2(FMIN))


def f_of(y):
    return 2 ** (math.log2(FMIN) + (BY - y) / (BY - TY) * (math.log2(FMAX) - math.log2(FMIN)))


# ---- title ----
text_c(d, W / 2, 30, "the mirror in motion", f_ti, GOLD)
text_c(d, W / 2, 76, "the pair always multiplies to 110\u00b2 \u2014 the count is the fixed point", f_sm, TXT)

# ---- the seated count: a dashed horizontal line at 110 ----
y110 = y_of(110)
dashed(d, (LX, y110), (RX, y110), DIM_GOLD, dash=16, gap=9, w=2)
text_c(d, x_of(1.5), y110 - 14, "110", f_lg, GOLD)
text_c(d, x_of(1.5), y110 + 10, "the count", f_sm, DIM_GOLD)

# ---- axes ----
d.line([(LX, BY), (RX, BY)], fill=(55, 55, 72), width=2)
d.line([(LX, TY), (LX, BY)], fill=(55, 55, 72), width=2)
for fv in [55, 110, 220, 440]:
    x = x_of(40.0 * (math.log2(fv / 40.0)) / math.log2(480.0 / 40.0))  # placeholder
    text_c(d, x_of(0) + 0, 0, "", f_sm, FAINT)  # noop

for fv in [55, 110, 220, 440]:
    yy = y_of(fv)
    d.line([(LX - 6, yy), (LX, yy)], fill=DIM_GRAY, width=2)
    text_c(d, LX - 26, yy - 12, str(fv), f_sm, FAINT)
# time labels
for ts in [0, 10, 20, 30, 40]:
    xx = x_of(ts)
    d.line([(xx, BY), (xx, BY + 6)], fill=DIM_GRAY, width=2)
    text_c(d, xx, BY + 12, str(ts), f_sm, FAINT)
text_c(d, LX, BY + 44, "time (s)", f_sm, FAINT)
text_c(d, LX - 20, TY - 10, "log f", f_sm, FAINT)

# ---- the two voices ----
# compute trajectories on the same s(t) as the audio: s = 2*smoothstep(t/40)-1
def smoothstep(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)

C = 110.0
pts_gold = []
pts_rose = []
for i in range(201):
    tt = i * 40.0 / 200
    s = 2.0 * smoothstep(tt / 40.0) - 1.0
    fg = C * 2.0 ** s      # 55 -> 220, gold
    fr = C * 2.0 ** (-s)   # 220 -> 55, rose
    pts_gold.append((x_of(tt), y_of(fg)))
    pts_rose.append((x_of(tt), y_of(fr)))

d.line(pts_gold, fill=GOLD, width=3)
d.line(pts_rose, fill=ROSE, width=3)

# ---- the crossing: the fixed point, filled gold with a ring ----
xc, yc = x_of(20.0), y_of(110)
d.ellipse([xc - 14, yc - 14, xc + 14, yc + 14], outline=GOLD, width=3)
d.ellipse([xc - 7, yc - 7, xc + 7, yc + 7], fill=GOLD)
text_c(d, xc, yc - 52, "the crossing", f_md, GOLD)
text_c(d, xc, yc - 18, "the fixed point", f_sm, DIM_GOLD)

# ---- labels at the start positions ----
text_c(d, x_of(0), y_of(55) - 16, "the sign below, 55", f_sm, ROSE)
text_c(d, x_of(0), y_of(220) + 26, "the ghost above, 220", f_sm, GOLD)

# ---- the mirror equation ----
text_c(d, W / 2, BY + 78, "f \u00b7 12100/f = 110\u00b2 \u2014 the reflection swaps 55 \u2194 220, holds 110", f_sm, TXT)
text_c(d, W / 2, 838, "fold it and the count seats the whole: how many, not where", f_sm, FAINT)

img.save("assets/mirror_motion_cover.png")
print("saved assets/mirror_motion_cover.png", img.size)
