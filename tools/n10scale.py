import numpy as np
from PIL import Image

im = np.asarray(Image.open('assets/n10_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper - im, 0, None) / paper
top = np.full(W, np.nan); bot = np.full(W, np.nan)
for c in range(W):
    r = np.where(ink[:, c] > 0.02)[0]
    if len(r):
        top[c], bot[c] = r.min(), r.max()
cen = (top + bot) / 2
s = H / 640
cents0 = (320 - cen / s) * 1200 / 78.0
xx = np.arange(W)
# climb = x < 933; hold = x >= 933
hold_c0 = 1200 - cents0[1000:1600].mean()   # c0 so that hold = +1200c (880.05)
print(f"H/640 = {s:.4f}; c0 to put hold on 880: {hold_c0:+.1f}c")
print(f"climb start under that c0: {cents0[0]+hold_c0:+.1f}c = {440*2**((cents0[0]+hold_c0)/1200):.1f} Hz")

# s-scan: for each s, c0 from hold anchor; report climb start and shape
print("\ns-scan (c0 anchored on hold=880):")
for s in [0.773, 0.897, 0.9105, 1.293, 1.5, 1.869, 2.31, 2.656]:
    cents = (320 - cen/s)*1200/78.0
    c0 = 1200 - cents[1000:1600].mean()
    start = cents[0] + c0
    home_x = np.interp(0.0, cents+c0, xx) if (cents[0]+c0) < 0 < (cents[933]+c0) else float('nan')
    print(f"  s={s:.4f}  c0={c0:+7.1f}c  climb start {start:+7.1f}c = {440*2**(start/1200):6.1f} Hz  "
          f"home at x={home_x:.0f}")
