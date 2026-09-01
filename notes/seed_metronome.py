#!/usr/bin/env python3
"""the root's metronome — 55 returns 16 times in 30,000 rungs; 110 never.

The exact CF of log2(3/2), 30k terms: the partial quotient 55 (the seed)
appears at rungs 15, 47, 1977, 4133, 6624, 9322, 10302, 13888, 14623,
18408, 19479, 20118, 20417, 21258, 23452, 28659 — sixteen returns with
irregular waits (299 to 5207 rungs). The partial quotient 110 (the count)
never appears: root returns; octave impossible.

Sound (150 s):
  - count 110 drones throughout (mono-safe, never struck)
  - the seed strikes 16x as a 55 Hz bell (odd partials only — no octave
    partial, the doubling is the grid's move it cannot coin), mono-safe
  - the one-time great records ring once each, faint, stereo-only
    (phase-split): 100, 964, 2436, 3308, 4878, 8228, 24477, 59599,
    folded into audible range as 110·(record/110)^(1/3)
  - fold to mono: the one-time landmarks vanish; the root's returns and
    the count's hold remain.

Time map: rung->sec, t(47)=2, then linear 148s over the 30k rungs.
"""
import numpy as np
import wave

sr = 44100
dur = 150.0
N = int(sr * dur)
t = np.arange(N) / sr

L = np.zeros(N)
R = np.zeros(N)

# --- the seed's sixteen returns, rung positions and mapped times ---
seed_rungs = [15, 47, 1977, 4133, 6624, 9322, 10302, 13888, 14623,
              18408, 19479, 20118, 20417, 21258, 23452, 28659]


def rung_time(r):
    if r <= 15:
        return 0.0
    if r <= 47:
        return 2.0 * (r - 15) / (47 - 15)
    return 2.0 + (r - 47) * (148.0 / (30000 - 47))


seed_times = [rung_time(r) for r in seed_rungs]
gaps = [seed_times[i + 1] - seed_times[i] for i in range(len(seed_times) - 1)]
print("seed times:", [f"{s:.1f}" for s in seed_times])
print("gaps:", [f"{g:.1f}" for g in gaps])

# --- count 110 drone: mono-safe, pure, never struck ---
drone = 0.09 * np.sin(2 * np.pi * 110 * t)
drone_env = np.ones(N)
drone_env[:int(3 * sr)] = np.linspace(0, 1, int(3 * sr))
fade = int(10 * sr)
drone_env[-fade:] = np.linspace(1, 0, fade)
L += drone * drone_env
R += drone * drone_env


def add_bell(L, R, t0, amp):
    """seed bell, mono-safe (the root survives any fold)."""
    # partials at odd multiples of 55; the octave (110) is absent on purpose
    partials = [(1.0, 1.00), (3.0, 0.50), (5.0, 0.30), (7.0, 0.18), (9.0, 0.10)]
    tau = [2.2, 1.3, 0.8, 0.5, 0.35]
    for (m, a), tau_p in zip(partials, tau):
        f = 55.0 * m
        msk = t >= t0
        e = np.exp(-(np.maximum(t[msk] - t0, 0)) / tau_p)
        s = amp * a * np.sin(2 * np.pi * f * t[msk]) * e
        L[msk] += s
        R[msk] += s


def add_ping(L, R, f, t0, amp):
    """one-time record, stereo-only (phase-split, folds to nothing)."""
    msk = t >= t0
    e = np.exp(-(np.maximum(t[msk] - t0, 0)) / 0.5)
    s = amp * np.sin(2 * np.pi * f * t[msk]) * e
    L[msk] += s
    R[msk] -= s


# --- the seed's sixteen returns ---
for i, tm in enumerate(seed_times):
    # fuller after a longer wait
    gap = gaps[i - 1] if i > 0 else 1.5
    amp = 0.16 + 0.07 * min(1.0, gap / 30.0)
    add_bell(L, R, tm, amp)

# --- the one-time great records, faint, stereo-only ---
records = [(219, 100), (231, 964), (331, 2436), (529, 3308),
           (2765, 4878), (4313, 8228), (18288, 24477), (21151, 59599)]
for r, val in records:
    tm = rung_time(r)
    f = 110.0 * (val / 110.0) ** (1.0 / 3.0)  # fold into audible range
    add_ping(L, R, f, tm, 0.035)

# --- normalise ---
peak = max(np.abs(L).max(), np.abs(R).max())
if peak > 0.97:
    L *= 0.97 / peak
    R *= 0.97 / peak
print("peak", peak)

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/seed_metronome.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())

# verify: a record ping should vanish in mono; the seed bell and drone remain
from numpy.fft import rfft
mono = (L + R) / 2
def segband(x, f0, t0a, t0b):
    seg_st = int(t0a * sr); seg_en = int(t0b * sr)
    freqs = np.fft.rfftfreq(seg_en - seg_st, 1 / sr)
    X = np.abs(rfft(x[seg_st:seg_en])); m = (freqs > f0 - 2.0) & (freqs < f0 + 2.0)
    return float(X[m].sum())
# 309 Hz = folded 2436 ping at t~3.4; 107 Hz = folded 100 ping at t~2.85 (near drone)
print("309 band @3.2-3.8  stereo-L", round(segband(L, 309, 3.2, 3.8), 1), " mono", round(segband(mono, 309, 3.2, 3.8), 1))
print("55  band @12-15    stereo-L", round(segband(L, 55, 12, 15), 1), " mono", round(segband(mono, 55, 12, 15), 1))
