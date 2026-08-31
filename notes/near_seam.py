#!/usr/bin/env python3
"""the seed near the seam.

Newton's method for x^2 - 12100 has roots +-110 and a pole at x=0.
A seed a hair from the seam (eps = 110/64) is flung by the first step to
N(eps) ~= 6050/eps = 3520.86 Hz, then descends: the halving cascade
3520 -> 1762 -> 884 -> 449 -> 238, then the ladder locks:
144 -> 114 (beat 4.1 Hz, wait 0.24 s) -> 110.07 (beat 0.07 Hz, wait 13.5 s)
-> 110.00002 (beat 2e-5 Hz, wait ~14 hr, beyond the piece) -> 110.

The descent is rendered in the sign's channel: the tone is phase-split in
antiphase, so mono (the count) hears only the drone — the seam is literal.
Stereo hears the whole approach, the beats slowing by the squaring law
T_{n+1} ~= 220 T_n^2. At the count the two roots coincide: one pitch read
twice, the seam reads silent. refused from both ends.
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
drone = drone * np.minimum(1.0, (DUR - t) / 1.2)   # fade out at the end

# ---- the orbit: (start, end, freq) stepped rungs with 50 ms glides ----
SEGS = [
    ( 9.00, 12.00, 3520.86),
    (12.00, 15.00, 1762.15),
    (15.00, 18.00,  884.51),
    (18.00, 21.00,  449.09),
    (21.00, 26.00,  238.02),
    (26.00, 34.00,  144.43),
    (34.00, 52.00,  114.10),
    (52.00, 86.00,  110.07),
    (86.00, 108.0,  110.00002),
]

# build an instantaneous-frequency array
f = np.zeros(N)
for (s, e, fr) in SEGS:
    s_i, e_i = int(s * SR), int(e * SR)
    g_i = int(0.05 * SR)  # 50 ms glide
    # linear ramp from the previous segment's frequency
    prev = f[s_i - 1] if s_i > 0 else fr
    ramp = np.linspace(prev, fr, min(g_i, e_i - s_i))
    f[s_i:s_i + len(ramp)] = ramp
    f[s_i + len(ramp):e_i] = fr
# anything past the last segment stays at its last value (silence for tone)
tone_on = np.zeros(N, bool)
for (s, e, fr) in SEGS:
    tone_on[int(s * SR):int(e * SR)] = True

# phase-split in antiphase: L = cos(phi+pi/2), R = cos(phi-pi/2)  => L+R = 0
phi = 2 * np.pi * np.cumsum(f) / SR
A_T = 0.135
amp = np.minimum(1.0, (t - 9.0) / 0.05)          # fade in at entry
amp = np.minimum(amp, np.minimum(1.0, (108.0 - t) / 1.0))  # fade out
amp = np.where(tone_on, amp, 0.0)

tone_L = A_T * amp * np.cos(phi + np.pi / 2)
tone_R = A_T * amp * np.cos(phi - np.pi / 2)

L = drone + tone_L
R = drone + tone_R

# peak check
print("peak L/R:", np.max(np.abs(L)), np.max(np.abs(R)))

# write stereo wav
frame = np.empty(N * 2)
frame[0::2] = L
frame[1::2] = R
pcm = (np.clip(frame, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/near_seam.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

# ---- verification ----
# mono sum should be ~ the drone only (tone cancels exactly)
mono = L + R
# find a window deep in the ladder where the tone is loud, measure residual
a = int(40 * SR); b = int(50 * SR)
resid = np.max(np.abs(mono[a:b] - 2 * drone[a:b]))
print("mono residual vs 2*drone (max):", resid)
print("done. length", DUR, "s")
