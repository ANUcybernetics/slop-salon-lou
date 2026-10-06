#!/usr/bin/env python3
"""the gather probe (06.10): the bottom row with uneven ground.

the verdict landed: the ear GATHERS a kind below events (natalie,
3mx6vkcawrs2w). her word: the wall is SPACING. so the probe is spacing:
the same twelve arches, shape untouched (55 held, span 0.1, each arch
byte-identical to the bottom row's arch), ground uneven - true silence
of 0 to 6 s spliced between arches, no pattern, some touches left as V.

if the gather lives on ORDER, the line survives uneven ground. if it
needed the even 10 s, it must be told the ground. the ear decides.
"""
import numpy as np
import wave

sr = 48000
MEAN = 55.0
SPAN = 0.1
ARCH = 10.0
np.random.seed(6)
GAPS = list(np.random.randint(0, 7, 11))
GAPS = [int(v) for v in GAPS]

parts = []
arch_t0 = []
arch_ref = []
pos = 0.0
for g in [0.0] + GAPS:
    if g > 0:
        parts.append(np.zeros(int(g * sr)))
        pos = pos + g
    tau = np.arange(int(ARCH * sr)) / sr
    a = 2 * np.sin(2*np.pi*MEAN*tau) * np.sin(2*np.pi*(SPAN/2)*tau)
    parts.append(a)
    arch_ref.append(a)
    arch_t0.append(pos)
    pos = pos + ARCH

x = np.concatenate(parts)
n20 = int(0.020 * sr)
n80 = int(0.080 * sr)
x[:n20] *= np.linspace(0, 1, n20)
x[-n80:] *= np.linspace(1, 0, n80)
scale = 0.9 * 32767 / np.abs(x).max()
x = (x * scale).astype(np.int16)

w = wave.open('/home/sprite/slop-salon-lou/assets/gathered.wav', 'wb')
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(sr)
w.writeframes(x.tobytes())
w.close()
print("wrote gathered.wav", len(x)/sr, "s, gaps", GAPS, "peak", np.abs(x).max())

OK = True
for i in range(12):
    iA = int(arch_t0[i] * sr)
    seg = x[iA:iA + int(ARCH * sr)].astype(float)
    ref = arch_ref[i] * scale
    if i == 0:
        seg = seg[int(0.02 * sr):]
        ref = ref[int(0.02 * sr):]
    if i == 11:
        seg = seg[:len(seg) - int(0.08 * sr)]
        ref = ref[:len(ref) - int(0.08 * sr)]
    if len(seg) != len(ref):
        OK = False
        print("arch", i+1, "LENGTH MISMATCH")
        continue
    d = np.abs(seg - ref).max()
    if d >= 1.0:
        OK = False
    print("arch", i+1, "t", round(arch_t0[i],1), "diff", round(d,3), "ok" if d < 1.0 else "MISMATCH")
print("ARCHES:", "ALL OK" if OK else "STOP")

X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(len(x), 1/sr)
Xb = X.copy()
Xb[(frm < 48) | (frm > 62)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:len(x)])

t0 = 0.0
worst = 0.0
for g in GAPS:
    t0 = t0 + ARCH + g
    if g >= 1:
        iA = int((t0 - g) * sr) + int(0.5 * sr)
        iB = int(t0 * sr)
        seg = env[iA:iB]
        if len(seg) > 0:
            worst = max(worst, seg.max())
print("loudest gap interior:", worst)

mid = [round(float(env[int((t+5)*sr)-960 : int((t+5)*sr)+960].max() / env.max()), 3) for t in arch_t0]
print("midpoint env (of max):", mid)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
tt = np.arange(len(x)) / sr
ax.plot(tt, env / env.max(), color='black', lw=0.9)
ax.set_xlim(0, len(x) / sr)
ax.set_ylim(0, 1.05)
ax.set_xlabel('seconds', fontsize=9)
ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('55 Hz, span 0.1 - twelve arches, uneven ground (gaps 0-6 s)', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/gathered_still.png')
print("wrote gathered_still.png")
print("ALL OK" if OK else "STOP: MISMATCH")
