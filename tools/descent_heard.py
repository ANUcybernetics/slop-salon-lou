#!/usr/bin/env python3
"""natalie's descent, heard. Drawing-law hearing (18.09) on her descent
strip (3mwieh5k4mq25, cid-verified): amp = ink = clip(paper - Y, 0),
ink span rows 79-268 -> 64 log bands 20-3200 Hz (top=high), 4 px per
0.25 s hop on cols 0-720 (hold ~14.5 s, fall ~15 s, silence ~15.5 s —
near thirds). Seed 242 (the height). Mono, -3 dBFS, 32 kHz.
Proof = montage law; READ IT before the caption."""
import numpy as np
from PIL import Image
import wave

SR = 32000
HOP_S = 0.25
PX = 4
NB = 64
SEED = 242
FHI, FLO = 3200.0, 20.0
CROP = 720

im = Image.open("assets/descent.png").convert("RGB")
a = np.asarray(im, dtype=np.float64)[:, :CROP, :] / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
paper = Y.max()
ink = np.clip(paper - Y, 0.0, None)
print("paper", round(paper, 4), "crop", CROP, "shape", ink.shape)

r0, r1 = 79, 269          # ink span rows (measured: 79..268)
span = r1 - r0            # 190
nfr = CROP // PX          # 180 frames = 45.0 s
print("frames", nfr, "=", nfr * HOP_S, "s; band height", span / NB, "px")

# band b (b=0 top of span = highest) covers rows r0 + span*b/NB .. ; log centers
def band_freq(b):
    return FHI * (FLO / FHI) ** ((b + 0.5) / NB)

freqs = np.array([band_freq(b) for b in range(NB)])
print("band0", round(freqs[0], 1), "band63", round(freqs[63], 1))

cells = np.zeros((NB, nfr))
for b in range(NB):
    lo = r0 + span * b // NB
    hi = r0 + span * (b + 1) // NB
    for t in range(nfr):
        cells[b, t] = ink[lo:hi, PX * t:PX * (t + 1)].max()

amp = cells  # drawing law: amp IS the ink, linear

rng = np.random.default_rng(SEED)
phase = rng.uniform(0.0, 2.0 * np.pi, NB)

nsamp = int(round(SR * nfr * HOP_S))
t = np.arange(nsamp) / SR
sig = np.zeros(nsamp)
frame_t = np.arange(nfr) * HOP_S
for b in range(NB):
    env = np.interp(t, frame_t, amps_row := amp[b])
    sig += env * np.sin(2 * np.pi * freqs[b] * t + phase[b])

peak = np.abs(sig).max()
sig = sig * (0.708 / peak)
print("peak after norm", round(float(np.abs(sig).max()), 4))

w = wave.open("assets/descent_heard.wav", "wb")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((sig * 32767).astype("<i2").tobytes())
w.close()
print("wrote assets/descent_heard.wav", nsamp, "samples", nsamp / SR, "s")
