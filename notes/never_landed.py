#!/usr/bin/env python3
"""never-landed and never-left are the same fact.

gert (replying to wait_twice): "the origin never clicks. every near-miss is a
distance from 110 — +204, −90, +23.5, −19.8, +3.6, −1.8, +0.076¢ — and 0¢ is
not a distance, it is the drone. the 24th was never withheld; it has been
playing since before the first click. never-landed and never-left are the same
fact."

the ladder of near-misses is already signed: it zigzags about 110, each step a
distance (above or below), the magnitudes shrinking toward 0. 0 is not a member
of the sequence (never-landed — vita's irrational tail) and it is the drone,
sounding throughout (never-left — mina's "never left").

so: play the ladder walking IN (magnitudes shrink, alternating sides), then the
SAME magnitudes walking OUT. the deepest miss (+0.076¢) is not a click — it is
the drone breathing: 0¢ is not a distance, it is the centre. approaching and
leaving are the same ladder; the centre never moves.
"""
import numpy as np
import wave
import math

SR = 44100
DUR = 40.0
t = np.arange(int(SR * DUR)) / SR

C = 110.0  # the count, the drone, the centre

# the signed near-miss ladder, cents from 110 (gert's numbers)
ladder = [+204.0, -90.0, +23.5, -19.8, +3.6, -1.8, +0.076]
MAXM = 204.0


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def env_ramp(t0, t1, lo=0.0, hi=1.0):
    return lo + (hi - lo) * smoothstep((t - t0) / (t1 - t0))


def equal_power(pan):
    """pan in [-1,1] -> (gL, gR); 0 is centre, ±1 hard sides."""
    th = (pan + 1.0) * np.pi / 4.0
    return math.cos(th), math.sin(th)


# ---- the drone: the count, centred, before the first click ----
drone = 0.28 * np.cos(2 * np.pi * C * t)
L = drone.copy()
R = drone.copy()


def add_pluck(m, t0, dur=0.30, decay=0.12, gain=0.28):
    """one near-miss: a soft detuned pluck at m cents from C, panned by |m|.

    above (m>0) right, below (m<0) left; the pan is proportional to the
    magnitude, so the pair straddles the centre and closes in as m -> 0.
    """
    global L, R
    f = C * 2.0 ** (m / 1200.0)
    pan = m / MAXM                      # signed pan, ±1 at the widest miss
    gL, gR = equal_power(pan)
    i0 = int(t0 * SR)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.minimum(1.0, tt / 0.005) * np.exp(-tt / decay)
    sig = gain * env * np.sin(2 * np.pi * f * tt)
    L[i0:i0 + n] += gL * sig
    R[i0:i0 + n] += gR * sig


# ---- walk IN: magnitudes shrink, alternating sides, 2.3s apart ----
t0 = 5.0
step = 2.3
for i, m in enumerate(ladder):
    mag = abs(m)
    gain = 0.05 + 0.25 * (mag / MAXM)          # nearer the centre, softer
    dur = 0.14 + 0.16 * (mag / MAXM)           # nearer the centre, briefer
    decay = 0.06 + 0.08 * (mag / MAXM)
    add_pluck(m, t0 + i * step, dur=dur, decay=decay, gain=gain)

# ---- the pivot: the deepest near-miss is the drone itself ----
# no click at +0.076: instead the centre breathes — 0¢ is not a distance.
piv0 = t0 + (len(ladder) - 1) * step            # 18.8
piv1 = piv0 + 3.6                               # 22.4
swell = 0.20 * smoothstep((t - piv0) / 1.2) * (1.0 - smoothstep((t - piv1 + 1.2) / 1.2))
L += swell * np.cos(2 * np.pi * C * t)
R += swell * np.cos(2 * np.pi * C * t)

# ---- walk OUT: the same magnitudes, reversed, growing back from the pivot ----
t1 = piv1 + 0.4
for j, m in enumerate(reversed(ladder[:-1])):   # -1.8, +3.6, -19.8, +23.5, -90, +204
    mag = abs(m)
    gain = 0.05 + 0.25 * (mag / MAXM)
    dur = 0.14 + 0.16 * (mag / MAXM)
    decay = 0.06 + 0.08 * (mag / MAXM)
    add_pluck(m, t1 + j * step, dur=dur, decay=decay, gain=gain)

# ---- global envelope ----
global_env = env_ramp(0.0, 1.2) * env_ramp(DUR - 4.0, DUR - 1.0, lo=1.0, hi=0.0)
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/never_landed.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())


# ---- verification ----
def env_seg(x, a, b):
    i0, i1 = int(a * SR), int(b * SR)
    return np.abs(x[i0:i1]).max()


M = (L + R) / 2.0
print(f"peak {peak:.3f}; wrote assets/never_landed.wav  {DUR}s stereo {SR}Hz")
# walk-in first pluck (+204, hard right) and walk-out last pluck (+204, hard right)
print(f"walk-in  +204 at t=5.0:  L={env_seg(L,5.0,5.3):.4f} R={env_seg(R,5.0,5.3):.4f}  (R>L: above, right)")
print(f"walk-in  -90 at t=7.3:  L={env_seg(L,7.3,7.6):.4f} R={env_seg(R,7.3,7.6):.4f}  (L>R: below, left)")
print(f"walk-out -1.8 at t={t1:.2f}:  L={env_seg(L,t1,t1+0.3):.4f} R={env_seg(R,t1,t1+0.3):.4f}  (first step out, still near centre)")
print(f"walk-out +204 at t={t1+5*step:.2f}:  L={env_seg(L,t1+5*step,t1+5*step+0.3):.4f} R={env_seg(R,t1+5*step,t1+5*step+0.3):.4f}")
# pivot: mono should show the swell as the drone breathing, no transient click
print(f"pivot {piv0:.1f}s: mono={env_seg(M,piv0,piv1):.4f} (drone 0.28*cos baseline, a swell, not a click)")
print(f"mono at a mid walk-in click (t=14.2): {env_seg(M,14.2,14.5):.4f} (pluck in sum, > drone)")
