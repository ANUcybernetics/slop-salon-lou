"""the due take (04.10): 13.75 held, span 0.268 Hz — the pen walk one octave
below the counted rung. At 1.86 s natalie counted twelve swells, steady; the
question walks down: does the ear still count at 3.73 s, or do the swells come
apart into events? ~40 swells in 2.5 minutes of material for the ear to live in.
"""
import numpy as np, wave

sr = 48000
MEAN = 13.75
LEAN = 0.00975          # the pen's own tenth: edges f*(1 +/- 0.00975)
SPAN = 2 * MEAN * LEAN  # 0.2681 Hz -> one swell every 3.728 s
DUR = 151.0
n = int(sr * DUR)
t = np.arange(n) / sr
x = np.sin(2 * np.pi * MEAN * (1 - LEAN) * t) + np.sin(2 * np.pi * MEAN * (1 + LEAN) * t)

n20, n80 = int(0.020 * sr), int(1.0 * sr)
x[:n20] *= np.linspace(0, 1, n20)
x[-n80:] *= np.linspace(1, 0, n80)
x = (x / np.abs(x).max() * 0.9 * 32767).astype(np.int16)

w = wave.open('/home/sprite/slop-salon-lou/assets/floorrung.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(x.tobytes()); w.close()
print(f"wrote floorrung.wav  {len(x)/sr:.1f} s  peak {np.abs(x).max()}")

# --- verify: edges resolve in the full hold ---
seg = x[int(10*sr):int(140*sr)].astype(float) * np.hanning(int(130*sr))
S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
kk = np.where((fr > 10) & (fr < 18))[0]
loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
top = loc[np.argsort(S[loc])[-2:]]
fs = sorted(fr[k] for k in top)
lo, hi = fs
print(f"edges read back: {lo:.3f} + {hi:.3f}  mean {(lo+hi)/2:.3f}  "
      f"span {hi-lo:.3f}  (law {SPAN:.3f})")

# --- verify: the envelope beats at 0.268 Hz ---
X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(n, 1/sr)
Xb = X.copy(); Xb[(frm < 8) | (frm > 22)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
i0, i1 = int(10*sr), int(140*sr)
e = env[i0:i1] - env[i0:i1].mean()
E = np.abs(np.fft.rfft(e * np.hanning(len(e))))
f2 = np.fft.rfftfreq(len(e), 1/sr)
band = (f2 > 0.1) & (f2 < 0.8)
peak = f2[band][np.argmax(E[band])]
print(f"envelope beat: {peak:.3f} Hz  = one swell every {1/peak:.3f} s  "
      f"(~{(i1-i0)/sr*peak:.0f} swells in the hold)")

# --- the still: the envelope itself, ~40 swells, one line ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
tt = np.arange(i1 - i0) / sr + 10
ax.plot(tt, env[i0:i1] / env[i0:i1].max(), color='black', lw=0.9)
ax.set_xlim(10, 140); ax.set_ylim(0, 1.05)
ax.set_xlabel('seconds', fontsize=9)
ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('13.75 Hz, span 0.268 — one swell every 3.73 s', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/floorrung_still.png')
print("wrote floorrung_still.png")
