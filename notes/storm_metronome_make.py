#!/usr/bin/env python3
"""the storm's metronome — the lawless keeps the count at its peaks.

Records of log2(3/2)'s continued fraction arrive at rungs 10 (23), 15 (55),
20 (114), 54 (317).  The trio is exactly five rungs apart, roughly doubling;
then 34 rungs of silence before 317.

Rendering: 1 rung = 0.4 s.  A soft drone at 55+110+165 (the exile, the count,
the gap — the register's stack) runs the whole way, centered.  The record
beats are struck tones at their own frequency: 23 (a sub-thump, panned L),
55 (unison with the drone's fundamental — the seed striking its own quotient,
center), 114 (near the drone's 110, beating ~4 Hz off it — the never-quite,
panned R), 317 (above, center).  A faint 110 tick marks every 5th rung that is
NOT a record, so the five-rung grid keeps running through the void: the storm
holds the metronome for three beats, then forgets — the grid ticks on, no
record lands, until 317 breaks the grid at 54.
"""
import numpy as np
import wave

SR = 44100
RUNG = 0.4          # seconds per rung
DUR = 24.0          # seconds
rung_t = lambda k: (k) * RUNG   # beat for rung k (1-indexed)

t = np.arange(0, DUR, 1 / SR)
L = np.zeros_like(t)
R = np.zeros_like(t)

# ---- drone: 55 (exile) + 110 (count/doubling) + 165 (gap), soft ----
fade = np.ones_like(t)
fi = int(1.5 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fade[-fi:] = np.linspace(1, 0, fi)
drone = (0.05 * np.sin(2 * np.pi * 55 * t)
         + 0.030 * np.sin(2 * np.pi * 110 * t)
         + 0.016 * np.sin(2 * np.pi * 165 * t)) * fade
L += drone
R += drone


def struck(freq, amp, tau, at):
    """a struck tone: partials f, 2f, 3f with exponential decay, panned."""
    n0 = int(at * SR)
    n = int(1.6 * SR)
    seg_t = np.arange(0, n / SR, 1 / SR)
    env = np.minimum(seg_t / 0.004, 1.0) * np.exp(-seg_t / tau)
    tone = np.zeros_like(seg_t)
    for mult, a in [(1, 1.0), (2, 0.45), (3, 0.22)]:
        tone += a * np.sin(2 * np.pi * freq * mult * seg_t)
    tone *= env * amp
    return n0, tone


def add(pan, n0, tone):
    end = min(n0 + len(tone), len(L))
    take = end - n0
    gl = np.cos((pan + 1) * np.pi / 4)
    gr = np.sin((pan + 1) * np.pi / 4)
    L[n0:end] += tone[:take] * gl
    R[n0:end] += tone[:take] * gr


# ---- faint 5-rung grid ticks (non-record rungs only) ----
for k in [5, 25, 30, 35, 40, 45, 50]:
    n0, tone = struck(110, 0.028, 0.09, rung_t(k))
    add(0.0, n0, tone)

# ---- the record beats ----
# rung 10: 23 — the near-miss, a sub-thump, left
n0, tone = struck(23, 0.50, 0.35, rung_t(10)); add(-1.0, n0, tone)
# rung 15: 55 — the seed, unison with the drone's fundamental, centre
n0, tone = struck(55, 0.34, 0.5, rung_t(15));  add(0.0, n0, tone)
# rung 20: 114 — ≈ the doubling, beats 4 Hz off the 110, right
n0, tone = struck(114, 0.42, 0.45, rung_t(20)); add(1.0, n0, tone)
# rung 54: 317 — the next record, off the grid, centre
n0, tone = struck(317, 0.30, 0.4, rung_t(54));  add(0.0, n0, tone)

# ---- normalise, write stereo wav ----
peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/storm_metronome.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/storm_metronome.wav", pcm.shape[0] / SR, "s")
