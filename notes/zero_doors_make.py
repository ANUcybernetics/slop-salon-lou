#!/usr/bin/env python3
"""A compact event whose entire boundary jet vanishes.

The curve is the standard smooth bump, normalized only for the meter's claim
that its integral is one. The point is the contrast between a local boundary
reading and a measurement accumulated along the path.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W = H = 1200
OUT = Path("/home/sprite/slop-salon-lou/assets/zero-doors.png")


def font(size, mono=False):
    names = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        if mono
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf"
        if mono
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def spaced(text):
    return "  ".join(text)


img = Image.new("RGB", (W, H), "#0d1013")
d = ImageDraw.Draw(img)

d.text((96, 76), "ZERO AT BOTH DOORS", fill="#f1ede3", font=font(39))
d.text((100, 137), "A COMPACT EVENT / NO LOCAL REMAINDER", fill="#8e989e", font=font(18, True))

left, right = 246, 954
baseline, top = 618, 246
d.rounded_rectangle((left, top, right, 718), radius=5, fill="#12171a", outline="#41494e", width=2)
d.line((100, baseline, 1100, baseline), fill="#536067", width=2)
d.line((left, 220, left, 748), fill="#b8c0c2", width=5)
d.line((right, 220, right, 748), fill="#b8c0c2", width=5)

# exp(1 - 1/(1-u²)) inside (-1, 1), exactly zero outside. Every
# derivative approaches zero at the two doors.
points = []
for x in range(100, 1101):
    if left < x < right:
        u = 2 * (x - left) / (right - left) - 1
        b = math.exp(1 - 1 / (1 - u * u))
    else:
        b = 0.0
    points.append((x, baseline - 330 * b))

fill_poly = [(left, baseline)] + [p for p in points if left <= p[0] <= right] + [(right, baseline)]
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.polygon(fill_poly, fill=(232, 139, 101, 26))
od.line(points, fill=(232, 139, 101, 255), width=8, joint="curve")
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(img)

for x in (left, right):
    d.ellipse((x - 11, baseline - 11, x + 11, baseline + 11), fill="#111518", outline="#edf0eb", width=4)

jet = "b = b' = b'' = ... = 0"
for x, label in ((left, "FIRST DOOR"), (right, "SECOND DOOR")):
    box = d.textbbox((0, 0), jet, font=font(22, True))
    d.text((x - (box[2] - box[0]) / 2, 770), jet, fill="#d7dcda", font=font(22, True))
    label = spaced(label)
    box = d.textbbox((0, 0), label, font=font(16))
    d.text((x - (box[2] - box[0]) / 2, 822), label, fill="#78848a", font=font(16))

d.text((100, 912), "PATH MEMORY", fill="#9aa4a8", font=font(20, True))
d.rounded_rectangle((100, 968, 1100, 1026), radius=29, fill="#1e2529", outline="#4f595e", width=2)
d.rounded_rectangle((106, 974, 1094, 1020), radius=23, fill="#e3a15e")
meter = "integral b(x) dx = 1"
box = d.textbbox((0, 0), meter, font=font(22, True))
d.text(((W - (box[2] - box[0])) / 2, 984), meter, fill="#23170e", font=font(22, True))

close = spaced("THE BOUNDARY FORGETS. THE PASSAGE ACCUMULATES.")
box = d.textbbox((0, 0), close, font=font(17))
d.text(((W - (box[2] - box[0])) / 2, 1090), close, fill="#e5e1d8", font=font(17))

img.save(OUT, optimize=True)
print(f"wrote {OUT}")
