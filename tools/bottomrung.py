#!/usr/bin/env python3
"""bottom-rung probe (04.10): the boundary rungs, on lelia's tape and
natalie's road. Keys from HER alt (55@1.07 -> 27.5@0.535 -> 13.75@0.2675,
breath mid-hold, 440 cal blips at the open). Two readings per rung:
  SPECTRUM: two edges or one smeared voice (long window, zero-padded).
  ENVELOPE: does the beat survive as amplitude modulation at span Hz.
The question underneath: where does the countable end?"""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt, hilbert

def load(path):
    sr, x = wavfile.read(path)
    x = x.astype(np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    return sr, x / np.abs(x).max()

def two_peaks(x, sr, lo, hi, T, pad=8, frac=0.15):
    """top-2 local maxima in [lo,hi] over a T-second window, zero-padded."""
    n = int(T * sr)
    if len(x) < n:
        return None
    w = np.hanning(n)
    N = int(2 ** np.ceil(np.log2(n * pad)))
    S = np.abs(np.fft.rfft(x[:n] * w, N))
    f = np.fft.rfftfreq(N, 1 / sr)
    b = (f >= lo) & (f <= hi)
    fb, Sb = f[b], S[b]
    loc = np.where((Sb[1:-1] > Sb[:-2]) & (Sb[1:-1] > Sb[2:]))[0] + 1
    loc = loc[Sb[loc] > Sb.max() * frac]
    if len(loc) < 2:
        return "ONE VOICE (no second peak)"
    def refine(k):
        a, bb, c = Sb[k-1], Sb[k], Sb[k+1]
        d = 0.5*(a-c)/(a-2*bb+c)
        return fb[k] + d*(fb[1]-fb[0])
    top = loc[np.argsort(Sb[loc])[-2:]]
    f1, f2 = refine(top[0]), refine(top[1])
    return sorted((f1, f2))

def env_beat(x, sr, t0, t1, fc, span_lo, span_hi):
    """beat from the envelope: bandpass around fc, |analytic|, detrended
    FFT -> dominant peak in [span_lo, span_hi]."""
    seg = x[int(t0*sr):int(t1*sr)]
    sos = butter(4, [max(fc - 3*span_hi, 0.5), fc + 3*span_hi],
                 btype='band', fs=sr, output='sos')
    y = sosfiltfilt(sos, seg)
    env = np.abs(hilbert(y))
    env = env - env.mean()
    N = int(2 ** np.ceil(np.log2(len(env) * 8)))
    E = np.abs(np.fft.rfft(env * np.hanning(len(env)), N))
    f = np.fft.rfftfreq(N, 1 / sr)
    b = (f >= span_lo) & (f <= span_hi)
    fb, Eb = f[b], E[b]
    k = Eb.argmax()
    a, bb, c = Eb[k-1], Eb[k], Eb[k+1]
    d = 0.5*(a-c)/(a-2*bb+c)
    return fb[k] + d*(fb[1]-fb[0]), Eb.max() / (Eb.max() if True else 1)

def spectrum_report(name, x, sr, windows, mean, beat, label):
    print(f"-- {name} [{label}]  expect mean {mean} span {beat}")
    for seg_t0, seg_t1 in windows:
        T = min(seg_t1 - seg_t0, 8.0)
        tp = two_peaks(x[int(seg_t0*sr):int(seg_t0*sr)+int(T*sr)],
                       sr, mean - 4*beat, mean + 4*beat, T)
        if tp is None:
            print(f"   t={seg_t0:5.1f}-{seg_t1:5.1f}  ONE VOICE (no second peak)")
        else:
            f1, f2 = tp
            print(f"   t={seg_t0:5.1f}-{seg_t1:5.1f}  edges {f1:.3f}+{f2:.3f}  "
                  f"mean {np.mean(tp):.3f}  span {f2-f1:.3f}")
    b, _ = env_beat(x, sr, windows[0][0], windows[-1][1], mean, beat/2, beat*3)
    print(f"   envelope beat over {windows[0][0]:.1f}-{windows[-1][1]:.1f}: "
          f"{b:.4f} Hz  (law {beat})")

if __name__ == '__main__':
    # --- lelia's tape: cal blips ~0-3 s, holds 3-14.5, 15.5-30.5, 31-51.5 ---
    sr, x = load('/tmp/lelia_breath.wav')
    # find the 440 cal blips in the first 3 s
    tp = two_peaks(x, sr, 400, 480, 2.5, pad=8)
    print("cal blips [0-2.5s]:", "none found" if tp is None else
          f"edges {tp[0]:.2f}+{tp[1]:.2f}")
    rungs = [
        ("rung 55",    3.0, 14.5, 55.00, 1.0725),
        ("rung 27.5", 15.5, 30.5, 27.50, 0.5363),
        ("rung 13.75", 31.0, 51.5, 13.75, 0.2681),
    ]
    for name, t0, t1, mean, beat in rungs:
        mid = (t0 + t1) / 2
        windows = [(t0, mid - 1.5), (mid + 1.5, t1)]
        spectrum_report(name, x, sr, windows, mean, beat, "lelia")
    # --- natalie's road: glide, arrival last seconds before the fade ---
    sr2, x2 = load('/tmp/nat_letgo4.wav')
    # instantaneous f via 0.5 s windows, hop 0.25 s
    WA = int(0.5*sr2); win = np.hanning(WA); hop = int(0.25*sr2)
    fa = np.fft.rfftfreq(WA, 1/sr2)
    print("-- natalie letgo4: instantaneous f over the glide")
    for t0 in range(0, len(x2)-WA, hop):
        S = np.abs(np.fft.rfft(x2[t0:t0+WA]*win, 8*WA))
        f = np.fft.rfftfreq(8*WA, 1/sr2)
        b = (f > 5) & (f < 80)
        k = np.where(b)[0][np.argmax(S[b])]
        a, bb, c = S[k-1], S[k], S[k+1]
        d = 0.0 if (a-2*bb+c) == 0 else 0.5*(a-c)/(a-2*bb+c)
        print(f"   t={t0/sr2:5.2f}  f={f[k]+d*(f[1]-f[0]):7.3f}  amp={S[k]/S.max():.3f}")
