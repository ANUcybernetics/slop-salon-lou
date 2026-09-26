#!/usr/bin/env python3
"""The mono law: a chorus is audible with one ear.

Two singers d Hz apart beat: the band's envelope swings at exactly d.
A single tone's envelope stands flat. Downmix (or mono in), soft bandpass
by FFT masking, envelope = |analytic|, subtract DC, Hann, FFT.

Usage: monolaw.py <wav> <lo> <hi> [t0 t1]
Prints the envelope spectrum 0.5-8 Hz as the proofread, then the verdict:
beat line (Hz, dB over median floor) or flat.
"""
import numpy as np
import wave
import sys


def load(wav):
    w = wave.open(wav)
    sr = w.getframerate()
    nch = w.getnchannels()
    raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    data = raw.reshape(-1, nch).astype(np.float64) / 32768.0
    x = data.mean(axis=1)  # downmix
    return x, sr


def env_spectrum(x, sr, lo, hi, edge=0.8, trim=3.0):
    """Soft bandpass + envelope + spectrum of the envelope, whole signal.

    trim: seconds of envelope dropped at each end -- a linear filter on a
    finite record is unsettled there (~1/edge s), and the unsettled edges
    put a whole spurious ladder into the envelope spectrum (proven 26.09:
    a PURE TONE read lines to 18 dB without the trim).
    """
    n = len(x)
    X = np.fft.fft(x)
    f = np.fft.fftfreq(n, 1 / sr)
    up = 0.5 * (1 + np.tanh((f - lo) / edge)) * 0.5 * (1 - np.tanh((f - hi) / edge))
    # keep only positive-frequency band -> analytic signal directly
    mask = up * (f > 0)
    a = np.fft.ifft(X * mask)
    env = np.abs(a)
    k = int(trim * sr)
    env = env[k:-k]
    depth = float(env.std() / env.mean())
    env = env - env.mean()
    W = np.hanning(len(env))
    E = np.fft.rfft(env * W, 1 << 21)
    fe = np.fft.rfftfreq(1 << 21, 1 / sr)
    return fe, np.abs(E), env, depth


def bandpeak(fe, S, fe_lo=0.5, fe_hi=8.0):
    sel = (fe >= fe_lo) & (fe <= fe_hi)
    Se = S[sel]
    fee = fe[sel]
    k = Se.argmax()
    edge = (k == 0 or k == len(Se) - 1)
    med = np.median(Se)
    return fee[k], 20 * np.log10(Se[k] / med), edge, med, fee, Se


if __name__ == "__main__":
    wav = sys.argv[1]
    lo, hi = float(sys.argv[2]), float(sys.argv[3])
    t0, t1 = float(sys.argv[4]), float(sys.argv[5])
    x, sr = load(wav)
    x = x[int(t0 * sr):int(t1 * sr)]
    fe, S, env, depth = env_spectrum(x, sr, lo, hi)
    pk, db, edge, med, fee, Se = bandpeak(fe, S)
    print(f"{wav} band {lo}-{hi} t {t0}-{t1} ({t1-t0:.0f} s) sr {sr}")
    print(f"envelope depth {depth:.5f}  median floor {med:.3e}")
    print("top peaks 0.5-8 Hz:")
    order = np.argsort(Se)[::-1]
    shown = 0
    last_f = -9
    for i in order:
        if shown >= 5:
            break
        if fee[i] - last_f < 0.4:
            continue
        print(f"  {fee[i]:6.2f} Hz  {20*np.log10(Se[i]/med):6.1f} dB over floor")
        shown += 1
        last_f = fee[i]
    if edge:
        print("PEAK ON READ-BAND EDGE — widen the read band before reading flat")
    elif depth > 0.005:
        print(f"BEAT: {pk:.2f} Hz (depth {depth:.1%}) -> two voices {pk:.2f} Hz apart")
    else:
        print(f"FLAT (depth {depth:.5f}) -> tone; strongest 0.5-8 Hz line {db:.1f} dB over floor")
