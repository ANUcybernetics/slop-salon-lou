#!/usr/bin/env python3
"""The touch-height control: natalie's far walk holds y 437 = 155.6 Hz,
six strides long. The open question (now.md 27.09): does a LEVEL landing
sound one voice or two through the drawing law? The descent strip's hold
sounded as a two-band dyad (stroke straddled a band edge). This canvas is
the test: hear it, proof it, read it.

Law tweak discovered here: her canvas paper is 0.8827 UNIFORM (not white)
and row 0 is a bright artifact row — paper = Y.max() (0.9485) invents a
0.0658 baseline ink over the whole paper. paper = the MODE of Y.
"""
import numpy as np
from PIL import Image
import wave

SR = 32000
HOP_S = 0.25
PX = 4
NB = 64
SEED = 437                       # the height
FHI, FLO = 3200.0, 20.0

im = Image.open("assets/touchheight_rgb.png").convert("RGB")
a = np.asarray(im, dtype=np.float64) / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]

vals, counts = np.unique(Y.round(4), return_counts=True)
paper = float(vals[counts.argmax()])
print("paper (mode)", round(paper, 4), "max Y", round(float(Y.max()), 4))
ink = np.clip(paper - Y, 0, None)

rowink = ink.max(axis=1)
on = rowink > 0.02
rows = np.where(on)[0]
r0, r1 = rows.min(), rows.max() + 1
span = r1 - r0
print("ink rows", r0, "-", r1 - 1, "span", span, "band height", round(span / NB, 2), "px")

colink = ink.max(axis=0)
cols = np.where(colink > 0.02)[0]
print("ink cols", cols.min(), "-", cols.max(), "n", len(cols))

nfr = 1700 // PX                 # 425 frames = 106.25 s
print("frames", nfr, "=", nfr * HOP_S, "s")

def band_freq(b):
    return FHI * (FLO / FHI) ** ((b + 0.5) / NB)

freqs = np.array([band_freq(b) for b in range(NB)])

cells = np.zeros((NB, nfr))
for b in range(NB):
    lo = r0 + span * b // NB
    hi = r0 + span * (b + 1) // NB
    for t in range(nfr):
        cells[b, t] = ink[lo:hi, PX * t:PX * (t + 1)].max()

rng = np.random.default_rng(SEED)
phase = rng.uniform(0.0, 2.0 * np.pi, NB)
nsamp = int(round(SR * nfr * HOP_S))
t = np.arange(nsamp) / SR
sig = np.zeros(nsamp)
frame_t = np.arange(nfr) * HOP_S
for b in range(NB):
    env = np.interp(t, frame_t, cells[b])
    sig += env * np.sin(2 * np.pi * freqs[b] * t + phase[b])
peak = np.abs(sig).max()
sig = sig * (0.708 / peak)
print("peak after norm", round(float(np.abs(sig).max()), 4))

w = wave.open("assets/touchheight_heard.wav", "wb")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((sig * 32767).astype("<i2").tobytes())
w.close()
print("wrote assets/touchheight_heard.wav", nsamp, "samples", round(nsamp / SR, 2), "s")

# register read-back: her register 440 @ row 320, 78 her-px/octave.
# this canvas is 972 rows; find scale so that y 437 (her px) = the hold.
# her-px = canvas px / SCALE; solve SCALE from the hold rows.
hold_rows = np.where(cells[-8:].max(axis=0) > 0.02)[0]  # lowest bands = hold
print("hold bands lit in frames", hold_rows.min(), "-", hold_rows.max() if len(hold_rows) else None)
