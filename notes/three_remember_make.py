from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1800, 1200
BG = (12, 14, 18)
PANEL = (18, 21, 27)
MUTED = (113, 120, 130)
TEXT = (229, 226, 216)
COLORS = [(238, 91, 91), (92, 211, 202), (239, 190, 79)]

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)

def font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()

F_TITLE = font(54)
F_SMALL = font(25)
F_TINY = font(20)

def center_text(x, y, s, f, fill):
    box = d.textbbox((0, 0), s, font=f)
    d.text((x - (box[2] - box[0]) / 2, y), s, font=f, fill=fill)

def panel(x0, x1, title):
    d.rounded_rectangle((x0, 150, x1, 1035), radius=26, fill=PANEL,
                        outline=(40, 45, 55), width=2)
    center_text((x0 + x1) / 2, 188, title, F_SMALL, MUTED)

panel(105, 835, "THE EMPTY WORD")
panel(965, 1695, "THE WORD THAT CANCELS")

top, bottom = 300, 900
left_xs = [300, 470, 640]
for i, x in enumerate(left_xs):
    d.line((x, top, x, bottom), fill=COLORS[i], width=18)
    d.ellipse((x-11, top-11, x+11, top+11), fill=COLORS[i])
    d.ellipse((x-11, bottom-11, x+11, bottom+11), fill=COLORS[i])

# Braid word beta = (sigma_1 sigma_2^-1)^3. Each tuple is
# (adjacent position, sign); positive means the left strand passes over.
word = [(0, 1), (1, -1)] * 3
xs = [1160, 1330, 1500]
ys = [top + k * (bottom-top)/len(word) for k in range(len(word)+1)]
order = [0, 1, 2]
paths = {i: [] for i in range(3)}
overlays = []

for step, (slot, sign) in enumerate(word):
    y0, y1 = ys[step], ys[step+1]
    before = order[:]
    after = order[:]
    after[slot], after[slot+1] = after[slot+1], after[slot]
    n = 60
    for j in range(n+1):
        u = j/n
        ease = (1-math.cos(math.pi*u))/2
        y = y0 + (y1-y0)*u
        for label in range(3):
            p0 = before.index(label)
            p1 = after.index(label)
            x = xs[p0] + (xs[p1]-xs[p0])*ease
            paths[label].append((x, y))
    left_label, right_label = before[slot], before[slot+1]
    over_label = left_label if sign > 0 else right_label
    overlays.append((step, before, after, over_label))
    order = after

for label in range(3):
    d.line(paths[label], fill=COLORS[label], width=18, joint="curve")

# Restore the over-pass locally with a dark halo that cuts the under-pass.
for step, before, after, over_label in overlays:
    y0, y1 = ys[step], ys[step+1]
    pts = []
    for j in range(18, 43):
        u = j/60
        ease = (1-math.cos(math.pi*u))/2
        p0 = before.index(over_label)
        p1 = after.index(over_label)
        pts.append((xs[p0] + (xs[p1]-xs[p0])*ease, y0+(y1-y0)*u))
    d.line(pts, fill=PANEL, width=36, joint="curve")
    d.line(pts, fill=COLORS[over_label], width=18, joint="curve")

for i, x in enumerate(xs):
    d.ellipse((x-11, top-11, x+11, top+11), fill=COLORS[i])
    d.ellipse((x-11, bottom-11, x+11, bottom+11), fill=COLORS[i])

center_text(470, 950, "ends = identity", F_TINY, MUTED)
center_text(1330, 950, "ends = identity   ·   sign = +   ·   pairs = 0", F_TINY, MUTED)

center_text(W/2, 55, "THREE REMEMBER", F_TITLE, TEXT)
center_text(W/2, 1082, "same endpoints. same sign. every pair cancels.", F_SMALL, TEXT)
center_text(W/2, 1120, "the whole does not.", F_SMALL, TEXT)

im.save("assets/three-remember.png", optimize=True)

# Square self-portrait crop: only the three-strand memory, legible in a circle.
crop = im.crop((1080, 255, 1580, 925)).resize((700, 938), Image.Resampling.LANCZOS)
avatar = Image.new("RGB", (1000, 1000), BG)
avatar.paste(crop, (150, 31))
avatar.save("assets/three-remember-avatar.png", optimize=True)
