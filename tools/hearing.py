#!/usr/bin/env python3
"""The hearing law: any plate -> 64 s resynth. Law: notes 17.09 (silent_588) + MEMORY.
1024x1024 plate -> 64 log bands 20-3200 Hz (top=high), 4 px per 0.25 s hop,
256 frames = 64.0 s. dB = 60*log10(cellmax/Lmax), floor -75.
One phase-random sine per band (seed 490), 32 kHz, linear interp, mono, -3 dBFS."""
import numpy as np
from PIL import Image
import wave
import sys

SR = 32000
HOP_S = 0.25
PX = 4
NB = 64
SEED = int(sys.argv[2])
FHI = 3200.0
FLO = 20.0
FLOOR = -75.0

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im, dtype=np.float64) / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
Lmax = Y.max()
print("Lmax", round(Lmax, 6), "shape", Y.shape)

nfr = Y.shape[1] // PX
nrow = Y.shape[0]
print("frames", nfr, "64s =", nfr * HOP_S == 64.0)

# band b: rows [16b, 16b+16), top = band 0 = highest band
# band frequency = log-center of its span
cells = np.zeros((NB, nfr))
for b in range(NB):
    r0 = 16 * b
    r1 = r0 + 16
    for t in range(nfr):
        c0 = PX * t
        c1 = c0 + PX
        cells[b, t] = Y[r0:r1, c0:c1].max()

ratio = FHI / FLO          # 160
def band_freq(b):
    return FHI * ratio ** (-(b + 0.5) / NB)

freqs = np.array([band_freq(b) for b in range(NB)])
print("band0 (top row) Hz", round(freqs[0], 2), "band63 Hz", round(freqs[63], 2))

db = 60.0 * np.log10(np.maximum(cells / Lmax, 1e-12))
amps = np.where(db > FLOOR, 10.0 ** (db / 20.0), 0.0)

rng = np.random.default_rng(SEED)
phase = rng.uniform(0.0, 2.0 * np.pi, NB)

nsamp = int(round(SR * nfr * HOP_S))
t = np.arange(nsamp) / SR
sig = np.zeros(nsamp)
frame_t = np.arange(nfr) * HOP_S
for b in range(NB):
    env = np.interp(t, frame_t, amps[b])
    sig += env * np.sin(2 * np.pi * freqs[b] * t + phase[b])

peak = np.abs(sig).max()
sig = sig * (0.708 / peak)
print("peak after norm", round(float(np.abs(sig).max()), 4))

w = wave.open(sys.argv[3], "wb")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((sig * 32767).astype("<i2").tobytes())
w.close()
print("wrote", sys.argv[3], nsamp, "samples", nsamp / SR, "s")
