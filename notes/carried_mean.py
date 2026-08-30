#!/usr/bin/env python3
"""the mean is carried, not arrived at.

rahel: "the count a constant of motion, not a fixed point — xy=110^2 holds
every instant, so the mean is carried, not arrived at." the averages register:
for a pair (x, y) with xy = 110^2, the arithmetic and harmonic means multiply
to the geometric mean squared,

    AM = (x+y)/2,   HM = 2xy/(x+y) = 110^2/AM,   AM * HM = 110^2.

so AM and HM are THEMSELVES a mirror pair about the count: their log-midpoint
is log 110, and their product is 110^2 at every instant. here that mirror pair
is the two voices, and u(t) carries them out and back through the crossing:

    f_AM(t) = 110 * cosh(u(t) ln2)     (137.5 = 110 * 5/4  at u = +/-1)
    f_HM(t) = 110 / cosh(u(t) ln2)     (  88   = 110 * 4/5  at u = +/-1)

at u = 0 both voices ARE the count: the three means fuse into one tone, and
the pair has exchanged — the arithmetic becomes the harmonic, the transposition
the crossing. but the drone at 110 never moves. fold the piece to mono and the
carried count survives cleanest; the mirror pair, half-strength, is the where.
"""
import numpy as np
import wave

SR = 44100
DUR = 50.0
t = np.arange(int(SR * DUR)) / SR
N = t.size

C = 110.0  # the count, carried


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def env_ramp(t0, t1, lo=0.0, hi=1.0):
    return lo + (hi - lo) * smoothstep((t - t0) / (t1 - t0))


# ---- the carrier u: two full departures-and-returns, passing the crossing
#      repeatedly. carried, never landed on. ----
u = np.sin(2 * np.pi * t / DUR * 2.0)          # u = +/-1 at the extremes, 0 at t=0,12.5,25,37.5,50

# ---- the two voices: arithmetic and harmonic mean of the pair xy=110^2 ----
ch = np.cosh(u * np.log(2.0))
fAM = C * ch                   # 110 -> 137.5
fHM = C / ch                   # 110 -> 88

# ---- phases, anchored so both voices sit at phase 0 (mod 2pi) at t=0,
#      where they are both the count and the drone is phase-0 there too ----
def glide_phase(f):
    ph = np.cumsum(2 * np.pi * f / SR)
    ph -= ph[0]
    return ph

phAM = glide_phase(fAM)
phHM = glide_phase(fHM)

# ---- the carried count, a constant 110 sine, phase 0 at t=0 ----
drone = np.cos(2 * np.pi * C * t)

# ---- voices, panned: AM to the left, HM to the right, drone centred ----
#      so the mirror pair is a position, and the fold hears the count.
gAM_L, gAM_R = 0.42, 0.20
gHM_L, gHM_R = 0.20, 0.42
L = gAM_L * np.cos(phAM) + gHM_L * np.cos(phHM) + 0.32 * drone
R = gAM_R * np.cos(phAM) + gHM_R * np.cos(phHM) + 0.32 * drone

# ---- global attack/release ----
global_env = env_ramp(0.0, 3.0) * env_ramp(DUR - 3.0, DUR - 1.0, lo=1.0, hi=0.0)
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/carried_mean.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())


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


# at the extreme (t=11-12.5), the left voice is near 137.5 (AM), the right near 88 (HM)
fp, vp = pitch_of_segment(L, 11, 12.2, 100, 180)
print(f"L voice, t=11-12.2:  {fp:6.2f} Hz (autocorr {vp:.3f})  [expect AM ~137.5]")
fr, vr = pitch_of_segment(R, 11, 12.2, 60, 110)
print(f"R voice, t=11-12.2:  {fr:6.2f} Hz (autocorr {vr:.3f})  [expect HM ~88]")
# the fold (mono) at the crossing (t=12-13): the drone is the count
M = (L + R) / 2.0
fc, vc = pitch_of_segment(M, 12.3, 13.3, 90, 140)
print(f"folded, crossing t=12.3-13.3: {fc:6.2f} Hz (autocorr {vc:.3f})  [expect 110]")

print(f"wrote assets/carried_mean.wav  {DUR}s stereo {SR}Hz  (peak {peak:.3f})")
