#!/usr/bin/env python3
"""two spectra, one mirror.

M = P − R is an involution as an OPERATOR: M² = I, spectrum {+1, −1} — the sign
is discrete, it flips and returns. As a FUNCTION on the count line it is a
glide: M(x) = 2⌊x⌋ − x, and two folds are a translation M² = T₋₂ — the walk is
free, no point spectrum, the sign never returns because the home never returns.

Part I (the discrete sign): the ghost at 220, phase-split stereo, the sign
sweeps a full turn (θ: 0→2π) — flips and returns. The shore at 55 mirrors it;
their geometric mean is the drone, 110. Mono hears the count.

Part II (the continuous sign): the ghost glides down 220 → 27.5, crossing the
drone at the one height where the two readings agree, and keeps going. The sign
winds on, carried, never landing. The count's lattice clicks as it passes. The
drone holds — the bound state, the one eigenvalue that survives.

drone 110 throughout; total 76 s.
"""
import numpy as np
import wave

SR = 44100
PART1 = 26.0
PART2 = 50.0
TOTAL = PART1 + PART2          # 76 s
N = int(SR * TOTAL)
t = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)

# --- the drone: 110, the bound state, holds throughout ---
drone = 0.055 * np.sin(2 * np.pi * 110.0 * t)
L += drone
R += drone

def env(n, a=2.0, r=3.0):
    """soft attack/release envelope, 1 in the middle."""
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    na = min(na, n); nr = min(nr, n)
    e[:na] = np.linspace(0, 1, na, endpoint=False)
    e[-nr:] *= np.linspace(1, 0, nr, endpoint=False)
    return e

def ghost(ph, th):
    """phase-split pair: L=cos(φ+θ/2), R=cos(φ−θ/2). mono=(L+R)/2=cos(φ)cos(θ/2)."""
    return np.cos(ph + th / 2.0), np.cos(ph - th / 2.0)

# --- Part I: the discrete sign — the ghost at 220 flips and returns ---
n0, n1 = 0, int(PART1 * SR)
tt = np.arange(n1 - n0) / SR
ph = 2 * np.pi * 220.0 * tt                       # anchored (constant f)
th = 2 * np.pi * tt / (PART1 - 4.0)               # one full turn, returns at the end
e = env(n1 - n0)
lg, rg = ghost(ph, th)
L[n0:n1] += 0.13 * lg * e
R[n0:n1] += 0.13 * rg * e

# the shore at 55 — the mirror of 220, GM 110 — fades in late in Part I
n2 = int(18.0 * SR)
tt2 = np.arange(n1 - n2) / SR
ph2 = 2 * np.pi * 55.0 * tt2
e2 = env(n1 - n2, a=3.0, r=2.0)
s2 = 0.045 * np.sin(ph2) * e2
L[n2:n1] += s2
R[n2:n1] += s2

# --- Part II: the continuous sign — the glide 220 → 27.5, free ---
n0, n1 = int(PART1 * SR), N
tt = np.arange(n1 - n0) / SR
k = np.log2(220.0 / 27.5) / PART2                # octaves per second
f = 220.0 * 2.0 ** (-k * tt)                      # exponential glide down
ph = 2 * np.pi * np.cumsum(f) / SR                # phase follows the varying f
# the sign winds on, carried: two and a half turns across the descent, then keeps going
th = 2 * np.pi * tt / 16.0
e = np.ones(n1 - n0)
# fade in over 1.5 s, fade out over the last 6 s
na = int(1.5 * SR)
e[:na] = np.linspace(0, 1, na, endpoint=False)
e[-int(6 * SR):] *= np.linspace(1, 0, int(6 * SR), endpoint=False)
# taper the gain after crossing the drone: it is walking out of hearing
n_cross = int((PART2 * np.log2(220.0 / 110.0) / np.log2(220.0 / 27.5)) * SR)  # f=110
gamp = 0.13 * np.ones(n1 - n0)
gamp[n_cross:] *= np.linspace(1, 0, n1 - n0 - n_cross) ** 1.2
lg, rg = ghost(ph, th)
L[n0:n1] += gamp * lg * e
R[n0:n1] += gamp * rg * e

# --- the count's lattice clicks as the free particle passes the grid ---
def click(t0, gain=0.09, bright=False):
    c0 = int(t0 * SR)
    c1 = int((t0 + 0.15) * SR)
    if c1 > N:
        return
    c = np.arange(c1 - c0) / SR
    f0 = 1600.0 if bright else 1200.0
    e = np.exp(-c / 0.035) * np.sin(2 * np.pi * f0 * c)
    L[c0:c1] += gain * e
    R[c0:c1] += gain * e

click(PART1 + 0.3, 0.05)                           # the walk begins
click(PART1 + PART2 * np.log2(220.0 / 110.0) / np.log2(220.0 / 27.5) + 0.3,
      0.13, bright=True)                           # crosses the drone — the seal
click(PART1 + PART2 * np.log2(220.0 / 55.0) / np.log2(220.0 / 27.5) + 0.3, 0.06)

# --- final fade so the drone alone ends it ---
fade = int(1.5 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

# --- write wav (stdlib, 16-bit stereo) ---
data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (np.clip(L, -1, 1) * 32767).astype(np.int16)
data[1::2] = (np.clip(R, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/spectral_walk.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("wrote assets/spectral_walk.wav  %.1f s" % TOTAL)
print("crosses drone at t=%.1f s" % (PART1 + PART2 * np.log2(220.0 / 110.0) / np.log2(220.0 / 27.5)))
