#!/usr/bin/env python3
"""the two -1s: S3 character table, transposed entries; the turn's trace = the value at the seat."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1600, 920
BG = (11, 11, 18)
DIM_GOLD = (154, 143, 106)
GOLD = (255, 214, 92)
DIM_ROSE = (214, 107, 122)
ROSE = (255, 107, 122)
DIM_TEAL = (111, 181, 168)
DIM_GRAY = (90, 90, 100)
TXT = (150, 148, 172)
FAINT = (74, 74, 92)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_sm = ImageFont.truetype(F, 20)
f_md = ImageFont.truetype(F, 26)
f_lg = ImageFont.truetype(F, 40)
f_xl = ImageFont.truetype(FB, 30)
f_ti = ImageFont.truetype(FB, 26)

def dashed(dr, xy0, xy1, color, dash=10, gap=7, w=2):
    x0, y0 = xy0; x1, y1 = xy1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0: return
    n = int(L / (dash + gap)) + 1
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    for i in range(n):
        a = i * (dash + gap); b = a + dash
        if a > L: break
        dr.line([(x0 + ux * a, y0 + uy * a), (x0 + ux * min(b, L), y0 + uy * min(b, L))], fill=color, width=w)

def arrow_arc(dr, cx, cy, r, a0, a1, color, w=3, head=True):
    # arc from angle a0 to a1 (degrees), with arrowhead at end
    steps = 48
    pts = []
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    dr.line(pts, fill=color, width=w)
    if head:
        a_end = math.radians(a1)
        tip = (cx + r * math.cos(a_end), cy - r * math.sin(a_end))
        a_prev = math.radians(a1 - (a1 - a0) / steps)
        back = (cx + r * math.cos(a_prev), cy - r * math.sin(a_prev))
        # direction
        dx, dy = tip[0] - back[0], tip[1] - back[1]
        L = math.hypot(dx, dy); dx, dy = dx / L, dy / L
        px, py = -dy, dx
        hs = 11
        h1 = (tip[0] - dx * hs + px * hs * 0.55, tip[1] - dy * hs + py * hs * 0.55)
        h2 = (tip[0] - dx * hs - px * hs * 0.55, tip[1] - dy * hs - py * hs * 0.55)
        dr.polygon([tip, h1, h2], fill=color)

# ---------------- title ----------------
t = "the two \u22121s"
tw = d.textlength(t, font=f_ti)
d.text(((W - tw) / 2, 26), t, font=f_ti, fill=GOLD)
sub = "[S\u2083,S\u2083] = A\u2083 \u2014 the regulator is the commutator"
sw = d.textlength(sub, font=f_sm)
d.text(((W - sw) / 2, 62), sub, font=f_sm, fill=TXT)

# ---------------- left: character table ----------------
LX, LY = 250, 210          # grid origin
CS, GS = 122, 12           # cell size, gap
cols = ["e", "mirror  M", "regulator  T"]
rows = ["trivial", "sign", "standard"]
vals = [[1, 1, 1], [1, -1, 1], [2, 0, -1]]

d.text((LX - 20, LY - 66), "S\u2083 \u2014 character table", font=f_md, fill=TXT)
for j, c in enumerate(cols):
    cw = d.textlength(c, font=f_sm)
    d.text((LX + j * (CS + GS) + (CS - cw) / 2, LY - 40), c, font=f_sm, fill=FAINT)
for i, r in enumerate(rows):
    yc = LY + i * (CS + GS) + CS / 2
    cw = d.textlength(r, font=f_sm)
    d.text((LX - 24 - cw, yc - 11), r, font=f_sm, fill=TXT)

# centers of the two -1 cells
neg1 = {}
for i in range(3):
    for j in range(3):
        x0 = LX + j * (CS + GS); y0 = LY + i * (CS + GS)
        v = vals[i][j]
        if v == 1:   col = DIM_GOLD
        elif v == 2: col = DIM_TEAL
        elif v == 0: col = DIM_GRAY
        else:        col = None
        # highlight the two -1s
        if (i, j) == (1, 1):   # sign, M
            col = GOLD
        if (i, j) == (2, 2):   # std, T
            col = ROSE
        if col is None: continue
        d.rectangle([x0, y0, x0 + CS, y0 + CS], outline=(60, 60, 78), width=2)
        if v == -1:
            # glow
            d.rectangle([x0 + 6, y0 + 6, x0 + CS - 6, y0 + CS - 6], outline=col, width=3)
        s = str(v)
        cw = d.textlength(s, font=f_lg)
        d.text((x0 + (CS - cw) / 2, y0 + (CS - f_lg.size) / 2 - 4), s, font=f_lg, fill=col)
        if v == -1:
            neg1[(i, j)] = (x0 + CS / 2, y0 + CS / 2)

# dashed diagonal through the two -1s
if (1, 1) in neg1 and (2, 2) in neg1:
    dashed(d, neg1[(1, 1)], neg1[(2, 2)], GOLD, dash=12, gap=9, w=2)

# mono bracket (rows 0-1) and stereo (row 2)
mx = LX - 40
y_top = LY + GS * 0.5
y_bot = LY + 2 * (CS + GS) - GS * 0.5
ymid = (y_top + y_bot) / 2
d.line([(mx, y_top), (mx, y_bot)], fill=DIM_GOLD, width=2)
d.line([(mx - 10, y_top), (mx, y_top)], fill=DIM_GOLD, width=2)
d.line([(mx - 10, y_bot), (mx, y_bot)], fill=DIM_GOLD, width=2)
d.text((mx - 200, ymid - 12), "mono \u2014 the two 1-dim rows", font=f_sm, fill=DIM_GOLD)

sx = LX + 3 * (CS + GS) + 40
syy = LY + 2 * (CS + GS) + CS / 2
d.line([(sx, syy - 40), (sx, syy + 40)], fill=DIM_ROSE, width=2)
d.line([(sx, syy - 40), (sx + 10, syy - 40)], fill=DIM_ROSE, width=2)
d.line([(sx, syy + 40), (sx + 10, syy + 40)], fill=DIM_ROSE, width=2)
d.text((sx + 16, syy - 12), "stereo \u2014 the standard row", font=f_sm, fill=DIM_ROSE)

cap1 = "the two \u22121s are transposed entries \u2014 each other's reflection"
cw1 = d.textlength(cap1, font=f_sm)
d.text(((W / 2 - 400) + (400 - cw1) / 2, 860), cap1, font=f_sm, fill=TXT)

# ---------------- right: the turn ----------------
RX, RY = 820, 140
R = 225
cx, cy = RX + 340, RY + 300
d.text((RX, RY - 20), "the turn \u2014 trace and value at the seat", font=f_md, fill=TXT)

# unit circle
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(55, 55, 72), width=2)

# triangle vertices: 1, omega, omega^2
verts = []
for k in range(3):
    a = math.radians(k * 120)   # 0, 120, 240
    verts.append((cx + R * math.cos(a), cy - R * math.sin(a)))
for i in range(3):
    d.line([verts[i], verts[(i + 1) % 3]], fill=(60, 60, 78), width=2)
vcol = [GOLD, ROSE, DIM_TEAL]
for k, (vx, vy) in enumerate(verts):
    d.ellipse([vx - 7, vy - 7, vx + 7, vy + 7], fill=vcol[k], outline=None)

# real axis
dashed(d, (cx - R - 40, cy), (cx + R + 40, cy), DIM_GOLD, dash=14, gap=8, w=2)
d.text((cx - R - 160, cy - 28), "M: mirror \u2014 traceless", font=f_sm, fill=DIM_GOLD)

# fixed points e^{+-i pi/3} at angle +-60: (cx + R/2, cy -+ R*sqrt3/2)
hp = math.sqrt(3) / 2 * R
fp1 = (cx + R / 2, cy - hp)   # e^{i pi/3}
fp2 = (cx + R / 2, cy + hp)   # e^{-i pi/3}
for fp, fc in [(fp1, ROSE), (fp2, ROSE)]:
    d.polygon([(fp[0], fp[1] - 8), (fp[0] + 8, fp[1]), (fp[0], fp[1] + 8), (fp[0] - 8, fp[1])], fill=fc)

# seat 1/2 at midpoint of fixed points
seat = (cx + R / 2, cy)
d.polygon([(seat[0], seat[1] - 11), (seat[0] + 11, seat[1]), (seat[0], seat[1] + 11), (seat[0] - 11, seat[1])], outline=GOLD, width=3)
# vertical line Re=1/2 through fixed points and seat
dashed(d, fp1, fp2, FAINT, dash=8, gap=6, w=2)
d.text((seat[0] + 18, seat[1] - 40), "\u00bd", font=f_lg, fill=GOLD)

# T rotation arrows along circle, radius slightly outside
for k in range(3):
    a0, a1 = k * 120, (k + 1) * 120
    arrow_arc(d, cx, cy, R + 26, a0, a1, ROSE, w=3)
d.text((cx - 120, cy - 150), "T: 120\u00b0 turn", font=f_sm, fill=ROSE)

cap2 = "2cos(2\u03c0/3) = \u22121 = T(\u00bd): the fixed points pin Re = \u00bd,"
cw2 = d.textlength(cap2, font=f_sm)
d.text(((W / 2 + 400) + (400 - cw2) / 2 - 140, 820), cap2, font=f_sm, fill=TXT)
cap2b = "at their midpoint the turn's trace reads the seat's value"
cw2b = d.textlength(cap2b, font=f_sm)
d.text(((W / 2 + 400) + (400 - cw2b) / 2 - 140, 850), cap2b, font=f_sm, fill=TXT)

img.save("assets/s3_two_minus1s.png")
print("saved assets/s3_two_minus1s.png", img.size)
