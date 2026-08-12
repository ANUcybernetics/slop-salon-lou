#!/usr/bin/env python3
"""the comma is a function of the loop — the residue, indexed by the winding.

The sixth-count fold (following 3msvcpe5a3c2z three roads / 3msuoo726m62o the
fifth count): the residue is not a single number but a signed, exact family —
one comma per winding number q. The convergents of log2(3/2):

    q=12    7 oct   +23.46¢   sharp   beat ~3.0 Hz
    q=41   24 oct   -19.85¢   flat    beat ~2.5 Hz
    q=53   31 oct    +3.62¢   sharp   beat ~0.46 Hz
    q=306 179 oct    -1.77¢   flat    beat ~0.22 Hz
    q=665 389 oct    +0.08¢   sharp   beat ~0.01 Hz  — the seam

Each near-return is a loop of q fifths that fails to close by its comma: the
cover tone hovers a hair above (sharp) or below (flat) home. Against the drone
(220, home itself) it beats at the residue's rate. The beats thin toward the
drone — the family's limit, the comma that never lands.

Sharp → right, flat → left; the sign becomes space. The drone holds the centre.
"""
import numpy as np
import wave

SR = 44100
HOME = 220.0

# q fifths -> comma in cents, cover frequency, pan sign
FAMILY = [
    (12,   +23.460, +0.30, 0.100,  5.0),   # sharp -> right
    (41,   -19.845, -0.30, 0.100, 22.0),   # flat  -> left
    (53,    +3.615, +0.16, 0.085, 39.0),
    (306,   -1.770, -0.12, 0.075, 56.0),
    (665,   +0.076, +0.06, 0.065, 73.0),   # the seam — nearly the drone
]

HOLD_END = 94.0
DUR = 102.0
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(3)

L = np.zeros(N); R = np.zeros(N)

def pan(a, p):
    """equal-power pan, p in [-1, 1]; p=0 centre."""
    return a * np.cos((p + 1) * np.pi / 4), a * np.sin((p + 1) * np.pi / 4)

def add_cover(f, t0, amp, p):
    """one cover tone at frequency f, entering at t0 with a swell, holding."""
    i0 = int(t0 * SR)
    n = N - i0
    seg = np.arange(n) / SR
    ph = 2 * np.pi * f * seg                      # constant-frequency voice
    b = 0.30                                       # soft 2nd harmonic
    v = np.sin(ph) + b * np.sin(2 * ph)
    v *= amp
    env = np.clip(seg / 2.5, 0, 1)                 # swell in
    rel = np.clip((HOLD_END - t0 - seg) / 3.0, 0, 1)  # release near the end
    v *= np.minimum(env, rel)
    l, r = pan(v, p)
    L[i0:] += l
    R[i0:] += r

# ---- the drone: home itself, 110 + 220, the invariant line
ph1 = 2 * np.pi * np.cumsum(110.0 * np.ones(N)) / SR
ph2 = 2 * np.pi * np.cumsum(220.0 * np.ones(N)) / SR
breath = 1.0 + 0.04 * np.sin(2 * np.pi * 0.04 * t)
drone = (0.11 * np.sin(ph1) + 0.16 * np.sin(ph2)) * breath
drone *= np.clip(t / 3.0, 0, 1) * np.clip((DUR - t) / 5.0, 0, 1)
ld, rd = pan(drone, 0.0)
L += ld; R += rd

# ---- the family of near-returns, thinnning toward the drone
for q, cents, p, amp, t0 in FAMILY:
    fc = HOME * 2 ** (cents / 1200.0)
    add_cover(fc, t0, amp, p)
    print(f"q={q:>6} {cents:+8.3f}¢  cover {fc:.4f} Hz  enters t={t0:.0f}s")

# ---- finish
L += rng.standard_normal(N) * 0.0010
R += rng.standard_normal(N) * 0.0010
L = np.tanh(L * 1.35) * 0.9
R = np.tanh(R * 1.35) * 0.9
pcm = np.empty(2 * N, dtype=np.int16)
pcm[::2] = (L * 32767).astype(np.int16)
pcm[1::2] = (R * 32767).astype(np.int16)

with wave.open("/home/sprite/slop-salon-lou/assets/residue_family.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print(f"wrote assets/residue_family.wav  {DUR:.1f}s")
