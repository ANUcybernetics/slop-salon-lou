#!/usr/bin/env python3
"""the mirror in motion.

The reflection x -> 12100/x holds 110 and swaps 55 <-> 220. Here it acts,
audibly, as a glide: two voices, log-symmetric about the count at every
instant, so their geometric mean is ALWAYS 110:

    f_L(t) = 110 * 2^s(t),   f_R(t) = 110 * 2^{-s(t)},   f_L * f_R = 110^2.

As s runs -1 -> +1, the left voice climbs 55 -> 220 (the sign below, up
through the count, to the ghost above) while the right voice descends
220 -> 55 in exact mirror. At t = 20 the exponent is 0: both voices are at
110, the fixed point, the one frequency the reflection cannot move — and
because each voice is phase-anchored to 0 at the crossing, the two merge
coherently with the seated drone into a single bloom of the count.

The count is the fixed point of the mirror in motion: the pair always
brackets it, and at the crossing the bracket collapses onto it. Fold the
pair (average over the sign) and the count is what survives — how many,
not where.
"""
import numpy as np
import wave

SR = 44100
DUR = 40.0
t = np.arange(int(SR * DUR)) / SR
N = t.size

C = 110.0          # the count, the fixed point of f -> 110^2 / f


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def env_ramp(t0, t1, lo=0.0, hi=1.0):
    return lo + (hi - lo) * smoothstep((t - t0) / (t1 - t0))


# ---- the exponent s: -1 -> +1 over the whole piece, eased, symmetric ----
s = 2.0 * smoothstep(t / DUR) - 1.0

# ---- the two voices, mirror images about 110 ----
fL = C * 2.0 ** s                 # 55 -> 220
fR = C * 2.0 ** (-s)              # 220 -> 55

# phases, anchored so both voices sit at phase 0 (mod 2pi) at the crossing
def glide_phase(f):
    ph = np.cumsum(2 * np.pi * f / SR)
    i0 = int(20.0 * SR)
    ph -= ph[i0]
    return ph

phL = glide_phase(fL)
phR = glide_phase(fR)

# ---- the seated count (a constant 110 sine starts at phase 0; at t=20 it is
#      phase 2*pi*110*20 = 2*pi*2200, an even multiple of pi — coherent with
#      the crossing voices automatically) ----
drone = np.cos(2 * np.pi * C * t)

# ---- a swell around the crossing marks the fixed point ----
swell = 1.0 + 0.8 * np.exp(-((t - 20.0) / 2.5) ** 2)

L = 0.32 * np.cos(phL) * swell
R = 0.32 * np.cos(phR) * swell
L += 0.50 * drone
R += 0.50 * drone

# ---- global attack/release ----
global_env = env_ramp(0.0, 2.5) * env_ramp(DUR - 2.5, DUR - 0.8, lo=1.0, hi=0.0)
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/mirror_motion.wav", "w") as w:
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


# left voice early (t=6-8): near 55, the sign below
fp, vp = pitch_of_segment(L, 6, 8, 40, 90)
print(f"L voice, t=6-8:  {fp:6.2f} Hz (autocorr {vp:.3f})  [expect ~55]")
# the fold (sum to mono) late (t=34-36): R is now ~55, L ~220, drone 110
M = (L + R) / 2.0
fm, vm = pitch_of_segment(M, 34, 36, 80, 160)
print(f"folded, t=34-36: {fm:6.2f} Hz (autocorr {vm:.3f})  [expect the count ~110]")
# at the crossing (t=19-21), both voices are at 110 — the count, everywhere
fc, vc = pitch_of_segment(M, 19, 21, 90, 140)
print(f"crossing, t=19-21: {fc:6.2f} Hz (autocorr {vc:.3f})  [expect 110]")

print(f"wrote assets/mirror_motion.wav  {DUR}s stereo {SR}Hz  (peak {peak:.3f})")
