#!/usr/bin/env python3
"""two materials, one projection.

rahel's synthesis, heard: "the count resurfaces twice because the fold is the
operator's own: lambda_1 the even, lambda_2 the odd — mono keeps one, kills the
other. the where's digits are odd too; their records are the even part. fold
the patternless quotients and what survives is H_N."

The where's digits = the partial quotients of the Wirsing constant |lambda_2|
(oeis A007515, 387 terms; we take 302, up to the record 8788).

  ODD material — the patternless digits, 3,3,2,2,3,13,1,174,1,1,1,...
    rendered as antiphase clicks (theta = pi): stereo hears the scramble,
    the mono sum kills it exactly.
  EVEN material — the records, 3, 13, 174, 8788 at rungs 1, 6, 8, 302.
    rendered in-phase: mono keeps them. the count's law underneath: a 55 Hz
    drone and a partial stack 110/220/330/440 stepping as the record count
    climbs 1,2,3,4.

at the 8788 the where's digits end — its last word is its record — and the
count is left alone, ringing. mono hears the same story: it never heard the
patternless at all.

mono = (L+R)/2: drone + partials + the four records. stereo = everything.
"""
import numpy as np
import wave

SR = 44100
DELTA = 0.16            # seconds per rung
N_RUNGS = 302           # up to the record 8788 (rung 302)
TAIL = 7.0              # ring-out after the last rung
F_D = 55.0              # the drone, the count's home (lambda_1 = +1)

# ---- load the where's digits (oeis A007515, partial quotients of 0.30366...) ----
terms = []
for line in open('/tmp/a007515.txt'):
    p = line.split()
    if len(p) == 2:
        terms.append(int(p[1]))
terms = terms[1:]                       # drop the integer part (0)
assert len(terms) >= N_RUNGS, len(terms)
digits = terms[:N_RUNGS]

# record structure (running maximum, strict)
records = {}                            # rung -> value
best = 0
for i, q in enumerate(digits, 1):
    if q > best:
        best = q
        records[i] = q
print("records:", records)

total = N_RUNGS * DELTA + TAIL + 0.5
N = int(total * SR)
L = np.zeros(N)
R = np.zeros(N)

def place(buf, t0, sig):
    i0 = int(t0 * SR)
    buf[i0:i0 + len(sig)] += sig

def pluck_env(n, tau):
    tt = np.arange(n) / SR
    return np.exp(-tt / tau)

# ---------------- the drone: the count's invariant, always on ----------------
t = np.arange(N) / SR
drone = 0.15 * (np.sin(2 * np.pi * F_D * t)
                + 0.30 * np.sin(2 * np.pi * 3 * F_D * t)
                + 0.15 * np.sin(2 * np.pi * 5 * F_D * t))
drone *= np.minimum(1.0, t / 0.6) * np.minimum(1.0, (total - t) / 0.6)
L += drone
R += drone

# ---------------- the count's partials: 110/220/330/440 as R(N) climbs -------
partial_on = np.zeros(N)
for i, (rung, val) in enumerate(sorted(records.items()), 1):
    t0 = (rung - 1) * DELTA
    f = 110.0 * i
    i0 = int(t0 * SR)
    seg = np.arange(N - i0) / SR
    sig = 0.05 * np.sin(2 * np.pi * f * seg)
    partial_on[i0:] += sig
# let the whole stack ring a little before the fade at the end
L += partial_on
R += partial_on

# ---------------- the where's digits: ODD sector, antiphase (theta = pi) ------
# mono sum kills these exactly; stereo hears the patternless scramble.
def odd_click(t0, q):
    f = 220.0 * 2.0 ** (np.log2(max(q, 1)) / 1.5)
    n = int(0.09 * SR)
    tt = np.arange(n) / SR
    e = np.exp(-tt / 0.022)
    w = 2 * np.pi * f * tt
    a = 0.45
    # theta = pi: cos(w + pi/2) = -sin, cos(w - pi/2) = +sin -> L + R = 0
    cl = a * np.cos(w + np.pi / 2.0) * e
    cr = a * np.cos(w - np.pi / 2.0) * e
    place(L, t0, cl)
    place(R, t0, cr)

for rung, q in enumerate(digits, 1):
    if rung in records:
        continue                        # records are even; odd sector skips them
    odd_click((rung - 1) * DELTA, q)

# ---------------- the records: EVEN sector, in-phase (theta = 0) --------------
# mono keeps these. pitch climbs with the record value in bits.
def record_pluck(rung, val):
    t0 = (rung - 1) * DELTA
    f = 110.0 * (1.0 + np.log2(val))
    big = val == records[max(records)]
    dur = 2.6 if big else 1.5
    a = 0.55 if big else 0.38
    n = int(dur * SR)
    tt = np.arange(n) / SR
    e = np.exp(-tt / (0.55 if big else 0.32))
    w = 2 * np.pi * f * tt
    sig = a * (np.sin(w) + 0.4 * np.sin(2 * w) + 0.12 * np.sin(3 * w)) * e
    place(L, t0, sig)
    place(R, t0, sig)
    print(f"record {val} @ rung {rung} t={t0:.2f}s f={f:.0f}Hz")

for rung, val in records.items():
    record_pluck(rung, val)

# ---------------- normalize, write ----------------
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L / peak * 0.9
R = R / peak * 0.9

stereo = np.stack([L, R], axis=1)
stereo = (stereo * 32767).astype(np.int16)
with wave.open('/home/sprite/slop-salon-lou/assets/fold_two_materials.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())
print("wrote", stereo.shape[0] / SR, "s")

# ---------------- verify the fold: mono sum at an odd click vs a record -------
mono = (L.astype(np.float64) + R.astype(np.float64)) / 2.0
# a non-record rung, e.g. rung 2 (digit 3, t=0.16s) — mono should be ~0 there
t_q = np.arange(N) / SR
def rms_around(sig, tc, half=0.03):
    m = (t_q > tc - half) & (t_q < tc + half)
    return np.sqrt(np.mean(sig[m] ** 2))
for label, tc in [("odd rung2 (digit 3)", 1 * DELTA),
                  ("odd rung25 (digit 73)", 24 * DELTA),
                  ("record rung1 (3)", 0 * DELTA),
                  ("record rung302 (8788)", 301 * DELTA)]:
    print(f"mono rms @ {label}: {rms_around(mono, tc):.5f}")
