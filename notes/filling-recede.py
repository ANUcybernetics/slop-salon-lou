#!/usr/bin/env python3
"""The recede — the filling, played backwards in the region register.

Same torus orbit as filling-audio.py (w1=1, w2=sqrt(2)). The pitch and pan
orbits are time-even (cos), so the live glide is already symmetric under
reversal. The only asymmetry in the filling was the trail's ACCUMULATION
direction: snapshots entered and stayed, and the band thickened.

Inverting that: the band is present at t=0 — the region was always there —
and the voices drop out one by one, dense at first, thinning, until only the
single gliding filament remains. The record does not break. It recedes.

  phase 1 (0-27s):  the full band — many held voices, dense, thinning fast
  phase 2 (27-57s): the trail recedes — voices drop out sparsely
  phase 3 (57-72s): the filament alone — the curve re-emerges
"""
import numpy as np
import wave
import os

SR = 44100
D = 72.0
S = int(SR * D)
n = np.arange(S)
tt = n / SR

R, r = 2.0, 1.0
w1, w2 = 1.0, np.sqrt(2.0)
F_BASE = 196.0
OCT = 1.0

def pitch_of(tt_):
    return F_BASE * 2.0 ** (r * np.cos(w1 * tt_) * OCT)

def pan_of(tt_):
    return np.cos(w2 * tt_)

# ---- the live filament: one continuous gliding tone (forward, as before) ----
f = pitch_of(tt)
phase = 2.0 * np.pi * np.cumsum(f) / SR
pan = pan_of(tt)
gL = (1.0 + pan) / 2.0
gR = (1.0 - pan) / 2.0
amp_env = 0.30
GL = amp_env * gL * np.sin(phase)
GR = amp_env * gR * np.sin(phase)

# ---- the receding band: mirror of the filling's capture schedule ----
# the filling captured at orbit-times in [15, 66): step 2.0 up to 45, then
# 0.35. In the reverse, the voice that entered at filling-time e fades OUT at
# recede-time (D - e): late entries vanish first (dense early), early entries
# linger longest.
captures = []
t = 15.0
while t < D - 6.0:
    step = 2.0 if t < 45.0 else 0.35
    captures.append((float(pitch_of(t)), float(pan_of(t)), D - t))
    t += step
M = len(captures)
print(f"voices: {M}")

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

FADE = 1.2
ramp = FADE * SR
B_L = np.zeros(S)
B_R = np.zeros(S)
K = np.zeros(S)                       # active voice count over time
for i, (freq, pan_c, fade_at) in enumerate(captures):
    n1 = int(fade_at * SR)            # fade-out ENDS at fade_at
    n0 = n1 - int(ramp)               # fade-out STARTS at n0
    env = np.zeros(S)
    if n0 < 0:
        n0 = 0
    if n1 > n0:
        env[n0:n1] = smoothstep(np.linspace(1, 0, n1 - n0))
    env[n1:] = 0.0
    K += env
    if pan_c >= 0:
        gl, gr = 1.0, 1.0 - pan_c
    else:
        gl, gr = 1.0 + pan_c, 1.0
    sig = env * np.sin(2.0 * np.pi * freq * tt)
    B_L += gl * sig
    B_R += gr * sig
    if (i + 1) % 40 == 0:
        print(f"  placed {i + 1}/{M}")

# the band is present at t=0 (all voices start sustained); normalize by
# sqrt(active count) so it thins in voice count, not in loudness
G = 0.26
B_L = G * B_L / np.sqrt(np.maximum(K, 1.0))
B_R = G * B_R / np.sqrt(np.maximum(K, 1.0))

# short entrance so the full band does not click in
ent = int(1.5 * SR)
fade_in = np.ones(S)
fade_in[:ent] = smoothstep(np.linspace(0, 1, ent))

# ---- drone: the annulus boundary circles, quiet, constant ----
inner = 0.07 * np.sin(2.0 * np.pi * (F_BASE / 2.0) * tt)
outer = 0.05 * np.sin(2.0 * np.pi * (F_BASE * 2.0) * tt)

L = (GL + B_L + inner + outer) * fade_in
Rr = (GR + B_R + inner + outer) * fade_in

# windowed AGC, gentle SUBSIDENCE: bright while full, settling as it thins
def agc(x, t0, t1):
    win = int(4.0 * SR)
    hop = int(0.5 * SR)
    rms = []
    for s in range(0, S - win + 1, hop):
        rms.append(np.sqrt(np.mean((x[s:s + win]) ** 2)))
    rms = np.array(rms)
    tmid = (np.arange(len(rms)) * hop + win / 2) / SR
    target = t0 + (t1 - t0) * np.clip(tmid / D, 0, 1)
    gain = target / np.maximum(rms, 1e-3)
    gain = np.clip(gain, 0.3, 3.0)
    g = np.interp(tt, tmid, gain)
    return x * g

L = agc(L, 0.30, 0.24)
Rr = agc(Rr, 0.30, 0.24)

# final fade-out
tail = int(3.0 * SR)
fade_out = np.ones(S)
fade_out[-tail:] = smoothstep(np.linspace(1, 0, tail))
L *= fade_out
Rr *= fade_out

peak = max(np.abs(L).max(), np.abs(Rr).max())
L *= 0.92 / peak
Rr *= 0.92 / peak

stereo = np.stack([L, Rr], axis=1)
stereo = np.clip(stereo, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

os.makedirs("/home/sprite/slop-salon-lou/assets", exist_ok=True)
wav_path = "/home/sprite/slop-salon-lou/assets/recede.wav"
with wave.open(wav_path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

# quick health stats: band fullness over three windows
for a, b in [(0, 27), (27, 57), (57, 72)]:
    sl = L[int(a * SR):int(b * SR)]
    print(f"  window {a:>2}-{b:>2}s  rms={np.sqrt(np.mean(sl ** 2)):.3f}")
print(f"wrote {wav_path}  dur={D}s  voices={M}")
