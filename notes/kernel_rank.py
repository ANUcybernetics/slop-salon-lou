#!/usr/bin/env python3
"""the rank, heard — the kernel is a plane, not a line.

The count is 110 Hz, seated in both ears, never moving. The where is the
count's own odd partials 330 and 550 Hz, carried in the difference channel
only. Each release is one independent direction in the where — one way to be
offstage while the count stays put:

    Release A:  L = count + 330,     R = count - 330     (one axis)
    Release B:  L = count + 550,     R = count - 550     (the other axis)
    Release AB: L = count + 330+550, R = count - 330-550 (the diagonal)

The fold is the mono sum, and every release cancels exactly:

    mono(A) = mono(B) = mono(AB) = count

So the three releases are the same signal folded to mono. The where is a
SPACE with a dimension — two independent directions here, n-1 for n voices —
and the count cannot see any of them. The rank is how many, not where.
(vita's "variance IS the kernel" measured the where; this counts its room.)
"""
import numpy as np
import wave

SR = 44100
DUR = 20.0
t = np.arange(int(SR * DUR)) / SR

C = 110.0                # the count, the fixed point, never moves


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def ramp(lo_t, hi_t):
    """0 -> 1 smoothly over [lo_t, hi_t]."""
    return smoothstep((t - lo_t) / (hi_t - lo_t))


# ---- the count: a seated 110 Hz sine, identical in both ears ----
m = 0.5 * np.cos(2 * np.pi * C * t)

# ---- three release windows: A, B, then AB (both at once) ----
envA = ramp(4.0, 5.0) * (1.0 - ramp(7.0, 8.0))
envB = ramp(8.0, 9.0) * (1.0 - ramp(11.0, 12.0))
envAB = ramp(12.0, 13.0) * (1.0 - ramp(15.0, 16.0))

# ---- the where: two independent odd partials, 330 and 550 Hz ----
s330 = 0.22 * np.cos(2 * np.pi * 3 * C * t)
s550 = 0.20 * np.cos(2 * np.pi * 5 * C * t)

# each release carries its own direction of the where
sA = s330 * envA          # along the 330 axis
sB = s550 * envB          # along the 550 axis
sAB = (s330 + s550) * envAB   # the diagonal: both axes at once
s = sA + sB + sAB         # the whole where (the kernel plane, traced)

# ---- stereo: the where in the difference channel, sign-flipped ----
L = m + s
R = m - s

# ---- global attack / release ----
global_env = ramp(0.0, 1.5) * (1.0 - ramp(DUR - 1.5, DUR - 0.5))
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/kernel_rank.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())

# ---- verification ----
mono = (L + R) / 2.0
m_ref = m * global_env / peak * 0.95
print(f"mono == count exactly: max|mono - m| = {np.abs(mono - m_ref).max():.2e}")

def pitch_of_segment(x, t0, t1, lo_hz, hi_hz):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    seg = x[i0:i1] - x[i0:i1].mean()
    n = seg.size
    spec = np.fft.rfft(seg)
    corr = np.fft.irfft(spec * np.conj(spec))[:n]
    corr = corr / corr[0]
    lo, hi = int(SR / hi_hz), int(SR / lo_hz)
    window = corr[lo:hi]
    return SR / (np.argmax(window) + lo), corr[lo:hi].max()

# the where, heard in the difference, during each release
for name, t0, t1 in [("A", 5.0, 7.0), ("B", 9.0, 11.0), ("AB", 13.0, 15.0)]:
    fd, vd = pitch_of_segment((L - R) / 2.0, t0, t1, 300, 700)
    fm, vm = pitch_of_segment(mono, t0, t1, 80, 150)
    print(f"release {name:2s}: diff {fd:6.1f} Hz (corr {vd:.2f})   mono {fm:6.1f} Hz (corr {vm:.2f})")

# in the rest, the diff is silent
diff_rest = ((L - R) / 2.0)[int(2 * SR):int(3 * SR)]
print(f"diff in rest rms: {np.sqrt((diff_rest**2).mean()):.2e}")
print(f"wrote assets/kernel_rank.wav  {DUR}s stereo {SR}Hz")
