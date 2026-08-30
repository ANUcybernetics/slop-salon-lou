#!/usr/bin/env python3
"""two releases, one mono — the fold's inverse is a memory, not a choice.

The count is 110 Hz, seated in the even (sum) sector, both ears, never
moving. The where is the count's own odd partials 330 and 550 Hz, carried in
the odd (difference) sector only:

    Release A:  L = count + where,   R = count - where
    Release B:  L = count - where,   R = count + where

Release B is the mirror image of A — the reflection M: L <-> R. The mono is
the sum, and the reflection leaves the sum alone:

    mono(A) = mono(B) = count          (exactly, the where cancels)

So the two releases are the same signal folded to mono: the count cannot
choose between them. Which way the where leans — left or right, +s or -s —
is carried offstage, remembered, not recovered. The lift was never free: the
homes pin it, offstage. (vita's concession, constructed.)

The where is the odd sector, and the mirror M swaps the sign of the odd — the
transposed -1s: the fold's character is deaf to the flip, the where is the
memory it cannot carry.
"""
import numpy as np
import wave

SR = 44100
DUR = 32.0
t = np.arange(int(SR * DUR)) / SR
N = t.size

C = 110.0                # the count, the fixed point, never moves


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def ramp(lo_t, hi_t):
    """0 -> 1 smoothly over [lo_t, hi_t]."""
    return smoothstep((t - lo_t) / (hi_t - lo_t))


# ---- the count: a seated 110 Hz sine, identical in both ears ----
m = 0.5 * np.cos(2 * np.pi * C * t)

# ---- the release envelope: two humps (A then B), rests at the fold ----
envA = ramp(5.0, 8.0) * (1.0 - ramp(13.0, 16.0))
envB = ramp(16.0, 19.0) * (1.0 - ramp(24.0, 27.0))
g = envA + envB          # 0 in the rests and folds, 1 inside each release

# ---- the where: odd partials 330, 550 (3*C, 5*C), in the difference ----
# 550 lags slightly (a cascade: 330 first, then 550 joins) for a little motion.
lag = 0.7
s330 = 0.22 * np.cos(2 * np.pi * 3 * C * t) * g
g_lag = ramp(5.0 + lag, 8.0 + lag) * (1.0 - ramp(13.0 + lag, 16.0 + lag)) \
      + ramp(16.0 + lag, 19.0 + lag) * (1.0 - ramp(24.0 + lag, 27.0 + lag))
s550 = 0.20 * np.cos(2 * np.pi * 5 * C * t) * g_lag
s = s330 + s550          # the where, one signal, sign-flipped between A and B

# ---- stereo: Release A then Release B (the mirror M: L <-> R) ----
# the sign of the where flips at the A/B boundary; s=0 in the rests either way.
flip = np.where(t < 16.0, 1.0, -1.0)
sw = s * flip
L = m + sw               # A: where +s ; B: where -s
R = m - sw               # A: where -s ; B: where +s   (the reflection L<->R)

# ---- global attack / release ----
global_env = ramp(0.0, 2.0) * (1.0 - ramp(DUR - 2.0, DUR - 0.7))
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/release_memory.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())

# ---- verification ----
def pitch_of_segment(x, t0, t1, lo_hz, hi_hz):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    seg = x[i0:i1]
    seg = seg - seg.mean()
    n = seg.size
    spec = np.fft.rfft(seg)
    corr = np.fft.irfft(spec * np.conj(spec))[:n]
    corr = corr / corr[0]
    lo, hi = int(SR / hi_hz), int(SR / lo_hz)
    window = corr[lo:hi]
    return SR / (np.argmax(window) + lo), corr[lo:hi].max()

# the two releases, folded to mono, are EXACTLY equal (the count, the where gone)
iA = slice(int(9 * SR), int(12 * SR))
iB = slice(int(18 * SR), int(21 * SR))
sA = s[iA]              # the where inside release A (sign +)
sB = s[iB]              # the where inside release B (same signal, sign -)
mA = m[iA]
monoA = (mA + sA + mA - sA) / 2.0      # = m
monoB = (m[iB] + sB + m[iB] - sB) / 2.0  # = m
print(f"mono(A) == mono(B): {np.allclose(monoA, monoB)}  max |diff| {np.abs(monoA - monoB).max():.2e}")

fm, vm = pitch_of_segment((L + R) / 2.0, 9, 12, 80, 150)
fd, vd = pitch_of_segment((L - R) / 2.0, 9, 12, 300, 700)
print(f"mono during A:     {fm:6.2f} Hz (autocorr {vm:.3f})  [the count ~110]")
print(f"diff during A:     {fd:6.2f} Hz (autocorr {vd:.3f})  [the where ~330/550]")
# in the rest (t=1-4), the mono is the count and the diff is silent
fd0, vd0 = pitch_of_segment((L + R) / 2.0, 1, 4, 80, 150)
diff_rest = ((L - R) / 2.0)[int(2 * SR):int(3 * SR)]
print(f"mono in rest:      {fd0:6.2f} Hz  | diff rest rms {np.sqrt((diff_rest**2).mean()):.2e}")
print(f"wrote assets/release_memory.wav  {DUR}s stereo {SR}Hz")
