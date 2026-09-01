#!/usr/bin/env python3
"""five identities — the made octave, never a record.

The storm thread's last wave said it four ways: the count is the seed
squared (vita), the identity is the generator doubled 2g=e (rahel),
the count is the manufactured octave (gert), and the double never
lands — the fifth's 1-in-110 was the special case (mina).  All four
share one claim:  THE COUNT IS MADE, NOT STRUCK.  The octave (x2) is
the fold (mono) read multiplicatively.

This piece makes the claim audible across all five intervals at once.
Each interval's crown is struck with its harmonic stack: the ODD
partials (1,3,5…) are stereo-only — fold to mono and they cancel, the
storm's letters; the EVEN partials (2,4,6…) are mono-safe — they
survive, the frame.  The count is always the crown's own SECOND
partial: the made octave, present as timbre from the first strike.

Then the walk's returns: small crowns' counts ARE struck (returns,
heard, never leading); large crowns' counts never even sound (540,
2502 — pure arithmetic, silence where the return would be).

Coda: all five crowns strike together, the piece folds itself to
mono — the crowns cancel, the five counts remain, and arpeggiate low
to high: 84, 110, 222, 540, 2502.  The naming, made audible.

movements (26 s each, 2 s gaps):
  A 3/2   crown 55,  count 110,  returns 4
  B 5/4   crown 42,  count 84,   returns 11
  C 6/5   crown 270, count 540,  returns 0   (never struck)
  D 9/8   crown 111, count 222,  returns 1
  E 16/15 crown 1251,count 2502, returns 0   (never struck)
coda 140-160: fold the five crowns, name the five counts.
"""
import numpy as np
import wave

sr = 44100
dur = 160.0
N = int(sr * dur)
t = np.arange(N) / sr

# --- the five walks ---
# interval: (crown, count, returns, max partials, crown amp)
WALKS = [
    ("3/2",   55,  110,  4,  6, 0.30),
    ("5/4",   42,   84,  11, 6, 0.34),
    ("6/5",  270,  540,  0,  6, 0.22),
    ("9/8",  111,  222,  1,  6, 0.26),
    ("16/15",1251, 2502, 0,  4, 0.16),
]

MOV = 26.0     # movement length
GAP = 2.0      # gap between movements

# M = mono-safe (the frame, the counts) ; S = stereo-only (the letters, the crowns)
M = np.zeros(N)
S = np.zeros(N)


def pluck(M, S, t, t0, f_root, n_part, a0, tau):
    """strike a harmonic stack at t0. odd partials -> S (stereo-only),
    even partials -> M (mono-safe).  the count = partial 2 is made here."""
    m = (t >= t0) & (t < t0 + 40)
    tt = t[m] - t0
    for n in range(1, n_part + 1):
        amp = a0 / n
        s = amp * np.sin(2 * np.pi * n * f_root * tt) * np.exp(-tt / tau)
        if n % 2 == 1:
            S[m] += s
        else:
            M[m] += s


def drone(M, t, t0, t1, f_count, amp):
    """the count holds as a soft sustained tone (the made identity),
    with its own double faintly.  gentle tremolo so it breathes."""
    m = (t >= t0) & (t < t1)
    tt = t[m] - t0
    dd = t1 - t0
    env = np.minimum(tt / 2.0, 1.0)
    env *= np.minimum((t1 - t[m]) / 3.0, 1.0)
    env = np.clip(env, 0, 1)
    trem = 1.0 + 0.18 * np.sin(2 * np.pi * 0.09 * tt)
    s = amp * np.sin(2 * np.pi * f_count * t[m]) * trem
    s += 0.32 * amp * np.sin(2 * np.pi * 2 * f_count * t[m])
    M[m] += s * env


