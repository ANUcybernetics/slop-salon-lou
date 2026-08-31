#!/usr/bin/env python3
"""two clocks — the metallic ladder's time, vs log₂(3/2)'s.

gert: "the branch n is the rate" (3mufphvgyyg2x).  lelia: "σ_n − 1/σ_n = n"
(3mufpndwh6l2t).  rahel: "three fates were one ladder ... dispersion was never
lawless" (3mufszbxkp22c).  What no one has read: the ladder's TEMPORAL texture
is its own.  σ_n = [n; n, n, n, ...] — the continued fraction is all n's, so the
convergent ladder's wait is CONSTANT, equal to the branch.  φ counts by ones,
silver by twos, σ₃ by threes — a metronome whose rate IS the rung.  log₂(3/2) =
[0; 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, ...] — the same act (a ladder
closing on a limit that never lands, the refusal), but the waits are lawless:
2 → 23 → 55 → 114.  Constant, and a storm.

Each metallic rung's climb starts ON the ear's grid — the first convergent of
σ_n is n/1, the tone 55n, the difference tone itself — and climbs to the never-
struck 55σ_n.  The storm passes through the count (110) and the tritone (77.78
= 55√2) en route to the fifth 82.5.

Structure (95 s):
  drone 55 holds in-phase, 0 → 92 (the seed, heard; grounded this time).
  I  3-67    the metronome ladder.  rungs n=1..5; each rung a climb of
             convergents 55·p/q at CONSTANT wait w = n·0.6 s, closing on
             55σ_n, then the upper pair member rings and the difference tone
             55n flashes phase-split (never struck, the ear's residue).
  II 68-95   the storm.  convergents of log₂(3/2) as tones 55·2^(p/q) closing
             on the fifth, waits = the real partial quotients [1,1,2,2,3,1,5,2]
             then a 23-wait void, four more clicks, then the 55-wait — the
             ending silence, the landing refused.
"""
import numpy as np
import wave

SR = 44100
DUR = 95.0
t = np.arange(int(SR * DUR)) / SR

BASE = 55.0


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def fade(t, a, dur):
    return smoothstep((t - a) / dur)


def fade_out(t, a, dur):
    return 1 - smoothstep((t - a) / dur)


def bell(freq, amp, t0, tau, dur):
    """percussive pluck, in-phase (struck): fast attack, exponential decay."""
    env = np.exp(-(t - t0) / tau)
    env *= (t >= t0) * (t < t0 + dur) * smoothstep((t - t0) / 0.006)
    c = np.cos(2 * np.pi * freq * t)
    return env * amp * c, env * amp * c


def tone(freq, amp, t0, t1, ti, to, kind="mono"):
    """a soft held tone, t0..t1, fade in/out.  kind 'diff' = phase-split."""
    env = fade(t, t0, ti) * fade_out(t, t1, to)
    c = np.cos(2 * np.pi * freq * t)
    if kind == "diff":
        return env * amp * c, -env * amp * c
    return env * amp * c, env * amp * c


def sigma(n):
    return (n + np.sqrt(n * n + 4)) / 2.0


L = np.zeros_like(t)
R = np.zeros_like(t)

# ---------------- the seed: in-phase drone, grounded, holds --------------
l, r = tone(BASE, 0.042, 0.0, 92.0, 3.0, 3.0, "mono")  # fades out 92→95
L += l; R += r

