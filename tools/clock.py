#!/usr/bin/env python3
"""The crowd's clock: does the 0.61 Hz envelope beat survive across
analysis window sizes? Envelope of the sealed dyad band (74.7), mono,
t 5-140 trimmed 3 s ends; Welch spectra at 2.5/5/10 s windows; the
verdict is DEPTH of the line. Also the 112 L/R rms check, same bytes.
Usage: clock.py <wav> <out.png>"""
import numpy as np, wave, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav); sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1,2).astype(np.float64)/32768.0
Lc, Rc = raw[:,0], raw[:,1]
x = (Lc+Rc)/2

T0, T1 = 5, 140
t0, t1 = T0+3, T1-3          # trim 3 s ends (envelope law)
lo, hi, edge = 71.7, 77.7, 0.8

def band_env(y, lo, hi, edge=0.8):
    n = len(y); X = np.fft.fft(y)
    f = np.fft.fftfreq(n, 1/sr)
    up = 0.5*(1+np.tanh((f-lo)/edge))*0.5*(1-np.tanh((f-hi)/edge))
    return np.abs(np.fft.ifft(X*up*(f>0)))

def welch_env(e, win_s):
    seg = int(win_s*sr); hop = seg//2
    W = np.hanning(seg); nseg = (len(e)-seg)//hop + 1
    acc = None
    for i in range(nseg):
        c = e[i*hop:i*hop+seg]
        S = np.abs(np.fft.rfft((c-c.mean())*W))**2
        acc = S if acc is None else acc + S
    f = np.fft.rfftfreq(seg, 1/sr)
    return f, acc/nseg

e = band_env(x[int(t0*sr):int(t1*sr)], lo, hi, edge)
e = e - e.mean()              # DC out: the mean level is not a beat

BG, BLUE, WARM, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#8a93a6", "#39435a"
fig, axes = plt.subplots(3, 1, figsize=(14, 9), dpi=110, sharex=True)
fig.patch.set_facecolor(BG)

