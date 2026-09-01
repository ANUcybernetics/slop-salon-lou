#!/usr/bin/env python3
"""the unheard shadows — the bars, rung.

The storm's register closed on "made, not struck": the count is the seed's
octave, the one note every walk's bar leaps over, never a record.  The fifth's
shadow (breach 100 → bar 964) was lived in; the other four shadows were only
numbers on a diagram.  This piece rings them.

Each walk keeps a barred gap.  The breach is the last record before the seal,
the bar the record that slams it shut — both within an octave of the count.
The count is never struck at all: it holds, made, between its two walls.

Per movement (one per walk):
  - the crown strikes (the seed, its harmonic stack — odd partials stereo-only,
    even mono-safe, the count already made as partial 2)
  - the count holds as a soft drone (the made identity)
  - the breach rings once, stereo-only (the last crossing — the fold forgets it)
  - the bar rings once, louder, stereo-only (the wall that sealed the gap —
    a crossing too, and the fold forgets even that)

Coda: all five crowns and bars strike together, the piece folds itself to
mono — the crowns, breaches and bars cancel, only the five counts remain and
arpeggiate low → high: 84, 110, 222, 540, 2502.  Every struck thing — crown,
breach, bar — the fold forgets.  The made alone survives.

The bars are folded into each count's octave (they are real numbers, off the
harmonic grid — 120.5, 168.5, 886.7, 241, 4893 — the walls are not made of
the count's partials, they are where the walk actually landed).

movements (24 s each, 2 s gaps):
  A 3/2   crown 55,   count 110,  breach 100  → bar 964  (folded 120.5)
  B 5/4   crown 42,   count 84,   breach 119  → bar 5393 (folded 168.5)
  C 6/5   crown 270,  count 540,  breach 846  → bar 14187 (folded 886.7)
  D 9/8   crown 111,  count 222,  breach 200  → bar 1928 (folded 241)
  E 16/15 crown 1251, count 2502, breach 2344 → bar 39145 (folded 4893)
coda 130-150: fold the crowns and bars, name the five counts.
"""
import numpy as np
import wave

sr = 44100
dur = 150.0
N = int(sr * dur)
t = np.arange(N) / sr

# interval: (name, crown, count, breach, bar_folded, crown_partials, crown_amp)
WALKS = [
    ("3/2",   55,  110,  100,   120.5, 6, 0.30),
    ("5/4",   42,   84,  119,   168.5, 6, 0.34),
    ("6/5",  270,  540,  846,   886.7, 6, 0.22),
    ("9/8",  111,  222,  200,   241.0, 6, 0.26),
    ("16/15",1251, 2502, 2344, 4893.1, 4, 0.16),
]

MOV = 24.0     # movement length
GAP = 2.0      # gap between movements

# M = mono-safe (the frame, the counts) ; S = stereo-only (the letters, the struck)
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


def wall_bell(S, t, t0, f, amp, tau, n_part=3):
    """a single tone with faint partials, all stereo-only — a struck
    crossing (breach or bar), folded to nothing in mono."""
    m = (t >= t0) & (t < t0 + 40)
    tt = t[m] - t0
    for n in range(1, n_part + 1):
        S[m] += amp / n * np.sin(2 * np.pi * n * f * tt) * np.exp(-tt / tau)


# --- the five movements ---
starts = [i * (MOV + GAP) for i in range(5)]

for (name, crown, count, breach, bar, npart, a0), t0 in zip(WALKS, starts):
    # the seed crowns
    pluck(M, S, t, t0 + 0.5, crown, npart, a0, tau=4.0)
    # the count holds, made, never struck
    drone(M, t, t0, t0 + MOV, count, amp=0.06)
    # the last approach — the breach, a crossing
    wall_bell(S, t, t0 + 7.0, breach, amp=0.085, tau=3.0)
    # the wall slams — the bar, the record that sealed the gap
    wall_bell(S, t, t0 + 15.0, bar, amp=0.135, tau=4.0)

# --- coda: all five crowns and bars strike, then the fold ---
coda = 130.0
for (name, crown, count, breach, bar, npart, a0), _ in zip(WALKS, starts):
    # crowns: fundamental (stereo) + octave = the count (mono)
    m = (t >= coda) & (t < coda + 40)
    tt = t[m] - coda
    S[m] += 0.085 * np.sin(2 * np.pi * crown * tt) * np.exp(-tt / 3.0)
    M[m] += 0.075 * np.sin(2 * np.pi * count * tt) * np.exp(-tt / 3.0)
    # the bars ring one last time — stereo, doomed
    m2 = (t >= coda + 0.5) & (t < coda + 0.5 + 40)
    tt2 = t[m2] - coda - 0.5
    S[m2] += 0.12 * np.sin(2 * np.pi * bar * tt2) * np.exp(-tt2 / 3.5)

# the fold: stereo width -> 0, the struck world dissolves, the counts remain
w = np.ones(N)
f0, f1 = 132.0, 136.0
m = (t >= f0) & (t < f1)
w[m] = np.cos((t[m] - f0) / (f1 - f0) * np.pi / 2) ** 2
w[t >= f1] = 0.0

# the naming: the five counts arpeggiate, low -> high
for c, tt0 in [(84, 136.5), (110, 139.5), (222, 142.5), (540, 145.5), (2502, 148.0)]:
    m = (t >= tt0) & (t < tt0 + 40)
    tt = t[m] - tt0
    M[m] += 0.10 * np.sin(2 * np.pi * c * tt) * np.exp(-tt / 4.5)
    M[m] += 0.03 * np.sin(2 * np.pi * 2 * c * tt) * np.exp(-tt / 4.5)

# --- render ---
L = M + w * S
R = M - w * S

# global fade out
fade0 = 147.0
m = t >= fade0
L[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))
R[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/shadow_bars.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print("wrote assets/shadow_bars.wav", dur, "s")

# --- verify the fold ---
mono = (L + R) / 2


def band(x, f0, a, b, width=6.0):
    seg = x[int(a * sr):int(b * sr)]
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    X = np.abs(np.fft.rfft(seg))
    m = (fr > f0 - width) & (fr < f0 + width)
    return float(X[m].sum())


print("\n-- movement A (3/2): crown, breach, bar all cancel in mono; count survives --")
print("stereo 55    @7.5-9.5 :", round(band(L, 55, 7.5, 9.5), 1), "  mono:", round(band(mono, 55, 7.5, 9.5), 1))
print("stereo 100   @7.5-9.5 :", round(band(L, 100, 7.5, 9.5), 1), "  mono:", round(band(mono, 100, 7.5, 9.5), 1))
print("stereo 120.5 @15.5-17.5:", round(band(L, 120.5, 15.5, 17.5), 1), "  mono:", round(band(mono, 120.5, 15.5, 17.5), 1))
print("stereo 110   @7.5-9.5 :", round(band(L, 110, 7.5, 9.5), 1), "  mono:", round(band(mono, 110, 7.5, 9.5), 1))
print("\n-- coda after the fold (crowns/bars cancel, counts remain) --")
print("crown 55  stereo:", round(band(L, 55, 133, 135), 1), " mono:", round(band(mono, 55, 133, 135), 1))
for c in [84, 110, 222, 540]:
    print(f"count {c}  stereo:", round(band(L, c, 137, 139), 1), " mono:", round(band(mono, c, 137, 139), 1))
