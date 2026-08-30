#!/usr/bin/env python3
"""the flock, heard — 48 birds, 24 homes, the 25th rung the seat.

mina's flock gathers around the count: birds come home in mirror pairs, one at
110·r and one at 110/r, so every home is a pair — the sign (which bird is
above, which below) is the fold's cargo, the where. rahel read the ladder: the
pairs at r = 2/1, 3/2, 4/3, 5/4, ... narrowing toward r = 1, and the 25th rung
the fused pair where both voices are one.

The rank register counts it: 48 birds, but each home is a ±pair — one where
each, the sign folded — so the flock has 24 homes, not 47. And the 25th rung,
r = 1, is not a home at all: its where is zero, rank 0. the count was never a
rung; it is where every rung lands.

Here each rung rings as a release: the pair carried in the difference channel
only, stereo, offstage — and the fold (mono) cancels every one of them, so the
count never moves. 24 homes, one count. then the seat: r = 1, the diff silent,
the count alone.
"""
import numpy as np
import wave

SR = 44100
C = 110.0                # the count, the fixed point, never moves
N = 24                   # mirror pairs = homes
CELL = 1.375             # seconds per rung
INTRO = 2.0              # the count seated alone
SEAT = 3.5               # the fused pair: diff silent, the landing
OUT = 1.0
DUR = INTRO + N * CELL + SEAT + OUT
t = np.arange(int(SR * DUR)) / SR


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def cell_env(start, length, a_frac=0.22, r_frac=0.38):
    """0->1->0 envelope for one cell; stays 1 in the middle."""
    t0 = int(start * SR)
    la = int(length * a_frac * SR)
    lr = int(length * r_frac * SR)
    e = np.zeros(int(length * SR))
    e[:la] = smoothstep(np.linspace(0, 1, la))
    e[-lr:] *= (1.0 - smoothstep(np.linspace(0, 1, lr)))
    e[la:-lr] = 1.0
    return e


# ---- the count: a seated 110 Hz sine, identical in both ears ----
m = 0.5 * np.cos(2 * np.pi * C * t)

# ---- 24 rungs: the superparticular ladder r = (n+1)/n, narrowing to 1 ----
s = np.zeros_like(t)          # the where: every home, offstage
for n in range(1, N + 1):
    f_hi = C * (n + 1) / n            # 110·(n+1)/n   above
    f_lo = C * n / (n + 1)            # 110·n/(n+1)   below
    start = INTRO + (n - 1) * CELL
    e = cell_env(start, CELL)
    i0 = int(start * SR)
    i1 = i0 + e.size
    pair = 0.20 * np.cos(2 * np.pi * f_hi * t[i0:i1]) + 0.20 * np.cos(2 * np.pi * f_lo * t[i0:i1])
    s[i0:i1] += pair * e

# ---- the seat: r = 1, the fused pair — nothing offstage. a swell of the count ----
seat_start = INTRO + N * CELL
swell = 1.0 + 0.35 * smoothstep((t - seat_start) / (SEAT - 0.5)) * \
        (1.0 - smoothstep((t - (seat_start + 2.4)) / 0.8))
m_swelled = m * np.where(t > seat_start, swell, 1.0)

# ---- stereo: the where in the difference channel, sign-flipped ----
L = m_swelled + s
R = m_swelled - s

# ---- global attack / release ----
global_env = smoothstep(t / 1.2) * (1.0 - smoothstep((t - (DUR - 1.2)) / 0.8))
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/flock_ladder.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())

# ---- verification ----
mono = (L + R) / 2.0
m_ref = m_swelled * global_env / peak * 0.95
print(f"mono == count exactly: max|mono - m| = {np.abs(mono - m_ref).max():.2e}")

def pitch_of_segment(x, t0, t1, lo_hz, hi_hz, n_peaks=3):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    seg = x[i0:i1] - x[i0:i1].mean()
    n = seg.size
    spec = np.fft.rfft(seg)
    corr = np.fft.irfft(spec * np.conj(spec))[:n]
    corr = corr / corr[0]
    lo, hi = int(SR / hi_hz), int(SR / lo_hz)
    window = corr[lo:hi]
    # find the top peaks
    idx = np.argsort(window)[-n_peaks:][::-1]
    idx.sort()
    return [(SR / (i + lo), window[i]) for i in idx]

# the where, heard in the difference, during a few rungs; mono holds 110
for n in [1, 6, 12, 24]:
    t0 = INTRO + (n - 1) * CELL + 0.25
    t1 = t0 + CELL - 0.5
    f_hi = C * (n + 1) / n
    f_lo = C * n / (n + 1)
    fd, vd = pitch_of_segment((L - R) / 2.0, t0, t1, 40, 260, n_peaks=2)[:2]
    fm, vm = pitch_of_segment(mono, t0, t1, 80, 150, n_peaks=1)[0]
    print(f"rung n={n:2d} pair ({f_lo:6.1f}, {f_hi:6.1f}): "
          f"diff peaks {fd[0]:6.1f}/{fd[1]:6.1f} Hz   mono {fm:6.1f} Hz")

# the seat: diff silent
i0 = int((seat_start + 1.0) * SR)
i1 = int((seat_start + 2.5) * SR)
diff_seat = ((L - R) / 2.0)[i0:i1]
print(f"diff in the seat rms: {np.sqrt((diff_seat**2).mean()):.2e}   "
      f"(the where is zero; rank 0)")
print(f"wrote assets/flock_ladder.wav  {DUR:.1f}s stereo {SR}Hz")
