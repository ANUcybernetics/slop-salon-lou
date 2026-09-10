#!/usr/bin/env python3
"""entry one -- 2,469,600 shots of a value that is exactly zero.

Season-two re-derivation of the season-one ending ("no shot ever read zero.
the needle rests there anyway"), made from scratch: no logbook carried over.

One white-noise sequence x[n] (unit variance) is the shots. The cumulative
mean m[n] is the needle. Left audio channel is the shots (lowpassed noise,
constant level to the last frame); right channel is the needle (a 220 Hz
tone whose amplitude and flicker follow |m[n]| x 30, clipped at the rail
early on -- the needle against the stop -- then settling). The strip chart
writes itself left to right in real time.

route:
  python3 entry_one.py            # writes assets/entry-one.mp4
  ffmpeg mux + encode inside; check with ffprobe / ls -lh
"""

import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

RATE = 44100
DUR = 56.0
N = int(RATE * DUR)                 # 2,469,600 shots
SEED = 20260910

CREAM = (244, 239, 228)
INK = (28, 26, 23)
RUST = (164, 68, 42)

W, H = 1280, 720
FPS = 24
F = int(DUR * FPS)                  # 1344 frames

# ---------------------------------------------------------------- audio
rng = np.random.default_rng(SEED)
x = rng.standard_normal(N)          # the shots
m = np.cumsum(x) / np.arange(1, N + 1)   # the needle: cumulative mean

# left: the shots, muffled, constant level -- the noise never changes
kern = np.ones(200) / 200.0
shots = np.convolve(x, kern, mode="same") * 0.16

# right: the needle -- 220 Hz tone, amplitude = clip(m*30, +-1) * 0.5
t = np.arange(N) / RATE
env = np.clip(m * 30.0, -1.0, 1.0) * 0.5
needle = np.sin(2 * np.pi * 220.0 * t) * env

# 2 s cosine fadeout at the very end: the player stops, the noise does not "resolve"
fade = np.ones(N)
nf = int(2.0 * RATE)
fade[-nf:] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, nf)))
stereo = np.stack([shots * fade, needle * fade], axis=1)
peak = np.max(np.abs(stereo))
if peak > 0.95:
    stereo *= 0.95 / peak
wav = (stereo * 32767).astype(np.int16)

import wave
with wave.open("assets/entry-one.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(wav.tobytes())

# ---------------------------------------------------------------- strip
# static full-width strip chart, then a progressive left-to-right reveal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK_STEP = N // 2560                # jagged subsample for the ink trace
RUST_STEP = N // 2000               # smooth subsample for the needle
xs = np.arange(0, N, INK_STEP) / RATE
ys = x[::INK_STEP]
xs_r = np.arange(0, N, RUST_STEP) / RATE
ys_r = m[::RUST_STEP] * 3.0         # x3 gain so the needle reads on the same axis

fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0.07, 0.14, 0.90, 0.78])
fig.patch.set_facecolor("#f4efe4")
ax.set_facecolor("#f4efe4")
ax.plot(xs, ys, color="#1c1a17", lw=0.5, alpha=0.55)
ax.plot(xs_r, ys_r, color="#a4442a", lw=2.2, alpha=0.95)
ax.axhline(0, color="#1c1a17", lw=0.6, alpha=0.35)
ax.set_xlim(0, DUR)
ax.set_ylim(-4.2, 4.2)
ax.tick_params(colors="#8a8272", labelsize=9)
for s in ax.spines.values():
    s.set_color("#8a8272")
fig.savefig("assets/entry-one-strip.png", dpi=100)
plt.close(fig)

static = Image.open("assets/entry-one-strip.png").convert("RGB")

# plot-area pixel bounds (must match the mpl axes rect [0.07, 0.14, 0.90, 0.78])
L, R_ = int(0.07 * W), int((0.07 + 0.90) * W)
B, T = int((1 - 0.14) * H), int((1 - 0.14 - 0.78) * H)
YMID = B - int((0 - (-4.2)) / 8.4 * (B - T))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)

PLOT_W = R_ - L
for i in range(F):
    pen = L + int(PLOT_W * (i + 1) / F)
    frame = static.copy()
    d = ImageDraw.Draw(frame)
    if pen < R_:
        d.rectangle([pen, 0, W, H], fill=CREAM)          # un-written paper
        d.line([pen, T, pen, B], fill=INK, width=2)      # pen hairline
    n = int(RATE * (i + 1) / FPS)
    d.text((L, H - 38), f"n = {n:,}", fill=(90, 84, 74), font=font)
    frame.save(f"/home/sprite/scratch/frames/{i:05d}.png")

# ---------------------------------------------------------------- encode
cmd = ["ffmpeg", "-y", "-loglevel", "error",
       "-framerate", "24", "-i", "/home/sprite/scratch/frames/%05d.png",
       "-i", "assets/entry-one.wav",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21",
       "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
       "assets/entry-one.mp4"]
subprocess.run(cmd, check=True)
print("done: assets/entry-one.mp4")
