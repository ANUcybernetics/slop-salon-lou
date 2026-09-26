#!/usr/bin/env python3
"""The occupancy piece: one band, two exposures.
Top: the whole-record fine spectrum — the time exposure that counted teeth.
Bottom: the fine spectrogram — the motion: flicker, no walker, no lattice.
Usage: occupancy.py <wav> <out.png>"""
import numpy as np
import wave
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

wav = sys.argv[1] if len(sys.argv) > 1 else "assets/472_32.wav"
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/occupancy.png"
w = wave.open(wav)
sr = w.getframerate()
d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
L = d[:, 0] / 32768.0
print("sr", sr, "dur", round(len(L) / sr, 2), "s")

BG, BLUE, TXT, GRID = "#0a0e14", "#8ecae6", "#8a93a6", "#39435a"
LO, HI = 73.5, 76.5

# --- top: whole-record fine spectrum (the time exposure) ---
n = len(L)
seg = L.copy()
seg -= seg.mean()
NP = 1 << 23
fr = np.fft.rfftfreq(NP, 1 / sr)
X = np.abs(np.fft.rfft(seg * np.hanning(n), NP)) ** 2
Xdb = 10 * np.log10(X / NP)
b = (fr >= LO) & (fr <= HI)
fb, Xb = fr[b], Xdb[b]
Xb -= Xb.max()

# --- bottom: fine spectrogram (the motion) ---
N, NP2 = 80000, 1 << 18  # 2.5 s window, 0.122 Hz bins
fr2 = np.fft.rfftfreq(NP2, 1 / sr)
b2 = (fr2 >= LO) & (fr2 <= HI)
fb2 = fr2[b2]
ts, cols = [], []
for s in range(0, int(152 * sr) - N, 40000):  # hop 1.25 s
    s2 = L[s:s + N].copy()
    s2 -= s2.mean()
    cols.append(10 * np.log10(np.abs(np.fft.rfft(s2 * np.hanning(N), NP2)) ** 2 / N)[b2])
    ts.append((s + N / 2) / sr)
M = np.array(cols).T
M -= M.max()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(22, 12), dpi=100,
                               gridspec_kw={"height_ratios": [1, 1.1]})
fig.patch.set_facecolor(BG)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(colors=TXT, labelsize=13)
    ax.grid(True, color=GRID, lw=0.5, alpha=0.5)

ax1.plot(fb, Xb, color=BLUE, lw=0.7)
ax1.set_xlim(LO, HI)
ax1.set_ylim(-42, 3)
ax1.set_ylabel("dB", color=TXT, fontsize=15)
ax1.text(0.008, 0.86, "still — one record, 190 s: the teeth",
         transform=ax1.transAxes, color=TXT, fontsize=16, family="monospace")

im = ax2.pcolormesh(ts, fb2, M, cmap="inferno",
                    vmin=M.max() - 50, vmax=M.max(), shading="auto")
ax2.set_xlim(0, 152)
ax2.set_ylabel("Hz", color=TXT, fontsize=15)
ax2.set_xlabel("s", color=TXT, fontsize=15)
ax2.text(0.008, 0.86, "moving — 2.5 s windows, 1.25 s hop: the crowd",
         transform=ax2.transAxes, color="#d8dbe2", fontsize=16, family="monospace")
cb = fig.colorbar(im, ax=ax2, pad=0.01)
cb.ax.tick_params(colors=TXT, labelsize=11)
for t in cb.ax.get_yticklabels():
    t.set_color(TXT)

fig.tight_layout()
fig.savefig(OUT, facecolor=BG)
print("wrote", OUT)
