#!/usr/bin/env python3
"""The tilt's scope: is the -2.7 dB R/L tilt a property of BANDS or of the
112 voice? Same in-band rms L/R machinery as clock.py (tanh bandpass,
5 s nonoverlap), three measurements:
  1. the 100 band, t 163-186 (tail, 3 s trimmed from its 160-189 span)
  2. null control: the 100 band where it is SILENT (t 20-50) - the
     pipeline must read ~1.00 on silence
  3. cross-checks: 112 (8-137) and 74.7 (8-137), same code path, must
     reproduce 0.737 / 1.039
Usage: tiltscope.py <wav> <out.png>"""
import numpy as np, wave, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav); sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1,2).astype(np.float64)/32768.0
Lc, Rc = raw[:,0], raw[:,1]

def band_env(y, lo, hi, edge=0.8):
    n = len(y); X = np.fft.fft(y)
    f = np.fft.fftfreq(n, 1/sr)
    up = 0.5*(1+np.tanh((f-lo)/edge))*0.5*(1-np.tanh((f-hi)/edge))
    return np.abs(np.fft.ifft(X*up*(f>0)))

def rl_trace(yL, yR, t0, t1, seg_s=5.0):
    eL = band_env(yL[int(t0*sr):int(t1*sr)], lo, hi)
    eR = band_env(yR[int(t0*sr):int(t1*sr)], lo, hi)
    seg = int(seg_s*sr)
    pts = []
    for i in range(0, min(len(eL), len(eR))-seg+1, seg):
        a = np.sqrt(np.mean(eL[i:i+seg]**2)); b = np.sqrt(np.mean(eR[i:i+seg]**2))
        pts.append((t0+i/sr+seg_s/2, 20*np.log10(b/a)))
    a = np.sqrt(np.mean(eL**2)); b = np.sqrt(np.mean(eR**2))
    return np.array(pts), b/a

results = {}
fig, ax = plt.subplots(figsize=(14, 5), dpi=110)
BG, BLUE, WARM, GREEN, TXT, GRID = "#0a0e14", "#8ecae6", "#f2a65a", "#9bd4a0", "#8a93a6", "#39435a"
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

specs = [
    ("112 band",  109.0, 115.0, 8,   137, WARM),
    ("74.7 band", 71.7,  77.7,  8,   137, BLUE),
    ("100 band (tail)", 97.0, 103.0, 160, 189, GREEN),
]
for name, lo, hi, T0, T1, col in specs:
    t0, t1 = T0+3, T1-3
    pts, whole = rl_trace(Lc, Rc, t0, t1)
    results[name] = (pts, whole, col)
    ax.plot(pts[:,0], pts[:,1], "-o", color=col, ms=4, lw=1.2, label=name)
    ax.axhline(20*np.log10(whole), color=col, lw=0.8, ls="--", alpha=0.5)
    print(f"{name:18s} t {t0:5.1f}-{t1:5.1f}: whole R/L {whole:.3f} ({20*np.log10(whole):+.1f} dB), "
          f"segments {pts[:,1].min():+.1f}..{pts[:,1].max():+.1f} dB")

# null control: the 100 band where it is silent (wakes at 157)
lo, hi = 97.0, 103.0
pts_n, whole_n = rl_trace(Lc, Rc, 20, 50)
results["100 silent"] = (pts_n, whole_n, GRID)
ax.plot(pts_n[:,0], pts_n[:,1], "-o", color=GRID, ms=4, lw=1.0, label="100 band, silent stretch (null)")
print(f"{'100 silent':18s} t  23.0- 47.0: whole R/L {whole_n:.3f} ({20*np.log10(whole_n):+.1f} dB), "
      f"segments {pts_n[:,1].min():+.1f}..{pts_n[:,1].max():+.1f} dB")

ax.axhline(0, color=TXT, lw=0.8, ls=":")
ax.set_xlabel("time (s)", color=TXT); ax.set_ylabel("R/L in-band rms (dB)", color=TXT)
ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=TXT, loc="upper right")
for s in ax.spines.values(): s.set_color(GRID)
ax.tick_params(colors=TXT, labelsize=9)
ax.grid(color=GRID, lw=0.4, alpha=0.4)
ax.set_title("the tilt is 112's signature — R/L per 5 s: 112 −2.7 dB, 74.7 +0.3, "
             "100 −0.6 (floor), silent null −0.2", color=TXT, fontsize=11, loc="left", pad=12)
fig.tight_layout(); fig.savefig(out, facecolor=BG)
print(f"{out} written")
