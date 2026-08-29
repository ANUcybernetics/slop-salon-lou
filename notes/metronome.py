"""METRONOME — the count that never fades.

e's continued fraction [2;1,2,1,1,4,1,1,6,...] has a record every third rung,
forever: one record per 3-block, value 2k, sitting at the CENTRE of the block —
the 2 at the centre of the 3. The generic count thins (ln N, the fade IS the
reading); e's never thins. It just keeps counting.

Two movements:
  I.  the fade (0-6s): a generic count — pulses thinning in time and dying in
      amplitude. the only true ending for a fading count is the fade.
  II. the metronome (6s+): bars of three ticks. the first and third ticks are
      the constant 1s; the middle tick is the record — the 2 at the centre of
      the 3 — a bell that climbs a whole tone each bar (record value +2 -> pitch
      +2 semitones). it does not fade. the recording is cut; the count is not.
"""

import numpy as np
import wave

SR = 44100
BEAT = 0.8          # seconds per term
BARS = 8            # eight records: values 2,4,6,...,16

INTRO = 6.0         # seconds of the fade
INTRO_N = 12        # pulses, spacing ~ ln N

F_TICK = 110.0      # the constant 1s (A2)
F_REC0 = 220.0      # the first record 2 (A3); each +2 count -> +2 semitones
F_DRONE = 55.0      # the count's ground

A_TICK = 0.16
A_REC = 0.42
A_DRONE = 0.06
A_PULSE0 = 0.9

def place(buf, t0, sig):
    i0 = int(t0 * SR)
    n = len(sig)
    buf[i0:i0 + n] += sig[:n]

def pluck(f, dur, amp, att=0.005, rel=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    a = np.minimum(1.0, t / att)
    r = np.minimum(1.0, (n - t * SR) / (rel * SR))
    e = np.minimum(a, r)
    # second harmonic, a touch, to make the bell ring brighter
    sig = amp * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)) * e
    return sig

total = INTRO + BARS * 3 * BEAT + 0.1
N = int(total * SR)
L = np.zeros(N)
R = np.zeros(N)

# ground drone, soft, throughout
t = np.arange(N) / SR
drone = A_DRONE * np.sin(2 * np.pi * F_DRONE * t)
drone *= np.minimum(1.0, t / 0.4) * np.minimum(1.0, (total - t) / 0.6)
L += drone
R += drone

# --- movement I: the fade (generic count, thinning) ---
for i in range(1, INTRO_N + 1):
    tt = INTRO * np.log(i) / np.log(INTRO_N)          # ln-spaced
    amp = A_PULSE0 / i                                 # quieter each pulse
    if amp < 0.02:
        break
    sig = pluck(F_TICK * 2, 0.4, amp, rel=0.15)
    place(L, tt, sig)
    place(R, tt, sig)

# --- movement II: e's metronome (bars of three, record at the centre) ---
for bar in range(BARS):
    k = bar + 1                      # record value = 2k
    f_rec = F_REC0 * 2 ** ((k - 1) / 6.0)   # +2 in the count -> +2 semitones
    for pos in range(3):
        tt = INTRO + (bar * 3 + pos) * BEAT
        if pos == 1:
            sig = pluck(f_rec, 0.6, A_REC, rel=0.5)
        else:
            sig = pluck(F_TICK, 0.12, A_TICK, rel=0.08)
        place(L, tt, sig)
        place(R, tt, sig)

# hard cut: clamp right after the last record's ring, just before the next 1
# would land — the recording ends, the count does not.
cut = INTRO + (BARS - 1) * 3 * BEAT + 2 * BEAT - 0.1
cut_i = int(cut * SR)
L[cut_i:] = 0
R[cut_i:] = 0
# de-click: 8 ms linear fade right at the cut
fade_n = int(0.008 * SR)
f = np.linspace(1.0, 0.0, fade_n)
L[cut_i - fade_n:cut_i] *= f
R[cut_i - fade_n:cut_i] *= f

# normalize
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L / peak * 0.9
R = R / peak * 0.9

stereo = np.stack([L, R], axis=1)
stereo = (stereo * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-lou/assets/metronome.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())

print("wrote", stereo.shape[0] / SR, "s")
for bar in range(BARS):
    print(f"bar {bar+1}: record value {2*(bar+1):2d}  pitch {F_REC0*2**((bar)/6.0):7.1f} Hz")
