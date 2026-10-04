"""the rung below rhythm (04.10): 55 held, span 0.535 Hz — one swell every
1.869 s, ~32 in a minute. The listen named 1.07 rhythm (natalie counted ten
swells at 932 ms); the question now is whether the count survives the octave
below. One minute of material for the ear to live in.
"""
import numpy as np, wave

sr = 48000
MEAN = 55.0
SPAN = 0.535            # half the boundary span (1.0725 = PEN*55)
DUR = 60.0
n = int(sr * DUR)
t = np.arange(n) / sr
x = np.sin(2 * np.pi * (MEAN - SPAN / 2) * t) + np.sin(2 * np.pi * (MEAN + SPAN / 2) * t)

n20, n80 = int(0.020 * sr), int(0.080 * sr)
x[:n20] *= np.linspace(0, 1, n20)
x[-n80:] *= np.linspace(1, 0, n80)
x = (x / np.abs(x).max() * 0.9 * 32767).astype(np.int16)

w = wave.open('/home/sprite/slop-salon-lou/assets/belowrung.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(x.tobytes()); w.close()
print(f"wrote belowrung.wav  {len(x)/sr:.1f} s  peak {np.abs(x).max()}")

# --- verify: edges resolve in the full hold ---
seg = x[int(4*sr):int(56*sr)].astype(float) * np.hanning(int(52*sr))
S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
kk = np.where((fr > 45) & (fr < 65))[0]
loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
top = loc[np.argsort(S[loc])[-2:]]
fs = sorted(fr[k] for k in top)
lo, hi = fs
print(f"edges read back: {lo:.3f} + {hi:.3f}  mean {(lo+hi)/2:.3f}  "
      f"span {hi-lo:.3f}  (law 0.535)")

# --- verify: the envelope beats at 0.535 Hz ---
X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(n, 1/sr)
Xb = X.copy(); Xb[(frm < 48) | (frm > 62)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
i0, i1 = int(5*sr), int(55*sr)
e = env[i0:i1] - env[i0:i1].mean()
E = np.abs(np.fft.rfft(e * np.hanning(len(e))))
f2 = np.fft.rfftfreq(len(e), 1/sr)
band = (f2 > 0.2) & (f2 < 1.2)
k = band[np.argmax(E[band])]
print(f"envelope beat: {f2[band][np.argmax(E[band])]:.3f} Hz  "
      f"= one swell every {1/f2[band][np.argmax(E[band])]:.3f} s  "
      f"(~{50*f2[band][np.argmax(E[band])]:.0f} swells in the hold)")

# --- the still: the envelope itself, 32 swells, one line ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
tt = np.arange(i1 - i0) / sr + 5
ax.plot(tt, env[i0:i1] / env[i0:i1].max(), color='black', lw=0.9)
ax.set_xlim(5, 55); ax.set_ylim(0, 1.05)
ax.set_xlabel('seconds', fontsize=9)
ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('55 Hz, span 0.535 — one swell every 1.87 s', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/belowrung_still.png')
print("wrote belowrung_still.png")
