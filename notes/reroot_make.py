#!/usr/bin/env python3
"""the count's half-integers — re-read the count as the root.

The storm closed on "made, never struck": the count 110 is the seed's
self-sum, the manufactured octave, the projection's fixed point.  This
piece takes the next step the register kept implying and never rung:
re-read the count AS A ROOT.

The frame of the seed 55 IS the harmonic series of the count 110 —
{110,220,330,440} = the even partials of 55 = the integers of 110.
Re-rooted, everything above 110 is the count's own series (the frame,
MADE, mono-safe, never struck).  And the seed's ODD partials — the
letters, 55, 165, 275, 385, 495… — become the count's HALF-INTEGERS:
0.5x, 1.5x, 2.5x, 3.5x…  the gaps in the root's series, the where the
fold forgets (STRUCK, stereo-only).  The exile 55 is the subharmonic,
a half below the fundamental.

Fold to mono and the half-integers cancel: the count keeps only what
it is — its own series, 110·{1,2,3,4,5,6,7,8}.  The recursion is the
doubling ladder read upward: every count is the next root.

movements:
  0-28   the root: 110 alone, the count made
  28-60  the half-integers: the letters ring and hold, stereo-only
  60-100 the integers join: the frame sustains, mono-safe
  100-152 full series; the ladder re-roots upward — 220, 440, 880 ring
  152-155 the fold: stereo -> mono, half-integers cancel, the frame remains
"""
import numpy as np
import wave

sr = 44100
dur = 168.0
N = int(sr * dur)
t = np.arange(N) / sr

# M = mono-safe (the count's integers: the frame, MADE)
# S = stereo-only (the count's half-integers: the letters, STRUCK)
M = np.zeros(N)
S = np.zeros(N)

COUNT = 110.0   # the count, re-read as the root
END = 166.0


def seg(t0, t1):
    return (t >= t0) & (t < t1)


def env_attack(t0, t1, atk, rel):
    m = seg(t0, t1)
    tt = t[m] - t0
    e = np.minimum(tt / atk, 1.0)
    e *= np.minimum((t1 - t[m]) / rel, 1.0)
    return m, np.clip(e, 0, 1)


def drone(M, t0, t1, f, amp, trem=0.0, double=0.3):
    """a sustained tone — the count and its frame, the made series."""
    m, e = env_attack(t0, t1, 3.0, 5.0)
    tt = t[m] - t0
    s = np.sin(2 * np.pi * f * t[m])
    if trem:
        s *= 1.0 + trem * np.sin(2 * np.pi * 0.09 * tt)
    M[m] += amp * s * e
    if double:
        M[m] += double * amp * np.sin(2 * np.pi * 2 * f * t[m]) * e


def letter(S, t0, f, amp, tau, sustain=0.5):
    """a struck half-integer that holds softly — stereo-only, the where
    the fold forgets.  PURE sine: no overtones, so the fold cancels it
    exactly and the integers keep only their own mono content.
    (the letters' octaves DO land on the frame — the exile's is the
    count itself — but that doubling is what the fold forgets.)"""
    t1 = END
    m = seg(t0, t1)
    tt = t[m] - t0
    env = np.exp(-tt / tau) * (1 - sustain) + sustain
    env *= np.minimum(tt / 2.0, 1.0)               # attack
    env *= np.minimum((t1 - t[m]) / 5.0, 1.0)      # release
    S[m] += amp * np.sin(2 * np.pi * f * tt) * env


def ladder_ring(M, t0, f, amp, tau):
    """a count rung as the next root — mono-safe, made."""
    m = seg(t0, t0 + 16)
    tt = t[m] - t0
    e = np.exp(-tt / tau)
    M[m] += amp * np.sin(2 * np.pi * f * tt) * e
    M[m] += 0.4 * amp * np.sin(2 * np.pi * 2 * f * tt) * e


# --- phase 1: the root (0-28) — the count alone, holding all piece ---
drone(M, 0.0, END, COUNT, amp=0.080, trem=0.15)

# --- phase 2: the half-integers (28-60) — the letters, stereo-only ---
LETTERS = [  # (multiple of count, entry time) — 0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5
    (0.5, 28.0), (1.5, 36.0), (2.5, 44.0), (3.5, 52.0),
    (4.5, 60.0), (5.5, 66.0), (6.5, 68.0), (7.5, 70.0),
]
for mult, t0 in LETTERS:
    letter(S, t0, COUNT * mult, amp=0.070, tau=6.0, sustain=0.55)

# --- phase 3: the integers join (60-100) — the frame, mono-safe ---
INTEGERS = [  # (multiple, entry time) — the count's series, 2..8
    (2.0, 60.0), (3.0, 68.0), (4.0, 76.0), (5.0, 84.0),
    (6.0, 92.0), (7.0, 100.0), (8.0, 104.0),
]
for mult, t0 in INTEGERS:
    drone(M, t0, END, COUNT * mult, amp=0.042 / max(mult, 2.0), double=0.0)

# --- phase 4: the ladder (108-150) — the count re-roots upward ---
for t0, f in [(108.0, 220.0), (120.0, 440.0), (132.0, 880.0)]:
    ladder_ring(M, t0, f, amp=0.090, tau=5.0)

# --- phase 5: the fold (152-155) — stereo width -> 0 ---
w = np.ones(N)
f0, f1 = 152.0, 155.5
m = (t >= f0) & (t < f1)
w[m] = np.cos((t[m] - f0) / (f1 - f0) * np.pi / 2) ** 2
w[t >= f1] = 0.0

L = M + w * S
R = M - w * S

# global fade out
fade0 = 158.0
m = t >= fade0
L[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))
R[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/reroot.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print("wrote assets/reroot.wav", dur, "s")

# --- verify the fold ---
mono = (L + R) / 2


def band(x, f0, a, b, width=4.0):
    segx = x[int(a * sr):int(b * sr)]
    fr = np.fft.rfftfreq(len(segx), 1 / sr)
    X = np.abs(np.fft.rfft(segx))
    m = (fr > f0 - width) & (fr < f0 + width)
    return float(X[m].sum())


print("\n-- full series before the fold (148-152), stereo hears letters + frame --")
for f, lbl in [(55, "0.5x exile"), (165, "1.5x seam"), (275, "2.5x letter"),
               (110, "1x count"), (220, "2x frame"), (330, "3x frame"),
               (440, "4x frame"), (550, "5x frame")]:
    print(f"  {lbl:<14} stereo:", round(band(L, f, 148, 152), 1),
          " mono:", round(band(mono, f, 148, 152), 1))

print("\n-- after the fold (156-160): half-integers gone, integers remain --")
for f, lbl in [(55, "exile"), (165, "seam"), (275, "letter"),
               (110, "count"), (220, "2x"), (330, "3x"), (440, "4x")]:
    print(f"  {lbl:<10} stereo:", round(band(L, f, 156, 160), 1),
          " mono:", round(band(mono, f, 156, 160), 1))
