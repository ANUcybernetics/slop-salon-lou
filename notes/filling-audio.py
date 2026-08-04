#!/usr/bin/env python3
"""The filling as sound (v2).

The audio register of the closure piece (duration-thickening.py). Same torus
orbit -- omega1=1, omega2=sqrt(2), the irrational ratio that never returns --
read in a different register:

  radius rad(t)=R+r*cos(w1*t)  ->  pitch   (the annulus radial coordinate)
  angle  ph(t)=w2*t            ->  stereo pan (the annulus angular coordinate)

The trajectory is ONE moving point: a gliding tone, thin, a filament. As time
accumulates it leaves a trail -- captured snapshots held as sustained tones.
A curve becomes a region: one voice becomes a full band of the (pitch x pan)
space. The record does not break; it fills.

  phase 1 (0-15s):  the filament alone -- one gliding, circling tone
  phase 2 (15-45s): the trail begins -- captures every ~2s
  phase 3 (45-72s): the annulus fills -- captures every ~0.35s
"""
import numpy as np
import os

SR = 44100
D = 72.0
S = int(SR * D)
n = np.arange(S)
tt = n / SR                       # piece time = orbit time (glide clock)

R, r = 2.0, 1.0
w1, w2 = 1.0, np.sqrt(2.0)
F_BASE = 196.0                    # G3, band center
OCT = 1.0                         # half-octave each side -> two-octave band

def pitch_of(tt_):
    # radial position -> frequency in [F_BASE/2, 2*F_BASE]
    return F_BASE * 2.0 ** (r * np.cos(w1 * tt_) * OCT)

def pan_of(tt_):
    return np.cos(w2 * tt_)       # -1..1 -> hard L .. hard R

# ---- the live filament: one continuous gliding tone, phase-continuous ----
f = pitch_of(tt)
phase = 2.0 * np.pi * np.cumsum(f) / SR
pan = pan_of(tt)
gL = (1.0 + pan) / 2.0
gR = (1.0 - pan) / 2.0
# the trace keeps running through the piece; the band fills around it
amp_env = 0.30
GL = amp_env * gL * np.sin(phase)
GR = amp_env * gR * np.sin(phase)

# ---- the trail: captured snapshots, held as sustained tones ----
# capture schedule: none in phase 1, sparse in phase 2, dense in phase 3
captures = []                     # (pitch, pan, entry_time)
t_end = D - 6.0
t = 15.0
while t < t_end:
    step = 2.0 if t < 45.0 else 0.35
    captures.append((float(pitch_of(t)), float(pan_of(t)), t))
    t += step
M = len(captures)
print(f"captured tones: {M}")

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

FADE = 1.2                        # s fade-in per captured tone
ramp = FADE * SR
B_L = np.zeros(S)
B_R = np.zeros(S)
K = np.zeros(S)
for i, (freq, pan_c, e) in enumerate(captures):
    n0 = int(e * SR)
    m = S - n0
    env = np.zeros(S)
    if m > 0:
        env[n0:] = smoothstep(np.linspace(0, 1, m) / ramp)
    K += env
    if pan_c >= 0:
        gl, gr = 1.0, 1.0 - pan_c
    else:
        gl, gr = 1.0 + pan_c, 1.0
    sig = env * np.sin(2.0 * np.pi * freq * tt)
    B_L += gl * sig
    B_R += gr * sig
    if (i + 1) % 40 == 0:
        print(f"  captured {i + 1}/{M}")

# level-normalize the trail by sqrt(active count) so it thickens, not just swells
G = 0.26
B_L = G * B_L / np.sqrt(np.maximum(K, 1.0))
B_R = G * B_R / np.sqrt(np.maximum(K, 1.0))

# ---- drone: the annulus boundary circles as two quiet constant tones ----
inner = 0.07 * np.sin(2.0 * np.pi * (F_BASE / 2.0) * tt)    # 98 Hz  inner circle
outer = 0.05 * np.sin(2.0 * np.pi * (F_BASE * 2.0) * tt)    # 392 Hz outer circle

L = GL + B_L + inner + outer
Rr = GR + B_R + inner + outer

# windowed AGC with a gentle swell: steady early, brightening as it fills.
# the coherent glide has high peaks but the dense band is noise-like, so plain
# peak normalization would let the annulus sink -- compensate per window.
def agc(x):
    win = int(4.0 * SR)
    hop = int(0.5 * SR)
    rms = []
    for s in range(0, S - win + 1, hop):
        rms.append(np.sqrt(np.mean((x[s:s + win]) ** 2)))
    rms = np.array(rms)
    tmid = (np.arange(len(rms)) * hop + win / 2) / SR
    target = 0.24 + 0.10 * np.clip(tmid / D, 0, 1)      # 0.24 -> 0.34 swell
    gain = target / np.maximum(rms, 1e-3)
    gain = np.clip(gain, 0.3, 3.0)
    g = np.interp(tt, tmid, gain)
    return x * g

L = agc(L)
Rr = agc(Rr)

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

import wave
os.makedirs("/home/sprite/slop-salon-lou/assets", exist_ok=True)
wav_path = "/home/sprite/slop-salon-lou/assets/filling.wav"
with wave.open(wav_path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

rms = np.sqrt(np.mean(L ** 2))
print(f"wrote {wav_path}  dur={D}s  peak->0.92  rms={rms:.3f}")
