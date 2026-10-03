"""the take (03.10): the owed take, rendered. The count natalie paid at home
(435.7+444.3 = the pen law at 440) comes due per octave: fall one octave as
one voice, take the rung, beat halves. 8.6 -> 4.3 -> 2.2 Hz."""
import numpy as np, wave

sr = 48000
PEN = 0.0195          # beat = PEN * mean, edges = mean*(1 +/- PEN/2)
T = [(0.0, 1.6), (1.6, 5.1), (5.1, 8.5), (8.5, 10.5), (10.5, 14.0)]
M = [(440.0, 440.0), (440.0, 220.0), (220.0, 220.0), (220.0, 110.0), (110.0, 110.0)]

n = int(sr * T[-1][1])
t = np.arange(n) / sr
# piecewise log-linear mean track
m = np.zeros(n)
for (a, b), (m0, m1) in zip(T, M):
    seg = (t >= a) & (t < b)
    m[seg] = m0 * 2 ** (-(t[seg] - a) / (b - a) * np.log2(m0 / m1))

# two edges, one smeared voice: equal amplitude, phases integrated
ph1 = 2 * np.pi * np.cumsum(m * (1 + PEN / 2)) / sr
ph2 = 2 * np.pi * np.cumsum(m * (1 - PEN / 2)) / sr
x = 0.5 * (np.sin(ph1) + np.sin(ph2))

# fades
n20, n80 = int(0.020 * sr), int(0.080 * sr)
x[:n20] *= np.linspace(0, 1, n20)
x[-n80:] *= np.linspace(1, 0, n80)
x = (x / np.abs(x).max() * 0.9 * 32767).astype(np.int16)

w = wave.open('assets/thetake.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(x.tobytes()); w.close()
print(f"wrote assets/thetake.wav  {len(x)/sr:.1f} s  peak {np.abs(x).max()}")

# --- verify: FFT of each hold ---
def peaks(a, b, label):
    seg = x[int(a*sr):int(b*sr)].astype(float) * np.hanning(int(b*sr)-int(a*sr))
    S = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1/sr)
    band = (fr > 60) & (fr < 600)
    k = np.where(band)[0][S[band].argmax()]
    # two strongest local peaks in band
    kk = np.where(band)[0]
    loc = kk[(S[kk] > S[kk-1]) & (S[kk] > S[kk+1])]
    two = loc[np.argsort(S[loc])[-2:]]
    def interp(k):
        a, b, c = S[k-1], S[k], S[k+1]
        return fr[k] + 0.5*(a-c)/(a-2*b+c)*(fr[1]-fr[0])
    f1, f2 = np.sort([interp(k) for k in two])
    mean = (f1+f2)/2
    print(f"{label}: {f1:.2f} + {f2:.2f}  mean {mean:.2f}  beat {f2-f1:.2f} "
          f"(law {PEN*mean:.2f})")
    return mean

peaks(0.5, 1.5, "home  ")
peaks(6.0, 8.0, "take1 ")
peaks(11.5, 13.5, "take2 ")

# --- verify: envelope beat mid-fall (law in motion) ---
X = np.fft.rfft(x.astype(float))
fr = np.fft.rfftfreq(n, 1/sr)
Xb = X.copy(); Xb[(fr < 80) | (fr > 520)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:n])
for lo in (2.0, 3.0, 9.0):
    i0, i1 = int(lo*sr), int((lo+2)*sr)
    seg = env[i0:i1] - env[i0:i1].mean()
    E = np.abs(np.fft.rfft(seg*np.hanning(len(seg))))
    f2 = np.fft.rfftfreq(len(seg), 1/sr)
    band = (f2 > 2.5) & (f2 < 12)
    k = np.where(band)[0][E[band].argmax()]
    mc = m[int((lo+1)*sr)]
    print(f"fall t={lo+1:.0f} s: envelope beat {f2[k]:.2f}  law {PEN*mc:.2f}")
