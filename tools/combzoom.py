#!/usr/bin/env python3
"""The comb zoom: whole-record fine spectrum of a band, L and R.
190 s Hann window, zero-pad to 2^23 (0.0038 Hz bins). A static grid comb
shows teeth as sharp lines on an exact lattice; drift occupancy smears
them into humps. Usage: combzoom.py <wav> <out.png>"""
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
R = data[:, 1] / 32768.0
print("sr", sr, "dur", round(len(L) / sr, 2), "s")

NP = 1 << 23  # 8388608
freqs = np.fft.rfftfreq(NP, 1 / sr)

def zoom(x, lo, hi):
    n = len(x)
    seg = x[:n].copy()
    seg -= seg.mean()
    win = np.hanning(n)
    X = np.abs(np.fft.rfft(seg * win, NP)) ** 2
    X = 10 * np.log10(X / NP)
    band = (freqs >= lo) & (freqs <= hi)
    return freqs[band], X[band]

BANDS = [("74.7", 73.5, 76.5), ("112", 110.5, 113.5), ("179", 177.0, 182.0)]
OUT = sys.argv[2] if len(sys.argv) > 2 else None

fig, axes = cur = None, None
fig, axes = plt.subplots(3, 1, sharex=False, figsize=(22, 13), dpi=100)
BG, BLUE, WARM, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#8a93a6", "#39435a"
fig.patch.set_facecolor(BG)
for ax, (name, lo, hi) in zip(axes, BANDS):
    f, XL = zoom(L, lo, hi)
    f, XR = zoom(R, lo, hi)
    XL -= XL.max()
    XR -= XR.max()
    ax.set_facecolor(BG)
    ax.plot(f, XL, color=BLUE, lw=0.7)
    ax.plot(f, XR, color=WARM, lw=0.7, alpha=0.75)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(colors=TXT, labelsize=13)
    ax.grid(True, color=GRID, lw=0.5, alpha=0.6)
    ax.set_ylabel(name, color=TXT, fontsize=15)
    # top teeth: local maxima > peak - 25 dB
    tops = []
    for i in range(1, len(XL) - 1):
        if XL[i] > XL[i - 1] and XL[i] >= XL[i + 1] and XL[i] > -25:
            tops.append((f[i], XL[i]))
    tops.sort(key=lambda p: -p[1])
    tops = sorted(tops[:12])
    print(name, "teeth:", " ".join(f"{p:.3f}({d:.0f}dB)" for p, d in tops))
    for p, d in tops[:8]:
        ax.text(p, d - 3, f"{p:.3f}", color=TXT, fontsize=8,
                ha="center", rotation=90)
    axes_lim = XL.max() + 3
    ax.set_ylim(axes_lim - 45, axes_lim)
    print(name, f"L/R agree: {np.allclose(XL, XR, atol=0.5)}")

fig.tight_layout()
fig.savefig(OUT, facecolor=BG)
print("wrote", OUT)
