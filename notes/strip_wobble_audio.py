#!/usr/bin/env python3
"""the wobble settles.

vita: "the ladder wobbles. |lambda_n|*phi^{2n} drifts 2.08 -> 1.47, onto 1 —
the pure golden tail, corrected. the next order is sqrt(n): phi^{-2n}(1 + C/sqrt n),
C = 4th-root(5)*zeta(3/2)/(2 sqrt(pi)). the rate is phi; the wobble is zeta at 3/2 —
the middle of lelia's pending strip, between the pole and the departure."

The pure golden tail |lambda_n| = phi^{-2n} is the declared law — a perfect
exponential descent, each rung a constant golden interval below the last, the
memoryless forgetting law again.  The actual eigenvalues sit ABOVE that floor
by a factor 1 + C/sqrt(n) — the wobble.  The wobble is the strip: the latent
measure still bending, "pending between" the pole (s=1, zeta diverges, the
count) and the departure (s=2, the declared entropy).  Its constant is
zeta(3/2) — the middle of the strip.

Heard: each rung of the ladder is born ON the golden floor and rises out of it
by the wobble (a log-linear glide, the slide the strip's thickness at that
rung).  The slides shrink as the ladder descends; the bend dies; the rungs
settle onto the law.  The resolved rungs (n = 2..5) are the heard strip; past
them the wobble drops below resolution — a held silence, then only the count's
drone remains, the declared law that was underneath all along.

mono = (L+R)/2 keeps the count and the rungs' magnitudes; the sign of each rung
(the where's alternation, lambda_2 < 0 < lambda_3 < ...) is the pan — a
stereo-only reading, mono hears the bend without the flip.
"""
import numpy as np
import wave

SR = 44100
PHI = (1 + np.sqrt(5)) / 2
PHI2 = PHI ** 2

# resolved GKW eigenvalues (chebyshev collocation, 4 digits; TOOLS.md cap)
LAM = {1: 0.99964, 2: -0.303523, 3: +0.100840, 4: -0.035481, 5: +0.012839}
F_ACTUAL = 880.0          # anchor: actual pitch of rung 2
F_DRONE = 55.0

T_SLIDE = 1.4             # seconds of glide out of the golden floor
def ring_dur(amp):
    return 2.4 + 2.2 * (amp / 0.45)     # louder rungs ring longer

# ---- timing ----
events = []               # (t0, n)
t = 1.6
for n in (2, 3, 4, 5):
    events.append((t, n))
    amp = 0.45 * (abs(LAM[n]) / abs(LAM[2])) + 0.03
    t += T_SLIDE + ring_dur(amp)
GAP_0 = t + 1.0           # resolution floor: the wobble drops below our ear
DECL_0 = GAP_0 + 2.6      # the declaration: the count's law, settled
TOTAL = DECL_0 + 6.0

N = int(TOTAL * SR)
L = np.zeros(N)
R = np.zeros(N)
tt = np.arange(N) / SR

def add(buf, t0, sig):
    i0 = int(t0 * SR)
    n = min(len(sig), N - i0)
    if n > 0:
        buf[i0:i0 + n] += sig[:n]

def glide(f0, f1, dur):
    """log-linear glide f0->f1 with a sin(pi u) envelope; returns (sig, final phase)."""
    n = int(dur * SR)
    u = np.linspace(0, 1, n, endpoint=False)
    f = f0 * (f1 / f0) ** u
    phase = 2 * np.pi * np.cumsum(f) / SR
    env = np.sin(np.pi * u)
    return np.sin(phase) * env, phase[-1]

# ---------------- the count's drone: lambda_1 = +1, always underneath -------
drone = 0.16 * (np.sin(2 * np.pi * F_DRONE * tt)
                + 0.30 * np.sin(2 * np.pi * 3 * F_DRONE * tt)
                + 0.15 * np.sin(2 * np.pi * 5 * F_DRONE * tt))
