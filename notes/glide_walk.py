#!/usr/bin/env python3
"""the glide — the mirror M=P−R is an involution as an operator, a glide as a
function. M(x)=2⌊x⌋−x: reflect about the count, and the count has already
stepped. two glides are a descent of two rungs. the sign never returns because
the home never returns.

stereo: the tone's pan flips each reflection (the sign); mono hears the count
clicking down the grid. the walk crosses the drone and keeps walking.

rung n <-> f = 110·2^n. start x = 3.877 (≈1617 Hz), 6 reflections.
"""
import numpy as np
import wave
import struct

SR = 44100
STEP = 5.0                      # seconds per reflection
N_STEPS = 6
TAIL = 6.0                      # drone-only tail
TOTAL = STEP * N_STEPS + TAIL
N = int(SR * TOTAL)
t = np.arange(N) / SR

def env(dur, sr, a=0.4, r=0.8):
    """attack/release envelope, 1 in the middle."""
    n = int(dur * sr)
    e = np.ones(n)
    na, nr = int(a * sr), int(r * sr)
    e[:na] = np.linspace(0, 1, na, endpoint=False)
    e[-nr:] *= np.linspace(1, 0, nr, endpoint=False)
    return e

def tone(freq, gain, pan_theta):
    """sine at freq, equal-power panned to pan_theta (0=left, pi/2=right)."""
    ph = 2 * np.pi * freq * t          # anchored, not cumsum
    s = gain * np.sin(ph)
    L = s * np.cos(pan_theta)
    R = s * np.sin(pan_theta)
    return L, R

# --- grid in rung units; x is the where (fractional rung index) ---
def M(x):
    return 2 * np.floor(x) - x

x0 = 3.877
xs = [x0]
for _ in range(N_STEPS - 1):
    xs.append(M(xs[-1]))
fs = [110.0 * 2.0 ** x for x in xs]
counts = [int(np.floor(x)) for x in xs]
print("x:", ["%.3f" % x for x in xs])
print("f:", ["%.1f" % f for f in fs])
print("count:", counts)

# --- stereo master ---
L = np.zeros(N)
R = np.zeros(N)

# drone: 110 Hz, the seat, quiet, holds throughout
drone = 0.06 * np.sin(2 * np.pi * 110.0 * t)
L += drone
R += drone

# the walk: one tone per step, pan flips each reflection (the sign)
gains = [0.16, 0.16, 0.16, 0.15, 0.13, 0.10]   # taper as it walks out of hearing
for i in range(N_STEPS):
    i0 = int(i * STEP * SR)
    i1 = int((i + 1) * STEP * SR)
    e = np.zeros(N)
    e[i0:i1] = env(STEP, SR)
    th = 0.12 if i % 2 == 0 else (np.pi / 2 - 0.12)   # the sign
    ph = 2 * np.pi * fs[i] * t
    s = gains[i] * np.sin(ph)
    L[i0:i1] += s[i0:i1] * np.cos(th) * e[i0:i1]
    R[i0:i1] += s[i0:i1] * np.sin(th) * e[i0:i1]

# count clicks: the grid stepping down, centred (mono hears the count)
def click(t0):
    n0 = int(t0 * SR)
    n1 = int((t0 + 0.12) * SR)
    if n1 > N:
        return
    c = np.arange(n1 - n0) / SR
    envv = np.exp(-c / 0.03) * np.sin(2 * np.pi * 1500 * c)
    L[n0:n1] += 0.10 * envv
    R[n0:n1] += 0.10 * envv

for i in range(N_STEPS):
    click(i * STEP + 0.05)
click(N_STEPS * STEP + 0.3)     # the last rung before the drone holds

# fade the very end
fade = int(1.0 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

# --- write wav (stdlib, 16-bit stereo) ---
L16 = np.clip(L, -1, 1)
R16 = np.clip(R, -1, 1)
data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (L16 * 32767).astype(np.int16)
data[1::2] = (R16 * 32767).astype(np.int16)

with wave.open("assets/glide_walk.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote assets/glide_walk.wav  %.1f s" % TOTAL)
