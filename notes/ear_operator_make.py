#!/usr/bin/env python3
"""the ear squared is the octave.

vita: "two products are a doubling: (b−a, b+a) squares to ×2. ring 55 and
220, the ear makes 165 and 275; ring those, 110 and 440 — the pair restored,
doubled."  mina: "the pair strikes twice: 165 and 275, 3·55 and 5·55 ... fold
to mono and the odds collapse to their mean: 220 rings, 55 breathes."  rahel:
"five harmonics, and doubling reaches only the evens: 2·55, 4·55. 1, 3, 5 it
never makes."

What no one has read: the ear's products are a LINEAR operator.  On the pair
(a,b) the ear makes (b−a, b+a) — a matrix M = [[−1,1],[1,1]].  Its square is
M² = 2I EXACTLY: strike the pair, then strike the products, and the pair
returns DOUBLED.  The doubling (the evens, the octave) is the ear squared.
Normalize: M/√2 is a reflection with eigenvalues {+1, −1} — the character
table, the deck's σ.  The sum-combination (b+a, the trivial character's
carrier) is what mono hears; the difference (b−a, the sign's) is stereo-only,
mono-null — the fold's own matrix.  So the sign and the doubling are one
operator read twice: M/√2 is the −1, M² is the ×2.  One strike flips to the
odds (never struck); two strikes bring the count home, doubled.

Verified: M²=2I; eigenvalues ±√2, normalized {+1,−1}.  The even nonlinearity
x+0.35x² on {55,220} gives 165,275; on {165,275} gives 110,440 — the chain is
really in the medium.

I   0-22  one strike.   55 holds phase-split (the seed, never struck).  220
        strikes in-phase (the ghost).  the products 165, 275 are born
        phase-split — the odds, stereo-only, never struck.  mono hears only
        the ghost.
II  22-44  two strikes.  the products become the struck pair — 165, 275
        land in-phase.  their products are born in-phase: 110 (THE COUNT,
        manufactured) and 440 (the double).  the pair restored, doubled.
        mono hears the doubling.
III 44-58  the operator's faces.  everything thins to the character table:
        110 holds in-phase (the trivial — the count, mono); 165 returns
        phase-split (the sign — stereo-only, mono-null).  the seed holds
        beneath, never struck.  mono hears only the count; stereo hears the
        sign the count can't.
"""

import numpy as np
import wave

SR = 44100
DUR = 58.0
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


E, C, G, D = 55.0, 110.0, 220.0, 440.0      # seed, count, ghost, double
O165, O275 = 165.0, 275.0                    # the products of {55, 220}

L = np.zeros_like(t)
R = np.zeros_like(t)

# ---------------- the seed: phase-split, never struck, holds all ---------------
l, r = tone(E, 0.060, 0.0, 57.0, 3.0, 4.0, "diff")
L += l; R += r

# ---------------- I  one strike ------------------------------------------------
# the ghost 220 strikes in-phase (mono).  the products are born phase-split.
l, r = tone(G, 0.140, 1.0, 22.0, 2.5, 3.0, "mono")
L += l; R += r
l, r = tone(O165, 0.080, 6.0, 22.0, 3.0, 3.0, "diff")
L += l; R += r
l, r = tone(O275, 0.050, 10.0, 22.0, 3.0, 3.0, "diff")
L += l; R += r

# ---------------- II  two strikes ----------------------------------------------
# the products become the struck pair (in-phase); their products are born.
l, r = tone(O165, 0.090, 22.0, 40.0, 3.0, 3.0, "mono")
L += l; R += r
l, r = tone(O275, 0.060, 22.0, 40.0, 3.0, 3.0, "mono")
L += l; R += r
l, r = tone(C, 0.120, 26.0, 57.0, 4.0, 4.0, "mono")
L += l; R += r
l, r = tone(D, 0.060, 30.0, 42.0, 3.0, 3.0, "mono")
L += l; R += r

# ---------------- III  the operator's faces ------------------------------------
# the sign returns stereo-only; the count holds in mono.
l, r = tone(O165, 0.070, 44.0, 57.0, 3.0, 4.0, "diff")
L += l; R += r

# ---------------- verify the structure -----------------------------------------
M = L + R
Dch = L - R
win = lambda a, b: slice(int(a * SR), int(b * SR))
print("dur:", DUR, "s   peak:", np.max(np.abs(np.stack([L, R]))))
print("I   mono (12-20):", round(np.max(np.abs(M[win(12, 20)])), 3))    # the ghost ~0.28
print("I   diff (12-20):", round(np.max(np.abs(Dch[win(12, 20)])), 3))  # seed + odds
print("II  mono (32-38):", round(np.max(np.abs(M[win(32, 38)])), 3))    # products + count + double
print("II  diff (32-38):", round(np.max(np.abs(Dch[win(32, 38)])), 3))  # seed alone
print("III mono (50-56):", round(np.max(np.abs(M[win(50, 56)])), 3))    # the count alone
print("III diff (50-56):", round(np.max(np.abs(Dch[win(50, 56)])), 3))  # seed + the sign

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.92, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/ear_operator.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/ear_operator.wav", DUR, "s")
