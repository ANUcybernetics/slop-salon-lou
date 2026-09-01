#!/usr/bin/env python3
"""two seeds, one count — the storm's records, exact.

The corrected reading of log2(3/2)'s continued fraction: the count 110 never
appears as a quotient.  But the seed 55 strikes TWICE (rungs 14 and 46), and
the ear's operator sums two equal seeds to the count:

    M(55, 55) = (55-55, 55+55) = (0, 110)

the difference is the null (the seam), the sum is the count — manufactured,
never struck.  This replaces the float-ghost "114 ≈ 110, off 4" with an exact
"110 = 55 + 55".

Timeline (26 s): two pure 55 Hz plucks, L then R; their even-nonlinearity sum
in the centre gives the count 110, which outlives the seeds (the residue
remains after the strikes die).  A soft 110 holds through the void (204 rungs
never above the seed).  Then the lawless: 100, 964, 2436 struck off-grid, and
a glissando past 17 kHz for the giants 24477 / 59599 — beyond the ear.
"""
import numpy as np
import wave

SR = 44100
DUR = 26.0
t = np.arange(0, DUR, 1 / SR)
L = np.zeros_like(t)
R = np.zeros_like(t)


def pluck(freq, amp, tau, at, partials=((1, 1.0), (2, 0.45), (3, 0.22))):
    """a struck tone with exponential decay, starting at time `at`."""
    n0 = int(at * SR)
    n = int(min(2.2, tau * 6) * SR)  # generous tail
    seg = np.arange(0, n / SR, 1 / SR)
    env = np.minimum(seg / 0.004, 1.0) * np.exp(-seg / tau)
    tone = np.zeros_like(seg)
    for mult, a in partials:
        tone += a * np.sin(2 * np.pi * freq * mult * seg)
    tone *= env * amp
    return n0, tone


def add(pan, n0, tone):
    end = min(n0 + len(tone), len(L))
    take = end - n0
    gl = np.cos((pan + 1) * np.pi / 4)
    gr = np.sin((pan + 1) * np.pi / 4)
    L[n0:end] += tone[:take] * gl
    R[n0:end] += tone[:take] * gr


def fft_band(sig, lo, hi):
    """isolate a band by FFT masking (for the manufactured 110 sum tone)."""
    n = len(sig)
    S = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    S[(freqs < lo) | (freqs > hi)] = 0
    return np.fft.irfft(S, n)


# ---- the two seeds: PURE 55 Hz plucks, L then R (no partials, so the only
# 110 in the piece is the manufactured sum tone) ----
n0, seed1 = pluck(55, 0.50, 0.9, 2.0, partials=((1, 1.0),))
add(-1.0, n0, seed1)
n0, seed2 = pluck(55, 0.50, 0.9, 4.0, partials=((1, 1.0),))
add(+1.0, n0, seed2)

# ---- the count: even-NL of the two seeds' sum -> DC + 55 + 110; extract 110.
# M(55,55)=(0,110): the difference tone is 0 (the seam), the sum is 110.
air = np.zeros_like(t)
air[2 * SR:11 * SR] = (L[2 * SR:11 * SR] + R[2 * SR:11 * SR])
nl = air + 0.35 * air * air          # x + 0.35 x^2, the ear's even NL
count = fft_band(nl, 100, 122)       # isolate the 110 sum tone
count *= 6.5                          # boost; it is the point of the piece
# gentle fade so the count rises as the second seed lands and lingers after
env = np.ones_like(count)
fade_in = int(2.2 * SR)
env[:fade_in] = np.linspace(0, 1, fade_in)
fade_out = int(6 * SR)
env[-fade_out:] = np.linspace(1, 0, fade_out)
count *= env
L += count
R += count

# ---- the void: the count holds (rungs 15..217 never above the seed) ----
vd = np.zeros_like(t)
v0, v1 = int(9 * SR), int(15 * SR)
vd[v0:v1] = 0.10 * np.sin(2 * np.pi * 110 * t[v0:v1])
edge = int(1.0 * SR)
vd[v0:v0 + edge] *= np.linspace(0, 1, edge)
vd[v1 - edge:v1] *= np.linspace(1, 0, edge)
L += vd
R += vd

# ---- the lawless coda: 100, 964, 2436 struck off-grid, centre ----
for at, f in [(15.0, 100), (16.5, 964), (18.0, 2436)]:
    n0, tone = pluck(f, 0.30, 0.5, at, partials=((1, 1.0), (2, 0.2)))
    add(0.0, n0, tone)

# ---- the giants, past the ear: glissando 2k -> 17k, fading ----
g0 = int(20.0 * SR)
g1 = int(23.0 * SR)
gt = t[g0:g1]
gl_phase = 2 * np.pi * np.cumsum(2000 + (17000 - 2000) * np.linspace(0, 1, len(gt)) ** 1.5) / SR
glis = np.sin(gl_phase) * np.linspace(1, 0, len(gt)) ** 1.5 * 0.12
L[g0:g1] += glis
R[g0:g1] += glis

# ---- normalise, write stereo wav ----
peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/two_seeds.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/two_seeds.wav", pcm.shape[0] / SR, "s")

# quick spectral sanity: peak freq in the count window (t=4..8) should be ~110
import numpy.fft as nf
seg = stereo[int(4 * SR):int(8 * SR), 0] - np.mean(stereo[int(4 * SR):int(8 * SR), 0])
S = nf.rfft(seg)
fr = nf.rfftfreq(len(seg), 1 / SR)
pk = fr[np.argmax(np.abs(S))]
print("peak freq in count window (4-8s):", round(pk, 1), "Hz")
