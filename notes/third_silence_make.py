#!/usr/bin/env python3
"""the third silence — the count unmakes itself.

rahel's S=0: the pair symmetric about zero, the sum null, only the sign
survives. "count, seam, pole: one point, three arms."

Three arms converging on one point (the count's silence), 110 only ever
played as a symmetric pair about zero so the mono sum is identically null
and the count exists nowhere but in the difference.

I  seam    0-16s  the fused pair (in-phase) unwinds to anti-phase; the
                 count dims in mono and is unmade.
II pole   16-26s  the anti-phase pair thins to nothing; the source unmade;
                 a beat of true silence — the one point.
III S=0   26-56s  the steady third silence: 110 and 220, each a symmetric
                 pair about zero, breathing; the sum stays zero and the
                 sign carries everything.
"""

import numpy as np
import wave

SR = 44100


def t_range(start, dur):
    n = int(SR * dur)
    return start + np.arange(n) / SR


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def env(t, a, rel=1.0):
    """fade in/out trapezoid at t0=a, t0+rel, t1-rel, t1."""
    dur = t[-1] - t[0]
    up = smoothstep((t - a) / rel)
    down = 1 - smoothstep((t - (a + dur - rel)) / rel)
    return up * down


# ---------------- I : the seam unwinds --------------------
t1 = t_range(0, 16.0)
th = np.pi * smoothstep(t1 / 16.0)          # 0 -> pi, eased
amp1 = env(t1, 0.0, 1.5)
L1 = amp1 * np.cos(2 * np.pi * 110 * t1 + th / 2)
R1 = amp1 * np.cos(2 * np.pi * 110 * t1 - th / 2)

# ---------------- II : the pole thins to nothing ----------
t2 = t_range(16.0, 10.0)
dec = 1 - smoothstep((t2 - 16.0) / 6.0)     # 1 -> 0 over 6 s
sil = 1 - smoothstep((t2 - 24.0) / 1.0)     # true silence after 24s
amp2 = dec * sil
L2 = amp2 * np.cos(2 * np.pi * 110 * t2 + np.pi / 2)
R2 = amp2 * np.cos(2 * np.pi * 110 * t2 - np.pi / 2)

# ---------------- III : the zero-sum steady state ---------
t3 = t_range(26.0, 30.0)
br1 = 0.62 + 0.38 * np.sin(2 * np.pi * (t3 - 26.0) / 5.0)
br2 = 0.55 + 0.45 * np.sin(2 * np.pi * (t3 - 26.0) / 8.0 + 1.3)
a3 = env(t3, 26.0, 2.5)
a1 = a3 * 0.8 * br1
a2 = a3 * 0.5 * br2
L3 = a1 * np.cos(2 * np.pi * 110 * t3) + a2 * np.cos(2 * np.pi * 220 * t3 + 0.6)
R3 = -(a1 * np.cos(2 * np.pi * 110 * t3) + a2 * np.cos(2 * np.pi * 220 * t3 + 0.6))

L = np.concatenate([L1, L2, L3])
R = np.concatenate([R1, R2, R3])

# verify the mono sum is null in the steady state (and, at the seam's end,
# at the anti-phase moment)
M = L + R
print("max |L+R| whole piece:", np.max(np.abs(M)))
i3 = int(26.0 * SR)
print("max |L+R| from 26s on:", np.max(np.abs(M[i3:])))

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.9, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/third_silence.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/third_silence.wav", len(L) / SR, "s")
