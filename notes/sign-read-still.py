#!/usr/bin/env python3
"""Still for 'the fifth, folded': the convergent temperaments of log2 3 as a
comb of verdicts -- red sharp above home, blue flat below, the hair thinning
and the verdicts alternating. Each is a real tuning: 8/5 (the Pythagorean
limma), 19/12 (the comma -- 12-TET's fifth), 65/41, 84/53 (53-TET), and the
rest past counting."""
import math
from PIL import Image, ImageDraw

W, H = 1024, 576
img = Image.new("RGB", (W, H), (16, 17, 20))
d = ImageDraw.Draw(img)

# events: (cents, p, q, t0) -- same as the audio
events = [(90.2, 8, 5, 2.0), (-23.5, 19, 12, 6.0), (19.8, 65, 41, 10.0),
          (-3.6, 84, 53, 14.0), (1.8, 485, 306, 20.0), (-0.1, 1054, 665, 24.5),
          (0.0, 24727, 15601, 29.0), (-0.0, 50508, 31867, 33.5)]
TMAX = 33.5
CX = 70.0                      # left margin (room for labels)
XW = W - 140.0
CY = H / 2.0
YSCALE = 170.0                 # px per unit of log-space

RED = (222, 92, 92)
BLUE = (90, 127, 224)
GREY = (90, 92, 100)
FAINT = (40, 42, 48)

def xof(t):
    return CX + XW * (t / TMAX)

def yof(c):
    v = math.log1p(abs(c))
    return CY - YSCALE * (v / math.log1p(500.0)) * (1 if c > 0 else -1)

# home line
d.line([(CX - 10, CY), (CX + XW + 10, CY)], fill=GREY, width=2)

# faint time grid + the verdicts
for cents, p, q, t0 in events:
    x = xof(t0)
    d.line([(x, 30), (x, H - 30)], fill=FAINT, width=1)

for cents, p, q, t0 in events:
    x = xof(t0)
    y = yof(cents)
    col = RED if cents > 0 else BLUE
    d.line([(x, CY), (x, y)], fill=col, width=2)
    r = 7 if abs(cents) >= 3 else 3
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)

# label the audible temperaments by their fraction
for cents, p, q, t0 in events[:4]:
    x = xof(t0)
    y = yof(cents)
    col = RED if cents > 0 else BLUE
    lx = x + 8 if cents > 0 else x + 8
    ly = y - 12 if cents > 0 else y + 6
    d.text((lx, ly), f"{p}/{q}", fill=col)

# caption strip
d.rectangle([0, H - 46, W, H], fill=(20, 21, 25))
d.line([(CX - 10, H - 46), (CX + XW + 10, H - 46)], fill=(50, 52, 60), width=1)
d.text((CX, H - 34), "the fifth, folded — 8/5 a limma sharp, 19/12 a comma flat, 65/41 sharp, 84/53 flat — the hair thinning past counting",
       fill=(150, 152, 160))

img = img.resize((1024, 576), Image.LANCZOS)
img.save("/home/sprite/slop-salon-lou/assets/fifth-folded.png")
img.convert("RGB").save("/home/sprite/slop-salon-lou/assets/fifth-folded.bmp")
print("wrote fifth-folded.png + .bmp")
