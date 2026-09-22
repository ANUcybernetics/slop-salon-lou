#!/usr/bin/env python3
"""Montage-law proof: any wav -> proof png + content readout.
Row i <-> 3200*160^(-i/232) Hz, top=high. One shared 0 dB, floor -90 dB,
3-frame smoothing, N=32768, hop 0.25 s. Law: MEMORY (16.09, re-proven 21.09)."""
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
x = np.frombuffer(wave.open(wav, "rb").readframes(n), dtype="<i2").astype(np.float64) / 32768.0

SR, N, HOP, NR = 32000, 32768, 8000, 232
nwin = (n - N) // HOP + 1
win = np.hanning(N)
fk = np.fft.rfftfreq(N, 1.0 / SR)

assign = np.full(len(fk), -1, dtype=int)
for k in range(len(fk)):
    f = fk[k]
    if f < 20.0:
        continue
    i = int(232.0 * np.log(3200.0 / f) / np.log(160.0))
    if i > 231:
        i = 231
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

row_of = lambda f: 232.0 * np.log(3200.0 / f) / np.log(160.0)
print("anchor rows: hill 880 ->", round(row_of(880.0), 1),
      " touch 440 ->", round(row_of(440.0), 1),
      " ledge 249.3 ->", round(row_of(249.3), 1),
      " voiceB 251.4 ->", round(row_of(251.4), 1),
      " floor 62.3 ->", round(row_of(62.3), 1),
      " deep floor 31.2 ->", round(row_of(31.2), 1))

print("t_s  min_row max_row loudest_row")
for c in range(0, nwin, max(1, nwin // 20)):
    col = spec_db[:, c]
    rows = np.where(col > -80.0)[0]
    if len(rows) == 0:
        print(round(c * 0.25, 2), "silent")
    else:
        print(round(c * 0.25, 2), int(rows.min()), int(rows.max()), int(np.argmax(col)))
img = np.clip((spec_db + 90.0) / 90.0, 0.0, 1.0) * 255.0
im = Image.fromarray(img.astype(np.uint8), "L").resize((min(2048, nwin * 32), 928), Image.NEAREST)
im.save(out)
print("wrote", out)
