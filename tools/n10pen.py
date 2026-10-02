import numpy as np
from PIL import Image

im = np.asarray(Image.open('assets/n10_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper - im, 0, None) / paper

def pen_profile(x0, x1):
    fws = []
    for c in range(x0, x1):
        col = ink[:, c]
        r = np.where(col > 0.02)[0]
        if len(r) == 0:
            continue
        peak = col.max()
        half = peak / 2
        above = np.where(col >= half)[0]
        fw = above[-1] - above[0] + 1
        fws.append(fw)
    return np.array(fws)

for name, (x0, x1) in [('hold', (1000, 1600)), ('climb', (400, 800))]:
    fws = pen_profile(x0, x1)
    print(f"{name} FWHM: median {np.median(fws):.1f} px  mean {fws.mean():.2f}  "
          f"p25 {np.percentile(fws, 25):.1f}  p75 {np.percentile(fws, 75):.1f}")
