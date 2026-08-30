#!/usr/bin/env python3
"""the kiss — two readings, one shared slope.

On the count's cell the fold M(x)=2⌊x⌋−x IS the line 220−x; the mirror
N(x)=12100/x is tangent to it at 110 — same value, same slope −1. The sign is
the SHARED SLOPE: the two readings agree to first order at the count and peel
to second order (for x=110+δ, N−M = δ²/110 + …). The kiss is where the loop
would close; the walk never seats it — the peel is the holonomy the return
cannot undo.

Two voices read the SAME descending x (220→55): L = the fold (kinked, on the
grid), R = the mirror (smooth, off it). L falls 220→55, R rises 55→220; they
kiss at 110 (the beat dies — the deepest miss, the wait lengthening to
infinity), then peel — L walks on below (the translation, M²(x)=x−2, one-way in
time), R returns above (the involution, N²(x)=x, the exact return). The two
absences are exchanged: one transposition, heard. Mono hears the drone — the
count holds.

drone 110 throughout; total 72 s.
"""
import numpy as np
import wave

SR = 44100
TOTAL = 72.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

# --- the drone: 110, the count, holds throughout ---
drone = 0.055 * np.sin(2 * np.pi * 110.0 * t)

# --- the shared descent: x goes 220 -> 55, slow at the kiss, fast on the peel ---
TA = 38.0   # approach 220 -> 110, slow tail (the waits lengthen)
NA = int(TA * SR)
tA = np.arange(NA) / SR
delta = 110.0 * (1.0 - tA / TA) ** 1.5            # 110 -> 0, slow near 0
xA = 110.0 + delta

NB = N - NA
tB = np.arange(NB) / SR
deltab = 55.0 * (tB / (TOTAL - TA)) ** 0.75       # 0 -> 55, fast start
xB = 110.0 - deltab

x = np.concatenate([xA, xB])

def fold(xx):
    return 2.0 * np.floor(xx) - xx

def mirror(xx):
    return 12100.0 / xx

fL = fold(x)          # the fold's reading: falls 220 -> 55
fR = mirror(x)        # the mirror's reading: rises 55 -> 220

# light smooth of the fold's kinks (the grid texture, not clicks); pad edges.
# smooth the approach and peel separately so the seam (the kiss) is not smeared.
def smooth(u, w=int(0.010 * SR)):
    k = np.ones(w) / w
    uu = np.pad(u, (w // 2, w // 2), mode="edge")
    return np.convolve(uu, k, mode="valid")

fL = np.concatenate([smooth(fL[:NA]), smooth(fL[NA:])])
# pin the kiss instant: both readings exactly 110 at t=TA
fL[NA - 1] = 110.0

# --- phases (integrate the varying frequencies; anchor at the kiss) ---
phL = 2 * np.pi * np.cumsum(fL) / SR
phR = 2 * np.pi * np.cumsum(fR) / SR

# --- gains: keep the low mirror audible; taper the fold as it walks out ---
gL = 0.13 * np.ones(N)
gR = 0.13 * np.ones(N)
# the fold walks down past 55 into the low; ease it out over the last seconds
out = int(8 * SR)
gL[-out:] *= np.linspace(1, 0, out) ** 1.3
# the mirror settles back at 220; fade the whole piece at the very end
fade = int(1.5 * SR)
gL[-fade:] *= np.linspace(1, 0, fade)
gR[-fade:] *= np.linspace(1, 0, fade)

# soft attack/release on each voice
e = np.ones(N)
na = int(1.2 * SR)
e[:na] = np.linspace(0, 1, na, endpoint=False)
e[-fade:] = np.linspace(1, 0, fade)

# --- stereo: L in the left ear, R in the right; the drone centre ---
Lch = gL * np.sin(phL) * e + drone
Rch = gR * np.sin(phR) * e + drone

# --- the seal: one bright click where the two readings are one (t=TA) ---
def click(buf, t0, gain=0.12, f0=1500.0, tau=0.03):
    c0 = int(t0 * SR)
    c1 = int((t0 + 0.18) * SR)
    if c1 > N:
        return
    c = np.arange(c1 - c0) / SR
    k = gain * np.exp(-c / tau) * np.sin(2 * np.pi * f0 * c)
    buf[c0:c1] += k

click(Lch, TA, 0.10, 1500.0)
click(Rch, TA, 0.10, 1500.0)
# the ladder's landing: faint ticks where the miss halves on the approach
for n in range(1, 9):
    dn = 110.0 / (2 ** n)
    tn = TA * (1.0 - (dn / 110.0) ** (1.0 / 1.5))
    if tn < TA - 0.4:
        click(Lch, tn, 0.04, 900.0 + 40 * n, tau=0.02)
        click(Rch, tn, 0.04, 900.0 + 40 * n, tau=0.02)

# --- write wav (stdlib, 16-bit stereo) ---
data = np.empty(N * 2, dtype=np.int16)
data[0::2] = (np.clip(Lch, -1, 1) * 32767).astype(np.int16)
data[1::2] = (np.clip(Rch, -1, 1) * 32767).astype(np.int16)

with wave.open("assets/kiss_readings.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("wrote assets/kiss_readings.wav  %.1f s" % TOTAL)
print("kiss at t=%.1f s (L=%.2f Hz, R=%.2f Hz)" % (TA, fL[NA - 1], fR[NA - 1]))
print("end: L=%.2f Hz, R=%.2f Hz" % (fL[-1], fR[-1]))
