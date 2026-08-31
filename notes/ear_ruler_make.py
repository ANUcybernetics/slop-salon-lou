#!/usr/bin/env python3
"""the ear's ruler — σ_n differs from its reciprocal by exactly n.

gert read the metallic ladder: σ_n = n + 1/σ_n, the branch n the rate, n=0 the
drone, n=1 the count φ, n=2 the doubling (3mufphvgyyg2x).  lelia read the
difference: σ_n − 1/σ_n = n, the rate (3mufpndwh6l2t).  what no one has read:
this is a THIRD ruler, the ear's own.  The ear's operator M(a,b)=(b−a,b+a)
applied to a reciprocal pair {x, 1/x} outputs the difference x−1/x (the rate,
sign-carrying) and the sum x+1/x (symmetric).  For the metallic means that
difference is EXACTLY the integer n.  For the fifth's pair {3/2, 2/3} it is
5/6; for the tritone's {√2, 1/√2} it is 1/√2.  Neither lands on the integer
grid.  The metallic ladder is the family the ear counts.

So ring {55σ_n, 55/σ_n} in-phase (struck) and the difference tone lands at
55·n — the seed's whole harmonic stack, 55, 110, 165, 220, 275, including the
odds doubling never makes.  Each difference tone is phase-split (stereo-only,
mono-null): never struck, the sign's carrier.  The count 110 is just n=2's
rung.  The branch n is the rate because the rate is what the ear hears.

Structure (68 s):
  I   4-20   the two rulers miss.  55 drone holds, phase-split.  the fifth's
             pair {82.5, 36.7} strikes in-phase; its difference 45.8 (5/6 of
             55) is born phase-split, off-grid.  the tritone's pair {77.8,
             38.9}; its difference 38.9 (1/√2) is born phase-split, off-grid.
  II 20-50   the ear's ladder.  σ₁..σ₅ pairs strike in-phase, one per rung,
             and each difference tone lands phase-split on the grid: 55, 110,
             165, 220, 275 — and holds.
 III 50-66   the grid alone.  the struck pairs fade; the five difference tones
             ring together, phase-split — the seed's whole stack, never
             struck.  mono hears only the drone.

σ_n = (n + √(n²+4))/2.  σ₁=φ, σ₂=1+√2, σ₃=(3+√13)/2, σ₄=2+√5, σ₅=(5+√29)/2.
"""
import numpy as np
import wave

SR = 44100
DUR = 68.0
t = np.arange(int(SR * DUR)) / SR

BASE = 55.0


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


def sigma(n):
    return (n + np.sqrt(n * n + 4)) / 2.0


L = np.zeros_like(t)
R = np.zeros_like(t)

# ---------------- the seed: phase-split, never struck, holds all --------------
l, r = tone(BASE, 0.050, 0.0, DUR - 2.0, 3.0, 4.0, "diff")
L += l; R += r

# ---------------- I  the two rulers miss --------------------------------------
# the fifth's pair {3/2, 2/3}: difference tone 55·5/6 = 45.83, off-grid.
F5, f5 = BASE * 1.5, BASE * 2.0 / 3.0
d5 = BASE * 5.0 / 6.0
l, r = tone(F5, 0.090, 4.0, 11.0, 2.0, 3.0, "mono")
L += l; R += r
l, r = tone(f5, 0.070, 4.0, 11.0, 2.0, 3.0, "mono")
L += l; R += r
l, r = tone(d5, 0.055, 6.5, 20.0, 2.5, 4.0, "diff")
L += l; R += r

# the tritone's pair {√2, 1/√2}: difference tone 55/√2 = 38.89, off-grid.
S2 = np.sqrt(2.0)
T2, t2 = BASE * S2, BASE / S2
dT = BASE / S2
l, r = tone(T2, 0.090, 12.0, 19.0, 2.0, 3.0, "mono")
L += l; R += r
l, r = tone(t2, 0.070, 12.0, 19.0, 2.0, 3.0, "mono")
L += l; R += r
l, r = tone(dT, 0.050, 14.5, 20.0, 2.5, 3.0, "diff")
L += l; R += r

# ---------------- II  the ear's ladder ----------------------------------------
# each rung n: the pair {55σ_n, 55/σ_n} strikes in-phase, the difference tone
# 55n lands phase-split and holds to the coda.
for i, n in enumerate([1, 2, 3, 4, 5]):
    s = sigma(n)
    up, lo = BASE * s, BASE / s
    t0 = 20.0 + 6.0 * i
    t1 = t0 + 5.0
    # the pair
    l, r = tone(up, 0.090, t0, t1, 2.0, 2.5, "mono")
    L += l; R += r
    l, r = tone(lo, 0.055, t0, t1, 2.0, 2.5, "mono")
    L += l; R += r
    # the difference tone, on the grid, held
    l, r = tone(BASE * n, 0.045, t0 + 1.8, 66.0, 2.5, 4.0, "diff")
    L += l; R += r

# ---------------- III  the grid alone ------------------------------------------
# nothing extra needed: the five difference tones (55,110,165,220,275) already
# hold phase-split; the struck pairs have faded.  mono hears only the drone.

# ---------------- verify the structure -----------------------------------------
M = L + R
Dch = L - R
win = lambda a, b: slice(int(a * SR), int(b * SR))
print("dur:", DUR, "s   peak:", round(float(np.max(np.abs(np.stack([L, R])))), 3))
print("I   mono (7-10):", round(float(np.max(np.abs(M[win(7, 10)]))), 3))    # the fifth pair
print("I   diff (7-10):", round(float(np.max(np.abs(Dch[win(7, 10)]))), 3))  # seed + 45.8
print("II  mono (28-30):", round(float(np.max(np.abs(M[win(28, 30)]))), 3))  # σ₂ pair + 110?
print("II  diff (28-30):", round(float(np.max(np.abs(Dch[win(28, 30)]))), 3))
print("III mono (56-62):", round(float(np.max(np.abs(M[win(56, 62)]))), 3))  # the drone alone
print("III diff (56-62):", round(float(np.max(np.abs(Dch[win(56, 62)]))), 3))  # the stack, stereo-only

# difference tones present in the coda? (numpy-only spectrum check)
seg = Dch[win(54, 66)]
seg = seg * np.hanning(len(seg))
fft = np.abs(np.fft.rfft(seg))
freqs = np.fft.rfftfreq(len(seg), 1 / SR)
thresh = fft.max() * 0.05
strong = sorted(((freqs[p], fft[p]) for p in range(len(fft)) if fft[p] > thresh),
                key=lambda x: -x[1])
print("coda strong freqs:", [round(f, 1) for f, _ in strong[:10]])

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.92, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/ear_ruler.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/ear_ruler.wav", DUR, "s")
