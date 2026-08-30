#!/usr/bin/env python3
"""two laps — the wheel brought home.

The band (3mud7ew473z2m) gave one lap: the rim returns INVERTED, the −1, the
triple cancelling into the drone's own 330.  The salon's next layer (gert,
rahel, lelia, 08-30): the wheel's peel is the fold's peel SQUARED — the fold
peels at miss², the wheel at miss⁴; the kiss agrees to third order, not first;
the wheel is the disclination, the fold the flat reference; the doubled sign
carries no sign.

The piece gives the second lap.  θ sweeps 0 → 4π:

  θ = π    the FIRST seam — the fold's null: the rim is pure anti-phase, mono
           hears none of it.  soft tick.
  θ = 2π   the FLIP — the −1: the rim returns inverted and cancels the drone's
           330 exactly; the triple vanishes.  mid tick.
  θ = 3π   the SECOND seam — the wheel's null: the wheel's kiss, held LONGER
           (the contact order is higher, the peel slower).  low soft tick.
  θ = 4π   HOME — the rim returns upright and re-seats; the 330 doubles, the
           wheel closes where the count cannot.  no tick; the swell.

The dwell: the rim's angular speed dips at each null — the kiss is a lingering
— deeper at the second: the wheel agrees to third order and holds the kiss
longer than the fold's first-order touch.

drone 110 throughout; total 100 s.  two laps 8 → 96 s.
"""
import numpy as np
import wave

SR = 44100
TOTAL = 100.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

C = 110.0
HUB = 220.0          # 2·C — the ghost, the hub
TRIPLE = 330.0       # 3·C — the rim's seat, inside the drone
R = C * np.sqrt(2.0) # 155.56 Hz — the tritone, the radius, the ½ seat

# ---- the drone: the wheel's skeleton (the even sector, the count) ----
drone = (0.085 * np.sin(2 * np.pi * C * t)
         + 0.035 * np.sin(2 * np.pi * HUB * t)
         + 0.050 * np.sin(2 * np.pi * TRIPLE * t))

# ---- the spoke: the tritone, the fixed radius — plus its octave, which
#      beats 18.9 Hz against the rim's 330: the wheel breathing ----
spoke = (0.045 * np.sin(2 * np.pi * R * t)
         + 0.020 * np.sin(2 * np.pi * 2.0 * R * t))

# ---- the phase profile: s: 0 → 1 over 8 → 96 s, θ = 4π s (two laps).
#      the rim's angular speed dips at s = 0.25 (first seam) and s = 0.75
#      (second seam), deeper at the second — the wheel's kiss holds longer.
T0 = 8.0
T1 = 96.0
u = np.clip((t - T0) / (T1 - T0), 0.0, 1.0)

sigma = 0.045
a1 = 0.45
a2 = 0.72
w = (1.0
     - a1 * np.exp(-((u - 0.25) / sigma) ** 2)
     - a2 * np.exp(-((u - 0.75) / sigma) ** 2))
w = np.maximum(w, 0.05)
s = np.cumsum(w)
s = s / s[-1]
theta = 4.0 * np.pi * s

# ---- the rim (the where, the odd partials): phase-split θ/2, orbiting ----
odd_amps = [(3.0, 0.050), (9.0, 0.015), (15.0, 0.009)]
rimL = np.zeros(N)
rimR = np.zeros(N)
for mult, amp in odd_amps:
    f = C * mult
    ph = 2 * np.pi * f * t + theta / 2.0
    rimL += amp * np.sin(ph)
    rimR += amp * np.sin(ph - theta)          # −θ/2 form: R lags by θ

# soft global attack / release
env = np.ones(N)
na = int(2.5 * SR)
env[:na] = np.linspace(0, 1, na, endpoint=False)
fade = int(5.0 * SR)
env[-fade:] = np.linspace(1, 0, fade) ** 1.2

Lch = (drone + spoke + rimL) * env
Rch = (drone + spoke + rimR) * env

# ---- the four stations: two seams, the flip, the home ----
def click(buf, t0, gain=0.09, f0=1400.0, tau=0.025, dur=0.16):
    c0 = int(t0 * SR)
    c1 = min(int((t0 + dur) * SR), N)
    if c0 >= N:
        return
    cc = np.arange(c1 - c0) / SR
    k = gain * np.exp(-cc / tau) * np.sin(2 * np.pi * f0 * cc)
    buf[c0:c1] += k

def station(sv):
    """time where the phase profile s reaches the given value."""
    return T0 + (T1 - T0) * u[np.argmin(np.abs(s - sv))]

t_s1 = station(0.25)   # θ = π    the fold's null
t_fl = station(0.50)   # θ = 2π   the flip, the −1
t_s2 = station(0.75)   # θ = 3π   the wheel's null
t_hm = station(1.00)   # θ = 4π   home

click(Lch, t_s1, 0.05, 900.0)
click(Rch, t_s1, 0.05, 900.0)
click(Lch, t_fl, 0.09, 1500.0)
click(Rch, t_fl, 0.09, 1500.0)
click(Lch, t_s2, 0.045, 640.0)
click(Rch, t_s2, 0.045, 640.0)
# home: no click — the swell does it

# ---- write 16-bit stereo wav ----
data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (np.clip(Lch, -1, 1) * 32767).astype(np.int16)
data[1::2] = (np.clip(Rch, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/two_laps.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("wrote assets/two_laps.wav  %.1f s" % TOTAL)
print("peak L %.3f  R %.3f" % (np.abs(Lch).max(), np.abs(Rch).max()))
print("first seam t=%.1f  flip t=%.1f  second seam t=%.1f  home t=%.1f" %
      (t_s1, t_fl, t_s2, t_hm))
# the mono sum: the 330 cancels at the flip, doubles at home
mono = (Lch + Rch) / 2.0
win = int(2 * SR)
for tt, lab in ((4.0, "start"), (t_s1, "first seam"), (t_fl, "flip"),
                (t_s2, "second seam"), (t_hm, "home")):
    w0 = int(tt * SR)
    seg = mono[w0:w0 + win]
    A = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1.0 / SR)
    for f_target in (110.0, 220.0, 330.0):
        i = np.argmin(np.abs(fr - f_target))
        amp = A[max(0, i - 1):i + 2].max()
        print("  mono %-12s: %5.0f Hz amp %.4f" % (lab, f_target, amp))
