#!/usr/bin/env python3
"""the taught rung (07.10): does the count-in teach the count or only start it?

the 7.46 s rung refused even ground (salon verdict, 05.10-06.10) with no
count-in. natalie's ear on the panels (07.10): silence teaches the number
by being it. so teach the refused rung in: two panels on the 7.46 s rung --
untaught (no count-in) vs taught (one FULL spacing of silence first).
byte-identical bodies after the start. if the taught panel counts, teaching
carries where even ground refused; if it comes apart too, the count-in
starts the count but the ear still lets go -- repetition is the only
carrier past the wall.
55 Hz, span 0.134 (envelope half-cycle = 7.4627 s = one spacing),
arch cut to leave a 0.63 s valley. twelve swells.
"""
import numpy as np
import wave

sr = 48000
F0 = 55.0
SPAN = 0.134
L = int(round(sr / SPAN))     # one spacing = envelope half-cycle: 358209
VAL = int(round(0.63 * sr))   # valley samples: 30240
N = 12
NONE, FULL = 0, L

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
    print(name, "first sound", (x != 0).argmax() / sr, "s, count-in",
          ci / sr, "s, duration", len(x) / sr, "s")
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

xu, tu = build(NONE)
xt, tt = build(FULL)
d = np.abs(xt[FULL:] - xu).max()
print("bodies identical after the start: max diff", d, "LSB")
print("ALL OK" if d == 0 else "MISMATCH")

for name, x, t0s, ci in (("untaught", xu, tu, NONE), ("taught", xt, tt, FULL)):
    print(name, "OK" if proofread(x, t0s, ci, name) else "MISMATCH")

for name, x in (("untaught", xu), ("taught", xt)):
    with wave.open(f'/tmp/taught_{name}.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(x.tobytes())
    print("wrote", f'/tmp/taught_{name}.wav')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for name, x in (("untaught", xu), ("taught", xt)):
    X = np.fft.rfft(x.astype(float))
    fr = np.fft.rfftfreq(len(x), 1/sr)
    X[(fr < 48) | (fr > 62)] = 0
    env = np.abs(np.fft.ifft(np.concatenate([X, np.conj(X[-2:0:-1])]))[:len(x)])
    env /= env.max()
    tt2 = np.arange(len(x)) / sr
    fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
    ax.plot(tt2, env, color='black', lw=0.9)
    ci = FULL if name == "taught" else NONE
    if ci:
        ax.axvspan(0, ci/sr, color='black', alpha=0.06, lw=0)
    ax.set_xlim(0, len(x)/sr); ax.set_ylim(0, 1.05)
    ax.set_xlabel('seconds', fontsize=9); ax.set_yticks([])
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.set_title('55 Hz, span 0.134 - twelve swells at 7.46 s, '
                 + ('taught in: one full spacing of silence first'
                    if name == 'taught' else 'untaught: no count-in'),
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(f'/tmp/taught_{name}_still.png')
    print("wrote", f'/tmp/taught_{name}_still.png')
