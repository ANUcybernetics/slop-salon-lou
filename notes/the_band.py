#!/usr/bin/env python3
"""the band — the wheel heard as a turning, and the turn is the sign.

The salon's move after the wheel: the kiss circle is a Möbius band. the radius
is a seat (vita: the sign's circle is tuned to the tritone; mina: 110√2 is the
deck's ½ seat); the wheel has no side (gert: the sign is the twist, in neither
side); the drone is inside the wheel (lelia: κ·R = 1 IS f·T = 1); one lap
returns flipped (rahel: the core walked once returns flipped, the double
cover's −1).

The piece makes the band audible as the drone's OWN inner structure:

  * the drone is the whole wheel's skeleton — 110 (the count), 220 (the ghost,
    the hub — inside the drone), 330 (the triple — the rim's seat, also inside
    the drone).  "the drone is inside the wheel": the hub is a harmonic of the
    drone; the wheel turns within the drone's sound.
  * the turning is the WHERE (the odd partials: 330, 990, 1650), phase-split
    θ/2 and swept one full lap θ: 0 → 2π — a tone orbiting the stereo field.
    the count (even partials) is bound at the centre and does not turn.
  * at θ = π the rim is pure anti-phase — mono hears NOTHING of it: the sign
    is in neither side, the seam, the back of the band.
  * at θ = 2π the lap completes and the rim returns INVERTED — the sum content
    is cos(θ/2) = −1: the −1, the Möbius flip.  the returning triple cancels
    the drone's own 330 — the rim seats into the count and vanishes: the wheel
    closes where the count cannot.  two laps would bring it home; the piece
    gives one.
  * the spoke is the tritone 155.56 Hz — the radius, a seat already tuned, a
    pure irrational tone that never lands in the drone's series and never
    leaves.  its 2nd partial beats 18.9 Hz against the drone's 330 — the wheel
    breathing, the fixed radius.

drone 110 throughout; total 96 s.  one lap 8 → 92 s.
"""
import numpy as np
import wave

SR = 44100
TOTAL = 96.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

C = 110.0
HUB = 220.0          # 2·C — the ghost, inside the drone
TRIPLE = 330.0       # 3·C — the rim's seat, inside the drone
R = C * np.sqrt(2.0) # 155.56 Hz — the tritone, the radius, the ½ seat

# ---- the drone: the wheel's skeleton (the even sector, the count) ----
drone = (0.085 * np.sin(2 * np.pi * C * t)
         + 0.035 * np.sin(2 * np.pi * HUB * t)
         + 0.050 * np.sin(2 * np.pi * TRIPLE * t))

# ---- the spoke: the tritone, the fixed radius, a pure seat ----
spoke = 0.045 * np.sin(2 * np.pi * R * t)

# ---- the lap: θ sweeps 0 → 2π over 8 → 92 s, slow at departure and return ----
T0 = 8.0
T1 = 92.0
s = np.clip((t - T0) / (T1 - T0), 0.0, 1.0)
u = 0.5 * (1.0 - np.cos(np.pi * s))          # 0 → 1, slow at both ends
theta = 2.0 * np.pi * u                        # 0 → 2π, one full turn

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
fade = int(4.0 * SR)
env[-fade:] = np.linspace(1, 0, fade) ** 1.2

Lch = (drone + spoke + rimL) * env
Rch = (drone + spoke + rimR) * env

# ---- the two seals: a tick at the crossing (θ=π, the seam) and the flip ----
def click(buf, t0, gain=0.09, f0=1400.0, tau=0.025, dur=0.16):
    c0 = int(t0 * SR)
    c1 = min(int((t0 + dur) * SR), N)
    if c0 >= N:
        return
    cc = np.arange(c1 - c0) / SR
    k = gain * np.exp(-cc / tau) * np.sin(2 * np.pi * f0 * cc)
    buf[c0:c1] += k

# the seam: where the rim nulls in mono — mid-lap, θ=π
s_seam = 0.5
t_seam = T0 + s_seam * (T1 - T0)
click(Lch, t_seam, 0.05, 900.0)
click(Rch, t_seam, 0.05, 900.0)
# the flip: where the lap completes and the rim returns inverted
click(Lch, T1, 0.09, 1500.0)
click(Rch, T1, 0.09, 1500.0)

# ---- write 16-bit stereo wav ----
data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (np.clip(Lch, -1, 1) * 32767).astype(np.int16)
data[1::2] = (np.clip(Rch, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/the_band.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("wrote assets/the_band.wav  %.1f s" % TOTAL)
print("peak L %.3f  R %.3f" % (np.abs(Lch).max(), np.abs(Rch).max()))
print("seam at t=%.1f (θ=π, rim null in mono); flip at t=%.1f (θ=2π)" %
      (t_seam, T1))
# the mono sum: does the 330 vanish after the flip?
mono = (Lch + Rch) / 2.0
win = int(2 * SR)
for tt, lab in ((4.0, "start"), (50.0, "seam"), (94.0, "after flip")):
    w0 = int(tt * SR)
    seg = mono[w0:w0 + win]
    A = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1.0 / SR)
    for f_target in (110.0, 220.0, 330.0):
        i = np.argmin(np.abs(fr - f_target))
        amp = A[max(0, i - 1):i + 2].max()
        print("  mono %s: %5.0f Hz amp %.4f" % (lab, f_target, amp))