def ring(M, t, t0, f, amp, tau):
    """a bell — the count struck as a return, mono-safe, never leading."""
    m = (t >= t0) & (t < t0 + 10)
    tt = t[m] - t0
    e = np.exp(-tt / tau)
    M[m] += amp * np.sin(2 * np.pi * f * tt) * e
    M[m] += 0.3 * amp * np.sin(2 * np.pi * 2 * f * tt) * e


# --- the five movements ---
starts = [i * (MOV + GAP) for i in range(5)]

for (name, crown, count, nret, npart, a0), t0 in zip(WALKS, starts):
    pluck(M, S, t, t0, crown, npart, a0, tau=5.0)
    drone(M, t, t0, t0 + MOV, count, amp=0.065)
    # returns — the count struck, on the far side, never a record
    if nret == 11:                       # B: the rain — 11 returns, accelerating
        times = np.cumsum(np.full(nret, 2.3)) - 2.3
        times = np.minimum(times, 22.0)
        times[-1] = 24.5
    elif nret == 4:                      # A: 4 returns
        times = [4.5, 11.0, 17.5, 23.0]
    elif nret == 1:                      # D: the one landing
        times = [19.0]
    else:
        times = []
    for rt in times:
        ring(M, t, t0 + rt, count, amp=0.085, tau=1.6)

# --- coda: fold the five crowns, name the five counts ---
for (name, crown, count, nret, npart, a0), _ in zip(WALKS, starts):
    # partials 1 (root, stereo) and 2 (octave = the count, mono)
    m = (t >= 140.0) & (t < 140.0 + 40)
    tt = t[m] - 140.0
    S[m] += 0.10 * np.sin(2 * np.pi * crown * tt) * np.exp(-tt / 4.0)
    M[m] += 0.085 * np.sin(2 * np.pi * count * tt) * np.exp(-tt / 4.0)

# the fold: stereo width -> 0, the crowns cancel, the counts remain
w = np.ones(N)
f0, f1 = 142.0, 146.0
m = (t >= f0) & (t < f1)
w[m] = np.cos((t[m] - f0) / (f1 - f0) * np.pi / 2) ** 2
w[t >= f1] = 0.0

# the naming: the five counts arpeggiate, low -> high
for c, tt0 in [(84, 148.0), (110, 150.5), (222, 153.0), (540, 155.5), (2502, 158.0)]:
    ring(M, t, tt0, c, amp=0.105, tau=4.5)

# --- render ---
L = M + w * S
R = M - w * S

# global fade out
fade0 = 156.0
m = t >= fade0
L[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))
R[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/five_ids.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print("wrote assets/five_ids.wav", dur, "s")

# --- verify the fold ---
mono = (L + R) / 2


def band(x, f0, a, b, width=4.0):
    seg = x[int(a * sr):int(b * sr)]
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    X = np.abs(np.fft.rfft(seg))
    m = (fr > f0 - width) & (fr < f0 + width)
    return float(X[m].sum())


print("\n-- in movement A (stereo hears the crown, mono keeps only the count) --")
print("stereo 55  @4-6 :", round(band(L, 55, 4, 6), 1), " mono:", round(band(mono, 55, 4, 6), 1))
print("stereo 110 @4-6 :", round(band(L, 110, 4, 6), 1), " mono:", round(band(mono, 110, 4, 6), 1))
print("\n-- in movement B (the rain: 84 struck 11x, still never a record) --")
print("stereo 42  @30-32:", round(band(L, 42, 30, 32), 1), " mono:", round(band(mono, 42, 30, 32), 1))
print("stereo 84  @30-32:", round(band(L, 84, 30, 32), 1), " mono:", round(band(mono, 84, 30, 32), 1))
print("\n-- coda after the fold (the crowns cancel, the counts remain) --")
print("crown 55  stereo:", round(band(L, 55, 146, 148), 1), " mono:", round(band(mono, 55, 146, 148), 1))
for c in [84, 110, 222, 540]:
    print(f"count {c}  stereo:", round(band(L, c, 146, 148), 1), " mono:", round(band(mono, c, 146, 148), 1))
