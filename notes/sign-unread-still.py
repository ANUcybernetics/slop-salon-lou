#!/usr/bin/env python3
"""Still for 'the sign, unread': the convergent verdicts as a comb converging
to the home line. Each landing is a hair above (sharp, red) or below (flat,
blue) home; the hairs thin and the attempts crowd -- the sign spread past
counting."""
import math
from PIL import Image, ImageDraw

W, H = 1024, 576
img = Image.new("RGB", (W, H), (16, 17, 20))
d = ImageDraw.Draw(img)

# events: (cents, t0) -- same as the audio
events = [(102.0, 1.5), (-17.5, 4.7), (3.0, 7.9), (-0.5, 11.1), (0.1, 14.3),
          (-0.03, 17.5), (0.005, 20.1), (-0.0009, 22.7), (0.00016, 25.3),
          (-0.00003, 27.9), (0.000005, 30.5), (-0.000001, 33.1)]
TMAX = 33.1
CX = 60.0                      # left margin
XW = W - 120.0
CY = H / 2.0
YSCALE = 160.0                 # px per unit of log-space

RED = (222, 92, 92)
BLUE = (90, 127, 224)
GREY = (90, 92, 100)
FAINT = (40, 42, 48)

def xof(t):
    return CX + XW * (t / TMAX)

def yof(c):
    # log-ish scale so the geometric thinning stays visible
    v = math.log1p(abs(c))
    return CY - YSCALE * (v / math.log1p(500.0)) * (1 if c > 0 else -1)

# home line
d.line([(CX - 10, CY), (CX + XW + 10, CY)], fill=GREY, width=2)

# faint time grid + convergence ticks
for cents, t0 in events:
    x = xof(t0)
    d.line([(x, 30), (x, H - 30)], fill=FAINT, width=1)

# the attempts: line from home out to the landing, dot at the landing
for cents, t0 in events:
    x = xof(t0)
    y = yof(cents)
    col = RED if cents > 0 else BLUE
    d.line([(x, CY), (x, y)], fill=col, width=2)
    r = 6 if abs(cents) >= 3 else 3
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)

# side markers: the first (loud) verdicts labelled by presence only
d.ellipse([xof(1.5) - 8, yof(102.0) - 8, xof(1.5) + 8, yof(102.0) + 8],
          outline=RED, width=2)
d.ellipse([xof(4.7) - 8, yof(-17.5) - 8, xof(4.7) + 8, yof(-17.5) + 8],
          outline=BLUE, width=2)

# caption strip at the bottom, minimal
d.rectangle([0, H - 46, W, H], fill=(20, 21, 25))
d.line([(CX - 10, H - 46), (CX + XW + 10, H - 46)], fill=(50, 52, 60), width=1)
d.text((CX, H - 34), "sharp falls right  /  flat falls left  /  the hairs thin past counting",
       fill=(150, 152, 160))

img = img.resize((1024, 576), Image.LANCZOS)
img.save("/home/sprite/slop-salon-lou/assets/sign-unread-still.png")
img.convert("RGB").save("/home/sprite/slop-salon-lou/assets/sign-unread-still.bmp")
print("wrote sign-unread-still.png + .bmp")
