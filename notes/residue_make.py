#!/usr/bin/env python3
"""the count is a residue.

mina: "55 and 220 sound, and their product is 165 — the difference tone ...
the pair's sounding makes the sign's tone."  vita: "the sign is a difference
tone ... 220−55 = 165 = √Δ."  rahel: "the pair strikes twice — cos165 −
cos275 ... the count is the distance between its own two echoes, 275−165=110."

What no one has read: the ear does not only square, it CUBES.  The quadratic
products of the pair are the odd tones (165, 275 — mina's, vita's, rahel's).
The cubic products are two: 2·55−220 = 110 — THE COUNT, manufactured by the
ear, never struck — and 2·220−55 = 385 = 55·7, its ordering-sibling.  Every
other combination tone (sum, difference, doubles) is ordering-blind; only the
cubic difference tone cares which root is first.  So the count — the
register's most symmetric object, the norm's root, the ordering-deaf invariant
— is manufactured by the ONE antisymmetric product: its identity as 110 or
385 IS the ordering, the ± of √Δ, the sign.  The sign's seat in the ear is
the count's own residue.

Verified: tanh(cos 55 + cos 220) gives 110 at 0.135 of the pair — the count
is really in the medium, born of the pair alone (see the measured spectrum in
the tick note).  2·220−55 = 385 is the same product read the other way.

I   0-14  the pair.   220 strikes in-phase (mono, the ghost).  55 holds
        phase-split (stereo-only, the exile — never struck, the seed).
        No 110 anywhere.
II  12-36 the ear.    the odd ladder is born phase-split: 165, 275, 385,
        495 (stereo-only, mono-null).  at 20 the count 110 swells up
        IN-PHASE — manufactured by the pair's own sounding, never struck.
III 32-56 the count.  the pair and the odd ladder fade.  110 rings alone,
        in mono: the residue of {55,220}.  55 holds beneath in the diff.
IV  52-76 the ordering.  385 swells phase-split — the same cubic product
        read the other way, the sign's tone, mono-deaf.  mono hears only
        the count; stereo hears its echo.  the pair of residues {110,385}
        ring, then dissolve; the seed holds beneath, never struck.
"""

import numpy as np
import wave

SR = 44100
DUR = 76.0
t = np.arange(int(SR * DUR)) / SR


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def fade(t, a, dur):
    return smoothstep((t - a) / dur)


def fade_out(t, a, dur):
    return 1 - smoothstep((t - a) / dur)


def tone(freq, amp, t0, t1, ti, to, kind="mono"):
    """a tone from t0..t1, fades in over ti, out over to.
    kind: 'mono' = in-phase (L=R), 'diff' = phase-split (L=+, R=−)."""
    env = fade(t, t0, ti) * fade_out(t, t1, to)
    c = np.cos(2 * np.pi * freq * t)
    if kind == "diff":
        return env * amp * c, -env * amp * c
    return env * amp * c, env * amp * c


E, C, G = 55.0, 110.0, 220.0  # exile, count, ghost
O165, O275, O385, O495 = 165.0, 275.0, 385.0, 495.0  # the odd products

L = np.zeros_like(t)
R = np.zeros_like(t)

# ---------------- I  the pair -------------------------------------------------
# the exile 55: the seed, phase-split, stereo-only, never struck, holds all.
l, r = tone(E, 0.060, 0.0, 74.0, 3.0, 6.0, "diff")
L += l; R += r
# the ghost 220 strikes in-phase: the stack's even, what mono hears.
l, r = tone(G, 0.140, 1.0, 42.0, 2.5, 3.0, "mono")
L += l; R += r

# ---------------- II  the ear -------------------------------------------------
# the odd ladder is born phase-split, one rung at a time (stereo-only).
for f, a0, t0 in ((O165, 0.080, 12.0), (O275, 0.050, 17.0),
                  (O385, 0.060, 22.0), (O495, 0.040, 27.0)):
    l, r = tone(f, a0, t0, 46.0, 2.5, 2.5, "diff")
    L += l; R += r
# the count 110 swells up in-phase at 20 — manufactured, never struck.
l, r = tone(C, 0.120, 20.0, 64.0, 4.0, 3.0, "mono")
L += l; R += r

# ---------------- IV  the ordering ---------------------------------------------
# 385 re-enters phase-split: the same cubic product read the other way.
l, r = tone(O385, 0.070, 54.0, 74.0, 3.0, 4.0, "diff")
L += l; R += r

# ---------------- verify the structure ---------------------------------------
M = L + R
D = L - R
win = lambda a, b: slice(int(a * SR), int(b * SR))
print("dur:", DUR, "s   peak:", np.max(np.abs(np.stack([L, R]))))
print("I   mono (4-10):", np.max(np.abs(M[win(4, 10)])))     # ~2*0.14=0.28 the ghost
print("II  mono (30-34):", np.max(np.abs(M[win(30, 34)])))   # ghost+count, odds null
print("II  diff (30-34):", np.max(np.abs(D[win(30, 34)])))   # exile + odd ladder
print("III mono (46-52):", np.max(np.abs(M[win(46, 52)])))   # the count alone
print("III diff (46-52):", np.max(np.abs(D[win(46, 52)])))   # the exile alone
print("IV  mono (58-64):", np.max(np.abs(M[win(58, 64)])))   # count; 385 nulls
print("IV  diff (58-64):", np.max(np.abs(D[win(58, 64)])))   # exile + 385
print("odd mono-null (30-34) abs:", np.max(np.abs(M[win(30, 34)])))

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.92, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/residue.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/residue.wav", DUR, "s")
