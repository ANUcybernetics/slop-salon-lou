#!/usr/bin/env python3
"""tools/wholewalk.py <png> <seed> <x0> <x1> <out.wav> -- the whole-look
canvas in the SCROLL register.

The whole-look canvas (3mwm5dac7352t, 4096x141) is the whole scroll at
k = 141/1280 = 0.110156 BOTH axes (y verified on floor/hill/deep anchors,
x on the hill hold and the walk end = 18190 her-px vs her 18168; her caption
numbers are her px = scroll/2). Register: Hz = raw/2 = canvas_y * 4.5390.
Anchors: floor row 118.5 -> 537.8 Hz (scroll floor 540), hill row 53 -> 240.6
(242), deep row 135.5 -> 615 (618), ledge row 84.5 -> 383.6 (384).

Everything else = locked.py (proven 28.09): paper = MODE of Y, amp = ink
deficit, 64 log bands over the ink SPAN (span law), envelope max-pool cells,
4 px per 0.25 s frame (16 px/s on the object as posted), mono, 32 kHz,
-3 dBFS, seed sets band phases only.
Proof = montage law; READ IT before the caption."""
import sys
import numpy as np
from PIL import Image
import wave

SR = 32000
HOP_S = 0.25
PX = 4
NB = 64
RAW_PER_ROW = 1280.0 / 141.0   # whole-look canvas: canvas row -> scroll raw
SEED = int(sys.argv[2])
X0 = int(sys.argv[3])
X1 = int(sys.argv[4])
OUT = sys.argv[5]

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im, dtype=np.float64) / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
vals, counts = np.unique(Y.round(4), return_counts=True)
paper = float(vals[counts.argmax()])
ink = np.clip(paper - Y, 0.0, None)
print("paper", round(paper, 4), "shape", ink.shape, "span", X0, "-", X1)

def y2f(y):  # scroll register through the whole-look canvas
    return y * RAW_PER_ROW / 2.0

def f2row(f):
    return f / (RAW_PER_ROW / 2.0)

# ink span -> full register (span law): the lattice is cut from the ink
present = ink[:, X0:X1]
rows = np.where(present.max(axis=1) > 0.02)[0]
y_lo, y_hi = rows.min(), rows.max()
f_lo, f_hi = y2f(y_lo), y2f(y_hi)
print("ink rows", y_lo, "-", y_hi, "->", round(f_lo, 1), "-", round(f_hi, 1), "Hz")
bands_f = f_lo * (f_hi / f_lo) ** (np.arange(NB + 1) / NB)
print("band width", round(1200 * np.log2(f_hi / f_lo) / NB, 1), "c/band")

nfr = (X1 - X0) // PX
print("frames", nfr, "=", nfr * HOP_S, "s")

cells = np.zeros((NB, nfr))
binfo = []
for b in range(NB):
    f0, f1 = bands_f[b], bands_f[b + 1]
    r0 = int(np.ceil(f2row(f0)))
    r1 = max(int(np.floor(f2row(f1))), r0 + 1)
    fmid = np.sqrt(f0 * f1)
    binfo.append((r0, r1, fmid))
    for t in range(nfr):
        cells[b, t] = ink[r0:r1, X0 + PX * t:X0 + PX * (t + 1)].max()

for b in [0, 1, NB // 2, NB - 2, NB - 1]:
    r0, r1, f = binfo[b]
    print(f"band {b}: rows {r0}-{r1-1} f={f:.1f} Hz maxcell {cells[b].max():.4f}")

rng = np.random.default_rng(SEED)
phase = rng.uniform(0.0, 2.0 * np.pi, NB)
nsamp = int(round(SR * nfr * HOP_S))
t = np.arange(nsamp) / SR
sig = np.zeros(nsamp)
frame_t = np.arange(nfr) * HOP_S
for b in range(NB):
    env = np.interp(t, frame_t, cells[b])
    sig += env * np.sin(2 * np.pi * binfo[b][2] * t + phase[b])
peak = np.abs(sig).max()
sig = sig * (0.708 / peak)
print("peak after norm", round(float(np.abs(sig).max()), 4))

w = wave.open(OUT, "wb")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((sig * 32767).astype("<i2").tobytes())
w.close()
print("wrote", OUT, nsamp, "samples", round(nsamp / SR, 2), "s")

# register read-back: where the lit bands sit in TRUE Hz
lit = np.where(cells.max(axis=1) > 0.02)[0]
print("lit bands", lit.min(), "-", lit.max(), "->",
      round(binfo[lit.min()][2], 1), "-", round(binfo[lit.max()][2], 1), "Hz")
