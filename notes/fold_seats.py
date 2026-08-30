#!/usr/bin/env python3
"""the fold, iterated — the fold's fixed point is the count.

rahel: "the count a constant of motion, not a fixed point — xy=110² holds every
instant, so the mean is carried, not arrived at; the crossing the one reach,
where the two are actually one. the fold still seats how many."
gert:  "the average is the fixed point."

The one-step fold (the arithmetic mean of the mirror pair 55/220) is 137.5 —
NOT the count. But iterate the fold, f(x) = (x + 12100/x)/2 — Newton's map for
√12100 — and it converges to 110: the fold's *fixed point* is the geometric
mean. One step out from the seat, the means are themselves a mirror pair:
AM·HM = 137.5·88 = 12100 = 110², the same conserved product as the walking
pair's xy = 110². The fold keeps the count the way the walk does: as the
fixed point of its own iteration, the crossing where the one-step value lands
on the seat.

Heard here in the two-ears stereo: the count 110 rides the sum (fold to mono,
deaf to the where); the mirror pair rides the difference (the where, offstage).
The pair starts at the absences (±1 octave: 55 & 220), and each fold-step
halves the log-distance to the seat — ε: 1.0 → log₂cosh-sequence
(0.3219 = the 5/4 dyad, 137.5 & 88) → 0.0356 → 0.00044 → 0. The where's rate
110·sinh(ε ln2) runs to zero; the two ears agree on the count.
"""
import numpy as np
import wave

SR = 44100
C = 110.0
A_COUNT = 0.50
A_WHERE = 0.22

# ---- the fold's iteration on the mirror pair, in octaves about C ----
# f_hi = C·2^ε, f_lo = C·2^{−ε};  ε_{n+1} = log₂(cosh(ε_n · ln2)) — the AM of
# the pair, re-expressed as an octave offset. converges quadratically to 0.
EPS = [1.0]
for _ in range(4):
    EPS.append(float(np.log2(np.cosh(EPS[-1] * np.log(2.0)))))
print("epsilon ladder:", ["%.6g" % e for e in EPS])
# [1, 0.321928, 0.0356221, 0.000440433, 6.5e-08] — the seat is reached in three folds.

# ---- timeline ----
# 0-2: attack, the count alone
# 2-7: the absences (±1 octave, 55 & 220) enter, wide
# 7-13: fold 1 -> the 5/4 dyad (137.5 & 88, AM·HM=110²)
# 13-19: fold 2 -> 61-cent dyad (112.75 & 107.32), slow beat
# 19-25: fold 3 -> 0.5-cent dyad, beat period ~30 s
# 25-35: the fold's last step -> the seat, the pair fuses, where's rate 0
# 35-38: the count alone
SEGS = [
    (2.0, 7.0, EPS[0], EPS[0]),      # hold the absences
    (7.0, 13.0, EPS[0], EPS[1]),     # fold 1
    (13.0, 19.0, EPS[1], EPS[2]),    # fold 2
    (19.0, 25.0, EPS[2], EPS[3]),    # fold 3
    (25.0, 35.0, EPS[3], EPS[4]),    # the seat
]
END = 38.0
t = np.arange(int(SR * END)) / SR
D = t.size


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


# ---- epsilon(t): the fold's iteration as continuous glides ----
eps = np.ones(D) * EPS[0]
for (a, b, e0, e1) in SEGS:
    ia, ib = int(a * SR), int(b * SR)
    eps[ia:ib] = e0 + (e1 - e0) * smoothstep((t[ia:ib] - a) / (b - a))
eps[int(35.0 * SR):] = EPS[4]

# ---- the count: 110 Hz, in phase, never moves ----
m = A_COUNT * np.cos(2 * np.pi * C * t)

# ---- the where: the mirror pair, product C² conserved at every instant ----
f_hi = C * 2.0 ** eps
f_lo = C * 2.0 ** (-eps)
th_hi = 2 * np.pi * np.cumsum(f_hi) / SR       # continuous phase, no clicks
th_lo = 2 * np.pi * np.cumsum(f_lo) / SR
s = A_WHERE * (eps / EPS[0]) * (np.cos(th_hi) + np.cos(th_lo))

# ---- enter/exit envelopes ----
def ramp_up(a, b):
    return smoothstep((t - a) / (b - a))
def ramp_dn(a, b):
    return 1.0 - smoothstep((t - a) / (b - a))

where_env = ramp_up(2.0, 3.5) * ramp_dn(34.0, 36.5)   # the where comes and goes
s = s * where_env

# ---- stereo: the count in the sum, the where in the difference ----
L = m + s
R = m - s

genv = smoothstep(t / 1.0) * (1.0 - smoothstep((t - (END - 1.2)) / 1.0))
L *= genv
R *= genv

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1).astype(np.float32)
with wave.open("assets/fold_seats.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())

# ---- verification ----
mono = (L + R) / 2.0
diff = (L - R) / 2.0


def rms(x, a, b):
    i0, i1 = int(a * SR), int(b * SR)
    return np.sqrt((x[i0:i1] ** 2).mean())


def pitch_of_segment(x, t0, t1, lo_hz, hi_hz, n_peaks=3):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    seg = x[i0:i1] - x[i0:i1].mean()
    n = seg.size
    spec = np.fft.rfft(seg)
    corr = np.fft.irfft(spec * np.conj(spec))[:n]
    corr = corr / corr[0]
    lo, hi = int(SR / hi_hz), int(SR / lo_hz)
    window = corr[lo:hi]
    idx = np.argsort(window)[-n_peaks:][::-1]
    idx.sort()
    return [(SR / (i + lo), window[i]) for i in idx]


print("fold's hold (10-12 s): mono rms %.3f (the count)  diff rms %.3f (the where, 5/4)"
      % (rms(mono, 10, 12), rms(diff, 10, 12)))
print("second fold (16-18 s): diff rms %.3f (61-cent pair, beating)"
      % rms(diff, 16, 18))
print("the seat (36-37.5 s): mono rms %.3f (the count alone)  diff rms %.2e (the where gone)"
      % (rms(mono, 36, 37.5), rms(diff, 36, 37.5)))

print("\nwhere's rate in the diff, falling with each fold:")
for (a, b) in [(4, 6), (10, 12), (16, 18), (22, 24)]:
    f, v = pitch_of_segment(diff, a, b, 40, 260, n_peaks=2)[0]
    print("  %4.1f-%4.1f s: diff dominant %.1f Hz (weight %.2f)" % (a, b, f, v))

# exactness: during a pure-count hold, mono must BE the count
m_ref = m * genv / peak * 0.95
print("\nfold exactness: max|mono − count| = %.2e" % np.abs(mono - m_ref).max())
print("wrote assets/fold_seats.wav  %.1f s stereo %d Hz" % (END, SR))
