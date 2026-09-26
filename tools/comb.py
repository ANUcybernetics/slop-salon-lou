#!/usr/bin/env python3
"""The comb paper: five voices, spectrum + L/R envelope overlay.
Every voice is a comb over a skirt; the envelope says shared or split.
Usage: comb.py <wav> <out.png>"""
import numpy as np, wave, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav); sr = w.getframerate()
nch = w.getnchannels()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1,nch).astype(np.float64)/32768.0
Lc, Rc = raw[:,0], raw[:,1]
x = (Lc+Rc)/2

ROWS = [  # name, lo, hi, t0, t1, shared?
    ("74.7",  71.7, 77.7,  5, 140, True),
    ("112",   109, 115,   5, 140, True),
    ("100",   97, 103,  160, 189, True),
    ("179",   175.5, 182.5, 5, 140, False),
    ("232",   226, 238, 165, 188, False),
]
BG, BLUE, WARM, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#8a93a6", "#39435a"
fig, axes = plt.subplots(5, 2, figsize=(18, 14), dpi=100)
fig.patch.set_facecolor(BG)

def band_env(y, lo, hi, edge=0.8):
    n = len(y); X = np.fft.fft(y)
    f = np.fft.fftfreq(n, 1/sr)
    up = 0.5*(1+np.tanh((f-lo)/edge))*0.5*(1-np.tanh((f-hi)/edge))
    return np.abs(np.fft.ifft(X*up*(f>0)))

for axL, axR, (name, lo, hi, t0, t1, shared) in zip(axes[:,0], axes[:,1], ROWS):
    col = BLUE if shared else WARM
    seg = x[int(t0*sr):int(t1*sr)]
    W = np.hanning(len(seg))
    S = np.abs(np.fft.rfft(seg*W, 1<<22)); f = np.fft.rfftfreq(1<<22, 1/sr)
    sel = (f>=lo)&(f<=hi); fs, Ss = f[sel], S[sel]
    db = 20*np.log10(Ss/Ss.max())
    axL.fill_between(fs, -40, db, color=col, lw=0, alpha=0.85)
    axL.set_xlim(lo, hi); axL.set_ylim(-40, 2)
    axL.text(0.02, 0.76, f"{name} Hz - {('shared' if shared else 'split')}",
             transform=axL.transAxes, color=TXT, fontsize=14, family="monospace")
    eL = band_env(Lc[int(t0*sr):int(t1*sr)], lo, hi)
    eR = band_env(Rc[int(t0*sr):int(t1*sr)], lo, hi)
    tt = np.arange(len(eL))/sr + t0
    m = max(eL.max(), eR.max())
    axR.plot(tt, eL/m, color=BLUE, lw=1.0, alpha=0.95)
    axR.plot(tt, eR/m, color=WARM, lw=1.0, alpha=0.8)
    axR.set_xlim(t0, t1); axR.set_ylim(0, 1.15)
    for ax in (axL, axR):
        for sp in ax.spines.values(): sp.set_visible(False)
        ax.tick_params(colors=TXT, labelsize=10)
        ax.grid(True, color=GRID, lw=0.5, alpha=0.6)
    axL.set_yticks([-40, -20, 0])
fig.suptitle("every voice is a comb - teeth one-sided above the carrier; "
             "locked envelopes = shared, independent = split",
             color=TXT, fontsize=15, family="monospace")
fig.tight_layout(rect=[0, 0, 1, 0.965])
fig.savefig(out, facecolor=BG)
print("wrote", out)
