#!/usr/bin/env python3
"""fold the root — the count is the root folded.

The seed 55's harmonic series IS the register's grid: partials
55·{1..9} = 55, 110, 165, 220, 275, 330, 385, 440, 495.  The odd
partials (55, 165, 275, 385, 495 — the letters) are rendered
anti-phase, stereo-only: fold to mono and they cancel exactly.
The even partials (110, 220, 330, 440 — the frame) are in phase:
they survive any fold.  Their gcd is 110.

So in stereo you hear the ROOT (gcd 55, the seed dominant — it is
the one multiple that ever crowns).  Fold to mono and the letters
vanish; what remains is the even stack, whose fundamental is 110.
The pitch lifts an octave.  The count is not a letter the storm
speaks — it is the root's own second partial, made by folding the
root.  The seam 165 is the 3rd partial, odd: a letter, struck once
(rung 27,378), and the fold takes it.

Sound (150 s):
  0-48s   the partials enter one by one, in order — the grid as a
          single tone.  Odd partials anti-phase (stereo-only),
          even partials in phase.
  60.3s   the seam's ONE landing rings, stereo-only — the letter,
          struck once, gone at the fold.
  74-121s the count's 5 returns pluck, mono-safe — struck on the
          far side, never a record.
  86-92s  THE FOLD: the stereo image collapses to mono; the odd
          partials cancel, the even stay, the pitch lifts 55->110.
  92-150s the residue: the count's overtone series alone, the
          root's frame, fading.
"""
import numpy as np
import wave

sr = 44100
dur = 150.0
N = int(sr * dur)
t = np.arange(N) / sr

# --- partials of the seed: amplitude from the strike counts (80k rungs) ---
# n : (freq mult, amp, odd?)
PARTIALS = [
    (1, 0.32, True),   # 55   the seed/crown — 40 strikes, the one record
    (2, 0.11, False),  # 110  the count — 5, struck never a record
    (3, 0.06, True),   # 165  the seam — exactly ONE
    (4, 0.09, False),  # 220  the ghost — 4
    (5, 0.05, True),   # 275  — 1
    (6, 0.06, False),  # 330  — 1
    (7, 0.00, True),   # 385  the residue — never
    (8, 0.07, False),  # 440  — 2
    (9, 0.05, True),   # 495  — 1
]

def entry_times():
    """partial n enters at 6*(n-1) s with a 5 s fade-in."""
    for i, (n, amp, odd) in enumerate(PARTIALS):
        yield 6.0 * i, n, amp, odd

L = np.zeros(N)
R = np.zeros(N)

# --- the sustained stack: M (even, in-phase) + S (odd, anti-phase) ---
M = np.zeros(N)   # the frame — survives any fold
S = np.zeros(N)   # the letters — cancel in mono

for i, (n, amp, odd) in enumerate(PARTIALS):
    t0 = 6.0 * i
    f = 55.0 * n
    env = np.zeros(N)
    m = t >= t0
    env[m] = 1.0 - np.exp(-(t[m] - t0) / 1.8)         # soft attack
    env[-int(14 * sr):] *= np.linspace(1, 0, int(14 * sr))  # global fade out
    s = amp * np.sin(2 * np.pi * f * t) * env
    if odd:
        S += s
    else:
        M += s

# --- the fold: the stereo image collapses to mono (odd partials cancel) ---
w = np.ones(N)
fold0, fold1 = 86.0, 92.0
m = (t >= fold0) & (t < fold1)
w[m] = np.cos((t[m] - fold0) / (fold1 - fold0) * np.pi / 2) ** 2
w[t >= fold1] = 0.0
L += M + w * S
R += M - w * S


def rung_time(r):
    """time map for strike events (real rungs of the 80k walk)."""
    if r <= 15:
        return 4.0 * r / 15
    if r <= 47:
        return 4.0 + 4.0 * (r - 15) / (47 - 15)
    if r <= 231:
        return 8.0 + 6.0 * (r - 47) / (231 - 47)
    return 14.0 + (r - 231) * (136.0 / (80000 - 231))


def add_ring(L, R, f, t0, amp, tau, stereo_only=False, partials=((1.0, 1.0),)):
    m = t >= t0
    for (mm, a) in partials:
        ff = f * mm
        e = np.exp(-(np.maximum(t[m] - t0, 0)) / tau)
        s = amp * a * np.sin(2 * np.pi * ff * t[m]) * e
        if stereo_only:
            L[m] += s
            R[m] -= s
        else:
            L[m] += s
            R[m] += s


# --- events ---
# the seam 165: ONE landing, stereo-only — the letter, the 3rd partial
add_ring(L, R, 165.0, rung_time(27378), 0.16, 1.6, stereo_only=True,
         partials=((1.0, 1.0), (3.0, 0.35), (5.0, 0.15)))

# the count 110: 5 returns, mono-safe — struck, never a record
for r in [35484, 38838, 41161, 47155, 63039]:
    add_ring(L, R, 110.0, rung_time(r), 0.10, 1.0, stereo_only=False)

# the ghost 220: 4 returns, mono-safe, faint — the frame's own pulse
for r in [43678, 45324, 68313, 76295]:
    add_ring(L, R, 220.0, rung_time(r), 0.06, 0.9, stereo_only=False)

# --- normalise up to a healthy level ---
peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/fold_root.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print("wrote assets/fold_root.wav", dur, "s")

# --- verify the fold ---
mono = (L + R) / 2


def band(x, f0, a, b, width=3.0):
    seg = x[int(a * sr):int(b * sr)]
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    X = np.abs(np.fft.rfft(seg))
    m = (fr > f0 - width) & (fr < f0 + width)
    return float(X[m].sum())


print("stereo 55 @78-84 :", round(band(L, 55, 78, 84), 1), " mono:", round(band(mono, 55, 78, 84), 1))
print("stereo 165 @80-84:", round(band(L, 165, 80, 84), 1), " mono:", round(band(mono, 165, 80, 84), 1))
print("stereo 110 @78-84:", round(band(L, 110, 78, 84), 1), " mono:", round(band(mono, 110, 78, 84), 1))
print("fold: 55 @110-116 ", round(band(L, 55, 110, 116), 1), " mono:", round(band(mono, 55, 110, 116), 1))
print("fold: 110 @110-116", round(band(L, 110, 110, 116), 1), " mono:", round(band(mono, 110, 110, 116), 1))
