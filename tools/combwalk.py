#!/usr/bin/env python3
"""The comb-walk probe: 5 s fine-frequency traces of a band, L and R.
N = 160000 (5 s at 32 kHz), NP = 524288 (0.061 Hz bins) so the ~0.2 Hz
comb teeth resolve. A walking trace = drift; a trace hopping between
fixed lines = a static comb with the peak picker jumping carrier/tooth.
Usage: combwalk.py <wav> <out.png> — fixed bands: dyad 74.7, 112, 179."""
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

N = 160000
NP = 524288
win = np.hanning(N)
freqs = np.fft.rfftfreq(NP, 1 / sr)

def peak(x, band, fb):
    X = np.abs(np.fft.rfft(x * win, NP)) ** 2
    Xb = X[band]
    k = Xb.argmax()
    if k == 0 or k == len(Xb) - 1:
        d = 0.0
    else:
        a, b, c = Xb[k - 1:k + 2]
        d = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) != 0 else 0.0
    return fb[k] + d * (freqs[1] - freqs[0]), 10 * np.log10(Xb[k] / NP)

BANDS = [("74.7", 73.0, 77.0), ("112", 110.0, 114.0), ("179", 176.0, 182.0)]
T0, T1 = 5.0, 150.0
OUT = sys.argv[2] if len(sys.argv) > 2 else None
FLOOR = -5.0  # dBFS: below this the voice is dead, frame dropped for that ear

def frames(lo, hi):
    band = (freqs >= lo - 2) & (freqs <= hi + 2)  # margin bins so the
    fb = freqs[band]  # parabola never needs a bin outside the slice
    fb = freqs[band]
    ts, FL, FR = [], [], []
    for s in range(int(T0 * sr), int(T1 * sr), 80000):  # hop 2.5 s
        if s + N > len(L):
            break
        fL, dL = peak(L[s:s + N], band, fb)
        fR, dR = peak(R[s:s + N], band, fb)
        ts.append((s + N / 2) / sr)
        FL.append(fL if dL > FLOOR else None)
        FR.append(fR if dR > FLOOR else None)
    return ts, FL, FR

traces = {}
for name, lo, hi in BANDS:
    traces[name] = frames(lo, hi)
    ts, FL, FR = traces[name]
    print(name, "frames", len(ts))
    for t, a, b in zip(ts, FL, FR):
        print(f"  {t:6.2f} {a!r:>8} {b!r:>8}")

# hop-vs-drift read: a static comb's trace values cluster on tooth lines
# (histogram spikes); drift spreads continuously.
for name in BANDS:
    n = name[0]
    ts, FL, FR = traces[n]
    for ear, vals in (("L", FL), ("R", FR)):
        v = np.array([x for x in vals if x is not None])
        if len(v) < 5:
            continue
        h, edges = np.histogram(v, bins=36)
        top = np.argsort(h)[::-1][:4]
        spans = " ".join(f"{edges[i]:.2f}x{h[i]}" for i in sorted(top))
        print(f"HIST {n} {ear}: n={len(v)} spread={v.max()-v.min():.3f} "
              f"top-bins: {spans}")

if OUT:
    BG, BLUE, WARM, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#8a93a6", "#39435a"
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(20, 11), dpi=100)
    fig.patch.set_facecolor(BG)
    for ax, name in zip(axes, ["74.7", "179"]):
        ts, FL, FR = traces[name]
        ax.set_facecolor(BG)
        ax.plot(ts, [np.nan if v is None else v for v in FL], color=BLUE, lw=6)
        ax.plot(ts, [np.nan if v is None else v for v in FR], color=WARM, lw=2.4)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.tick_params(colors=TXT, labelsize=13)
        ax.grid(True, color=GRID, lw=0.5, alpha=0.6)
        ax.set_ylabel(name, color=TXT, fontsize=15)
        ax.text(0.008, 0.86, name + " Hz", transform=ax.transAxes,
                color=TXT, fontsize=17, family="monospace")
    axes[0].set_ylim(72, 78)
    axes[1].set_ylim(172, 187)
    axes[1].set_xlabel("s", color=TXT, fontsize=15)
    fig.tight_layout()
    fig.savefig(OUT, facecolor=BG)
    print("wrote", OUT)
