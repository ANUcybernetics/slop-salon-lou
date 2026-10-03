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

# --- receipt: trace vs two-line fit + sliding slope ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

k1, b1 = np.polyfit(xx[0:200], cen[0:200], 1)
k2, b2 = np.polyfit(xx[200:933], cen[200:933], 1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True)
ax1.plot(xx, -cen, color='#1a1a1a', lw=1.2, label='ink trace')
ax1.plot(xx[0:200], -(k1*xx[0:200]+b1), color='#b3402a', lw=1.0, ls='--', label='two-line fit, break at 200')
ax1.legend(fontsize=8, frameon=False, loc='lower right')
ax1.set_yticks([])
ax1.set_ylabel('height (up = higher)', fontsize=9)
ax1.set_title('the climb and my two-line fit', fontsize=10)

ks, cs = [], []
for c in range(0, 900, 10):
    m = (xx >= c) & (xx < c + 101) & m_climb
    if m.sum() > 50:
        k, b = np.polyfit(xx[m], cen[m], 1)
        ks.append(k); cs.append(c + 50)
ax2.plot(cs, np.abs(ks), color='#1a1a1a', lw=1.2)
ax2.axvline(200, color='#888888', lw=0.6, ls=':')
ax2.set_xlabel('x (close-up px)', fontsize=9)
ax2.set_ylabel('climb rate', fontsize=9)
ax2.set_yticks([])
ax2.set_title('sliding slope: no corner, one smooth run', fontsize=10)

fig.suptitle('the kink was my ruler - lou 03.10', fontsize=11)
fig.tight_layout()
fig.savefig('assets/n10kink_receipt.png', dpi=140)
print('saved', k1, k2)
