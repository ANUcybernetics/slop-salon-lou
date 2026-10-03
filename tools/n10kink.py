import numpy as np
from PIL import Image

# n10 close-up: does the kink at x=200 survive any calibration?
# Slope ratio is invariant under affine pitch calibration and uniform x-rescale,
# so measure in rows and check the ratio directly.

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

# climb = x < 933 (hold starts there, per n10ink.py)
xx = np.arange(W)
m_climb = (xx < 933) & ~np.isnan(cen)

# sliding linear fit, 101-px window, step 10
print("sliding slope (rows/px), 101-px window:")
for c in range(0, 900, 10):
    m = (xx >= c) & (xx < c + 101) & m_climb
    if m.sum() > 50:
        k, b = np.polyfit(xx[m], cen[m], 1)
        resid = cen[m] - (k * xx[m] + b)
        print(f"  x {c:4d}-{c+100:4d}  slope {k:+.4f} rows/px  rms {np.sqrt((resid**2).mean()):.2f} rows")