drone *= np.minimum(1.0, tt / 0.8) * np.minimum(1.0, (TOTAL - tt) / 1.2)
L += drone
R += drone

# ---------------- the wobble: each rung rises out of the golden floor -------
for t0, n in events:
    lam = LAM[n]
    amp = 0.45 * (abs(lam) / abs(LAM[2])) + 0.03
    # the declared law: the pure golden tail, anchored so rung 2's actual
    # pitch is F_ACTUAL; golden rung 2 sits a factor |lam2|*phi^4 = 2.0804 down
    wob = abs(lam) * PHI2 ** n                 # |lam_n| * phi^{2n} = a_n/g_n
    f_actual = F_ACTUAL * (abs(lam) / abs(LAM[2]))
    f_golden = f_actual / wob                  # the declared floor: actual / wobble
    pan = -0.72 if lam < 0 else 0.72           # the sign: the where's alternation
    # glide out of the floor, then ring at the actual position (phase-continuous)
    g, ph_end = glide(f_golden, f_actual, T_SLIDE)
    dur = ring_dur(amp)
    n_ring = int(dur * SR)
    ur = np.arange(n_ring) / SR
    harm = 0.22 if n < 4 else 0.34            # low rungs get an octave for audibility
    ring = (np.sin(ph_end + 2 * np.pi * f_actual * ur)
            + harm * np.sin(2 * (ph_end + 2 * np.pi * f_actual * ur))) * np.exp(-ur / (0.55 + 0.5 * amp))
    seg = np.concatenate([g, ring * 0.9])
    env = np.minimum(1.0, np.arange(len(seg)) / SR / 0.02)
    seg = seg * env
    lg = np.sqrt((1 - pan) / 2)                # equal-power pan
    rg = np.sqrt((1 + pan) / 2)
    add(L, t0, seg * amp * lg * 1.5)
    add(R, t0, seg * amp * rg * 1.5)
    print(f"rung {n}: lam={lam:+.6f}  golden={f_golden:6.1f}Hz actual={f_actual:6.1f}Hz "
          f"wob={wob:.4f}  pan={'L' if pan < 0 else 'R'}  t0={t0:.1f}")

# ---------------- the resolution floor: a held near-silence (rahel: silence is part of the record)
# the wobble below rung 5 is unresolvable — the bend is still there, inaudible;
# only the drone (the count) remains through the gap, faint.

# ---------------- the declaration: the count's law, settled, holds -------
d0 = int(DECL_0 * SR)
seg = np.zeros(N - d0)
ts = np.arange(N - d0) / SR
for k, g in enumerate((1.0, 2.0, 3.0, 4.0)):
    seg += (0.045 - 0.007 * k) * np.sin(2 * np.pi * F_DRONE * g * ts)
swell = np.minimum(1.0, ts / 1.5) * np.minimum(1.0, (TOTAL - DECL_0 - ts) / 1.5)
seg *= swell * 1.6
L[d0:] += seg
R[d0:] += seg

# ---------------- normalize, write ----------------
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
stereo = (stereo * 32767).astype(np.int16)
with wave.open('/home/sprite/slop-salon-lou/assets/strip_wobble.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())
print(f"wrote assets/strip_wobble.wav  {stereo.shape[0]/SR:.1f}s  peak={peak:.3f}")

# ---------------- verify: rung pitches, slide ratios, mono keeps magnitudes -------
mono = (L.astype(np.float64) + R.astype(np.float64)) / 2
def rms_around(buf, tc, half=0.25):
    m = (tt > tc - half) & (tt < tc + half)
    return float(np.sqrt(np.mean(buf[m] ** 2)))
for t0, n in events:
    print(f"  rung {n} t={t0:.1f}  Lrms={rms_around(L, t0 + 0.8):.3f}  Rrms={rms_around(R, t0 + 0.8):.3f}  monorms={rms_around(mono, t0 + 0.8):.3f}")
