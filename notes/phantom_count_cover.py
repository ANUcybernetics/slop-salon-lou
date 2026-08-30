#!/usr/bin/env python3
"""cover: the phantom count. three hearings, one shared frequency axis — the
count at 110 is a vertical gold line that never moves. left, the count present
(110 solid). centre, the count deleted (110 hollow) yet the ear still lands on
it — the gcd of {220,330,440}. right, the fold to mono (330 gone) and only the
ghost's octave 220:440 stands, the count still beneath as the missing
fundamental. you cannot subtract the fixed point."""
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
HOLLOW = (58, 52, 66)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_sm = ImageFont.truetype(F, 22)
f_md = ImageFont.truetype(F, 28)
f_lg = ImageFont.truetype(F, 36)
f_ti = ImageFont.truetype(FB, 34)

def tsize(txt, fnt):
    return d.textlength(txt, font=fnt)

def text_l(dr, xy, txt, fnt, fill):
    dr.text(xy, txt, font=fnt, fill=fill)

def text_r(dr, x_right, y, txt, fnt, fill):
    dr.text((x_right - tsize(txt, fnt), y), txt, font=fnt, fill=fill)

def text_c(dr, x_center, y, txt, fnt, fill):
    dr.text((x_center - tsize(txt, fnt) / 2, y), txt, font=fnt, fill=fill)

def dashed(dr, xy0, xy1, color, dash=12, gap=8, w=2):
    x0, y0 = xy0; x1, y1 = xy1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0: return
    n = int(L / (dash + gap)) + 1
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    for i in range(n):
        a = i * (dash + gap); b = a + dash
        if a > L: break
        dr.line([(x0 + ux * a, y0 + uy * a), (x0 + ux * min(b, L), y0 + uy * min(b, L))], fill=color, width=w)

def arrow(dr, xy0, xy1, color, w=3):
    x0, y0 = xy0; x1, y1 = xy1
    dr.line([xy0, xy1], fill=color, width=w)
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    px, py = -uy, ux
    hs = 12
    tip = (x1, y1)
    h1 = (tip[0] - ux * hs + px * hs * 0.5, tip[1] - uy * hs + py * hs * 0.5)
    h2 = (tip[0] - ux * hs - px * hs * 0.5, tip[1] - uy * hs - py * hs * 0.5)
    dr.polygon([tip, h1, h2], fill=color)

# ---------------- title ----------------
text_c(d, W / 2, 24, "the phantom count", f_ti, GOLD)
text_c(d, W / 2, 66, "you cannot subtract the fixed point", f_sm, TXT)

# shared frequency axis 40..480, three panels at same scale
FMIN, FMAX = 40.0, 480.0
BY = 720            # baseline
MAXH = 250
def amp_h(f):
    # 1/k amplitudes, tallest at 110 (=1.0)
    k = f / 110.0
    return MAXH * (1.0 / k) if k >= 1 else MAXH

def stem(dr, x, f, solid):
    h = amp_h(f)
    if solid:
        d.rectangle([x - 10, BY - h, x + 10, BY], outline=GOLD, width=3)
    else:
        # hollow: outline box only
        d.rectangle([x - 10, BY - h, x + 10, BY], outline=HOLLOW, width=2)

def axes(dr, LX, BW):
    dr.line([(LX, BY), (LX + BW, BY)], fill=(55, 55, 72), width=2)
    for fv in range(100, 500, 100):
        x = LX + BW * (fv - FMIN) / (FMAX - FMIN)
        dr.line([(x, BY), (x, BY + 8)], fill=DIM_GRAY, width=2)
        text_c(dr, x, BY + 14, str(fv), f_sm, FAINT)

panels = [
    (140, "the count, present", "110 is in the stack"),
    (780, "the count, deleted", "the ear keeps the gcd"),
    (1420, "the fold, the octave", "the count beneath"),
]
PW = 500
fx = lambda LX, f: LX + PW * (f - FMIN) / (FMAX - FMIN)

for LX, title, sub in panels:
    axes(d, LX, PW)
    text_l(d, (LX, 130), title, f_md, TXT)
    text_l(d, (LX, 164), sub, f_sm, FAINT)

# panel 1: 110, 220, 330, 440 solid
for f in [110, 220, 330, 440]:
    stem(d, fx(140, f), f, True)
# panel 2: 220, 330, 440 solid, 110 hollow (deleted)
for f in [220, 330, 440]:
    stem(d, fx(780, f), f, True)
stem(d, fx(780, 110), 110, False)
# panel 3: 220, 440 solid, 330 hollow (folded away)
for f in [220, 440]:
    stem(d, fx(1420, f), f, True)
stem(d, fx(1420, 330), 330, False)

# ---- the fixed point: a gold vertical line at 110 through all three panels ----
y_top = 200
for LX in [140, 780, 1420]:
    x110 = fx(LX, 110)
    dashed(d, (x110, y_top), (x110, BY - 6), GOLD, dash=10, gap=7, w=2)

# label the 110 line across the top, once
x110 = fx(140, 110)
text_c(d, x110, y_top - 34, "110", f_lg, GOLD)
text_c(d, x110, y_top + 2, "the count", f_sm, DIM_GOLD)

# annotations
text_c(d, fx(140, 110), BY - amp_h(110) - 40, "heard", f_sm, GOLD)
text_c(d, fx(780, 110), BY - amp_h(110) - 40, "rebuilt", f_sm, GOLD)
text_c(d, fx(1420, 110), BY - amp_h(110) - 40, "missing fundamental", f_sm, GOLD)

# arrows between panels
arrow(d, (140 + PW + 12, 430), (780 - 12, 430), DIM_GRAY, w=3)
text_c(d, (140 + PW + 780) / 2, 408, "delete the count", f_sm, TXT)
arrow(d, (780 + PW + 12, 430), (1420 - 12, 430), DIM_GRAY, w=3)
text_c(d, (780 + PW + 1420) / 2, 408, "fold to mono", f_sm, TXT)

# ================= caption =================
cap = "delete the count and the ear keeps it; fold what\u2019s left and the odd partial dies \u2014 110 never moves"
text_c(d, W / 2, 846, cap, f_sm, TXT)

img.save("assets/phantom_count_cover.png")
print("saved assets/phantom_count_cover.png", img.size)