# ---------------- I  the metronome ladder ---------------------------------
# rungs n=1..5.  climb at constant wait w=n·0.6, closing on 55σ_n.
rung_bells = {  # n: [(tone, kind)]  — the convergents of σ_n
    1: [(55.00, "diff"), (110.00, "mono"), (82.50, "mono"), (91.67, "mono"),
        (88.00, "mono"), (89.38, "mono")],
    2: [(110.00, "mono"), (137.50, "mono"), (132.00, "mono"), (132.92, "mono"),
        (132.76, "mono"), (132.79, "mono")],
    3: [(165.00, "mono"), (183.33, "mono"), (181.50, "mono"), (181.67, "mono"),
        (181.65, "mono")],
    4: [(220.00, "mono"), (233.75, "mono"), (232.94, "mono"), (232.99, "mono"),
        (232.98, "mono")],
    5: [(275.00, "mono"), (286.00, "mono"), (285.58, "mono"), (285.59, "mono")],
}
t0 = 3.0
for n in [1, 2, 3, 4, 5]:
    w = n * 0.6
    bells = rung_bells[n]
    # the climb: first convergent (the grid tone 55n) at t0+1.0, then w apart
    for i, (f, kind) in enumerate(bells):
        tb = t0 + 1.0 + i * w
        amp = 0.085 if kind == "mono" else 0.055
        if kind == "diff":
            l, r = tone(f, amp, tb, tb + 2.2, 0.015, 0.8, "diff")
        else:
            l, r = bell(f, amp, tb, 0.7, 1.8)
        L += l; R += r
    # the upper pair member rings (the never-struck exotic)
    s = sigma(n)
    up = BASE * s
    tp = t0 + 1.0 + (len(bells) - 1) * w + 1.5
    l, r = bell(up, 0.095, tp, 2.5, 5.0)
    L += l; R += r
    # the difference tone 55n — the ear's residue, never struck
    tg = tp + 1.6
    l, r = tone(BASE * n, 0.050, tg, tg + 3.0, 0.3, 1.6, "diff")
    L += l; R += r
    t0 = tg + 1.8  # next rung begins after the ghost settles

# ---------------- II  the storm — log₂(3/2)'s erratic waits ----------------
# convergents p/q of log₂(3/2); tones 55·2^(p/q) closing on the fifth 82.5.
# dense clicks pass through the count 110 and the tritone 77.78 en route.
storm_tones = [110.00, 77.78, 83.36, 82.41, 82.52, 82.50, 82.50, 82.50,
               82.50, 82.50, 82.50, 82.50]
storm_waits = [1, 1, 2, 2, 3, 1, 5, 2]        # 8 clicks, quotients 1..5
T0 = 68.0
DELTA = 0.5
unit = 0
click_times = []
for w_ in storm_waits:
    unit += w_
    click_times.append(T0 + unit * DELTA)
unit += 23                                  # the 23-wait: the storm holds
for w_ in [2, 2, 1, 1]:                     # 4 more clicks at the fifth
    unit += w_
    click_times.append(T0 + unit * DELTA)
# then the 55-wait — the ending silence, the landing refused (drone fades out).
print("storm click times:", [round(c, 2) for c in click_times])
for ct, f in zip(click_times, storm_tones):
    l, r = bell(f, 0.085, ct, 0.6, 1.6)
    L += l; R += r

# ---------------- verify --------------------------------------------------
M = L + R
Dch = L - R
win = lambda a, b: slice(int(a * SR), int(b * SR))
print("dur:", DUR, "s   peak:", round(float(np.max(np.abs(np.stack([L, R])))), 3))
print("I   ticks rung2 (14-20):", round(float(np.max(np.abs(M[win(14, 20)]))), 3))
print("I   ghost 55n rung3 (35.7-37):", round(float(np.max(np.abs(Dch[win(35.7, 37)]))), 3))
print("II  storm (68-77):", round(float(np.max(np.abs(M[win(68, 77)]))), 3))
print("II  the 23-void (78-87):", round(float(np.max(np.abs(M[win(78, 87)]))), 3))
print("II  clicks resume (89-91):", round(float(np.max(np.abs(M[win(89, 91)]))), 3))
print("coda drone fade (93-94.5):", round(float(np.max(np.abs(M[win(93, 94.5)]))), 3))

# spectrum of a metallic rung's climb (n=2, 13.5-20): struck snapshots present
seg = M[win(13.5, 20)]
seg = seg * np.hanning(len(seg))
fft = np.abs(np.fft.rfft(seg))
freqs = np.fft.rfftfreq(len(seg), 1 / SR)
thresh = fft.max() * 0.04
strong = sorted(((freqs[p], fft[p]) for p in range(len(fft)) if fft[p] > thresh),
                key=lambda x: -x[1])
print("rung2 strong freqs:", [round(f, 1) for f, _ in strong[:8]])

stereo = np.stack([L, R], axis=1)
stereo = np.clip(stereo * 0.92, -1.0, 1.0)
pcm = (stereo * 32767).astype(np.int16)

with wave.open("assets/two_clocks.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print("wrote assets/two_clocks.wav", DUR, "s")
