import numpy as np
from PIL import Image

im = np.asarray(Image.open('assets/n10_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper - im, 0, None) / paper

top = np.full(W, np.nan)
bot = np.full(W, np.nan)
for c in range(W):
    r = np.where(ink[:, c] > 0.02)[0]
    if len(r):
        top[c], bot[c] = r.min(), r.max()

have = np.where(~np.isnan(top))[0]
x0, x1 = int(have[0]), int(have[-1])
s = H / 640
cen = (top + bot) / 2
cents = (320 - cen / s) * 1200 / 78.0
xx = np.arange(W)

print(f"frame {W} x {H}, s={s:.4f}, paper={paper}")
for lo in range(0, W, 100):
    m = (xx >= lo) & (xx < lo + 100) & ~np.isnan(cen)
    if m.sum():
        print(f"x {lo:4d}  centroid {np.nanmean(cents[m]):+7.1f}c  rows {np.nanmin(top[m]):.0f}-{np.nanmax(bot[m]):.0f}")
print(f"x0={x0} x1={x1}")
