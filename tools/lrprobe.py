#!/usr/bin/env python3
"""Band L/R probe: is a band a tone or noise, on the bytes.
Per frame: parabolic-interp peak in [lo,hi] Hz per channel, level dBFS per
channel, magnitude-squared coherence L vs R in-band.
Tones: L/R agree sub-bin, coh -> 1. Noise: peaks wander, coh -> 0.
Usage: lrprobe.py <wav> <lo> <hi> [stride=4]   (stride 4 = 1 s steps)"""
import numpy as np
import wave
import sys

wav = sys.argv[1]
LO, HI = float(sys.argv[2]), float(sys.argv[3])
STRIDE = int(sys.argv[4]) if len(sys.argv) > 4 else 4
w = wave.open(wav)
sr = w.getframerate()
data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
L = data[:, 0] / 32768.0
R = data[:, 1] / 32768.0
print("sr", sr, "dur", round(len(L) / sr, 2), "s")

N = 32768
NP = 131072
win = np.hanning(N)
freqs = np.fft.rfftfreq(NP, 1 / sr)
band = (freqs >= LO) & (freqs <= HI)
fb = freqs[band]

def peak(x):
    X = np.abs(np.fft.rfft(x * win, NP)) ** 2
    Xb = X[band]
    k = Xb.argmax()
    a, b, c = Xb[max(k - 1, 0):k + 2]
    d = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) != 0 else 0.0
    return fb[k] + d * (freqs[1] - freqs[0]), 10 * np.log10(b / NP)

t0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
t1 = float(sys.argv[6]) if len(sys.argv) > 6 else len(L) / sr
print("   t   fL      fR     dHz   dBL    dBR   coh")
for i in range(int(t0 * 4), int(t1 * 4), STRIDE):
    s = i * sr // 4
    if s + N > len(L):
        break
    fL, dL = peak(L[s:s + N])
    fR, dR = peak(R[s:s + N])
    XL = np.fft.rfft(L[s:s + N] * win, NP)
    XR = np.fft.rfft(R[s:s + N] * win, NP)
    Sxy = np.abs(np.sum(XL[band] * np.conj(XR[band]))) ** 2
    Sxx = np.sum(np.abs(XL[band]) ** 2)
    Syy = np.sum(np.abs(XR[band]) ** 2)
    coh = Sxy / (Sxx * Syy)
    print(f"{i/4:6.2f} {fL:7.1f} {fR:7.1f} {abs(fL-fR):5.2f} {dL:6.1f} {dR:6.1f} {coh:6.3f}")
