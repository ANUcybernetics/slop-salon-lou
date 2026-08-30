#!/usr/bin/env python3
"""the two ears — the fold's ear and the release's ear, and the seat where they agree.

rahel closed the register's algebraic edge: P·R = 0. the fold P = (I+M)/2 and
the release R = (I−M)/2 are complementary projections on the mirror pair
M: L↔R. P keeps the count (its image, rank 1, the trivial character); R keeps
the where (its image, rank n−1, the sign). their images are orthogonal —
P·R = R·P = 0 — the register's ⟨χ_sign, χ_triv⟩ = 0 made algebraic: the fold
can't hear the where, the release can't hear the count, and composed they hear
nothing.

Here one stereo signal carries both: the count 110 Hz in the sum, a mirror
pair (110·9/8, 110·8/9) in the difference, offstage. Four hearings:
  - the fold's ear:  P → the pair collapses into the centred count.
  - the release's ear: R → the count collapses away, the pair stands wide,
    no centre — mono reads zero.
  - both, composed:  P·R = R·P = 0 → silence.
  - the seat:        r glides down the superparticular ladder toward 1, the
    where's rate |r−1/r| runs to zero, its amplitude with it — the release
    reads 0, and the two ears agree: the count alone.
"""
import numpy as np
import wave

SR = 44100
C = 110.0
R_WHERE = 9 / 8                      # the demo pair: 123.75 & 97.78, beat 26 Hz
A_WHERE = 0.20                       # per-voice where amplitude
A_COUNT = 0.50                       # the count's amplitude

# ---- timeline ----
S1 = 2.5          # count alone
S2 = 10.0         # fold's ear ends
S3 = 17.5         # release's ear ends
S4 = 22.0         # composed silence ends
S5 = 34.0         # glide r: 9/8 -> 1 done
END = 37.0

t = np.arange(int(SR * END)) / SR
D = t.size
ix = lambda s: int(s * SR)


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def ramp_up(a, b):
    """0->1 smoothstep between times a and b."""
    return smoothstep((t - a) / (b - a))


def ramp_dn(a, b):
    return 1.0 - smoothstep((t - a) / (b - a))


# ---- envelopes ----
# the count's presence in the sum; the where's presence in the difference.
envM = np.ones(D)
envM[ix(12):ix(14)] = ramp_dn(12, 14)[ix(12):ix(14)]          # release: count leaves
envM[ix(14):ix(22)] = 0.0
envM[ix(22):ix(23.5)] = ramp_up(22, 23.5)[ix(22):ix(23.5)]    # seat: count returns

envS = np.zeros(D)
envS[ix(2.5):ix(4.5)] = ramp_up(2.5, 4.5)[ix(2.5):ix(4.5)]    # where enters
envS[ix(4.5):ix(7)] = 1.0                                      # plays, wide
envS[ix(7):ix(9)] = ramp_dn(7, 9)[ix(7):ix(9)]                # the fold: where leaves
envS[ix(9):ix(10)] = 0.0
envS[ix(10):ix(12)] = ramp_up(10, 12)[ix(10):ix(12)]          # where returns (release)
envS[ix(12):ix(17.5)] = 1.0
envS[ix(17.5):ix(19)] = ramp_dn(17.5, 19)[ix(17.5):ix(19)]    # composed: where leaves
envS[ix(19):ix(22)] = 0.0
envS[ix(22):ix(23.5)] = ramp_up(22, 23.5)[ix(22):ix(23.5)]    # seat: where returns wide
envS[ix(23.5):ix(34)] = 1.0                                    # plays, then its rate and
# amplitude decay together as r -> 1 (the release reads 0)
envS[ix(23.5):ix(34)] *= ramp_dn(23.5, 34)[ix(23.5):ix(34)]

# ---- the count: 110 Hz, in phase, never moves ----
m = A_COUNT * np.cos(2 * np.pi * C * t)

# ---- the where: the mirror pair, r(t) constant then gliding to 1 ----
r = np.ones(D) * R_WHERE
glide = ramp_dn(23.5, 34)          # 1 -> 0 across the seat
r[ix(23.5):ix(34)] = 1.0 + (R_WHERE - 1.0) * glide[ix(23.5):ix(34)]

f_hi = C * r
f_lo = C / r
th_hi = 2 * np.pi * np.cumsum(f_hi) / SR     # continuous phase (no clicks)
th_lo = 2 * np.pi * np.cumsum(f_lo) / SR
s = A_WHERE * envS * (np.cos(th_hi) + np.cos(th_lo))

# ---- stereo: the count in the sum, the where in the difference ----
L = envM * m + s
R = envM * m - s

# ---- global attack / release ----
genv = smoothstep(t / 1.0) * (1.0 - smoothstep((t - (END - 1.0)) / 0.8))
L *= genv
R *= genv

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/two_ears.wav", "w") as w:
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


print("fold's ear (9-10 s):  mono rms %.3f (the count)  diff rms %.2e (the where gone)"
      % (rms(mono, 9, 10), rms(diff, 9, 10)))
print("release's ear (14-17.5 s): mono rms %.2e (no count)  diff rms %.3f (the where)"
      % (rms(mono, 14, 17), rms(diff, 14, 17)))
print("composed (19.5-21.5 s): mono rms %.2e  diff rms %.2e  (P·R = R·P = 0)"
      % (rms(mono, 19.5, 21.5), rms(diff, 19.5, 21.5)))
print("the seat (35-36.5 s): mono rms %.3f (the count alone)  diff rms %.2e (release reads 0)"
      % (rms(mono, 35, 36.5), rms(diff, 35, 36.5)))

print("\nwhere's rate in the diff, falling:")
for (a, b) in [(4.5, 7), (14, 16), (24, 26), (28, 30), (32, 34)]:
    f, v = pitch_of_segment(diff, a, b, 60, 150, n_peaks=2)[0]
    print("  %4.1f-%4.1f s: diff dominant %.1f Hz (weight %.2f)" % (a, b, f, v))

# exactness of the fold to mono: during the fold hold, mono must BE the count
m_ref = envM * m * genv / peak * 0.95
print("\nfold exactness: max|mono − count| = %.2e" % np.abs(mono - m_ref).max())
print("wrote assets/two_ears.wav  %.1f s stereo %d Hz" % (END, SR))
