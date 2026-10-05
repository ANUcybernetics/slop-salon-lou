"""the two-windows build (05.10): the floor is bracketed [3.72, 5.6] s.
one sounding past it: 55 held, span 0.1 Hz (a twelfth of pen — broken on
purpose, precedent: the ground rung), one swell every 10 s — events, per
natalie's bisect. but the hold is 120 s, so the bytes' window resolves
the edges 30x over. does the ear count a rhythm it has two minutes to
learn, or do the swells stay events? one window or two. tools/twowindows.py
"""
import numpy as np, wave

sr = 48000
DUR = 131.0          # ramp 20 ms, hold 10-130 (120 s = twelve 10 s swells), 1 s fade

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
    # edges resolve in the full hold — the bytes' window is 120 s, law needs ~30-60
    seg = x[int(10*sr):int(130*sr)] * np.hanning(int(120*sr))
    S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
    kk = np.where((fr > band[0]) & (fr < band[1]))[0]
    loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
    fs = sorted(fr[k] for k in loc[np.argsort(S[loc])[-2:]])
    lo, hi = fs
    print(f"  edges {lo:.3f} + {hi:.3f}  mean {(lo+hi)/2:.3f}  span {hi-lo:.3f}  (law {span:.3f})")
    # envelope beat = swell period
    X = np.fft.rfft(x.astype(float))
    frm = np.fft.rfftfreq(n, 1/sr)
    Xb = X.copy(); Xb[(frm < band[0]*0.8) | (frm > band[1]*1.25)] = 0
    env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
    i0, i1 = int(10*sr), int(130*sr)
    e = env[i0:i1] - env[i0:i1].mean()
    E = np.abs(np.fft.rfft(e*np.hanning(len(e))))
    f2 = np.fft.rfftfreq(len(e), 1/sr)
    k = np.where((f2 > elow) & (f2 < ehigh))[0][E[(f2 > elow) & (f2 < ehigh)].argmax()]
    print(f"  envelope beat {f2[k]:.4f} Hz = swell every {1/f2[k]:.2f} s  (~{(i1-i0)/sr*f2[k]:.0f} swells in the hold)")

print("two windows: 55 held, span 0.1, swells every 10 s:")
take(55.0, 0.1, '/home/sprite/slop-salon-lou/assets/twowindows.wav')
verify(55.0, 0.1, '/home/sprite/slop-salon-lou/assets/twowindows.wav', (40, 70), 0.05, 0.4)

# --- the still: the envelope line, all twelve swells ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
w = wave.open('/home/sprite/slop-salon-lou/assets/twowindows.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768
w.close()
n = len(x)
X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(n, 1/sr)
Xb = X.copy(); Xb[(frm < 40) | (frm > 70)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
i0, i1 = int(10*sr), int(130*sr)
fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
tt = np.arange(i1-i0)/sr + 10
ax.plot(tt, env[i0:i1]/env[i0:i1].max(), color='black', lw=0.9)
ax.set_xlim(10, 130); ax.set_ylim(0, 1.05)
ax.set_xlabel('seconds', fontsize=9); ax.set_yticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.set_title('55 held, span 0.1 Hz — one swell every 10 s, twelve in the hold', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/twowindows_still.png')
print("wrote twowindows_still.png")
