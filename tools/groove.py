#!/usr/bin/env python3
"""the groove probe (06.10, evening): repetition, not evenness.

both verdicts landed: the rest rung HELD (count crosses 0.63 s of valley)
and uneven ground LET GO (no repeated spacing, no count). natalie's law:
"no repeated spacing, no count. the wall is spacing." natalie named the
start: the rest before the first swell is the count-in (verified on her
file: first sound 3.748 s = one full 3.73 s spacing of silence).

the empty cell: is the wall EVENNESS or REPETITION? same twelve arches,
byte-identical (55 held, span 0.1, 10 s each), rests alternating 2 s / 4 s
- a groove, uneven but REPEATED. count-in = one full first rest (2 s), per
the count-in law; a 2+4 count-in is inaudible as two rests (silence has no
marks) - the groove teaches itself from its first cycle. if the ear locks
to the groove, the wall is repetition, not evenness. the ear decides.
"""
import numpy as np
import wave

sr = 48000
MEAN = 55.0
SPAN = 0.1
ARCH = 10.0
GAPS = ([2.0, 4.0] * 5) + [2.0]  # 11 rests: 2,4,2,4,...,2

parts = []
arch_t0 = []
arch_ref = []
pos = 0.0
for g in [2.0]:  # count-in: the groove's first rest, one full spacing
    parts.append(np.zeros(int(g * sr)))
    pos = pos + g
for i in range(12):
    if i > 0:
        g = GAPS[i-1]
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

w = wave.open('/home/sprite/slop-salon-lou/assets/groove.wav', 'wb')
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(sr)
w.writeframes(x.tobytes())
w.close()
print("wrote groove.wav", round(len(x)/sr, 2), "s, gaps", GAPS, "peak", np.abs(x).max())

# THE READ-BACK IS THE PROOFREAD (05.10 law): span vs commanded.
# twelve arches byte-identical to the commanded shape at commanded t0;
# eleven rests true silence of commanded length; count-in = 2 s silence.
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
        it = False
        print("arch", i+1, "LENGTH MISMATCH")
        continue
    d = np.abs(seg - ref).max()
    if d >= 1.0:
        OK = False
    print("arch", i+1, "t", round(arch_t0[i],1), "diff", round(d,3), "ok" if d < 1.0 else "MISMATCH")

sil_ok = True
for i, g in enumerate(GAPS):
    iA = int((arch_t0[i] + ARCH) * sr)
    iB = int(arch_t0[i+1] * sr)
    seg = np.abs(x[iA:iB]).max() if iB > iA else 0
    exp = int(round(g * sr))
    if seg != 0 or (iB - iA) != exp:
        sil_ok = False
        print("rest", i+1, "commanded", g, "len", iB-iA, "expected", exp, "max", seg, "MISMATCH")
print("RESTS:", "ALL OK" if sil_ok else "STOP")

ciA = int(arch_t0[0] * sr)
ci = np.abs(x[:ciA]).max()
ci_ok = (ci == 0 and ciA == int(round(2.0 * sr)))
print("count-in:", ciA, "samples, max", ci, "ok" if ci_ok else "MISMATCH")
print("ARCHES:", "ALL OK" if OK else "STOP: MISMATCH")
print("ALL OK" if (OK and sil_ok and ci_ok) else "STOP: MISMATCH")

X = np.fft.rfft(x.astype(float))
frm = np.fft.rfftfreq(len(x), 1/sr)
Xb = X.copy()
Xb[(frm < 48) | (frm > 62)]= 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:len(x)])

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
ax.set_title('55 Hz, span 0.1 - twelve arches, groove ground (rests 2 s / 4 s, count-in 2 s)', fontsize=10)
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-lou/assets/groove_still.png')
print("wrote groove_still.png")
