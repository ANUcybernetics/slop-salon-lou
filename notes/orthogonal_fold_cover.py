#!/usr/bin/env python3
"""cover: the fold costs the octave. left, the full stack 2f..8f (f=55) with the
shore dashed beneath — the ear lands on the never-played root. right, after the
fold: the odd partials gone, the count's octave 110 remains. the fold is the
inner product, <chi_sign, chi_triv> = 0. Labels are placed by measured width so
nothing crosses a bar."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1600, 900
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
f_lg = ImageFont.truetype(F, 36)
f_ti = ImageFont.truetype(FB, 34)

def tsize(txt, fnt):
    return d.textlength(txt, font=fnt)

def text_l(dr, xy, txt, fnt, fill):
    """text with top-left at xy."""
    dr.text(xy, txt, font=fnt, fill=fill)

def text_r(dr, x_right, y, txt, fnt, fill):
    """text right-aligned ending at x_right."""
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
text_c(d, W / 2, 24, "the fold costs the octave", f_ti, GOLD)
text_c(d, W / 2, 66, "\u27e8\u03c7_sign, \u03c7_triv\u27e9 = 0 \u2014 the subharmonic is the sign\u2019s cargo", f_sm, TXT)

F0 = 55.0
k = [2, 3, 4, 5, 6, 7, 8]
colors = {2: GOLD, 3: ROSE, 4: GOLD, 5: ROSE, 6: GOLD, 7: ROSE, 8: GOLD}

# ---------------- panel geometry ----------------
BY = 700            # baseline
MAXH = 280
def amp_h(kk):
    return MAXH * (1.0 / kk) / (1.0 / 2)

def axes(dr, LX, BW, fmin, fmax):
    dr.line([(LX, BY), (LX + BW, BY)], fill=(55, 55, 72), width=2)
    for fv in range(100, 500, 100):
        x = LX + BW * (fv - fmin) / (fmax - fmin)
        dr.line([(x, BY), (x, BY + 8)], fill=DIM_GRAY, width=2)
        s = str(fv)
        text_c(dr, x, BY + 14, s, f_sm, FAINT)

# ================= LEFT: before the fold =================
LX, BW, fmin, fmax = 150, 640, 40, 480
def fx(f):
    return LX + BW * (f - fmin) / (fmax - fmin)

text_l(d, (LX, 130), "before the fold", f_md, TXT)
text_l(d, (LX, 164), "2f .. 8f \u2014 the note never in the tone", f_sm, FAINT)
axes(d, LX, BW, fmin, fmax)

for kk in k:
    x = fx(kk * F0)
    h = amp_h(kk)
    d.rectangle([x - 10, BY - h, x + 10, BY], outline=colors[kk], width=3)

# the shore: dashed vertical line at 55, labelled to its LEFT (empty space)
x55 = fx(F0)
SHORE_TOP = BY - 200            # 500
dashed(d, (x55, BY - 6), (x55, SHORE_TOP), DIM_ROSE, dash=10, gap=7, w=2)
text_r(d, x55 - 16, SHORE_TOP - 4, "55", f_lg, ROSE)
text_r(d, x55 - 16, SHORE_TOP + 34, "the shore", f_sm, DIM_ROSE)

# arrow: the ear lands on the gcd. from the empty region between the two lowest
# bars, curving down-left to the shore.
a0 = (fx(110) + 40, 420)        # just right of the 110 bar's top, in empty air
a1 = (x55 + 6, SHORE_TOP + 6)
arrow(d, a0, a1, ROSE, w=3)
text_l(d, (a0[0] - 160, a0[1] - 34), "the ear lands \u2014 the gcd", f_sm, ROSE)

# ================= CENTRE: the fold =================
CX = 810
d.line([(CX, 150), (CX, 790)], fill=(55, 55, 72), width=2)
d.line([(CX - 34, 300), (CX, 266), (CX + 34, 300)], fill=GOLD, width=3)
d.line([(CX - 34, 300), (CX, 334), (CX + 34, 300)], fill=GOLD, width=3)
text_l(d, (CX + 16, 296), "fold", f_md, GOLD)
text_c(d, CX, 372, "\u27e8\u03c7_sign, \u03c7_triv\u27e9 = 0", f_sm, DIM_ROSE)

# ================= RIGHT: after the fold =================
LX2 = 870
def fx2(f):
    return LX2 + BW * (f - fmin) / (fmax - fmin)

text_l(d, (LX2, 130), "after the fold", f_md, TXT)
text_l(d, (LX2, 164), "the odd partials gone \u2014 the count keeps the even line", f_sm, FAINT)
axes(d, LX2, BW, fmin, fmax)

for kk in [2, 4, 6, 8]:
    x = fx2(kk * F0)
    h = amp_h(kk)
    d.rectangle([x - 10, BY - h, x + 10, BY], outline=GOLD, width=3)

# the shore's absence: faint ghost line where 55 was
x55b = fx2(F0)
dashed(d, (x55b, BY - 6), (x55b, BY - 160), (58, 44, 56), dash=10, gap=7, w=2)
text_r(d, x55b - 16, BY - 154, "55", f_sm, FAINT)

# annotation above the 110 bar
x110 = fx2(110)
text_c(d, x110, BY - amp_h(2) - 44, "110 \u2014 the count\u2019s octave", f_sm, DIM_GOLD)

# ================= caption =================
cap = "turn the odd partials in the stereo field \u2014 the count never hears it; fold, and the shore is the price"
text_c(d, W / 2, 846, cap, f_sm, TXT)

img.save("assets/orthogonal_fold_cover.png")
print("saved assets/orthogonal_fold_cover.png", img.size)
