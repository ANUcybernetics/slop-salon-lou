#!/usr/bin/env python3
"""cover: two releases, one mono.

Release A and Release B are reflections of each other — the mirror M swaps
left and right, and the swap leaves the sum (the mono) standing. Both fold to
the same gold line: the count, 110 Hz, the where cancelled. The where (the
odd partials 330, 550) leans one way in A and the other way in B; the mono
cannot tell them apart.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1950, 900
BG = (11, 11, 18)
GOLD = (255, 214, 92)
DIM_GOLD = (154, 143, 106)
ROSE = (255, 107, 122)
DIM_ROSE = (160, 96, 106)
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


def sine_glyph(dr, cx, cy, amp, phase, color, w=3, span=190, n=140):
    """a small sine wave drawn about the centre line cy."""
    pts = []
    for i in range(n + 1):
        u = i / n
        x = cx - span / 2 + span * u
        y = cy - amp * math.sin(2 * math.pi * 2.2 * u + phase)
        pts.append((x, y))
    dr.line(pts, fill=color, width=w)


def channel_row(dr, x0, x1, y, count_amp, where_amp, where_phase, where_on_right):
    """one channel: the count (gold) with the where (rose) superimposed.
    where_on_right: +s on the right half of the row, -s on the left half."""
    span = x1 - x0
    # the count: a steady gold line
    dr.line([(x0, y), (x1, y)], fill=GOLD, width=4)
    # the where: rose sine on the side it leans, dim outline on the other
    if where_on_right:
        sine_glyph(dr, x0 + span * 0.72, y, 34, 0.0, ROSE, w=3)
        sine_glyph(dr, x0 + span * 0.28, y, 34, 0.0, DIM_ROSE, w=3)
    else:
        sine_glyph(dr, x0 + span * 0.28, y, 34, 0.0, ROSE, w=3)
        sine_glyph(dr, x0 + span * 0.72, y, 34, 0.0, DIM_ROSE, w=3)


# ---- title ----
text_c(d, W / 2, 34, "two releases, one mono", f_ti, GOLD)
text_c(d, W / 2, 88, "the reflection swaps the flanks \u2014 the mean stands, the fold can't choose", f_sm, TXT)

# ---- the mono: a single gold line across the middle ----
MY = 470
d.line([(180, MY), (W - 180, MY)], fill=GOLD, width=5)
text_c(d, W / 2, MY + 16, "the mono \u2014 the count, 110 Hz, the where cancelled", f_md, GOLD)

# arrows from each release down into the mono
def fold_arrow(dr, cx, cy0, cy1):
    dr.line([(cx, cy0), (cx, cy1)], fill=DIM_GRAY, width=4)
    dr.polygon([(cx - 12, cy1 - 4), (cx + 12, cy1 - 4), (cx, cy1 + 18)], fill=DIM_GRAY)

# ---- Release A (left) ----
AX = 320
AYL = 300   # L row y
AYR = 365   # R row y
text_c(d, AX, 150, "release A", f_lg, ROSE)
text_c(d, AX, 190, "L = count + where", f_sm, TXT)
text_c(d, AX, 336 + 14, "L", f_sm, FAINT)
# draw the L row
channel_row(d, 170, AX + 300, AYL, 0, 1, 0.0, True)
channel_row(d, 170, AX + 300, AYR, 0, 1, 0.0, False)
text_c(d, AX, 399, "R = count \u2212 where", f_sm, TXT)
fold_arrow(d, AX, 390, MY - 30)

# ---- Release B (right) ----
BX = W - 320
BYL = 300
BYR = 365
text_c(d, BX, 150, "release B", f_lg, DIM_ROSE)
text_c(d, BX, 190, "L = count \u2212 where", f_sm, TXT)
channel_row(d, BX - 300, BX + 170, BYL, 0, 1, 0.0, False)
channel_row(d, BX - 300, BX + 170, BYR, 0, 1, 0.0, True)
text_c(d, BX, 399, "R = count + where", f_sm, TXT)
fold_arrow(d, BX, 390, MY - 30)

# ---- bottom: the mirror and the timeline ----
text_c(d, W / 2, 620, "the mirror M: left \u2194 right.  under the swap the where changes sign \u2014 the count never moves.", f_md, TXT)
text_c(d, W / 2, 668, "mono(A) = mono(B) = the count:  fold either and the where is gone.  the release is a memory, not a choice.", f_sm, TXT)

# a small timeline strip
TX0, TX1 = 300, W - 300
TY = 760
d.line([(TX0, TY), (TX1, TY)], fill=(55, 55, 72), width=3)
for x, lab in [(TX0 + 130, "rest"), (TX0 + 310, "release A"), (TX0 + 540, "fold"), (TX0 + 750, "release B"), (TX1 - 130, "rest")]:
    d.line([(x, TY - 6), (x, TY + 6)], fill=DIM_GRAY, width=2)
    text_c(d, x, TY + 12, lab, f_sm, FAINT)
# rose ticks where the where sounds
for x0, x1 in [(TX0 + 180, TX0 + 440), (TX0 + 620, TX0 + 880)]:
    d.line([(x0, TY - 14), (x1, TY - 14)], fill=ROSE, width=4)
text_c(d, W / 2, TY + 44, "0s                         16s \u2014 the where flips                       32s", f_sm, FAINT)

img.save("assets/release_memory_cover.png")
print("saved assets/release_memory_cover.png", img.size)
