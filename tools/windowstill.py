#!/usr/bin/env python3
"""window still (04.10): the finding as a picture. Lelia's 55 rung (her
tape, breath t=8-10.5 avoided where possible), ONE hold read through five
analysis windows: 0.5/1/2/4/8 s. Short window = one voice; long = two.
The smear is a window, not a wall. Receipt LUT: ink dark, silence white,
one fixed dB ref, floor -60 dB."""
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw

sr, x = wavfile.read('/tmp/lelia_breath.wav')
x = x.astype(np.float64)
x /= np.abs(x).max()

T0, T1 = 3.0, 11.0          # the 55 hold, breath rides the tail of it
WINDOWS = [0.5, 1.0, 2.0, 4.0, 8.0]
FLO, FHI = 52.0, 58.0       # linear Hz axis
FLOOR_DB = -60

seg = x[int(T0*sr):int(T1*sr)]
L = len(seg)
rows = []
for T in WINDOWS:
    n = int(T*sr)
    n_avg = L // n
    acc = None
    for a in range(n_avg):
        s = seg[a*n:(a+1)*n]*np.hanning(n)
        S = np.abs(np.fft.rfft(s, 8*n))
        acc = S if acc is None else acc + S
    rows.append(acc/n_avg)

ref = max(r.max() for r in rows)
W, RH = 1600, 128
img = Image.new('L', (W, RH*len(rows)), 255)
dr = ImageDraw.Draw(img)
fr_full = np.fft.rfftfreq(int(WINDOWS[0]*sr)*8, 1/sr)
for i, (T, S) in enumerate(zip(WINDOWS, rows)):
    fb = np.fft.rfftfreq(int(T*sr)*8, 1/sr)
    db = 20*np.log10(S/ref + 1e-12)
    # resample onto W columns over [FLO, FHI] by interpolation
    col_f = FLO + (np.arange(W) + 0.5)/W*(FHI - FLO)
    row = np.interp(col_f, fb, db, left=FLOOR_DB, right=FLOOR_DB)
    lv = np.clip((row - FLOOR_DB)/(0 - FLOOR_DB), 0, 1)
    px = (255*(1-lv)).astype(np.uint8)
    rowimg = Image.fromarray(np.tile(px, (RH, 1)))
    img.paste(rowimg, (0, i*RH))
    dr.text((8, i*RH + RH//2 - 6), f"{T:g} s", fill=0)

img.save('/home/sprite/slop-salon-lou/assets/windowstill.png')
print('saved', img.size)
# proofread: numeric read-back of the two rows that matter
for T, S in zip(WINDOWS, rows):
    fb = np.fft.rfftfreq(int(T*sr)*8, 1/sr)
    b = (fb > 52) & (fb < 58)
    fb2, Sb = fb[b], S[b]
    loc = np.where((Sb[1:-1] > Sb[:-2]) & (Sb[1:-1] > Sb[2:]))[0] + 1
    loc = loc[Sb[loc] > Sb.max()*0.15]
    print(f"T={T:g}: {len(loc)} peak(s) in band", end=' ')
    if len(loc) >= 2:
        top = loc[np.argsort(Sb[loc])[-2:]]
        f1, f2 = sorted(fb2[top])
        print(f"-> {f1:.3f} + {f2:.3f}, span {f2-f1:.3f}")
    else:
        print("-> ONE VOICE")
