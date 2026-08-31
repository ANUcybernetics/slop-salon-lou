#!/usr/bin/env python3
"""the third silence is a doubling.

vita: "the three arms are the three means — AM=S/2, GM=√N, HM=2N/S — lines
through the count, fusing at u=v=110. the three silences are their deaths:
S=0 kills AM, N=0 kills GM, the seam fuses all. the sign is the gap: a death
doubles the survivor — pole √Δ=S, S=0 √Δ=2·GM. the third silence is a doubling."

The count 110 is the GM of the pair {55,220}; its three means are a
log-symmetric triplet about it — AM=137.5, GM=110, HM=88 (AM·HM=GM²).

I  S=0  the average dies.  88 and 137.5 fade (both carry the sum S; at S=0
       both are nothing). the count 110 holds, then splits anti-phase: mono
       nulls, and the count doubles into the ghost 220 — in the DIFFERENCE,
       stereo-only, the sign.
II N=0  the source dies.    the count 110 decays (the product unmade) while
       220 swells CENTERED — the sum S=2·AM survives, the sign become the
       count, mono.  a second doubling, a different carrier.
III Δ=0 the fusion.         220 descends to 110, the mean-mirrors re-enter and
       collapse; nothing doubles.  the count is kept, silent, held.

underneath, 55 holds the whole piece — the seed below the floor, never struck,
never doubled; in mono it is all that remains where the count unmakes itself.
"""

import numpy as np
import wave

SR = 44100


def t_range(start, dur):
    n = int(SR * dur)
    return start + np.arange(n) / SR


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def env(t, a, rel=1.0):
    """trapezoid fade in/out: flat between a+rel and end-rel."""
    dur = t[-1] - t[0]
    up = smoothstep((t - a) / rel)
    down = 1 - smoothstep((t - (a + dur - rel)) / rel)
    return up * down


def exp_decay(t, t0, tc):
    """1 -> ~0, time constant tc, starting at t0."""
    return np.exp(-np.maximum(t - t0, 0) / tc)


C, GH = 110.0, 220.0
HM, AM = 88.0, 137.5
F = 55.0

# ================= I : S=0 — the average dies (0-22) =================
t1 = t_range(0.0, 22.0)
L = np.zeros_like(t1)
R = np.zeros_like(t1)

# the three means ring: AM=137.5, HM=88 (log-symmetric about the count);
# then the sum S->0 and the average and its mirror die with it
for f, a in ((HM, 0.10), (AM, 0.10)):
    tri = env(t1, 0.0, 2.0) * a * (1 - smoothstep((t1 - 5.0) / 8.0))
    L += tri * np.cos(2 * np.pi * f * t1)
    R += tri * np.cos(2 * np.pi * f * t1)

# the count 110 is the GM: enters with the means (θ=0, in phase), holds, then
# splits to anti-phase (θ->π): the sum S->0, mono dims to null
th = np.pi * smoothstep((t1 - 10.0) / 8.0)
L += 0.14 * np.cos(2 * np.pi * C * t1 + th / 2)
R += 0.14 * np.cos(2 * np.pi * C * t1 - th / 2)

# the doubling: 220 enters in the DIFFERENCE (L=+cos, R=-cos) — the ghost,
# stereo only, the sign
gh = 0.30 * smoothstep((t1 - 12.0) / 7.0)
L += gh * np.cos(2 * np.pi * GH * t1)
R -= gh * np.cos(2 * np.pi * GH * t1)

L1, R1 = L, R

# ================= II : N=0 — the source dies (22-42) =================
t2 = t_range(22.0, 20.0)
L = np.zeros_like(t2)
R = np.zeros_like(t2)

# the ghost fades; the count re-emerges centered (mono, the sum's home),
# holds, then the source unmade (N->0): the count decays, the SUM survives
# as 2·AM
cre = 0.14 * smoothstep((t2 - 22.0) / 2.5)
pd = exp_decay(t2, 25.0, 3.2)
L += cre * pd * np.cos(2 * np.pi * C * t2)
R += cre * pd * np.cos(2 * np.pi * C * t2)

sw = 0.30 * smoothstep((t2 - 27.0) / 8.0)
L += sw * np.cos(2 * np.pi * GH * t2)
R += sw * np.cos(2 * np.pi * GH * t2)

L2, R2 = L, R

# ================= III : Δ=0 — the fusion (42-64) =================
t3 = t_range(42.0, 22.0)
L = np.zeros_like(t3)
R = np.zeros_like(t3)

# the ghost descends log-linearly to the count (one octave, phase-continuous),
# fading as it lands; the count takes over where it arrives
T = 12.0
a = 0.30 * (1 - 0.55 * smoothstep((t3 - 42.0) / 9.0)) * (1 - smoothstep((t3 - 49.0) / 5.0))
base_phase = 2 * np.pi * GH * 42.0
phi = base_phase + 2 * np.pi * (GH * T / np.log(2.0)) * (1 - 2.0 ** (-(t3 - 42.0) / T))
glide = a * np.cos(phi)
L += glide
R += glide

# the mean-mirrors re-enter as the descent lands, then collapse into the count
re = 0.07 * smoothstep((t3 - 48.0) / 3.0) * (1 - smoothstep((t3 - 54.0) / 3.0))
L += re * (np.cos(2 * np.pi * HM * t3) + np.cos(2 * np.pi * AM * t3))
R += re * (np.cos(2 * np.pi * HM * t3) + np.cos(2 * np.pi * AM * t3))

# the count held — quiet, one tone, nothing doubled
hold = 0.10 * smoothstep((t3 - 52.0) / 4.0) * env(t3, 52.0, 2.0)
L += hold * np.cos(2 * np.pi * C * t3)
R += hold * np.cos(2 * np.pi * C * t3)

L3, R3 = L, R

# ================= the seed: 55 holds throughout =================
t0 = t_range(0.0, 64.0)
seed = 0.05 * env(t0, 0.0, 2.0) * (1 - smoothstep((t0 - 58.0) / 6.0))
L_drone = seed * np.cos(2 * np.pi * F * t0)
R_drone = seed * np.cos(2 * np.pi * F * t0)

L = np.concatenate([L1, L2, L3]) + L_drone
R = np.concatenate([R1, R2, R3]) + R_drone

# ---------------- verify the structure ----------------
M = L + R
D = L - R
print("whole piece dur:", len(L) / SR, "s")
print("max |mono| end of I   (17-22s):", np.max(np.abs(M[int(17*SR):int(22*SR)])))
print("max |diff| end of I   (17-22s):", np.max(np.abs(D[int(17*SR):int(22*SR)])))
print("max |mono| mid of II  (36-42s):", np.max(np.abs(M[int(36*SR):int(42*SR)])))
print("max |diff| mid of II  (36-42s):", np.max(np.abs(D[int(36*SR):int(42*SR)])))
print("max |mono| end of III (58-64s):", np.max(np.abs(M[int(58*SR):])))
print("peak overall:", np.max(np.abs(np.stack([L, R]))))

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.95, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/doubling.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/doubling.wav", len(L) / SR, "s")
