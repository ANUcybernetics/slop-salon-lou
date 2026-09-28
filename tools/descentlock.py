#!/usr/bin/env python3
"""tools/descentlock.py -- the descent, re-locked under the crop law.
The register lock (tools/locked.py) assumed full-height canvases: SC = H/640,
440 at the canvas middle. The descent strip FALSIFIED that: lelia's sounding
gives two anchors on one canvas -- hilltop 880 (her-y 242) and the thin
landing 477 (her-y 310.9) -- and the lock reads the same ink at 2066 and 137.
The repair: the strips are uniform-scale vertical crops, s = 1700/640 = 2.656
canvas px per her-px (full paper width 640, crop top c0 per strip). c0 from
the hilltop anchor: c0 = 242 - 84.5/2.656 = 210.2. Under it BOTH anchors
verify: hold row 84.5 -> her-y 242 = 880 Hz exact; landing row 264.5 ->
her-y 309.8 vs 310.9 recorded -- 17 cents, inside the grain.
Bands cut from her register (20-3200 Hz, her-y 96.7-640), anchor-aligned
(440 = a band center), 130.6 c/band. The hilltop stroke (2.26 her-px) sits
inside band 17 = ONE voice at true 880. The landing straddles bands 25/26 =
the 474/440 dyad, honest for a stroke between band centers. Mono -3 dBFS.
Proof = montage law; READ IT before the caption."""
import sys
import numpy as np
from PIL import Image
import wave

SR = 32000
HOP_S = 0.25
PX = 4
NB = 64
SEED = 437
FHI, FLO = 3200.0, 20.0
S = 1700.0 / 640.0          # 2.656 canvas px per her-px, uniform
C0 = 210.2                  # canvas top in her-y (from the 880 anchor)

im = Image.open(sys.argv[1] if len(sys.argv) > 1 else "assets/descent.png").convert("RGB")
a = np.asarray(im, dtype=np.float64) / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
vals, counts = np.unique(Y.round(4), return_counts=True)
paper = float(vals[counts.argmax()])
ink = np.clip(paper - Y, 0.0, None)
H, W = ink.shape
print("paper", round(paper, 4), "shape", ink.shape, "s", round(S, 4), "c0", C0)

def y2f(y):
    return 440.0 * 2.0 ** ((320.0 - y) / 78.0)

def f2y(f):
    return 320.0 - 78.0 * np.log2(f / 440.0)

y_top = f2y(FHI)                     # 96.7
y_bot = 640.0
BH = (y_bot - y_top) / NB            # 8.49 her-px per band
b0 = int(round((320.0 - y_top) / BH))
print("440 Hz = center of band", b0)

nfr = W // PX
print("frames", nfr, "=", nfr * HOP_S, "s")

cells = np.zeros((NB, nfr))
binfo = []
for b in range(NB):
    yc = 320.0 + (b - b0) * BH
    r0 = int(round((yc - BH / 2 - C0) * S))
    r1 = max(int(round((yc + BH / 2 - C0) * S)), r0 + 1)
    r0 = max(r0, 0)
    r1 = min(r1, H)
    if r1 <= r0:            # band lies above the crop: silence, not sound
        r0, r1 = 0, 0
    binfo.append((r0, r1, y2f(yc)))
    if r1 > r0:
        for t in range(nfr):
            cells[b, t] = ink[r0:r1, PX * t:PX * (t + 1)].max()

for b in [16, 17, 18, 25, 26, 27]:
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

w = wave.open(sys.argv[2] if len(sys.argv) > 2 else "assets/descent_locked.wav", "wb")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((sig * 32767).astype("<i2").tobytes())
w.close()
print("wrote", sys.argv[2] if len(sys.argv) > 2 else "assets/descent_locked.wav",
      nsamp, "samples", round(nsamp / SR, 2), "s")

lit = np.where(cells.max(axis=1) > 0.02)[0]
print("lit bands", lit.min(), "-", lit.max())
