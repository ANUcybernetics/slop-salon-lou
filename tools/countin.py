#!/usr/bin/env python3
"""lelia's count-in probe (07.10): two panels on the floor rung.
panel one: count-in = one FULL spacing. panel two: HALF.
same twelve swells after the count-in; byte-identical panels after it.
55 Hz, span 0.268, spacing = envelope half-cycle, valley 0.63 s.
"""
import numpy as np
import wave

sr = 48000
F0 = 55.0
SPAN = 0.268
L = int(round(sr / SPAN))     # one spacing = envelope half-cycle: 179104
VAL = int(round(0.63 * sr))   # valley samples
N = 12
FULL, HALF = L, L // 2

tau = np.arange(L) / sr
arch = 2 * np.sin(2*np.pi*F0*tau) * np.sin(2*np.pi*(SPAN/2)*tau)
arch[-VAL:] = 0.0

def build(ci):
    x = np.zeros(ci + N * L)
    t0s = [ci + i * L for i in range(N)]
    for t0 in t0s:
        x[t0:t0 + L] = arch
    n80 = int(0.08 * sr)
    x[-n80:] *= np.linspace(1, 0, n80)
    x = np.round(x * (0.9 * 32767 / np.abs(x).max())).astype(np.int16)
    return x, t0s

def proofread(x, t0s, ci, name):
    ok = True
    tail = N * L
    print(name, "first sound", (x != 0).argmax() / sr, "s, count-in",
          ci / sr, "s")
    for i in range(N):
        seg = x[t0s[i]:t0s[i] + L].astype(int)
        ref = np.round(arch * (0.9 * 32767 / np.abs(arch).max())).astype(int)
        if i == N - 1:
            seg = seg[:-80]
            ref = ref[:-80]
        d = np.abs(seg - ref).max()
        if d > 0:
            print(name, "arch", i + 1, "diff", d)
            ok = False
    for i in range(N - 1):
        seg = x[t0s[i] + L - VAL: t0s[i] + L].max()
        if seg != 0:
            print(name, "valley", i + 1, "MISMATCH")
            ok = False
    return ok

xa, ta = build(FULL)
xb, tb = build(HALF)
d = np.abs(xa[L:FULL + N * L] - xb[HALF:HALF + N * L]).max()
print("bodies identical after count-in: max diff", d, "LSB")
print("ALL OK" if d == 0 else "MISMATCH")

for name, x, t0s, ci in (("full", xa, ta, FULL), ("half", xb, tb, HALF)):
    print(name, "OK" if proofread(x, t0s, ci, name) else "MISMATCH")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for name, x in (("full", xa), ("half", xb)):
    X = np.fft.rfft(x.astype(float))
    fr = np.fft.rfftfreq(len(x), 1/sr)
    X[(fr < 48) | (fr > 62)] = 0
    env = np.abs(np.fft.ifft(np.concatenate([X, np.conj(X[-2:0:-1])]))[:len(x)])
    env /= env.max()
    tt = np.arange(len(x)) / sr
    fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
    ax.plot(tt, env, color='black', lw=0.9)
    ci = FULL if name == "full" else HALF
    ax.axvspan(0, ci/sr, color='black', alpha=0.06, lw=0)
    ax.set_xlim(0, len(x)/sr); ax.set_ylim(0, 1.05)
    ax.set_xlabel('seconds', fontsize=9); ax.set_yticks([])
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.set_title('55 Hz, span 0.268 - twelve swells at 3.73 s; count-in '
                 + ('FULL spacing (3.73 s)' if name == 'full'
                    else 'HALF spacing (1.87 s)'), fontsize=10)
    fig.tight_layout()
    fig.savefig(f'/tmp/countin_{name}_still.png')
    print("wrote", f'/tmp/countin_{name}_still.png')
