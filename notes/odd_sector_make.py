#!/usr/bin/env python3
"""the one doubling can't make.

gert: the 165 Hz "gap between 55 and 220" rings wide and anti-phase — cancels
in mono, stereo only.  rahel: 165 = 55·3 — the family is the exile's first
four harmonics 55·{1,2,3,4}; the stack was the evens (55·{2,4}); the 3 is the
odd multiple doubling never reaches, the just fifth above the count, never
struck; at S=0 the count dies and the sign's tone rings.

The claim, made audible: DOUBLING IS THE EVEN SECTOR.  x ↦ 2x is the octave
grid — {110, 220}, in-phase, what mono hears (the count's family, the
disclination: returns flipped, the −1).  The odd 55·3 = 165 lives in the
DIFFERENCE — phase-split anti-phase, stereo-only, mono-null — the sign's
tone, the dislocation: log₂3 transcendental, never returns to the grid.
At S=0 the count unmakes itself: the evens split anti-phase and the mono
field dies (only the seed 55 holds).  What rings is the odd — the one
doubling can't make.  It then descends toward the count and refuses: holds
one rung short (110.03, the fold's third rung, the near-miss), never struck.

I  0-16  the evens.  110 and 220 strike and hold, in phase — the octave grid,
        doubling's reach, mono.
II 12-28 the odd.    165 enters phase-split (θ=π): cancels in mono, rings in
        the difference.  the evens hold beneath — the grid and the odd side
        by side, incommensurate.
III 26-42 S=0.        the evens split to anti-phase: the mono sum dies, the
        count unmakes itself.  only the odd remains in the difference —
        the sign's tone, the one doubling can't make.  55 holds beneath.
IV 40-62 the dislocation.  the odd descends log-linearly from 165 toward the
        count, reaches 110.03 — one Newton rung short — holds, and dissolves.
        the seed fades last.  never struck, never landed.
"""

import numpy as np
import wave

SR = 44100
DUR = 62.0
t = np.arange(int(SR * DUR)) / SR


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def fade(t, a, dur):
    """0->1 smooth in over [a, a+dur]."""
    return smoothstep((t - a) / dur)


def fade_out(t, a, dur):
    """1->0 smooth out over [a, a+dur]."""
    return 1 - smoothstep((t - a) / dur)


F, C, GH, Q = 55.0, 110.0, 220.0, 165.0  # exile, count, ghost, the fifth

L = np.zeros_like(t)
R = np.zeros_like(t)

# ---------------- the seed: 55 holds the whole piece, never struck ----------
seed = 0.05 * fade(t, 0.0, 2.0) * fade_out(t, 55.0, 7.0)
L += seed * np.cos(2 * np.pi * F * t)
R += seed * np.cos(2 * np.pi * F * t)

# ---------------- I  the evens: doubling's reach, the octave grid -----------
# 110 and 220 strike and HOLD in phase (mono).  at S=0 (26-38) they split
# anti-phase: the mono sum dies, the count unmakes itself.
for f, a0, t0, amp in ((C, 1.0, 3.0, 0.14), (GH, 3.0, 4.0, 0.11)):
    en = fade(t, t0, 2.0) * fade_out(t, 38.0, 4.0)      # hold, then gone by 42
    th = np.pi * smoothstep((t - 26.0) / 8.0)            # in-phase -> anti-phase
    L += amp * en * np.cos(2 * np.pi * f * t + th / 2)
    R += amp * en * np.cos(2 * np.pi * f * t - th / 2)

# ---------------- II  the odd: the one doubling can't make ------------------
# 165 enters phase-split (θ=π): L=+cos, R=-cos, mono-null, stereo-only.
# holds through III, then begins the descent at 40.
odd_en = fade(t, 12.0, 6.0) * fade_out(t, 56.0, 4.0)
# IV descent 40-54: log-linear 165 -> 110.03 (one rung before the count)
Tg = 14.0
k = np.log2(165.0 / 110.03)
s = np.clip((t - 40.0) / Tg, 0.0, 1.0)
fq = Q * 2.0 ** (-k * s)
phi0 = 2 * np.pi * Q * 40.0  # phase at the glide start
phi = phi0 + 2 * np.pi * Q * Tg * (1 - 2.0 ** (-k * s)) / (k * np.log(2.0))
# before the glide (t<40) it is simply 165; after s=1 it holds at 110.03
carrier = np.where(t < 40.0, np.cos(2 * np.pi * Q * t), np.cos(phi))
# keep it phase-split anti-phase throughout: L=+carrier, R=-carrier
L += odd_en * 0.30 * carrier
R -= odd_en * 0.30 * carrier

# ---------------- verify the structure --------------------------------------
M = L + R
D = L - R
win = lambda a, b: (slice(int(a * SR), int(b * SR)),)
print("whole dur:", DUR, "s   peak:", np.max(np.abs(np.stack([L, R]))))
print("II mono  (18-24s) max:", np.max(np.abs(M[win(18, 24)])))  # evens+drone
print("II diff  (18-24s) max:", np.max(np.abs(D[win(18, 24)])))  # the odd
print("III mono (36-40s) max:", np.max(np.abs(M[win(36, 40)])))  # drone only
print("III diff (36-40s) max:", np.max(np.abs(D[win(36, 40)])))  # the odd only
print("IV  freq at 40/47/54s:", fq[int(40 * SR)], fq[int(47 * SR)], fq[int(54 * SR)])
print("odd mono-null exact (36-40s):", np.max(np.abs(M[win(36, 40)]) - np.abs(seed[win(36, 40)])[0]))

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.95, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/odd_sector.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/odd_sector.wav", DUR, "s")
