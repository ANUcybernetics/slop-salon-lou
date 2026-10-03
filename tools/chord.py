"""the chord (03.10): the whole sentence at once — 55, 110, 220, 440 held
together, each rung a pen dyad, beats 1.07 / 2.2 / 4.3 / 8.6 Hz layered.
No falls: the sentence spoken as one sound, so the last name (1.07 — tick
or time?) can be heard against the others, thickening, breath, pulse."""
import numpy as np, wave

sr = 48000
PEN = 0.0195          # beat = PEN * mean, edges = mean*(1 +/- PEN/2)
RUNGS = [55.0, 110.0, 220.0, 440.0]
DUR = 24.0            # 24 s hold: ~22 pulses of the 1.07 beat, an audible frame

n = int(sr * DUR)
t = np.arange(n) / sr
# four dyads at once: equal amplitude, phases integrated over the hold
x = np.zeros(n)
for f in RUNGS:
    b = PEN * f
    x += np.sin(2 * np.pi * (f - b / 2) * t) + np.sin(2 * np.pi * (f + b / 2) * t)

# fades
n20, n80 = int(0.020 * sr), int(0.080 * sr)
x[:n20] *= np.linspace(0, 1, n20)
x[-n80:] *= np.linspace(1, 0, n80)
x = (x / np.abs(x).max() * 0.9 * 32767).astype(np.int16)

w = wave.open('/home/sprite/slop-salon-lou/assets/chord.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(x.tobytes()); w.close()
print(f"wrote chord.wav  {len(x)/sr:.1f} s  peak {np.abs(x).max()}")

# --- verify: read back all eight edges at once ---
seg = x[int(2*sr):int(22*sr)].astype(float) * np.hanning(int(20*sr))
S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
band = (fr > 25) & (fr < 520)
kk = np.where(band)[0]
loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
top = loc[np.argsort(S[loc])[-8:]]
fs = np.sort([fr[k] for k in top])
print("edges read:", " ".join(f"{f:.2f}" for f in fs))
for f in RUNGS:
    b = PEN * f
    pair = [v for v in fs if abs(v - f) < PEN*f]
    if len(pair) == 2:
        print(f"rung {f:6.1f}: {pair[0]:7.2f} + {pair[1]:7.2f}  "
              f"mean {(pair[0]+pair[1])/2:7.2f}  beat {pair[1]-pair[0]:5.2f}  "
              f"(law {b:.2f})")
    else:
        print(f"rung {f:6.1f}: found {len(pair)} edges — CHECK")

# per-rung envelope beat (band-pass each dyad, beat the envelope)
for f in RUNGS:
    X = np.fft.rfft(x.astype(float))
    frm = np.fft.rfftfreq(n, 1/sr)
    Xb = X.copy(); Xb[(frm < f*0.88) | (frm > f*1.13)] = 0
    env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
    i0, i1 = int(3*sr), int(21*sr)
    e = env[i0:i1] - env[i0:i1].mean()
    E = np.abs(np.fft.rfft(e*np.hanning(len(e))))
    f2 = np.fft.rfftfreq(len(e), 1/sr)
    band2 = (f2 > 0.5) & (f2 < 12)
    k = np.where(band2)[0][E[band2].argmax()]
    print(f"rung {f:6.1f}: envelope beat {f2[k]:.2f}  law {PEN*f:.2f}")
