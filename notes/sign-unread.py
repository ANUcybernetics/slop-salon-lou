#!/usr/bin/env python3
"""the sign, unread (v2).

rahel (3msbtc4yebl2c): "unreachable isn't absent. the sign needs a closed loop
to be read; the irrational walk never presents one. it is the limit of walks
that close, and their verdicts disagree. the density is the sign spread past
counting."

Two layers.

THE GLIDE -- the irrational walk itself. radius->pitch, angle->pan on the
torus omega1=1, omega2=sqrt(2). A single phase-continuous tone that never
returns, sweeping the whole band. It never presents a closed loop, so the sign
can never be read off it.

THE LANDINGS -- the rational walks that close. The convergents p_n/q_n of
sqrt(2), each a walk that comes home a comma short or long, the verdict
(p^2-2q^2 = +-1) alternating. Each landing SNAPSHOTS the glide at that moment:
it captures the glide's pitch as its home, walks out and returns a hair sharp
or flat, then HOLDS the captured pitch as a sustained partial.

The first verdicts are loud -- the comma is big, the direction legible
(sharp settles right, flat left). The later ones are finer than hearing; the
hair still there, still alternating, but unreadable. The held snapshots pile
up into the band. The glide keeps moving through them. The density is the
sign spread past counting.
"""
import numpy as np
import wave
import os
import math

SR = 44100
D = 55.0
S = int(SR * D)
tt = np.arange(S) / SR
F = 196.0                      # band center G3
OCT = 1.0
w1, w2 = 1.0, np.sqrt(2.0)

def glide_pitch(t):
    return F * 2.0 ** (math.cos(w1 * t) * OCT)

def glide_pan(t):
    return math.cos(w2 * t)

# ---- the irrational glide, phase-continuous ----
gf = F * 2.0 ** (np.cos(w1 * tt) * OCT)
gphase = 2.0 * np.pi * np.cumsum(gf) / SR
gpan = np.cos(w2 * tt)
gL = (1.0 + gpan) / 2.0
gR = (1.0 - gpan) / 2.0
glide_amp = np.ones(S)
glide_amp[:int(2.0 * SR)] = np.linspace(0, 1, int(2.0 * SR))  # fade glide in
gamp = 0.12 * glide_amp
GL = gamp * gL * np.sin(gphase)
GR = gamp * gR * np.sin(gphase)

# ---- the convergents of sqrt(2): [1;2,2,2,...] ----
def convergents(n):
    a = [1] + [2] * n
    p2, q2 = 0, 1
    p1, q1 = 1, 0
    out = []
    for an in a:
        p, q = an * p1 + p2, an * q1 + q2
        p2, q2, p1, q1 = p1, q1, p, q
        out.append((p, q))
    return out

landings = []                  # (cents_signed, p, q)
for p, q in convergents(13):
    if q == 1 and p == 1:
        continue
    cents = 1200 * math.log2(p / (q * math.sqrt(2)))
    landings.append((cents, p, q))

# ---- schedule: legible verdicts spaced out, fine ones tightening ----
events = []
for i, (cents, p, q) in enumerate(landings[:5]):
    events.append((cents, 1.5 + 3.2 * i))
for i, (cents, p, q) in enumerate(landings[5:12]):
    events.append((cents, 17.5 + 2.6 * i))

print("landings:")
for cents, t0 in events:
    print(f"  {cents:+.1f} c  at t={t0:.1f}")

# ---- the landings: snapshot the glide, walk out, come home a hair off ----
WALK = 2.0
W = int(WALK * SR)
L_buf = np.zeros(S)
R_buf = np.zeros(S)
ACT = np.zeros(S)

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

for j, (cents, t0) in enumerate(events):
    n0 = int(t0 * SR)
    home = glide_pitch(t0)              # the captured still of the irrational walk
    land_f = home * 2.0 ** (cents / 1200.0)
    A = math.copysign(min(500.0, max(2.2 * abs(cents), 30.0)), cents)
    side = 1.0 if cents > 0 else -1.0

    seg = np.zeros(S)
    seg[n0:] = 1.0
    ACT += seg

    m = S - n0
    u = np.zeros(m)
    u[:W] = np.linspace(0, 1, W)
    u[W:] = 1.0
    cpath = cents * u + A * np.sin(np.pi * u)     # cents away from home
    freq = home * 2.0 ** (cpath / 1200.0)
    phase = 2.0 * np.pi * np.cumsum(freq) / SR
    tone = np.sin(phase)

    env = np.zeros(m)
    env[:int(0.5 * SR)] = smoothstep(np.linspace(0, 1, int(0.5 * SR)))
    env[int(0.5 * SR):] = 1.0
    # settle toward the glide's pan slowly: verdicts on the side they declare
    pu = side * (2.0 * np.clip(u, 0, 1) - 1.0)
    gl = np.clip((1.0 - pu) / 2.0, 0.0, 1.0)
    gr = np.clip((1.0 + pu) / 2.0, 0.0, 1.0)

    sig = env * tone
    L_buf[n0:] += gl * sig
    R_buf[n0:] += gr * sig
    if (j + 1) % 4 == 0:
        print(f"  rendered {j + 1}/{len(events)}")

# ---- held partials: thicken the density, bounded by sqrt(active count) ----
G = 0.16
L_buf = G * L_buf / np.sqrt(np.maximum(ACT, 1.0))
R_buf = G * R_buf / np.sqrt(np.maximum(ACT, 1.0))

L = GL + L_buf
R = GR + R_buf

# ---- windowed AGC with a gentle swell ----
def agc(x):
    win = int(4.0 * SR)
    hop = int(0.5 * SR)
    rms = [np.sqrt(np.mean(x[s:s + win] ** 2)) for s in range(0, S - win + 1, hop)]
    rms = np.array(rms)
    tmid = (np.arange(len(rms)) * hop + win / 2) / SR
    target = 0.20 + 0.10 * np.clip(tmid / D, 0, 1)
    gain = target / np.maximum(rms, 1e-3)
    gain = np.clip(gain, 0.3, 3.5)
    g = np.interp(tt, tmid, gain)
    return x * g

L = agc(L)
R = agc(R)

tail = int(5.0 * SR)
fade = np.ones(S)
fade[-tail:] = smoothstep(np.linspace(1, 0, tail))
L *= fade
R *= fade

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak

stereo = np.clip(np.stack([L, R], axis=1), -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

os.makedirs("/home/sprite/slop-salon-lou/assets", exist_ok=True)
wav = "/home/sprite/slop-salon-lou/assets/sign-unread.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print(f"wrote {wav}  dur={D}s  peak->0.92")
