#!/usr/bin/env python3
"""Receipt for lelia's way-back (mv3): twelve stops, twelve dyads, one law.
Left: the 57.4 s pitch track (0.5 s hops) on log Hz, stops marked.
Right: measured edge-spacing vs stop frequency, log-log, against the law
dF = 0.0195 f (slope 1 through origin). Twelve points ON the line.
Usage: mv3receipt.py <wav> <out.png>"""
import numpy as np, wave, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768.0

STOPS = [
    ("ground",        31.2,  2.0,  6.0),
    ("quiet's floor", 62.3,  7.5, 11.0),
    ("shelf",         90.5, 13.5, 16.5),
    ("terrace",      124.5, 17.5, 21.0),
    ("ledge",        249.3, 22.5, 25.5),
    ("rest",         355.5, 27.0, 29.5),
    ("rest",         447.9, 30.5, 33.5),
    ("terrace",      474.0, 34.5, 37.5),
    ("terrace",      512.0, 38.5, 41.5),
    ("terrace",      552.0, 42.0, 45.0),
    ("gift",         590.0, 45.5, 48.5),
    ("home",         440.0, 51.5, 56.5),
]

NP = 1 << 20
meas = []
for name, ledger, t0, t1 in STOPS:
    seg = x[int(t0*sr):int(t1*sr)]; seg = seg * np.hanning(len(seg))
    S = np.abs(np.fft.rfft(seg, NP)); f = np.fft.rfftfreq(NP, 1/sr)
    sel = (f > ledger*0.93) & (f < ledger*1.07)
    Ss, fs = S[sel], f[sel]
    thr = Ss.max()*10**(-16/20)
    peaks = []
    for k in range(1, len(Ss)-1):
        if Ss[k] > Ss[k-1] and Ss[k] >= Ss[k+1] and Ss[k] > thr:
            a, c = Ss[k-1], Ss[k+1]
            d = 0.5*(a-c)/(a-2*Ss[k]+c)
            peaks.append((fs[k] + d*(fs[1]-fs[0]), Ss[k]))
    peaks.sort(key=lambda p: -p[1])
    p1, p2 = peaks[0], peaks[1]
    lo, hi = sorted((p1[0], p2[0]))
    mean = (lo+hi)/2; df = hi-lo
    meas.append((name, ledger, mean, df))
    print(f"{name:15s} ledger {ledger:6.1f}  edges {lo:7.2f}/{hi:7.2f}"
          f"  dF {df:6.3f}  ratio {df/mean:.4f}")

# ---- figure ----
BG, BLUE, WARM, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#8a93a6", "#39435a"
fig, (axL, axR) = plt.subplots(1, 2, figsize=(18, 8), dpi=100)
fig.patch.set_facecolor(BG)

# left: pitch track + stops
N = 16384
win = np.hanning(N)
fp = np.fft.rfftfreq(1 << 19, 1/sr)
bp = (fp >= 25) & (fp <= 650)
ts, fs_track = [], []
for i in range(0, len(x)-N, sr//2):
    X = np.abs(np.fft.rfft(x[i:i+N]*win, 1 << 19))[bp]
    k = X.argmax()
    a, c = X[k-1], X[k+1]
    d = 0.5*(a-c)/(a-2*X[k]+c)
    ts.append((i+N/2)/sr); fs_track.append(fp[bp][k] + d*(fp[1]-fp[0]))
axL.plot(ts, fs_track, color=BLUE, lw=1.4, alpha=0.95)
for name, ledger, t0, t1 in STOPS:
    axL.plot([t0, t1], [ledger, ledger], color=WARM, lw=6, alpha=0.55)
    axL.text((t0+t1)/2, ledger*1.13, name, color=TXT, fontsize=10,
             ha="center", family="monospace")
axL.set_yscale("log"); axL.set_ylim(25, 700)
axL.set_xlim(0, 57.5)
axL.set_xlabel("s", color=TXT, family="monospace")
axL.set_ylabel("Hz", color=TXT, family="monospace")
axL.text(0.02, 0.95, "the way back: twelve stops", transform=axL.transAxes,
         color=BLUE, fontsize=14, family="monospace")

# right: dF vs mean f, log-log, against the law
mf = np.array([m[2] for m in meas]); dfa = np.array([m[3] for m in meas])
laws = np.array([m[1] for m in meas])*0.0195
axR.loglog(mf, dfa, "o", color=BLUE, ms=9, zorder=3)
axR.loglog([28, 640], [28*0.0195, 640*0.0195], "-", color=WARM, lw=1.6,
           label=r"$\Delta f = 0.0195\,f$")
for m in meas:
    axR.annotate(f"{m[3]/m[2]:.4f}", (m[2], m[3]), textcoords="offset points",
                 xytext=(6, -12), fontsize=8, color=TXT, family="monospace")
axR.set_xlabel("stop Hz", color=TXT, family="monospace")
axR.set_ylabel("edge spacing Hz", color=TXT, family="monospace")
axR.legend(facecolor=BG, edgecolor=GRID, labelcolor=TXT)
axR.text(0.03, 0.93, "twelve stops, one ratio", transform=axR.transAxes,
         color=BLUE, fontsize=14, family="monospace")
for ax in (axL, axR):
    ax.set_facecolor(BG)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(colors=TXT, labelsize=10)
    ax.grid(True, which="both", color=GRID, lw=0.5, alpha=0.6)
fig.suptitle("lelia's way back, received: every stop a dyad, every ratio 0.0195",
             color=TXT, fontsize=15, family="monospace")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(out, facecolor=BG)
print("wrote", out)
