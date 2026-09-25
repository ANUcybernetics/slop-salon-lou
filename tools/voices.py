#!/usr/bin/env python3
"""472 voice inventory render: the dyad. Linear 60-240 Hz, top=high, one
shared 0 dB, floor -90 dB, 3-frame smoothing, N=32768, hop 0.25 s,
pale-blue LUT on near-black. cp tailspec.py + range edits, 25.09.
Anchors (row_of, linear): 232->6.9, 179->53.0, 112->110.9, 100->121.3,
74.7->143.2. (Log 60-240 stripes at the bottom: rows 0.53 Hz < bins
0.98 Hz - unassigned rows render black. Linear 1.15 Hz rows, all fed.)"""
import numpy as np
import wave
import sys
from PIL import Image

wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav, "rb")
sr = w.getframerate()
n = w.getnframes()
w.close()
print("wav", wav, sr, "Hz", n, "samples", round(n / sr, 2), "s")
x = np.frombuffer(wave.open(wav, "rb").readframes(n), dtype="<i2").astype(np.float64).reshape(-1, 2)
x = x.mean(axis=1) / 32768.0

SR, N, HOP, NR = 32000, 32768, 8000, 157
nwin = (n - N) // HOP + 1
win = np.hanning(N)
fk = np.fft.rfftfreq(N, 1.0 / SR)

assign = np.full(len(fk), -1, dtype=int)
for k in range(len(fk)):
    f = fk[k]
    if f < 60.0:
        continue
    i = int(round(156.0 * (240.0 - f) / 180.0))
    if i > 156:
        i = 156
    A = assign
    A[k] = i

spec = np.zeros((NR, nwin))
for t in range(nwin):
    m = A >= 0
    xx = x[t * HOP: t * HOP + N]
    mm = np.abs(np.fft.rfft(xx * win))
    np.maximum.at(spec, (A[m], t), mm[m])

spec_db = 20.0 * np.log10(np.maximum(spec / spec.max(), 1e-12))
spec_db = np.maximum(spec_db, -90.0)
sm = spec_db.copy()
sm[:, 1:-1] = np.maximum(spec_db[:, 1:-1], np.maximum(spec_db[:, :-2], spec_db[:, 2:]))
spec_db = sm

np.save(out.replace(".png", ".npy"), spec_db)

row_of = lambda f: 156.0 * (240.0 - f) / 180.0
print("anchor rows: 232 ->", round(row_of(232.0), 1),
      " 179 ->", round(row_of(179.0), 1),
      " 112 ->", round(row_of(112.0), 1),
      " 100 ->", round(row_of(100.0), 1),
      " 74.7 ->", round(row_of(74.7), 1))

print("t_s  min_row max_row loudest_row  lum232")
r232 = int(round(row_of(232.0)))
for c in range(0, nwin, max(1, nwin // 20)):
    col = spec_db[:, c]
    rows = np.where(col > -80.0)[0]
    l232 = round(float(col[r232]), 1)
    if len(rows) == 0:
        print(round(c * 0.25, 2), "silent", l232)
    else:
        print(round(c * 0.25, 2), int(rows.min()), int(rows.max()), int(np.argmax(col)), l232)
img = np.clip((spec_db + 90.0) / 90.0, 0.0, 1.0)
lut_r = img ** 3.0 * 255.0 * 0.55
lut_g = img ** 1.6 * 255.0 * 0.72
lut_b = img * 255.0
rgb = np.dstack([lut_r, lut_g, lut_b]).astype(np.uint8)
im = Image.fromarray(rgb).resize((min(2048, nwin * 32), 928), Image.NEAREST)
im.save(out)
print("wrote", out)
