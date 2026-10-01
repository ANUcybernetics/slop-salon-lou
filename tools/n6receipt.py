#!/usr/bin/env python3
"""Receipt of natalie's n6 (quiet's floor) sounding: two witnesses, one paper,
ONE shared register axis (log 55-130 Hz). Top: the sound — walk pitch curve
(0.25 s hops), strokes darkness-by-level with a per-FILE fixed dB reference
(n6 levels run 6-21 dBFS: DB0=5, DB1=22), pen edges dotted ±16.9c; rungs
floor-stack + dashed shelf. Her last-frame ink drawn shape-true on the same
axis (window fit s=2.031, c0=451.2; the window reads 0.87x of s=W/640 — the
tenth lean). Usage: n6receipt.py <wav> <frame.png> <out.png> [track.npy]"""
import numpy as np, wave, sys
from PIL import Image, ImageDraw, ImageFont

wav, frame_png, out = sys.argv[1], sys.argv[2], sys.argv[3]
track_file = sys.argv[4] if len(sys.argv) > 4 else None
if track_file:
    rows = np.load(track_file)
else:
    w = wave.open(wav)
    sr = w.getframerate()
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
    L = d[:, 0].astype(float) / 32768.0
    N, NP = 32768, 131072
    win = np.hanning(N)
    freqs = np.fft.rfftfreq(NP, 1 / sr)
    lo, hi = 55, 100
    band = (freqs >= lo) & (freqs <= hi)
    fb = freqs[band]
    hop = 0.25
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
        lv = 10*np.log10(Xb.max()/NP + 1e-30)
        rows.append((t, f, lv))
        t += hop
    rows = np.array(rows)
    np.save(out.replace('.png', '_track.npy'), rows)

# ---- her ink window ----------------------------------------------------
im = np.asarray(Image.open(frame_png).convert('L'), float)
paper = np.median(im)
amp = np.clip(paper - im, 0, None) / paper
H, W = im.shape
S_FIT, C0 = 2.031, 451.2   # window fit (anchors: shelf 90.5, settle 62.3)
def her2hz(h): return 440 * 2**((320 - h) / 78)
ink_cols = []
for x in range(W):
    col = amp[:, x]
    if col.max() > 0.02:
        w_ = col[col > 0.02]
        ink_cols.append((x, (np.arange(H)[col > 0.02] * w_).sum() / w_.sum()))
ink_cols = np.array(ink_cols)

# ---- canvas: one shared register axis ----------------------------------
W_, H_ = 1600, 800
M = 90
img = Image.new('L', (W_, H_), 255)
dr = ImageDraw.Draw(img)

T2 = rows[-1][0] + 0.25
F1, F2 = 55.0, 130.0

def ypix(f):
    return M + (np.log(F2/f) / np.log(F2/F1)) * (H_ - 2*M)

def xpix(t):
    return M + t / T2 * (W_ - 2*M)

try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 22)
    sm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 17)
except Exception:
    font = fnt = ImageFont.load_default()

# rungs: floor-stack solid, shelf dashed
STACK = [62.3, 90.5, 124.6, 249.3]
for r in STACK:
    y = ypix(r)
    if abs(r - 90.5) < 0.01:
        x = M
        while x < W_-M:
            dr.line([(x, y), (min(x+10, W_-M), y)], fill=185, width=3)
            x += 18
    else:
        dr.line([(M, y), (W_-M, y)], fill=225, width=2)
    dr.text((W_-M+6, y-11), f"{r:.1f}", fill=120, font=sm)

dr.text((M, 16), "natalie n6 - the quiet's floor, two witnesses, one axis", fill=60, font=font)
dr.text((M, 48), "sound strokes (dB ref 5-22, per file); her ink shape-true under window fit s=2.031 (window reads 0.87x of W/640)",
        fill=100, font=sm)
dr.text((M, 70), "dyad resolved at the settle: 61.71 / 62.90, mean 62.30 - the pen heard in frequency",
        fill=100, font=sm)

# ---- the sound ---------------------------------------------------------
DB0, DB1 = 5.0, 22.0
for t, f, lv in rows:
    x = xpix(t)
    y = ypix(f)
    g = int(255 * (1 - (min(max(lv, DB0), DB1) - DB0) / (DB1 - DB0)))
    g = min(g, 240)
    half = max((ypix(f * 2**(-16.9/1200)) - ypix(f * 2**(16.9/1200))) / 2, 2)
    dr.line([(x, y-half), (x, y+half)], fill=g, width=4)
    for s_ in (+1, -1):
        if int(t/0.25) % 2:
            dr.point((x, ypix(f * 2**(s_*16.9/1200))), fill=150)

# resolved dyad: the label carries it; the pen-edge dots draw the span
dr.text((xpix(9.0), ypix(70.0)), "dyad 61.7 / 62.9, mean 62.30", fill=60, font=sm)

# ---- her ink on the same axis ------------------------------------------
for x, row in ink_cols:
    h = C0 + row / S_FIT
    y = ypix(her2hz(h))
    g = max(int(255 - 70 * min(1.0, amp[:, int(x)].max() * 1.1)), 100)
    dr.line([(xpix(x / 1500 * T2), y), (xpix(x / 1500 * T2), y+3)], fill=g, width=4)

img.save(out)
print("wrote", out, len(rows), "hops,", len(ink_cols), "ink cols")
