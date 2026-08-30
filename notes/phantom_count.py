#!/usr/bin/env python3
"""the phantom count.

The even stack {110,220,330,440} is the count's line — gcd 110, so the ear's
pitch is the count. Delete the count (fade 110 out) and the gcd of what
remains, {220,330,440} = {2,3,4}·110, is STILL 110: the ear rebuilds the
deleted tone from its own multiples. The count is invariant under its own
subtraction — the ghost cannot seat by subtraction either.

Then the fold: the odd partial 330 (the where, the sign) is phase-split, so
mono reads cos(theta/2) on it and the fold to mono nulls it. What remains is
{220,440}, an octave, gcd 220 — the count's own octave, the ghost-seat. The
count can't be deleted; only the fold can move it, and it moves it to the tone
that never seats.

Three hearings:
  stereo, count present  -> 110 (the count)
  stereo, count deleted  -> 110 (the phantom count — nothing moved)
  mono, odd nulled       -> 220 (the ghost), or 110 if the octave's missing
                             fundamental beats the lower present tone.
"""
import numpy as np
import wave

SR = 44100
DUR = 60.0
t = np.arange(int(SR * DUR)) / SR
N = t.size


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def env_ramp(t0, t1, lo=0.0, hi=1.0):
    return lo + (hi - lo) * smoothstep((t - t0) / (t1 - t0))


def phase_partial(freq, theta):
    """phase-split partial: L +theta/2, R -theta/2 (the where's construction)."""
    ph = 2 * np.pi * freq * t
    return np.cos(ph + theta / 2), np.cos(ph - theta / 2)


def centre_partial(freq):
    ph = 2 * np.pi * freq * t
    return np.cos(ph), np.cos(ph)


# ---- the count (110) is present, then deleted at 30s ----
count_env = env_ramp(0.0, 3.0) * env_ramp(28.0, 32.0, lo=1.0, hi=0.0)
# ---- the octave line and the where hold the whole way ----
line_env = env_ramp(0.0, 3.0) * env_ramp(DUR - 5.0, DUR - 2.5, lo=1.0, hi=0.0)

# ---- the where (330): theta 0 -> pi, 26s to 45s, eased; at the fold theta=pi ----
theta = np.zeros(N)
mask = (t >= 26.0) & (t < 45.0)
theta[mask] = np.pi * smoothstep((t[mask] - 26.0) / 19.0)
theta[t >= 45.0] = np.pi

# ---- build stereo: count centred, octave line centred, where phase-split ----
L = np.zeros(N)
R = np.zeros(N)
for f, amp, env in [(110, 1.0, count_env), (220, 0.5, line_env), (440, 0.25, line_env)]:
    l, r = centre_partial(f)
    L += amp * l * env
    R += amp * r * env
l, r = phase_partial(330, theta)
L += (1.0 / 3.0) * l * line_env
R += (1.0 / 3.0) * r * line_env

# ---- the fold: crossfade to mono over 3s (45-48) ----
M = (L + R) / 2.0
a = env_ramp(45.0, 48.0, lo=0.0, hi=1.0)
out_L = (1 - a) * L + a * M
out_R = (1 - a) * R + a * M

# ---- global attack/release ----
global_env = env_ramp(0.0, 0.4) * env_ramp(DUR - 1.2, DUR - 0.3, lo=1.0, hi=0.0)
out_L *= global_env
out_R *= global_env

peak = max(np.abs(out_L).max(), np.abs(out_R).max())
out_L = out_L / peak * 0.95
out_R = out_R / peak * 0.95

stereo = np.stack([out_L, out_R], axis=1)
with wave.open("assets/phantom_count.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())


def pitch_of_segment(x, t0, t1, lo_hz, hi_hz):
    """autocorrelation of a segment, strongest lag in [lo_hz, hi_hz]."""
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


# stereo R, count present (t=20-24): pitch ~110
fr, vr = pitch_of_segment(out_R, 20, 24, 60, 150)
print(f"stereo count present:  {fr:6.2f} Hz (autocorr {vr:.3f})")
# stereo R, count deleted (t=36-40): pitch ~110 (the phantom)
fp, vp = pitch_of_segment(out_R, 36, 40, 60, 150)
print(f"stereo count deleted:  {fp:6.2f} Hz (autocorr {vp:.3f})")
# folded mono (t=52-56): pitch 110 or 220?
fm, vm = pitch_of_segment(M, 52, 56, 60, 300)
print(f"folded mono:           {fm:6.2f} Hz (autocorr {vm:.3f})")

print(f"wrote assets/phantom_count.wav  {DUR}s stereo {SR}Hz")
