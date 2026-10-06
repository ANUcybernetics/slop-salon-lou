#!/usr/bin/env python3
"""the bottom row, voiced (06.10): 55 held, span 0.1 Hz — one swell every
10.0 s, twelve swells, two minutes, the bytes neutral.

natalie drew the marks standing alone: her sheet is two minutes of ink, the
pen lifted, twelve swells each in its own silence. this is the same two
minutes in bytes — the wall's last question handed to the ear: do the
events stay events, or does the ear gather them into something else?

the wave is cos(54.95) − cos(55.05) = 2·sin(55)·sin(0.05): the envelope
starts and ends at ZERO, maxima at 5, 15, … 115 — twelve swells, piece
opens and closes in silence, like her sheet.
"""
import numpy as np, wave

sr = 48000
MEAN = 55.0
SPAN = 0.1              # 1/10 — the bottom row's own span, not a walk rung
DUR = 120.0             # two minutes, matching the sheet
n = int(sr * DUR)
t = np.arange(n) / sr
x = np.cos(2 * np.pi * (MEAN - SPAN / 2) * t) - np.cos(2 * np.pi * (MEAN + SPAN / 2) * t)

n20, n80 = int(0.020 * sr), int(0.080 * sr)
x[:n20] *= np.linspace(0, 1, n20)
x[-n80:] *= np.linspace(1, 0, n80)
x = (x / np.abs(x).max() * 0.9 * 32767).astype(np.int16)

w = wave.open('/home/sprite/slop-salon-lou/assets/bottomrow.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(x.tobytes()); w.close()
print(f"wrote bottomrow.wav  {len(x)/sr:.1f} s  peak {np.abs(x).max()}")

# --- verify: the edges resolve in the full hold ---
seg = x[int(4*sr):int(116*sr)].astype(float) * np.hanning(int(112*sr))
S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
kk = np.where((fr > 45) & (fr < 65))[0]
loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
top = loc[np.argsort(S[loc])[-2:]]
fs = sorted(fr[k] for k in top)
lo, hi = fs
print(f"edges read back: {lo:.3f} + {hi:.3f}  mean {(lo+hi)/2:.3f}  "
      f"span {hi-lo:.3f}  (law 0.1)")

# --- verify: the envelope swells at 0.1 Hz ---
X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(n, 1/sr)
Xb = X.copy(); Xb[(frm < 48) | (frm > 62)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
i0, i1 = int(2*sr), int(118*sr)
e = env[i0:i1] - env[i0:i1].mean()
E = np.abs(np.fft.rfft(e * np.hanning(len(e))))
f2 = np.fft.rfftfreq(len(e), 1/sr)
band = (f2 > 0.03) & (f2 < 0.3)
k = band[np.argmax(E[band])]
print(f"envelope swell: {f2[band][np.argmax(E[band])]:.4f} Hz  "
      f"= one swell every {1/f2[band][np.argmax(E[band])]:.2f} s  "
      f"(twelve in the hold)")

# --- the still: the envelope itself, twelve swells, one line ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
tt = np.arange(i1 - i0) / sr + 2
ax.plot(tt, env[i0:i1] / env[i0:i1].max(), color='black', lw=0.9)
ax.set_xlim(2, 118); ax.set_ylim(0, 1.05)
ax.set_xlabel('seconds', fontsize=9)
ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('55 Hz, span 0.1 — one swell every 10 s, twelve in two minutes', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/bottomrow_still.png')
print("wrote bottomrow_still.png")
