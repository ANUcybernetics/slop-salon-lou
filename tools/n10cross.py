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
xx = np.arange(W)
s = 0.909
hold_read = (320 - (cen[1000:1600].mean()/s))*1200/78.0
c0 = 1200 - hold_read
cents = (320 - cen/s)*1200/78.0 + c0

STOPS = [('ground', 31.2), ('qfloor', 62.3), ('shelf', 90.5), ('terrace', 124.5),
         ('ledge', 249.3), ('rest', 355.5), ('home', 440.0), ('t474', 474.0),
         ('t512', 512.0), ('t552', 552.0), ('gift', 590.0), ('hill', 880.0)]

climb = np.arange(0, 934)
cc = cents[0:934]
print(f"under s={s}, c0={c0:+.1f}c:")
for name, f in STOPS:
    target = 1200*np.log2(f/440.0)
    if target < cc[0] or target > cc[-1]:
        print(f"  {name:8s} {f:6.1f} Hz  OFF-FRAME")
        continue
    x = np.interp(target, cc, climb)
    print(f"  {name:8s} {f:6.1f} Hz  crossed at x={x:6.1f}")
print(f"kink (x=200): {cents[200]:+.1f}c = {440*2**(cents[200]/1200):.2f} Hz")
print(f"x=0: {cents[0]:+.1f}c = {440*2**(cents[0]/1200):.2f} Hz")
