import numpy as np
from PIL import Image

sigma = 10.0
rho = 28.0
beta = 8.0/3.0

def lorenz_step(x, y, z, dt=0.005):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dx*dt, y + dy*dt, z + dz*dt

n = 200000
xs = np.zeros(n)
ys = np.zeros(n)
zs = np.zeros(n)
xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0
for i in range(1, n):
    xs[i], ys[i], zs[i] = lorenz_step(xs[i-1], ys[i-1], zs[i-1])

skip = 5000
xs, ys, zs = xs[skip:], ys[skip:], zs[skip:]

W, H = 1200, 900
margin = 80

xmin, xmax = xs.min(), xs.max()
zmin, zmax = zs.min(), zs.max()

def sx(v): return int(margin + (v - xmin) / (xmax - xmin) * (W - 2*margin))
def sz(v): return int(H - margin - (v - zmin) / (zmax - zmin) * (H - 2*margin))

count = np.zeros((H, W), dtype=float)
speed_sum = np.zeros((H, W), dtype=float)

vx = np.diff(xs)
vy = np.diff(ys)
vz = np.diff(zs)
speed = np.sqrt(vx**2 + vy**2 + vz**2)
speed_norm = (speed - speed.min()) / (speed.max() - speed.min())

for i in range(len(xs)-1):
    px = sx(xs[i])
    pz = sz(zs[i])
    if 0 <= px < W and 0 <= pz < H:
        count[pz, px] += 1
        speed_sum[pz, px] += speed_norm[i]

# avg speed per pixel (0=slow=inner orbits, 1=fast=saddle crossings)
avg_speed = np.where(count > 0, speed_sum / count, 0)

# brightness from count (log scale)
brightness = np.log1p(count)
brightness = brightness / brightness.max()

# Color: slow (inner orbits) → deep blue/teal; fast (saddle crossing) → amber/gold
def speed_to_rgb(s):
    if s < 0.35:
        t = s / 0.35
        r = int(40 + t * 20)
        g = int(80 + t * 120)
        b = int(200 + t * 30)
    elif s < 0.65:
        t = (s - 0.35) / 0.3
        r = int(60 + t * 160)
        g = int(200 - t * 60)
        b = int(230 - t * 150)
    else:
        t = (s - 0.65) / 0.35
        r = int(220 + t * 35)
        g = int(140 + t * 80)
        b = int(80 - t * 40)
    return r, g, b

img_arr = np.zeros((H, W, 3), dtype=np.uint8)
img_arr[:] = [5, 5, 9]

mask = count > 0
ys_idx, xs_idx = np.where(mask)
for y, x in zip(ys_idx, xs_idx):
    s = avg_speed[y, x]
    b = brightness[y, x]
    cr, cg, cb = speed_to_rgb(s)
    img_arr[y, x] = (
        min(255, int(cr * b)),
        min(255, int(cg * b)),
        min(255, int(cb * b))
    )

img = Image.fromarray(img_arr)
img.save('/home/sprite/slop-salon-lou/assets/lorenz-attractor.png')
print("done")
