#!/usr/bin/env python3
"""The census probe: coherence traces of the two tail voices on 472.
Long window (N = 131072 = 4.096 s at 32 kHz), same math as lrprobe_long.
Top: 100 Hz — seals (one voice, two ears). Bottom: 232 Hz — never locks.
Usage: census.py <wav> <out.png>"""
import numpy as np
import wave
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

wav = sys.argv[1]
w = wave.open(wav)
sr = w.getframerate()
data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
L = data[:, 0] / 32768.0
R = se = data[:, 1] / 32768.0
print("sr", sr, "dur", round(len(L) / sr, 2), "s")

N = 131072
NP = 131072
win = np.hanning(N)
freqs = np.fft.rfftfreq(NP, 1 / sr)

BANDS = [("100", 97.0, 103.0), ("232", 226.0, 238.0)]
T0, T1 = 155.0, 190.0
STRIDE = 8000  # 0.25 s between frame starts
FLOOR = -75.0  # dBFS: below this the voice is dead, frame dropped

def coh_trace(lo, hi):
    band = (freqs >= lo) & (freqs <= hi)
    ts, cs = [], []
    for s in range(int(T0 * sr), int(T1 * sr) - N, STRIDE):
        XL = np.fft.rfft(L[s:s + N] * win, NP)
        XR = np.fft.rfft(R[s:s + N] * win, NP)
        Sxy = np.abs(np.sum(XL[band] * np.conj(XR[band]))) ** 2
        Sxx = np.sum(np.abs(XL[band]) ** 2)
        Syy = np.sum(np.abs(XR[band]) ** 2)
        ts.append((s + N / 2) / sr)
        cs.append(Sxy / (Sxx * Syy))
    return ts, cs

traces = {}
for name, lo, hi in BANDS:
    traces[name] = coh_trace(lo, hi)
    ts, cs = traces[name]
    print(name, "frames", len(ts))
    for t, c in zip(ts, cs):
        print(f"  {t:7.2f} {c:6.3f}")

if len(sys.argv) > 2:
    OUT = sys.argv[2]
    BG, BLUE, WARM, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#8a93a6", "#39435a"
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(20, 11), dpi=100)
    fig.patch.set_facecolor(BG)
    for ax, (name, lo, hi), col in zip(axes, BANDS, [BLUE, WARM]):
        ts, cs = traces[name]
        ax.set_facecolor(BG)
        ax.plot(ts, cs, color=col, lw=5)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_ylim(0, 1.05)
        ax.tick_params(colors=TXT, labelsize=13)
        ax.grid(True, color=GRID, lw=0.5, alpha=0.6)
        ax.text(0.008, 0.84, name + " Hz", transform=ax.transAxes,
                color=TXT, fontsize=17, family="monospace")
    axes[1].set_xlabel("s", color=TXT, fontsize=15)
    fig.tight_layout()
    fig.savefig(OUT, facecolor=BG)
    print("wrote", OUT)