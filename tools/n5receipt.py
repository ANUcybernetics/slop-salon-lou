#!/usr/bin/env python3
"""Receipt of natalie's n5 (shelf) sounding: the walk's pitch curve with the
old lattice drawn in. Silence renders WHITE (receipt LUT); fixed dB reference.
Rungs: floor-stack 62.3×1..4, shelf 90.5 dashed (the rung the pen never drew),
pen edges dotted at ±16.9¢.
Usage: n5receipt.py <wav> <out.png> [track.npy]"""
import numpy as np, wave, sys
from PIL import Image, ImageDraw, ImageFont

wav, out = sys.argv[1], sys.argv[2]
track_file = sys.argv[3] if len(sys.argv) > 3 else None
if track_file:
    rows = np.load(track_file)
else:
    w = wave.open(wav)
    sr = w.getframerate()
    d = inline = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
    L = d[:, 0].astype(float) / 32768.0
    N, NP = 32768, 131072
    win = np.hanning(N)
    freqs = np.fft.rfftfreq(NP, 1 / sr)
    lo, hi = 55, 300
    band = (freqs >= lo) & (freqs <= hi)
    fb = freqs[band]
    hop = 0.25 * sr
    rows = []
    t = 0.0
    while t + 1.0 < len(L) / sr:
        s = int(t * sr)
        X = np.abs(np.fft.rfft(L[s:s+N]*win, NP))**2
        Xb = X[band]
        k = Xb.argmax()
        a, b, c = Xb[max(k-1,0):k+2]
        dp = 0.5*(a-c)/(a-2*b+c+1e-30)
        f = fb[k] + dp*(fb[1]-fb[0])
        lv = 10*np.log10(Xb.max()+1e-30)
        rows.append((t, f, lv))
        t += 0.25
    rows = np.array(rows)

W, H = 1600, 800
M = 90  # margins
img = Image.new('L', (W, H), 255)
dr = ImageDraw.Draw(img)

T1, T2 = 0.0, rows[-1][0] + 0.25
F1, F2 = 55.0, 300.0  # log axis

def ypix(f):
    return M + (np.log(F2/f) / np.log(F2/F1)) * (H-2*M)

def xpix(t):
    return M + (t - T1) / (T2 - T1) * (W-2*M)

# rungs
STACK = [62.3, 124.6, 186.9, 249.3]
SHELF = 90.5
PEN_C = 16.9  # cents

try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 22)
except Exception:
    font = ImageFont.load_default()
try:
    sm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 17)
    fnt = sm
except Exception:
    fnt = font

# paper grid: faint rungs, full width
for r in STACK:
    y = ypix(r)
    dash = (4, 6) if abs(r - SHELF) < 0.01 else (8, 6)
    if abs(r - SHELF) < 0.01:
        continue
    dr.line([(M, y), (W-M, y)], fill=225, width=2)
# shelf: dashed (pen never drew it)
ys = ypix(SHELF)
x = M
while x < W-M:
    dr.line([(x, ys), (min(x+10, W-M), ys)], fill=185, width=3)
    x += 18
# stack labels right side
for r in STACK:
    y = ypix(r)
    dr.text((W-M+6, y-11), f"{r:.1f}", fill=120, font=fnt)
dr.text((W-M+6, ys-11), "90.5", fill=120, font=fnt)
dr.text((M, 18), "natalie n5 - the shelf receipt", fill=60, font=font)
dr.text((M, 50), "runes: floor-stack (62.3 x1..4), shelf dashed = the rung the pen never drew; dotted = pen edges +-16.9c",
        fill=100, font=fnt)

# walk ink: each hop a vertical stroke, darkness by level (fixed ref)
DB0, DB1 = 25.0, 65.0  # below 25 dB -> white
for t, f, lv in rows:
    x = xpix(t)
    y = ypix(f)
    g = int(255 * (1 - (min(max(lv, DB0), DB1) - DB0) / (DB1 - DB0)))
    g = min(g, 240)
    # stroke height = pen edges span (2 x 16.9c) in px, min 4 px
    half = (ypix(f * 2**(-PEN_C/1200)) - ypix(f * 2**(PEN_C/1200))) / 2
    half = max(half, 2)
    dr.line([(x, y-half), (x, y+half)], fill=g, width=5)
# pen edges as dotted envelope around the track
for t, f, lv in rows:
    for s in (+1, -1):
        fe = f * 2**(s*PEN_C/1200)
        x = xpix(t)
        if int(t/0.25) % 2:
            dr.point((x, ypix(fe)), fill=150)

img.save(out)
print("wrote", out, len(rows), "hops")
