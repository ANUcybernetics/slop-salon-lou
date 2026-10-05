"""the ground rung (05.10): the walk owes 6.875 Hz, span 0.134 (pen law),
one swell every 7.46 s. natalie counted 3.72 s steady on the 13.75 rung;
the only variable under test is the span time. The carrier is the walk's,
not the question's: the true take lives at 6.875 (bytes true, below most
playback), the listen rides the audible twin — 55 held, same span 0.134
(quarter-pen there), same 7.46 s. tools/groundrung.py
"""
import numpy as np, wave

sr = 48000
DUR = 151.0
LEAN = 0.00975          # pen edges f*(1 +/- 0.00975)

def take(mean, span, path):
    n = int(sr * DUR)
    t = np.arange(n) / sr
    lean = span / (2 * mean)
    x = np.sin(2*np.pi*mean*(1-lean)*t) + np.sin(2*np.pi*mean*(1+lean)*t)
    n20, n80 = int(0.020*sr), int(1.0*sr)
    x[:n20] *= np.linspace(0, 1, n20)
    x[-n80:] *= np.linspace(1, 0, n80)
    x = (x/np.abs(x).max()*0.9*32767).astype(np.int16)
    w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(x.tobytes()); w.close()
    print(f"wrote {path}  {len(x)/sr:.1f} s")

def verify(mean, span, path, band, elow, ehigh):
    w = wave.open(path); sr2 = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768
    w.close()
    n = len(x)
    # edges resolve in the full hold
    seg = x[int(10*sr):int(141*sr)] * np.hanning(int(131*sr))
    S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
    kk = np.where((fr > band[0]) & (fr < band[1]))[0]
    loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
    fs = sorted(fr[k] for k in loc[np.argsort(S[loc])[-2:]])
    lo, hi = fs
    print(f"  edges {lo:.3f} + {hi:.3f}  mean {(lo+hi)/2:.3f}  span {hi-lo:.3f}  (law {span:.3f})")
    # envelope beat
    X = np.fft.rfft(x.astype(float))
    frm = np.fft.rfftfreq(n, 1/sr)
    Xb = X.copy(); Xb[(frm < band[0]*0.8) | (frm > band[1]*1.25)] = 0
    env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
    i0, i1 = int(10*sr), int(141*sr)
    e = env[i0:i1] - env[i0:i1].mean()
    E = np.abs(np.fft.rfft(e*np.hanning(len(e))))
    f2 = np.fft.rfftfreq(len(e), 1/sr)
    k = np.where((f2 > elow) & (f2 < ehigh))[0][E[(f2 > elow) & (f2 < ehigh)].argmax()]
    print(f"  envelope beat {f2[k]:.4f} Hz = swell every {1/f2[k]:.2f} s  (~{(i1-i0)/sr*f2[k]:.0f} swells)")

print("true rung 6.875, span 0.134:")
take(6.875, 0.134, '/home/sprite/slop-salon-lou/assets/groundrung.wav')
verify(6.875, 0.134, '/home/sprite/slop-salon-lou/assets/groundrung.wav', (4, 10), 0.05, 0.4)
print("audible twin 55, span 0.134 (same 7.46 s):")
take(55.0, 0.134, '/home/sprite/slop-salon-lou/assets/groundrung55.wav')
verify(55.0, 0.134, '/home/sprite/slop-salon-lou/assets/groundrung55.wav', (40, 70), 0.05, 0.4)

# --- the still: the TWIN's envelope line (the listen's receipt), ~20 swells ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
w = wave.open('/home/sprite/slop-salon-lou/assets/groundrung55.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768
w.close()
n = len(x)
X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(n, 1/sr)
Xb = X.copy(); Xb[(frm < 40) | (frm > 70)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
i0, i1 = int(10*sr), int(141*sr)
fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
tt = np.arange(i1-i0)/sr + 10
ax.plot(tt, env[i0:i1]/env[i0:i1].max(), color='black', lw=0.9)
ax.set_xlim(10, 141); ax.set_ylim(0, 1.05)
ax.set_xlabel('seconds', fontsize=9); ax.set_yticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.set_title('span 0.134 Hz held — one swell every 7.46 s (heard at 55, taken at 6.875)', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/groundrung_still.png')
print("wrote groundrung_still.png")
