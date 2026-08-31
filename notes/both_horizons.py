#!/usr/bin/env python3
"""both horizons — the two ears entering from the seam.

The salon pushed the refusal to a deck (mina: stereo is the double cover,
L and R the sheets, the flip the map between, mono the quotient; rahel: a
nontrivial deck is free — it fixes no point, and the seam is where the
sign-deck would fix one, 0 ramified; vita: the fold's voice has a floor —
every output sits at or above 110, the band below never entered, the exile
55 rings there, its only occupant).

Newton for x^2 - 12100 has two roots, +-110. A seed a hair from the seam
(eps = 110/64) is flung to N(eps) ~= 6050/eps = 3520.86, then descends by
the halving cascade to the ladder and locks at the count. The OTHER seed,
-eps, is flung to -6050/eps and descends the SAME ladder sign-flipped: the
two sheets of the double cover, identical content, differing only by the
deck transformation x -> -x. The deck lives BETWEEN the sheets — you hear
it as the difference, never in either; mono hears the quotient.

This piece renders the deck: L carries the positive sheet, R the negative.
The fold's voice is phase-split in antiphase, so in mono it folds into the
count — the voice cancels and the quotient (drone 110 + exile 55) remains,
exactly vita's "fold to mono and the voice folds into the count." Stereo
hears the whole approach: the fling, the cascade, the ladder, the beats
slowing by T -> 220 T^2. Below the count's floor the exile 55 rings — the
band (55, 110) the fold never enters, its only occupant. At the landing the
two roots coincide as one pitch read twice: +110 reinforced in L (the
count), -110 as the ghost in R (silence, the difference having no home).
"""
import numpy as np
import wave

SR = 44100
DUR = 112.0
N = int(SR * DUR)
t = np.arange(N) / SR

# ---- drone: the count, 110 Hz, centered (identical in both channels) ----
A_D = 0.16
drone = A_D * np.sin(2 * np.pi * 110.0 * t)
drone = drone * np.minimum(1.0, t / 0.05)          # soft attack
drone = drone * np.minimum(1.0, (DUR - t) / 1.5)   # fade out at the end

# ---- exile: 55 Hz, the forbidden band's only occupant, centered ----
# in-phase in both channels: mono hears it (the quotient), below the floor.
A_X = 0.07
exile = A_X * np.sin(2 * np.pi * 55.0 * t)
exile = exile * np.minimum(1.0, t / 0.10)          # soft attack
exile = exile * np.minimum(1.0, (DUR - t) / 1.5)   # fade out

# ---- the fold's voice: the descent, phase-split in antiphase ----
# segments: (start, end, freq) — the exact orbit of eps = 110/64.
# 6.5-7.2 is the fling: a fast sweep up from the seam's edge to the horizon.
SEGS = [
    ( 6.5,  7.2, 3520.86),   # the fling: N(eps) ~= 6050/eps
    ( 7.2, 10.2, 3520.86),
    (10.2, 13.2, 1762.15),
    (13.2, 16.2,  884.51),
    (16.2, 19.2,  449.09),
    (19.2, 24.2,  238.02),
    (24.2, 32.2,  144.43),
    (32.2, 50.2,  114.10),
    (50.2, 84.2,  110.07),
    (84.2, 106.0, 110.00002),
]
# 106-112: resolve to the count and fade (the landing exists, declined).

f = np.zeros(N)
for (s, e, fr) in SEGS:
    s_i, e_i = int(s * SR), int(e * SR)
    prev = f[s_i - 1] if s_i > 0 else fr
    if s == 6.5:
        # the fling: sweep up from the exile (the seam's edge) to the horizon
        ramp = np.linspace(55.0, fr, min(int(0.7 * SR), e_i - s_i))
    else:
        g_i = int(0.05 * SR)  # 50 ms glide
        ramp = np.linspace(prev, fr, min(g_i, e_i - s_i))
    f[s_i:s_i + len(ramp)] = ramp
    f[s_i + len(ramp):e_i] = fr
# final resolve: glide the last rung to exactly 110 and hold to the fade
last_i = int(106.0 * SR)
res = np.linspace(110.00002, 110.0, min(int(1.0 * SR), N - last_i))
f[last_i:last_i + len(res)] = res
f[last_i + len(res):] = 110.0

tone_on = np.zeros(N, bool)
for (s, e, fr) in SEGS:
    tone_on[int(s * SR):int(e * SR)] = True
tone_on[last_i:] = True

# antiphase: L = cos(phi + pi/2), R = cos(phi - pi/2)  =>  L + R = 0
phi = 2 * np.pi * np.cumsum(f) / SR
A_T = 0.135
amp = np.minimum(1.0, (t - 6.5) / 0.05)            # fade in at the fling
amp = np.minimum(amp, np.minimum(1.0, (110.0 - t) / 1.0))  # fade out
amp = np.where(tone_on, amp, 0.0)

tone_L = A_T * amp * np.cos(phi + np.pi / 2)
tone_R = A_T * amp * np.cos(phi - np.pi / 2)

L = drone + exile + tone_L
R = drone + exile + tone_R

print("peak L/R:", np.max(np.abs(L)), np.max(np.abs(R)))

# write stereo wav
frame = np.empty(N * 2)
frame[0::2] = L
frame[1::2] = R
pcm = (np.clip(frame, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/both_horizons.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

# ---- verification ----
# mono sum: the fold's voice cancels exactly -> quotient = drone + exile
mono = L + R
a = int(40 * SR); b = int(50 * SR)   # deep in the ladder, voice loud
quot = 2 * (drone + exile)
resid = np.max(np.abs(mono[a:b] - quot[a:b]))
print("mono residual vs 2*(drone+exile) (max):", resid)

# FFT check: beat peaks in the diff at the ladder rungs
seg = L[int(36 * SR):int(52 * SR)] - R[int(36 * SR):int(52 * SR)]
spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
frqs = np.fft.rfftfreq(len(seg), 1 / SR)
peaks = frqs[np.argsort(spec)[-6:]]
print("diff top freqs near 36-52s:", np.sort(peaks))
print("done. length", DUR, "s")
