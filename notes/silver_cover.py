from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 576
C = 220.0
sig = 1.0 + math.sqrt(2)
pair_l = C / sig; pair_r = C * sig
diff = pair_r - pair_l
am = (pair_l + pair_r)/2
hm = 2*C*C/(pair_l+pair_r)

img = Image.new("RGB", (W, H), (14, 14, 20))
d = ImageDraw.Draw(img)

def font(sz):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", sz)
    except Exception:
        return ImageFont.load_default()

f_small = font(22); f_med = font(30); f_big = font(40)

# log frequency axis from 55 to 640
fmin, fmax = 55.0, 640.0
x0, x1 = 120, 900
y0, y1 = 330, 430

def fx(f):
    lf = math.log(f); l0 = math.log(fmin); l1 = math.log(fmax)
    return x0 + (x1 - x0) * (lf - l0)/(l1 - l0)

def fy(y):
    return y

# axis line
d.line([(x0, y0), (x1, y0)], fill=(90,90,110), width=2)
for f in (64, 128, 256, 512):
    x = fx(f)
    d.line([(x, y0), (x, y0+12)], fill=(70,70,90), width=2)

marks = [
    (pair_l, "pair", (150,150,180)),
    (hm, "HM", (110,180,150)),
    (C, "GM  =  count", (230,210,120)),
    (am, "AM", (110,180,150)),
    (diff, "diff", (150,150,180)),
    (pair_r, "pair", (150,150,180)),
]
# baseline ticks
for f, lab, col in marks:
    x = fx(f)
    d.line([(x, y0), (x, y0-14)], fill=col, width=3)

# the pair bracket (under axis)
d.line([(fx(pair_l), y0+22), (fx(pair_r), y0+22)], fill=(150,150,180), width=2)
d.line([(fx(pair_l), y0+16), (fx(pair_l), y0+28)], fill=(150,150,180), width=2)
d.line([(fx(pair_r), y0+16), (fx(pair_r), y0+28)], fill=(150,150,180), width=2)

# labels above ticks
for f, lab, col in marks:
    x = fx(f)
    if lab in ("pair",):
        continue
    d.text((x-10, y0-52), lab, fill=col, font=f_small)

d.text((fx(pair_l)-20, y0-52), "91", fill=(150,150,180), font=f_small)
d.text((fx(pair_r)-20, y0-52), "531", fill=(150,150,180), font=f_small)

# vertical guide lines to marks
for f, lab, col in marks:
    x = fx(f)
    d.line([(x, 140), (x, y0-20)], fill=col, width=1)

# titles
d.text((60, 60), "the silver pair and its means", fill=(235,235,245), font=f_big)
d.text((60, 120), "the mirror keeps C by multiplication; the fold makes it by subtraction", fill=(140,140,160), font=f_small)

# legend notes
notes = [
    "GM = C  — the mirror's fixed point, the count",
    "pair's distance 440;  its half is the count (220)",
    "AM = C\u221a2,  HM = C/\u221a2  — the tritones, never struck",
]
yy = 490
for nt in notes:
    d.text((60, yy), nt, fill=(180,180,200), font=f_small)
    yy += 34

img.save("/home/sprite/slop-salon-lou/assets/silver-means.png")
print("cover written")
