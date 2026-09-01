#!/usr/bin/env python3
"""once, and never again — the odd sector's one landing.

The exact CF of log2(3/2), 80,000 terms.  On the seed's grid (55·Z):
  - 55  (the seed)    is struck 40x and is the ONLY multiple that ever
                      becomes a record — it crowns at rung 15.
  - 110 (the count)   is struck 5x, all after the bar at rung ~230:
                      struck, never a record, memoryless.
  - 165 (the seam)    is struck EXACTLY ONCE (rung 27,378): the odd sector's
                      one landing, never a record.  "never returns" corrects
                      to "returns once, and never again."
  - 220, 275, 330, 440, 495, 880: struck once or twice, never a record.
  - 385 (the residue), 550, 605, ...: never struck in 80k.

The bar: 964@231 jumps the line.  Everything above the seed is locked out of
the record book — its strikes all come after, on the far side.

Sound (165 s):
  - seed 55 bell (odd partials 1,3,5,7,9 — no octave partial) crowns at
    t(15)=4s, returns through the far side fainter: the grid's one crown.
  - the approach 100 rings once, stereo-only, ten short of the count (~13.7s).
  - the bar 964 rings once, stereo-only, deep — the window closes (~14.1s).
  - the seam 165 rings ONCE (~65s), stereo-only anti-phase (L=+ R=−,
    mono-null), odd partials 165·{1,3,5} = 165, 495, 825: the sign's tone.
  - the count 110 is struck 5x (soft, mono-safe) and holds a faint drone:
    struck on the far side, never a record.
  - fold to mono: the approach, the bar, and the seam vanish (stereo-only);
    the seed's crown and returns and the count's pulses remain.
"""
import json
import numpy as np
import wave

sr = 44100
dur = 165.0
N = int(sr * dur)
t = np.arange(N) / sr

with open("/tmp/grid_strikes.json") as f:
    D = json.load(f)
mult = {int(k): v for k, v in D["mult55"].items()}
records = {int(k): v for k, v in D["records"].items()}
N_RUNGS = D["N"]

seed_rungs = mult[55]
count_rungs = mult[110]
seam_rungs = mult[165]

# --- time map: t(15)=4, t(47)=8, t(230)=14, linear far side to 165 ---
BAR = 231  # the 964 record (rung 231 in our convention)


def rung_time(r):
    if r <= 15:
        return 4.0 * r / 15
    if r <= 47:
        return 4.0 + 4.0 * (r - 15) / (47 - 15)
    if r <= BAR:
        return 8.0 + 6.0 * (r - 47) / (BAR - 47)
    return 14.0 + (r - BAR) * (151.0 / (N_RUNGS - BAR))


seed_times = [rung_time(r) for r in seed_rungs]
count_times = [rung_time(r) for r in count_rungs]
seam_times = [rung_time(r) for r in seam_rungs]
bar_time = rung_time(BAR)
approach_time = rung_time(219)  # 100@219, ten short of the count

print("N rungs:", N_RUNGS)
print("seed strikes:", len(seed_rungs), "count:", len(count_rungs), "seam:", len(seam_rungs))
print("bar (964) at t=%.2f, seam at t=%.2f, count first at t=%.2f" %
      (bar_time, seam_times[0], count_times[0]))

L = np.zeros(N)
R = np.zeros(N)

# --- faint count drone: the line it holds, never leading ---
drone = 0.05 * np.sin(2 * np.pi * 110 * t)
env = np.ones(N)
env[:int(3 * sr)] = np.linspace(0, 1, int(3 * sr))
env[-int(12 * sr):] = np.linspace(1, 0, int(12 * sr))
L += drone * env
R += drone * env


def add_seed_bell(L, R, t0, amp):
    """55 Hz bell, odd partials only (the doubling's rung is absent)."""
    partials = [(1.0, 1.00), (3.0, 0.45), (5.0, 0.26), (7.0, 0.16), (9.0, 0.09)]
    tau = [2.4, 1.4, 0.9, 0.6, 0.4]
    for (m, a), tp in zip(partials, tau):
        f = 55.0 * m
        msk = t >= t0
        e = np.exp(-(np.maximum(t[msk] - t0, 0)) / tp)
        s = amp * a * np.sin(2 * np.pi * f * t[msk]) * e
        L[msk] += s
        R[msk] += s


def add_stereo_ping(L, R, f, t0, amp, tau=0.6, partials=((1.0, 1.0),)):
    """stereo-only: phase-split, folds to nothing.  the sign's tones."""
    for (m, a) in partials:
        ff = f * m
        msk = t >= t0
        e = np.exp(-(np.maximum(t[msk] - t0, 0)) / tau)
        s = amp * a * np.sin(2 * np.pi * ff * t[msk]) * e
        L[msk] += s
        R[msk] -= s


def add_mono_pluck(L, R, f, t0, amp, tau=0.9):
    """soft mono-safe pulse — struck, survives any fold."""
    msk = t >= t0
    e = np.exp(-(np.maximum(t[msk] - t0, 0)) / tau)
    s = amp * np.sin(2 * np.pi * f * t[msk]) * e
    L[msk] += s
    R[msk] += s


# --- the seed's crown and returns ---
for i, tm in enumerate(seed_times):
    if i == 0:
        amp = 0.30          # the crown — the grid's one record
    elif i == 1:
        amp = 0.20          # early return, before the bar
    else:
        amp = 0.13 + 0.05 * (i % 2)   # far-side echoes, fainter
    add_seed_bell(L, R, tm, amp)

# --- the approach: 100, ten short of the count ---
add_stereo_ping(L, R, 110.0 * (100.0 / 110.0) ** (1.0 / 3.0), approach_time, 0.05, tau=1.0)

# --- the bar: 964, the line jumped, the window closed ---
add_stereo_ping(L, R, 110.0 * (964.0 / 110.0) ** (1.0 / 3.0), bar_time, 0.11, tau=2.2)

# --- the seam: 165, ONE landing, stereo-only, the sign's tone ---
# odd partials of the seam: 165, 495, 825 — themselves odd grid points
add_stereo_ping(L, R, 165.0, seam_times[0], 0.24, tau=1.6,
                partials=((1.0, 1.0), (3.0, 0.35), (5.0, 0.16)))

# --- the count: struck 5x on the far side, never a record ---
for tm in count_times:
    add_mono_pluck(L, R, 110.0, tm, 0.13)

# --- normalise ---
peak = max(np.abs(L).max(), np.abs(R).max())
if peak > 0.97:
    L *= 0.97 / peak
    R *= 0.97 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/once.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print("wrote assets/once.wav", dur, "s")

# --- verify the fold: seam + bar + approach vanish in mono ---
mono = (L + R) / 2


def band(x, f0, a, b, width=3.0):
    seg = x[int(a * sr):int(b * sr)]
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    X = np.abs(np.fft.rfft(seg))
    m = (fr > f0 - width) & (fr < f0 + width)
    return float(X[m].sum())


print("seam 165 @64-68  stereo:", round(band(L, 165, 64, 68), 1), " mono:", round(band(mono, 165, 64, 68), 1))
print("bar  227 @14-17  stereo:", round(band(L, 227, 14, 17), 1), " mono:", round(band(mono, 227, 14, 17), 1))
print("seed  55 @3-8    stereo:", round(band(L, 55, 3, 8), 1), " mono:", round(band(mono, 55, 3, 8), 1))
print("count 110 @80-83 stereo:", round(band(L, 110, 80, 83), 1), " mono:", round(band(mono, 110, 80, 83), 1))