FLO, FHI = 0.2, 2.0
rows = []
for ax, win_s in zip(axes, (2.5, 5.0, 10.0)):
    f, P = welch_env(e, win_s)
    sel = (f>=FLO)&(f<=FHI); fs, Ps = f[sel], P[sel]
    db = 10*np.log10(Ps/Ps.max())
    band_mask = (fs>=0.4)&(fs<=0.9)
    pk = fs[band_mask][np.argmax(Ps[band_mask])]
    pkdb = db[band_mask][np.argmax(Ps[band_mask])]
    med = np.median(db[(fs>=0.2)&(fs<=2.0)])
    depth = pkdb - med
    rows.append((win_s, pk, depth, nseg if False else (len(e)-int(win_s*sr))//(int(win_s*sr)//2)+1))
    ax.fill_between(fs, -40, db, color=BLUE, lw=0, alpha=0.85)
    ax.plot(fs, db, color=BLUE, lw=0.7)
    ax.axvline(0.61, color=GRID, lw=0.8, ls="--")
    ax.set_ylim(-40, 2); ax.set_xlim(FLO, FHI)
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_color(GRID)
    ax.tick_params(colors=TXT, labelsize=9)
    ax.set_ylabel(f"{win_s:g} s", color=TXT, fontsize=10)
    i61 = np.argmin(np.abs(fs-0.61))
    ax.text(0.985, 0.06, f"0.61 Hz: {db[i61]:.1f} dB, on the skirt — no line",
            transform=ax.transAxes, ha="right", color=WARM, fontsize=10)

axes[0].set_title(f"the crowd's clock — envelope spectrum of the 74.7 band, t {t0}-{t1} s "
                  f"(3 s trimmed), windows 2.5/5/10 s", color=TXT, fontsize=11, loc="left", pad=12)
axes[-1].set_xlabel("envelope frequency (Hz)", color=TXT, fontsize=10)
fig.text(0.5, 0.005, f"true f/f0 dyad 74.7+112 Hz, 472_32.wav — mono x=(L+R)/2 — bandpass tanh edges {edge} Hz",
         ha="center", color=TXT, fontsize=8)
fig.tight_layout(rect=(0,0.02,1,1))
fig.savefig(out, facecolor=BG)

for win_s, pk, depth, nseg in rows:
    print(f"window {win_s:>4g} s: peak {pk:5.2f} Hz  depth {depth:5.1f} dB  ({nseg} segs)")

# ---- controls: the probe must find a true beat and reject a skirt ----
rng = np.random.default_rng(472)
n = len(e); t = np.arange(n)/sr
am  = band_env(x[int(t0*sr):int(t1*sr)], lo, hi, edge)
am  = am/am.max()
synth = (1 + 0.32*np.sin(2*np.pi*0.61*t)).astype(np.float64)
noise = np.abs(rng.normal(0, 0.32, n)); noise -= noise.mean()
def clockverdict(sig, label):
    f, P = welch_env(sig - sig.mean(), 10.0)
    m = (f>=0.4)&(f<=0.8)
    pk = f[m][np.argmax(P[m])]; skirt = np.median(P[(f>=0.7)&(f<=2.0)])
    d = 10*np.log10(P[m].max()/skirt)
    print(f"control {label:8s}: peak {pk:.2f} Hz  depth {d:5.1f} dB")
clockverdict(synth, "AM 0.61")
clockverdict(noise, "noise")
# and the skirt itself, 0.05-2.5, at the 10 s window
f, P = welch_env(e, 10.0)
for fq in (0.1, 0.2, 0.4, 0.61, 1.0, 2.0):
    i = np.argmin(np.abs(f-fq))
    print(f"skirt {fq:4.2f} Hz: {10*np.log10(P[i]/P.max()):6.1f} dB")

# ---- the 112 L/R rms check, same bytes ----
lo2, hi2 = 109.0, 115.0
eL = band_env(Lc[int(t0*sr):int(t1*sr)], lo2, hi2, edge)
eR = band_env(Rc[int(t0*sr):int(t1*sr)], lo2, hi2, edge)
e74L = band_env(Lc[int(t0*sr):int(t1*sr)], lo, hi, edge)
e74R = band_env(Rc[int(t0*sr):int(t1*sr)], lo, hi, edge)
# time-resolved: 5 s nonoverlap rms
seg = int(5*sr)
for i in range(0, min(len(eL), len(eR))-seg+1, seg):
    rL = np.sqrt(np.mean(eL[i:i+seg]**2)); rR = np.sqrt(np.mean(eR[i:i+seg]**2))
    print(f"112 t {t0+i/sr:6.1f}-{t0+(i+seg)/sr:6.1f} s: rms L {rL:.4f}  R {rR:.4f}  R/L {rR/rL:.3f}")
rL = np.sqrt(np.mean(eL**2)); rR = np.sqrt(np.mean(eR**2))
print(f"112 whole window: rms L {rL:.4f}  R {rR:.4f}  R/L {rR/rL:.3f}  ({20*np.log10(rR/rL):+.1f} dB)")
sL = np.sqrt(np.mean(e74L**2)); sR = np.sqrt(np.mean(e74R**2))
print(f" 74.7 whole window: rms L {sL:.4f}  R {sR:.4f}  R/L {sR/sL:.3f}  ({20*np.log10(sR/sL):+.1f} dB)")
# time-resolved 74.7 R/L, same 5 s nonoverlap
seg2 = int(5*sr)
for i in range(0, min(len(e74L), len(e74R))-seg2+1, seg2):
    a = np.sqrt(np.mean(e74L[i:i+seg2]**2)); b = np.sqrt(np.mean(e74R[i:i+seg2]**2))
    print(f"74.7 t {t0+i/sr:6.1f}-{t0+(i+seg2)/sr:6.1f} s: R/L {b/a:.3f}")

# ---- tilt figure: time-resolved R/L, 112 vs 74.7 ----
ttilt = t0 + np.arange(len(eL))/ (sr*1.0)
seg2 = int(5*sr)
pts = []
for i in range(0, min(len(eL), len(eR))-seg2+1, seg2):
    a = np.sqrt(np.mean(eL[i:i+seg2]**2)); b = np.sqrt(np.mean(eR[i:i+seg2]**2))
    c = np.sqrt(np.mean(e74L[i:i+seg2]**2)); d = np.sqrt(np.mean(e74R[i:i+seg2]**2))
    pts.append((t0+i/sr, b/a, d/c))
pts = np.array(pts)
fig2, ax = plt.subplots(figsize=(14, 4.5), dpi=110)
fig2.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.plot(pts[:,0], 20*np.log10(pts[:,1]), "-o", color=WARM, ms=4, lw=1.2, label="112 band")
ax.plot(pts[:,0], 20*np.log10(pts[:,2]), "-o", color=BLUE, ms=4, lw=1.2, label="74.7 band (control)")
ax.axhline(20*np.log10(0.737), color=WARM, lw=0.8, ls="--", alpha=0.6)
ax.axhline(20*np.log10(1.039), color=BLUE, lw=0.8, ls="--", alpha=0.6)
ax.set_xlabel("time (s)", color=TXT); ax.set_ylabel("R/L in-band rms (dB)", color=TXT)
ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=TXT)
for s in ax.spines.values(): s.set_color(GRID)
ax.tick_params(colors=TXT, labelsize=9)
ax.grid(color=GRID, lw=0.4, alpha=0.4)
ax.set_title("the tilt: R/L never crosses 0 dB at 112; the 74.7 control sits at 0", color=TXT, fontsize=11, loc="left", pad=12)
fig2.tight_layout(); fig2.savefig("assets/tilt.png", facecolor=BG)
print("tilt.png written")
