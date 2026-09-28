#!/usr/bin/env python3
"""natalie's far walk off the touch (3mwkaxtrn572r, cid+size-verified), heard
REGISTER-LOCKED for the first time: no ink-span zoom. Bands are cut on her
register (440 @ her-y 320, 78 her-px/oct, scale 1183/640 = 1.8484 cpx/herpx):
the audible window 20-3200 Hz covers her-y 133.7-640, 64 log bands -> 83.6
c/band, 7.91 her-px = 14.6 canvas px each. A 3-4 px stroke sits INSIDE a
band -> a level hold should sound ONE voice at its TRUE pitch (the dyad law
predicted this: span-zoom band height 5.44 was the problem, not the law).
paper = MODE (toned paper, 0.8827). amp = ink linear. Seed 437 (the height).
Mono, -3 dBFS, 32 kHz. Proof = montage law; READ IT before the caption."""
import numpy as np
from PIL import Image
import wave

SR = 32000
HOP_S = 0.25
PX = 4
NB = 64
SEED = 437
FHI, FLO = 3200.0, 20.0
CROP = 1700

im = Image.open("assets/offthetouch.png").convert("RGB")
a = np.asarray(im, dtype=np.float64)[:, :CROP, :] / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
vals, counts = np.unique(Y.round(4), return_counts=True)
paper = float(vals[counts.argmax()])
ink = np.clip(paper - Y, 0.0, None)
print("paper", round(paper, 4), "crop", CROP, "shape", ink.shape)

SC = ink.shape[0] / 640.0            # canvas px per her-px
print("scale", round(SC, 4))

def y2f(y):                          # her register: 440 at her-y 320
    return 440.0 * 2.0 ** ((320.0 - y) / 78.0)

def f2y(f):
    return 320.0 - 78.0 * np.log2(f / 440.0)

y_top = f2y(FHI)                     # 3200 Hz line
y_bot = min(f2y(FLO), 640.0)         # canvas floor = 640 her-px = 25.3 Hz
BH = (y_bot - y_top) / NB            # her-px per band
cents = 1200 * np.log2(FHI / y2f(y_bot))
print("window her-y", round(y_top, 1), "-", round(y_bot, 1),
      "=", round(y_bot - y_top, 1), "px =", round(cents, 0), "cents;",
      "band height", round(BH, 2), "her-px =", round(BH * SC, 1),
      "canvas px;", round(cents / NB, 1), "c/band")

# anchor-aligned lattice: band centers at 320 + (b-b0)*BH so 440 Hz (y 320)
# is a band CENTER -- the lattice is cut from the touch.
b0 = int(round((320.0 - y_top) / BH))   # band whose center lands on the 440 line
print("440 Hz = center of band", b0)

nfr = CROP // PX                     # 425 frames = 106.25 s
print("frames", nfr, "=", nfr * HOP_S, "s")

cells = np.zeros((NB, nfr))
binfo = []
for b in range(NB):
    yc = 320.0 + (b - b0) * BH
    y0 = yc - BH / 2
    y1 = yc + BH / 2
    r0 = int(round(y0 * SC))
    r1 = max(int(round(y1 * SC)), r0 + 1)
    fmid = y2f(yc)
    binfo.append((r0, r1, fmid))
    for t in range(nfr):
        cells[b, t] = ink[r0:r1, PX * t:PX * (t + 1)].max()

for b in [0, 1, b0 - 1, b0, b0 + 1, 50, 63]:
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

w = wave.open("assets/offthetouch_heard.wav", "wb")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((sig * 32767).astype("<i2").tobytes())
w.close()
print("wrote assets/offthetouch_heard.wav", nsamp, "samples", round(nsamp / SR, 2), "s")

# register read-back: where the lit bands sit in TRUE Hz
lit = np.where(cells.max(axis=1) > 0.02)[0]
print("lit bands", lit.min(), "-", lit.max())
for b in [lit.min(), lit.max()]:
    print("  band", b, f"{binfo[b][2]:.1f} Hz")
