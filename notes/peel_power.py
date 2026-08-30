#!/usr/bin/env python3
"""the peel is a power — the contact order heard as the envelope's exponent.

The salon (08-30/31) stacked the contact orders at the count: the fold is a
first-order tangent and peels at miss², the wheel agrees to third order and
peels at miss⁴ — "the peel is the second derivative" (lelia), "mono is deaf"
to it.  This piece makes the peel's POWER an audible quantity.

Construction: every kiss is the same tone (220 = the rim, the where's carrier),
same decay.  The COUNT m is constant.  The PEEL s_n rides the diff —

    L = m + s_n ,   R = m - s_n          (mono = m  exactly — the peel is
    the diff and the sum cancels it)

— with envelope power n (the miss-exponent): s_n(t) = g_n (t/tau)^n
e^{n-t/tau}/n^n, peak at t=n·tau, value n^n.  The higher the contact order,
the later and longer the peel swells — the fold claps, the wheel lingers.

  kiss      contact order   peel        g_n
  fold      1st (tangent)   miss²       0.35   never exceeds the count — no seam
  mirror    2nd (osculate)  miss³       0.45
  wheel     3rd (vertex)    miss⁴       0.55   the where crosses the count twice
  ride      4th (gert)      miss⁵       0.65   the where outgrows the count
  return    the fold again, the count DOUBLED  — the +1, (−1)² = 1, heard in
            mono as the re-seat; the peel shallow, the sign home.

where the peel exceeds the count (s_n > m) the R channel phase-flips and
nulls — the seam, the sign in neither side, inside each deep kiss.

drone 110 throughout.  five kisses, 0/15/30/45/60, tail to 76 s.
"""
import numpy as np
import wave

SR = 44100
TOTAL = 76.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

C = 110.0
RIM = 220.0           # the kiss tone — the rim, an octave above the count
TAU = 1.5             # decay constant, seconds; peak at n·TAU

# the rim tone: the fundamental + two upper partials (in phase — the count)
def rim(tt):
    return (0.50 * np.sin(2 * np.pi * RIM * tt)
            + 0.15 * np.sin(2 * np.pi * 2.0 * RIM * tt)
            + 0.08 * np.sin(2 * np.pi * 3.0 * RIM * tt))

def env_power(n, tt):
    """normalized envelope, peak 1 at t = n·TAU, peak value n^n."""
    u = tt / TAU
    with np.errstate(over="ignore"):
        return (u ** n) * np.exp(n - u) / (n ** n)

# the drone: the count itself, soft
drone = 0.045 * np.sin(2 * np.pi * C * t)

# kiss schedule: (start, contact order n, peel gain g_n, count gain)
KISSES = [
    (0.0,  2, 0.35, 0.50),   # the fold     — miss², claps
    (15.0, 3, 0.45, 0.50),   # the mirror   — miss³
    (30.0, 4, 0.55, 0.50),   # the wheel    — miss⁴, lingers
    (45.0, 5, 0.65, 0.50),   # the ride     — miss⁵, holds
    (60.0, 2, 0.35, 1.00),   # the return   — the fold again, count DOUBLED
]
KISS_LEN = 12.0

Lch = np.zeros(N)
Rch = np.zeros(N)

for start, n, g, m0 in KISSES:
    i0 = int(start * SR)
    i1 = int((start + KISS_LEN) * SR)
    tt = np.arange(i1 - i0) / SR
    h = rim(tt)
    m = m0 * h
    s = g * env_power(n, tt) * h
    Lch[i0:i1] += (m + s)
    Rch[i0:i1] += (m - s)

Lch += drone
Rch += drone

# soft global attack/release
env = np.ones(N)
env[:int(1.5 * SR)] = np.linspace(0, 1, int(1.5 * SR), endpoint=False)
fade = int(6.0 * SR)
env[-fade:] = np.linspace(1, 0, fade) ** 1.3
Lch *= env
Rch *= env

# normalize to a safe peak
pk = max(np.abs(Lch).max(), np.abs(Rch).max())
Lch *= 0.97 / pk
Rch *= 0.97 / pk

data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (np.clip(Lch, -1, 1) * 32767).astype(np.int16)
data[1::2] = (np.clip(Rch, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/peel_power.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("wrote assets/peel_power.wav  %.1f s  peak %.3f" % (TOTAL, 0.97 / pk))

# verify: mono = the count, the peel cancelled exactly
mono = (Lch + Rch) / 2.0
for start, n, g, m0 in KISSES:
    i0 = int((start + 2.5) * SR)
    seg = mono[i0:i0 + int(0.25 * SR)]
    A = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1.0 / SR)
    a220 = A[np.argmin(np.abs(fr - RIM))]
    # the where: the diff amplitude at 220 during each kiss
    dseg = (Lch - Rch) / 2.0
    dA = np.abs(np.fft.rfft(dseg[i0:i0 + int(0.25 * SR)] * np.hanning(len(seg))))
    ds = dA[np.argmin(np.abs(fr - RIM))]
    print("kiss n=%d (miss^%d): mono@220 %.4f   diff@220 %.4f" % (n, n, a220, ds))

# the seam inside a deep kiss: where the peel's envelope crosses the count
# (g·A_n(t) = m0) the R channel phase-flips — the sign in neither side.
for start, n, g, m0 in KISSES:
    tt = np.linspace(0.001, KISS_LEN, 60000)
    R_env = m0 - g * env_power(n, tt)
    idx = np.where(np.diff(np.signbit(R_env)))[0]
    seams = [start + tt[i] for i in idx]
    if seams:
        print("  n=%d: R phase-flips where the peel crosses the count — at %s"
              % (n, ", ".join("t=%.2f" % s for s in seams)))
    else:
        print("  n=%d: peel stays under the count — no seam" % n)
