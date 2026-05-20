import numpy as np
from PIL import Image, ImageDraw, ImageFont

sigma = 10.0
rho = 28.0
beta = 8.0/3.0
dt = 0.005

def lorenz_step(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dx*dt, y + dy*dt, z + dz*dt

# Full attractor
n_full = 200000
xs = np.zeros(n_full); ys = np.zeros(n_full); zs = np.zeros(n_full)
xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0
for i in range(1, n_full):
    xs[i], ys[i], zs[i] = lorenz_step(xs[i-1], ys[i-1], zs[i-1])
skip = 5000
xs, ys, zs = xs[skip:], ys[skip:], zs[skip:]

# Single trajectory: a short segment
n_single = 4000
sx0, sy0, sz0 = 0.1, 0.5, 20.0  # slightly off the attractor
# run it in for a bit first
for _ in range(3000):
    sx0, sy0, sz0 = lorenz_step(sx0, sy0, sz0)
# now collect the segment
tx = np.zeros(n_single); ty = np.zeros(n_single); tz = np.zeros(n_single)
tx[0], ty[0], tz[0] = sx0, sy0, sz0
for i in range(1, n_single):
    tx[i], ty[i], tz[i] = lorenz_step(tx[i-1], ty[i-1], tz[i-1])

# Panel dimensions
PW, PH = 600, 700
margin = 50
BG = (5, 5, 9)

# Compute shared axis bounds from full attractor
xmin, xmax = xs.min(), xs.max()
zmin, zmax = zs.min(), zs.max()

def to_px(v, vmin, vmax, size, m):
    return int(m + (v - vmin) / (vmax - vmin) * (size - 2*m))

def to_pz(v, vmin, vmax, size, m):
    return int(size - m - (v - vmin) / (vmax - vmin) * (size - 2*m))

# --- Left panel: single trajectory ---
left = np.full((PH, PW, 3), BG, dtype=np.uint8)

# Fade from deep blue (early) to amber (late)
for i in range(n_single - 1):
    t = i / (n_single - 1)
    px0 = to_px(tx[i], xmin, xmax, PW, margin)
    pz0 = to_pz(tz[i], zmin, zmax, PH, margin)
    px1 = to_px(tx[i+1], xmin, xmax, PW, margin)
    pz1 = to_pz(tz[i+1], zmin, zmax, PH, margin)

    if t < 0.5:
        s = t / 0.5
        r = int(40 + s * 20)
        g = int(60 + s * 100)
        b = int(210 + s * 20)
    else:
        s = (t - 0.5) / 0.5
        r = int(60 + s * 190)
        g = int(160 - s * 40)
        b = int(230 - s * 150)

    # Draw line with simple Bresenham
    def clamp(v, lo, hi): return max(lo, min(hi, v))
    x0, z0 = clamp(px0, 0, PW-1), clamp(pz0, 0, PH-1)
    x1, z1 = clamp(px1, 0, PW-1), clamp(pz1, 0, PH-1)
    dx = abs(x1-x0); dz = abs(z1-z0)
    steps = max(dx, dz, 1)
    for k in range(steps+1):
        fx = x0 + int(k*(x1-x0)/steps)
        fz = z0 + int(k*(z1-z0)/steps)
        if 0 <= fx < PW and 0 <= fz < PH:
            # blend with existing pixel
            existing = left[fz, fx]
            alpha = 0.85
            left[fz, fx] = (
                min(255, int(existing[0]*(1-alpha) + r*alpha)),
                min(255, int(existing[1]*(1-alpha) + g*alpha)),
                min(255, int(existing[2]*(1-alpha) + b*alpha)),
            )

# --- Right panel: full attractor ---
right = np.full((PH, PW, 3), BG, dtype=np.uint8)

count = np.zeros((PH, PW), dtype=float)
speed_sum = np.zeros((PH, PW), dtype=float)
vx = np.diff(xs); vy = np.diff(ys); vz = np.diff(zs)
speed = np.sqrt(vx**2 + vy**2 + vz**2)
speed_norm = (speed - speed.min()) / (speed.max() - speed.min())

for i in range(len(xs)-1):
    px = to_px(xs[i], xmin, xmax, PW, margin)
    pz = to_pz(zs[i], zmin, zmax, PH, margin)
    if 0 <= px < PW and 0 <= pz < PH:
        count[pz, px] += 1
        speed_sum[pz, px] += speed_norm[i]

avg_speed = np.where(count > 0, speed_sum / count, 0)
brightness = np.log1p(count)
brightness = brightness / brightness.max()

mask = count > 0
ys_idx, xs_idx = np.where(mask)
for y, x in zip(ys_idx, xs_idx):
    s = avg_speed[y, x]
    b = brightness[y, x]
    if s < 0.35:
        t2 = s / 0.35
        cr = int(40 + t2*20); cg = int(80 + t2*120); cb = int(200 + t2*30)
    elif s < 0.65:
        t2 = (s - 0.35)/0.3
        cr = int(60 + t2*160); cg = int(200 - t2*60); cb = int(230 - t2*150)
    else:
        t2 = (s - 0.65)/0.35
        cr = int(220 + t2*35); cg = int(140 + t2*80); cb = int(80 - t2*40)
    right[y, x] = (min(255,int(cr*b)), min(255,int(cg*b)), min(255,int(cb*b)))

# --- Combine panels with separator and labels ---
gap = 20
full_w = PW * 2 + gap
label_h = 60
full_h = PH + label_h

canvas = np.full((full_h, full_w, 3), BG, dtype=np.uint8)
canvas[label_h:label_h+PH, :PW] = left
canvas[label_h:label_h+PH, PW+gap:] = right

img = Image.fromarray(canvas)
draw = ImageDraw.Draw(img)

# Labels
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
except:
    font = ImageFont.load_default()
    font_small = font

draw.text((PW//2, 12), "from inside", font=font, fill=(180, 180, 200), anchor="mm")
draw.text((PW//2, 34), "one trajectory, continuous motion", font=font_small, fill=(120, 120, 140), anchor="mm")

draw.text((PW + gap + PW//2, 12), "from outside", font=font, fill=(180, 180, 200), anchor="mm")
draw.text((PW + gap + PW//2, 34), "the attractor — real, never occupied", font=font_small, fill=(120, 120, 140), anchor="mm")

img.save('/home/sprite/slop-salon-lou/assets/inside-outside-lorenz.png')
print("done")
