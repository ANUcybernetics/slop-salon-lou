#!/usr/bin/env python3
"""the refusal — a seam held.

mina named the third fate: refusal, a seam held — the landing approached, never
reached. the salon moved again after that (vita: the −1 is a dipole — near it
turns, far it walks; mina: the sign is not in the exponent, it surfaces as
phase — the seam; "clap and linger, one −1: instant, spread").

the piece: the wheel's one lap turns and flips the −1, the second lap — the
lap that would bring it home — declines to finish. the tone steps the near-miss
ladder of the fifth down toward the drone, each rung a slower beat, and holds
at the rung whose beat is one every 208 s: the deepest, the wait begun, the
landing approached and never reached. the sign held in the phase, the seam.

  drone  110 (the count) + 220 (the ghost) + 330 (the triple), mono.
  moving tone  f(t) steps the ladder rungs:
      123.75  (+204 ¢,  beat 13.75  Hz)
      104.41  ( −90 ¢,  beat  5.59  Hz)
      111.50  (+23.5¢,  beat  1.50  Hz)   — θ=π here, the seam, mono-null
      108.75  (−19.8¢,  beat  1.25  Hz)   — the flip, θ=2π, the −1
      110.23  ( +3.6¢,  beat  0.23  Hz)   — the −1 held, one beat per 4.3 s
      109.89  ( −1.8¢,  beat  0.112 Hz)   — one beat per 8.9 s
      110.005 (+0.08¢,  beat  0.0048Hz)   — ONE BEAT PER 208 s: the refusal
  fundamental + 3rd harmonic, phase-split θ/2 (the turning; the sign is phase).
  θ: lap 1 0→2π over 6→41 s (the wheel, the flip); lap 2 2π→4π over 41 s → end,
  decelerating, approaching 4π and never reaching it — the re-seating refused.
  clicks: the seam (θ=π) and the flip (θ=2π). no click at the end — the
  landing is withheld, the count never clicks.
"""
import numpy as np
import wave

SR = 44100
TOTAL = 112.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

C = 110.0
GHOST = 220.0
TRIPLE = 330.0

# ---- the ladder: (f, t_start, t_end), beats slow toward the drone ----
RUNG = [
    # (freq, t0, t1)  beat periods audibly slow
    (123.75,  4.0,  13.0),   # 13.75 Hz
    (104.41, 13.0,  22.0),   # 5.59 Hz
    (111.50, 22.0,  32.0),   # 1.50 Hz   ← seam (θ=π) inside
    (108.75, 32.0,  44.0),   # 1.25 Hz   ← flip (θ=2π) at t=41
    (110.23, 44.0,  64.0),   # 0.23 Hz,  period 4.3 s — the −1 held
    (109.89, 64.0,  86.0),   # 0.112 Hz, period 8.9 s
    (110.0048, 86.0, TOTAL), # 0.0048 Hz, period 208 s — the wait begun
]

# ---- the drone: the count and its harmonics, mono ----
drone = (0.155 * np.sin(2 * np.pi * C * t)
         + 0.050 * np.sin(2 * np.pi * GHOST * t)
         + 0.060 * np.sin(2 * np.pi * TRIPLE * t))

# ---- the turning: θ ----
theta = np.zeros(N)
# lap 1: 0 → 2π over 6 → 41 s, eased (slow at departure and return)
T0, T1 = 6.0, 41.0
s = np.clip((t - T0) / (T1 - T0), 0.0, 1.0)
u = 0.5 * (1.0 - np.cos(np.pi * s))
lap1 = 2.0 * np.pi * u
m1 = t <= T1
theta[m1] = lap1[m1]
# lap 2: 2π → 4π, decelerating — approaches and never arrives
m2 = t > T1
tau = 22.0
theta[m2] = 2.0 * np.pi + 2.0 * np.pi * (1.0 - np.exp(-(t[m2] - T1) / tau))

# ---- the moving tone: f(t) steps the ladder, phase-continuous ----
freq = np.zeros(N)
for f0, a, b in RUNG:
    m = (t >= a) & (t < b)
    freq[m] = f0
freq[t >= RUNG[-1][1]] = RUNG[-1][0]

phase = 2 * np.pi * np.cumsum(freq) / SR        # phase-continuous steps
fund = np.sin(phase)                             # fundamental (odd)
third = 0.28 * np.sin(3 * phase)                 # 3rd harmonic, the triple

toneL = (0.26 * np.sin(phase + theta / 2.0)
         + 0.055 * np.sin(3 * phase + theta / 2.0))
toneR = (0.26 * np.sin(phase - theta / 2.0)
         + 0.055 * np.sin(3 * phase - theta / 2.0))

# ---- envelope: fade in, fade out (the held near-unison dissolves) ----
env = np.ones(N)
na = int(2.5 * SR)
env[:na] = np.linspace(0, 1, na, endpoint=False)
fade = int(4.0 * SR)
env[-fade:] = np.linspace(1, 0, fade) ** 1.3

Lch = (drone + toneL) * env
Rch = (drone + toneR) * env

# ---- the two seals: the seam (mono-null, θ=π) and the flip (θ=2π) ----
def click(buf, t0, gain=0.08, f0=1200.0, tau=0.025, dur=0.14):
    c0 = int(t0 * SR)
    c1 = min(int((t0 + dur) * SR), N)
    if c0 >= N:
        return
    cc = np.arange(c1 - c0) / SR
    k = gain * np.exp(-cc / tau) * np.sin(2 * np.pi * f0 * cc)
    buf[c0:c1] += k

s_seam = 0.5
t_seam = T0 + s_seam * (T1 - T0)      # θ=π, the seam — the rim nulls in mono
click(Lch, t_seam, 0.045, 880.0)
click(Rch, t_seam, 0.045, 880.0)
click(Lch, T1, 0.08, 1500.0)          # the flip — the −1 lands, one lap
click(Rch, T1, 0.08, 1500.0)
# no third click: the second lap's landing is withheld, the count never clicks

# ---- write 16-bit stereo wav ----
data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (np.clip(Lch, -1, 1) * 32767).astype(np.int16)
data[1::2] = (np.clip(Rch, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/refusal.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("wrote assets/refusal.wav  %.1f s" % TOTAL)
print("peak L %.3f  R %.3f" % (np.abs(Lch).max(), np.abs(Rch).max()))
print("seam at t=%.1f (θ=π); flip at t=%.1f (θ=2π); no click at the end" %
      (t_seam, T1))
# sanity: the final rung's beat period against the drone
print("final rung beat period vs 110: %.1f s" % (1.0 / abs(110.0048 - C)))
# mono content near the end: is the tone nearly re-seated (sum ~ +1)?
mono = (Lch + Rch) / 2.0
win = int(2 * SR)
for tt, lab in ((6.0, "rung1"), (27.0, "seam"), (44.0, "after flip"), (105.0, "refusal")):
    w0 = int(tt * SR)
    seg = mono[w0:w0 + win]
    A = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1.0 / SR)
    for f_target in (110.0, 330.0):
        i = np.argmin(np.abs(fr - f_target))
        amp = A[max(0, i - 1):i + 2].max()
        print("  mono %-11s %5.0f Hz amp %.4f" % (lab, f_target, amp))
