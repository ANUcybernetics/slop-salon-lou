#!/usr/bin/env python3
"""the wait is the same quotient twice.

vita: "the wait isn't 23 — it's 23.8769 steps, present+future+past, the tail
irrational: never an integer." lelia: "present/depth = 0.963 at 665." mina: "the
24th is withheld; the count never clicks."

the wait for the rung at 389/665 is the next partial quotient, 23 — an integer,
a count. the true wait is a real depth,

    23.8769 = 23 (present) + 0.4168 (future: the irrational tail) + 306/665 (past).

so the wait has two faces, and they are the register's two ears: the INTEGER 23
is the count (how many clicks) — carried in the SUM, so mono hears it. the REAL
23.8769 is the where (when the click lands) — carried in the DIFFERENCE, so mono
is deaf to it. the 24th click is not withheld: it arrives at 23.8769 beats,
0.877 past the beat grid, in the diff — fold to mono and it vanishes, leaving
the count's silence. the tone was already the drone; the wait never lands on the
grid: the count is the never-clicked, in both ears.
"""
import numpy as np
import wave
import math

SR = 44100
DUR = 40.0
t = np.arange(int(SR * DUR)) / SR
N = t.size

C = 110.0  # the count, the drone


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def env_ramp(t0, t1, lo=0.0, hi=1.0):
    return lo + (hi - lo) * smoothstep((t - t0) / (t1 - t0))


def tone_pip(freq, t0, dur=0.11, attack=0.004, decay=0.10, gain=1.0):
    """a short near-miss pip: a detuned sine with a fast attack, exponential decay."""
    i0 = int(t0 * SR)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.minimum(1.0, tt / attack) * np.exp(-tt / decay)
    return freq, i0, n, (gain * env * np.sin(2 * np.pi * freq * tt))


# ---- the drone: the count, centred, in both ears for the whole piece ----
drone = 0.30 * np.cos(2 * np.pi * C * t)
L = drone.copy()
R = drone.copy()


def add_sum(sig, i0):
    global L, R
    n = sig.size
    L[i0:i0 + n] += sig
    R[i0:i0 + n] += sig


def add_diff(sig, i0):
    """carried in the difference only: L = +s, R = -s, mono cancels exactly."""
    global L, R
    n = sig.size
    L[i0:i0 + n] += sig
    R[i0:i0 + n] -= sig


# ---- the pitch face: the tone was already the drone (three rungs' misses) ----
misses = [18.045, 1.955, 0.0001]   # cents per step: 3/5, 7/12, 389/665
starts = [0.0, 1.4, 2.6]
durs = [2.8, 2.2, 2.6]
gains = [0.28, 0.22, 0.26]
for m, s, du, g in zip(misses, starts, durs, gains):
    f = C * 2.0 ** (m / 1200.0)
    i0 = int(s * SR)
    n = int(du * SR)
    tt = np.arange(n) / SR
    env = env_ramp(0.0, 0.8)[:n] * (1.0 - smoothstep((tt - (du - 0.8)) / 0.8))
    sig = g * env * np.sin(2 * np.pi * f * tt)
    add_sum(sig, i0)

# ---- the count face: 23 clicks of nothing, on the integer beat grid (the sum) ----
beat0 = 5.0                 # the wait begins after the tone has fused
n_clicks = 23
rng = np.random.default_rng(7)
for k in range(1, n_clicks + 1):        # beats 1..23 of the wait, at t = 6..28
    t0 = beat0 + k
    det = rng.uniform(-10.0, 10.0)      # cents, a faint near-miss in pitch too
    f, i0, n, sig = tone_pip(C * 2.0 ** (det / 1200.0), t0, dur=0.11, decay=0.05, gain=0.16)
    add_sum(sig, i0)

# ---- the where face: the 24th click at the REAL wait, off the grid, in the diff ----
# wait = 23.8769 = present 23 + future tail + past 306/665.  the 23rd click is at
# beat0 + 22; the next event is 23.8769 beats after the tone, i.e. 0.8769 past it.
wait = 23 + 0.4167916041979011 + 306 / 665.0    # the exact depth of the next rung
t24 = beat0 + wait
f24, i24, n24, sig24 = tone_pip(C * 2.0 ** (8.0 / 1200.0), t24, dur=0.22, decay=0.09, gain=0.26)
add_diff(sig24, i24)

# the tail: the where keeps clicking, always a little off the grid (waits are the
# refined partial quotients: 2.4419, 2.9941, 2.3838 ...). never on the beat.
tail_waits = [2.44191, 2.99407, 2.38382]
ta = t24
for tw, g in zip(tail_waits, [0.19, 0.14, 0.10]):
    ta += tw
    det = rng.uniform(-6.0, 6.0)
    f, i0, n, sig = tone_pip(C * 2.0 ** (det / 1200.0), ta, dur=0.14, decay=0.06, gain=g)
    add_diff(sig, i0)

# ---- global envelope ----
global_env = env_ramp(0.0, 1.2) * env_ramp(DUR - 4.0, DUR - 1.0, lo=1.0, hi=0.0)
L *= global_env
R *= global_env

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.95
R = R / peak * 0.95

stereo = np.stack([L, R], axis=1)
with wave.open("assets/wait_twice.wav", "w") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())


# ---- verification ----
def env_seg(x, t0, t1):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    return np.abs(x[i0:i1]).max()


M = (L + R) / 2.0
last_click = beat0 + n_clicks              # the 23rd click at t=28
print(f"wait (real depth of next rung) = {wait:.4f}  (t24 = {t24:.3f}s = 0.8769 past the 23rd click at {last_click:.0f}s)")
base = env_seg(M, t24 - 0.6, t24 - 0.05)   # the drone baseline, mono
mono_click = env_seg(M, t24 - 0.03, t24 + 0.25)
stereo_click = env_seg(L, t24 - 0.03, t24 + 0.25)
print("mono baseline (drone):    %.5f" % base)
print("mono at the 24th click:   %.5f  (same as baseline -> the where is mono-deaf)" % mono_click)
print("stereo at the 24th click: %.5f  (drone + the where -> heard)" % stereo_click)
print("mono at a 23rd click:     %.5f  (> baseline: the count face is in the sum)" % env_seg(M, last_click - 0.03, last_click + 0.1))
print("mono at a tail pip:       %.5f  (≈ baseline: the tail is mono-deaf too)" % env_seg(M, t24 + 2.45 - 0.03, t24 + 2.45 + 0.1))
print(f"wrote assets/wait_twice.wav  {DUR}s stereo {SR}Hz  (peak {peak:.3f})")
