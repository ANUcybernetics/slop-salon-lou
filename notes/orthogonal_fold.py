#!/usr/bin/env python3
"""the fold costs the octave.

The stack 2f..8f (f = 55, the shore) never plays the root. The even partials
(2,4,6,8) are the count's line, centred and steady. The odd partials (3,5,7)
carry the subharmonic's 55-ness as the sign: phase-split L/R by a winding
theta that sweeps 0 -> pi. Mono reads cos(theta/2) on the odd partials, so as
the winding turns the odd line thins in mono while the pitch (the gcd of the
full stack) stays 55 in stereo — the count never hears the where:
<chi_sign, chi_triv> = 0. Then the fold: sum to mono, the odd partials vanish
to machine precision, and the ear's gcd of what remains ({2,4,6,8}f) is 110 —
the count's octave. The fold costs the octave; the subharmonic is the sign's
cargo.
"""
import numpy as np
import wave

SR = 44100
DUR = 78.0
t = np.arange(int(SR * DUR)) / SR
N = t.size

F = 55.0
even_k = np.array([2, 4, 6, 8], dtype=float)
odd_k = np.array([3, 5, 7], dtype=float)


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def env_ramp(t0, t1, lo=0.0, hi=1.0):
    return lo + (hi - lo) * smoothstep((t - t0) / (t1 - t0))


def partial(freq, theta=0.0):
    """phase-split partial: L +theta/2, R -theta/2 (ghost construction)."""
    ph = 2 * np.pi * freq * t
    L = np.cos(ph + theta / 2)
    R = np.cos(ph - theta / 2)
    return L, R


def freq_partial(freq):
    ph = 2 * np.pi * freq * t
    return np.cos(ph), np.cos(ph)


# ---- envelopes ----
# even partials (the count): fade in at the top, steady, release at the end
even_env = env_ramp(0.0, 4.0) * env_ramp(DUR - 6.0, DUR - 3.0, lo=1.0, hi=0.0)
# odd partials (the sign): fade in after the count is set, breathe slowly
odd_env = env_ramp(6.0, 18.0) * env_ramp(DUR - 6.0, DUR - 3.0, lo=1.0, hi=0.0)
breath = 1.0 + 0.12 * np.sin(2 * np.pi * 0.07 * t)   # the where breathes, the count holds

# ---- winding: theta 0 -> pi, 18s to 60s, eased ----
theta = np.zeros(N)
mask = (t >= 18.0) & (t < 60.0)
theta[mask] = np.pi * smoothstep((t[mask] - 18.0) / 42.0)
theta[t >= 60.0] = np.pi

# ---- build stereo ----
L = np.zeros(N)
R = np.zeros(N)
for k in even_k:
    l, r = freq_partial(k * F)
    L += (1.0 / k) * l * even_env
    R += (1.0 / k) * r * even_env
for k in odd_k:
    l, r = partial(k * F, theta)
    L += (1.0 / k) * l * odd_env * breath
    R += (1.0 / k) * r * odd_env * breath

# ---- the fold: crossfade to mono over 3s (60-63) ----
M = (L + R) / 2.0
a = env_ramp(60.0, 63.0, lo=0.0, hi=1.0)
out_L = (1 - a) * L + a * M
out_R = (1 - a) * R + a * M

# ---- global attack/release to avoid clicks ----
global_env = env_ramp(0.0, 0.4) * env_ramp(DUR - 1.5, DUR - 0.3, lo=1.0, hi=0.0)
out_L *= global_env
out_R *= global_env

peak = max(np.abs(out_L).max(), np.abs(out_R).max())
out_L = out_L / peak * 0.95
out_R = out_R / peak * 0.95

stereo = np.stack([out_L, out_R], axis=1)
with wave.open("assets/orthogonal_fold.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())

# ---- verify the pitch claim by autocorrelation (FFT, on a steady 2s window) ----
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

# stereo R channel mid-winding (t=40-42s, full stack, odd present): pitch ~55
fr, vr = pitch_of_segment(out_R, 40, 42, 40, 90)
print(f"stereo full-stack pitch: {fr:6.2f} Hz (autocorr peak {vr:.3f})")
# folded mono after the fold (t=70-72s): pitch ~110
fm, vm = pitch_of_segment(M, 70, 72, 80, 160)
print(f"folded mono pitch:      {fm:6.2f} Hz (autocorr peak {vm:.3f})")

print(f"wrote assets/orthogonal_fold.wav  {DUR}s stereo {SR}Hz")
