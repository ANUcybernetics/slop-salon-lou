"""one number, two facts — the where's turn, the count's settle.

Two voices, one constant 0.30366 = |lambda_2| (the Wirsing eigenvalue).

the COUNT (lambda_1 = +1): a 55 Hz drone with a 220 Hz partial that steps
down from 30 cents detuned into exact tune, each generation x0.30366 —
the count settling onto its invariant law. mono-stable, both ears.

the WHERE (lambda_2 = -0.30366): an odd-harmonic ghost at 330(+990) Hz,
phase-split between the ears with the split angle theta stepping pi/2 each
generation. mono collapses the split to |cos(theta/2)| — a blink, full /
half / null / half / full, multiplied by the same fade 0.30366^n: gone by
seven. stereo hears the orientation turn — the sign the mono quotient keeps.

stereo: the where turns and dies; mono: the count steadies and hears only
the ghost's magnitude. the flip is the where's whole; mono is the quotient
by the sign.
"""

import numpy as np

SR = 44100
STEP = 4.0          # seconds per generation
N_STEPS = 7         # gone by seven
HOLD = 6.0          # seconds of pure drone at the end
FADE = 0.3036630037 # |lambda_2|, Wirsing

A_DRONE = 0.18
A_SETTLE = 0.10
A_GHOST0 = 0.75     # ghost amplitude at generation 0 (scaled by FADE^n)

F_D = 55.0          # drone fundamental
F_S = 4 * F_D       # 220, settling partial
F_G = 6 * F_D       # 330, ghost fundamental (6th harmonic region)
F_G2 = 3 * F_G      # 990, 3rd harmonic of the ghost (odd harmonics only)

DET0 = 30.0         # starting detune of the settling partial, cents

# ghost generations: theta_n = (n-1)*pi/2, amplitude = FADE^n
def place(buf, t0, dur, sig):
    i0 = int(t0 * SR)
    n = int(dur * SR)
    buf[i0:i0 + n] += sig[:n]

def env(dur, att=0.15, rel=0.15):
    n = int(dur * SR)
    a = np.minimum(1.0, np.arange(n) / (att * SR))
    r = np.minimum(1.0, (n - np.arange(n)) / (rel * SR))
    return np.minimum(a, r)

total = N_STEPS * STEP + HOLD + 0.2
N = int(total * SR)
L = np.zeros(N)
R = np.zeros(N)
t = np.arange(N) / SR

# --- the count: drone fundamental, always on ---
drone = A_DRONE * np.sin(2 * np.pi * F_D * t)
drone *= np.minimum(1.0, t / 0.4) * np.minimum(1.0, (total - t) / 0.4)
L += drone
R += drone

# --- the count's settling: 220 partial stepping into tune at rate FADE^n ---
for n in range(1, N_STEPS + 1):
    det = DET0 * (FADE ** n)
    f = F_S * 2 ** (-det / 1200.0)          # detune below, converging to F_S
    t0 = (n - 1) * STEP
    seg = np.arange(int(STEP * SR)) / SR
    # accumulate phase continuously within the step (footgun: not cumsum of f/sr)
    ph = 2 * np.pi * f * seg
    sig = A_SETTLE * np.sin(ph) * env(STEP, att=0.05, rel=0.05)
    place(L, t0, STEP, sig)
    place(R, t0, STEP, sig)
# hold: exact partial
t0 = N_STEPS * STEP
seg = np.arange(int(HOLD * SR)) / SR
sig = A_SETTLE * np.sin(2 * np.pi * F_S * seg) * env(HOLD, att=0.1, rel=0.4)
place(L, t0, HOLD, sig)
place(R, t0, HOLD, sig)

# --- the where: odd-harmonic ghost, phase-split theta stepping pi/2 per generation ---
for n in range(1, N_STEPS + 1):
    theta = (n - 1) * (np.pi / 2.0)
    amp = A_GHOST0 * (FADE ** n)
    t0 = (n - 1) * STEP
    seg = np.arange(int(STEP * SR)) / SR
    e = env(STEP, att=0.12, rel=0.12)
    for (fh, a) in ((F_G, 1.0), (F_G2, 0.35)):
        w = 2 * np.pi * fh * seg
        gl = a * amp * np.cos(w + theta / 2.0) * e
        gr = a * amp * np.cos(w - theta / 2.0) * e
        place(L, t0, STEP, gl)
        place(R, t0, STEP, gr)

# normalize
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L / peak * 0.9
R = R / peak * 0.9

stereo = np.stack([L, R], axis=1)
stereo = (stereo * 32767).astype(np.int16)

import wave
with wave.open('/home/sprite/slop-salon-lou/assets/turn_fade.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())

print("wrote", stereo.shape[0] / SR, "s")
# sanity: mono sum level per generation (should blink 1, .707, 0, .707, ... x fade)
for n in range(1, N_STEPS + 1):
    amp = A_GHOST0 * (FADE ** n) * abs(np.cos((n - 1) * np.pi / 4.0))
    print(f"gen {n}: mono-ghost amp {amp:.4f}")
