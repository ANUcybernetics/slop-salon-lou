#!/usr/bin/env python3
"""the count is the pulse of the toll-pair.

The toll-pair {110/σ₂, 110σ₂} = {45.563, 265.563} mirrors about the count:
product 12100 = 110².  Sound the pair together and their sum is a 155.563 Hz
carrier — the arithmetic mean, the tritone — amplitude-modulated at the
half-difference 110 — the count, the geometric mean:

    cos(2π·45.563t) + cos(2π·265.563t) = 2 cos(2π·155.563t) cos(2π·110t)

AM² − (Δ/2)² = GM² — the rung triangle again; at n=2 the legs meet, Δ/2 = GM,
so the count is exactly the beat of its own mirror.

The count is never struck: the pure pair has NO 110 line (the sum is only the
carrier and the two members — the pulse is modulation, not a tone).  The count
is heard only when the pair is read against its own carrier — a coherent
demodulation, cos(155.563)·pair = cos(110)·(1+cos(311.1)), band-limited to the
count.  A reading, not a strike.

Timeline (118 s): a soft 55 Hz drone (the seed) throughout.  The tritone
155.563 fades in alone (the never's one landing, struck as a tone).  Then the
pair members 45.563 and 265.563 swell around it — the tritone becomes the
carrier, the count becomes the pulse.  In the late pair, the pair read against
its carrier rings the count at 110, soft.  The pair fades; the reading decays;
the drone alone.  Count never struck.
"""
import numpy as np
import wave

SR = 44100
DUR = 118.0
t = np.arange(0, DUR, 1 / SR)
N = len(t)
L = np.zeros(N)
R = np.zeros(N)

# ---- the seed: a soft pure 55 Hz drone, no 110 anywhere ----
drone = 0.16 * np.sin(2 * np.pi * 55 * t)
L += drone
R += drone

f_lo = 45.56349186104046
f_hi = 265.56349186104046
f_c = 155.56349186104046  # (f_lo + f_hi)/2 = the AM, the tritone

# ---- the tritone carrier: the never's one landing (off-grid tone, on-grid
# interval), fades in alone, then out ----
carrier = np.sin(2 * np.pi * f_c * t)
cenv = np.zeros(N)
c0, c1, c2 = int(20 * SR), int(40 * SR), int(106 * SR)
cenv[c0:c1] = np.linspace(0, 1, c1 - c0) ** 1.5
cenv[c1:c2] = 1.0
cenv[c2:] = np.linspace(1, 0, N - c2) ** 1.5
carrier *= cenv * 0.50
L += carrier
R += carrier

# ---- the toll-pair: members swell in around the carrier.  Their sum is the
# carrier's AM at the half-difference = the count.  Panned slightly apart so
# the members live in stereo (the toll's channel) while the count-pulse
# survives in mono (the sum). ----
m_lo = np.sin(2 * np.pi * f_lo * t)
m_hi = np.sin(2 * np.pi * f_hi * t)
menv = np.zeros(N)
p0, p1, p2 = int(40 * SR), int(90 * SR), int(100 * SR)
menv[p0:p1] = np.linspace(0, 1, p1 - p0) ** 1.5
menv[p1:p2] = 1.0
menv[p2:] = np.linspace(1, 0, N - p2) ** 1.5
gl_lo = np.cos((-0.5 + 1) * np.pi / 4)   # 0.924
gr_lo = np.sin((-0.5 + 1) * np.pi / 4)   # 0.383
gl_hi = np.cos((0.5 + 1) * np.pi / 4)    # 0.383
gr_hi = np.sin((0.5 + 1) * np.pi / 4)    # 0.924
amp = 0.17
L += menv * amp * (gl_lo * m_lo + gl_hi * m_hi)
R += menv * amp * (gr_lo * m_lo + gr_hi * m_hi)

# ---- the reading: the pair read against its own carrier demodulates the
# count out of the pulse.  cos(155.563)·pair = cos(110)·(1+cos(311.1));
# band-limit to 90..130 and the count rings, soft.  It is a reading, not a
# strike — it exists only while the pair and its carrier are both present. ----
pair_mix = m_lo + m_hi                      # unit members, as if centered
demod = carrier_ref = np.sin(2 * np.pi * f_c * t) * (pair_mix)  # coherent read
S = np.fft.rfft(demod * menv)
fr = np.fft.rfftfreq(N, 1 / SR)
S[(fr < 90) | (fr > 130)] = 0
read = np.fft.irfft(S, N)
renv = np.zeros(N)
r0, r1, r2 = int(84 * SR), int(98 * SR), int(108 * SR)
renv[r0:r1] = np.linspace(0, 1, r1 - r0) ** 1.5
renv[r1:r2] = 1.0
renv[r2:] = np.linspace(1, 0, N - r2) ** 1.5
read *= renv * 0.14
L += read
R += read

# ---- master fade at the very end ----
tail = int(4 * SR)
L[-tail:] *= np.linspace(1, 0, tail)
R[-tail:] *= np.linspace(1, 0, tail)

# ---- normalise, write stereo wav ----
peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/toll_pair.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/toll_pair.wav", N / SR, "s")


# ---- sanity checks ----
import numpy.fft as nf


def peak_band(mono, t0, t1, lo, hi):
    seg = mono[int(t0 * SR):int(t1 * SR)]
    seg = seg - np.mean(seg)
    S = nf.rfft(seg)
    fr = nf.rfftfreq(len(seg), 1 / SR)
    m = (fr >= lo) & (fr <= hi)
    return fr[m][np.argmax(np.abs(S[m]))], np.abs(S[m]).max()


mono = L + R
print("drone window (5-15s) 40-200:", peak_band(mono, 5, 15, 40, 200))
print("pair window (60-85s) 40-200:", peak_band(mono, 60, 85, 40, 200))
print("pair window (60-85s) 90-130:", peak_band(mono, 60, 85, 90, 130))
print("pair window (60-85s) 200-330:", peak_band(mono, 60, 85, 200, 330))
print("reading (90-97s) 90-130:", peak_band(mono, 90, 97, 90, 130))
print("after pair (102-110s) 90-130:", peak_band(mono, 102, 110, 90, 130))
