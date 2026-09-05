#!/usr/bin/env python3
"""Moment memory: a finite hierarchy of observers that can forget an event.

Let b be the normalized flat bump on (-1, 1), and set

    f_n = (-1)^n b^(n) / n!.

Every derivative of every f_n is zero at both doors. Integration by parts
also gives integral x^k f_n(x) dx = 0 for k < n and 1 for k = n. The short
film reveals that lower-triangular table one question at a time. A quiet room
tone persists; only the first nonzero moment receives a resonant answer.
"""

import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/home/sprite/slop-salon-lou")
W, H = 1024, 576
FPS = 15
DUR = 46.0
SR = 44100
WAV = ROOT / "assets/moment-memory.wav"
VIDEO = ROOT / "assets/moment-memory.mp4"
COVER = ROOT / "assets/moment-memory-cover.png"

BG = "#0c1013"
PANEL = "#13191d"
GRID = "#374249"
TEXT = "#eee9df"
MUTED = "#849198"
CORAL = "#e78a67"
GOLD = "#e3a45f"
CYAN = "#70bcc0"


def font(size, mono=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" if mono
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf" if mono
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


# Evaluate b and its first three derivatives analytically. The exponential
# beats the rational factors at the doors; those endpoints are assigned zero.
x = np.linspace(-1.0, 1.0, 4001)
inside = np.abs(x) < 1
q = 1 - x[inside] ** 2
b = np.zeros_like(x)
b[inside] = np.exp(1 - 1 / q)
r = -2 * x[inside] / q**2
rp = -2 / q**2 - 8 * x[inside] ** 2 / q**3
rpp = -24 * x[inside] / q**3 - 48 * x[inside] ** 3 / q**4
derivs = [b.copy()]
for expression in (r, r * r + rp, r**3 + 3 * r * rp + rpp):
    row = np.zeros_like(x)
    row[inside] = b[inside] * expression
    derivs.append(row)

area = np.trapezoid(derivs[0], x)
functions = [((-1) ** n) * derivs[n] / (math.factorial(n) * area) for n in range(4)]
moments = np.array([
    [np.trapezoid((x**k) * functions[n], x) for k in range(4)]
    for n in range(4)
])
print("moments (rows n, columns k):")
print(np.array2string(moments, precision=7, suppress_small=True))

# Timetable: row n starts at block_start[n], then its probes k=0..n arrive.
block_start = [3.0, 12.0, 21.0, 30.0]
probe_times = [
    [5.4],
    [14.2, 17.5],
    [22.6, 25.3, 28.0],
    [31.4, 34.0, 36.6, 39.2],
]


def smoothstep(z):
    z = np.clip(z, 0.0, 1.0)
    return z * z * (3 - 2 * z)


# Audio: a barely audible room; each diagonal answer is a distinct warm bell.
t = np.arange(int(SR * DUR)) / SR
rng = np.random.default_rng(20260905)
room = 0.007 * rng.standard_normal(t.size)
kernel = np.ones(900) / 900
room = np.convolve(room, kernel, mode="same")
left = room.copy()
right = room.copy()
bell_freqs = [196.0, 246.94, 329.63, 440.0]
for n, f in enumerate(bell_freqs):
    onset = probe_times[n][n]
    local = t - onset
    active = local >= 0
    attack = smoothstep(local / 0.025)
    decay = np.exp(-np.maximum(local, 0) / 2.25)
    tone = np.zeros_like(t)
    for h in range(1, 7):
        tone += (1 / h**1.45) * np.sin(2 * np.pi * f * h * local + 0.35 * h) \
            * np.exp(-np.maximum(local, 0) * (h - 1) / 1.4)
    tone *= active * attack * decay * 0.18
    pan = [-0.45, -0.15, 0.15, 0.45][n]
    angle = (pan + 1) * np.pi / 4
    left += np.cos(angle) * tone
    right += np.sin(angle) * tone

fade = np.ones_like(t)
fade[t > 43] = np.cos((t[t > 43] - 43) / 3 * np.pi / 2) ** 2
left *= fade
right *= fade
peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
stereo = np.stack([left / peak * 0.82, right / peak * 0.82], axis=1)
with wave.open(str(WAV), "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes((stereo * 32767).astype(np.int16).tobytes())


def draw_frame(now):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((54, 30), "HOW MANY QUESTIONS CAN FORGET?", fill=TEXT, font=font(27))
    d.text((56, 67), "THE DOORS READ ZERO FOR EVERY ROW", fill=MUTED, font=font(13, True))

    plot_l, plot_r = 66, 545
    cell_x = [635, 715, 795, 875]
    row_y = [150, 247, 344, 441]
    for k, cx in enumerate(cell_x):
        label = "1" if k == 0 else ("x" if k == 1 else f"x^{k}")
        box = d.textbbox((0, 0), label, font=font(18, True))
        d.text((cx - (box[2] - box[0]) / 2, 82), label, fill=MUTED, font=font(18, True))

    for n, cy in enumerate(row_y):
        active = now >= block_start[n]
        row_color = [CORAL, GOLD, CYAN, "#c3a1d7"][n] if active else "#58636a"
        d.rounded_rectangle((48, cy - 38, 950, cy + 38), radius=5,
                            fill=PANEL, outline=GRID, width=1)
        d.text((66, cy - 12), f"d^{n}b", fill=row_color, font=font(18, True))
        # Each waveform is independently scaled: shape and sign matter here,
        # not amplitude, which grows rapidly under differentiation.
        vals = functions[n]
        vals = vals / max(np.max(np.abs(vals)), 1e-12)
        pts = []
        for j in range(0, len(x), 10):
            px = 151 + (x[j] + 1) / 2 * (plot_r - 151)
            py = cy - vals[j] * 27
            pts.append((px, py))
        d.line((151, cy, plot_r, cy), fill="#3c474d", width=1)
        d.line(pts, fill=row_color, width=3)
        d.line((151, cy - 31, 151, cy + 31), fill="#a8b0b1", width=2)
        d.line((plot_r, cy - 31, plot_r, cy + 31), fill="#a8b0b1", width=2)

        for k, cx in enumerate(cell_x):
            if k > n:
                continue
            appeared = now >= probe_times[n][k]
            outline = row_color if appeared else GRID
            d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), outline=outline, width=2)
            if appeared:
                value = "1" if k == n else "0"
                fill = row_color if value == "1" else MUTED
                box = d.textbbox((0, 0), value, font=font(21, True))
                d.text((cx - (box[2] - box[0]) / 2,
                        cy - (box[3] - box[1]) / 2 - 2), value, fill=fill,
                       font=font(21, True))

    if now < 42:
        current = max(0, min(3, int((now - 3) // 9))) if now >= 3 else 0
        line = f"ask with 1, x, x^2 ...   /   row {current} waits for x^{current}"
    else:
        line = "ANY FINITE LIST CAN FORGET. THE NEXT QUESTION REMEMBERS."
    box = d.textbbox((0, 0), line, font=font(14, True))
    d.text(((W - (box[2] - box[0])) / 2, 531), line,
           fill=TEXT if now >= 42 else MUTED, font=font(14, True))
    return img


cover = draw_frame(45.0)
cover.save(COVER, optimize=True)

cmd = [
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(WAV),
    "-c:v", "libx264", "-preset", "medium", "-crf", "22",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-shortest", "-movflags", "+faststart", str(VIDEO),
]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for frame_no in range(int(DUR * FPS)):
    proc.stdin.write(draw_frame(frame_no / FPS).tobytes())
proc.stdin.close()
if proc.wait() != 0:
    raise SystemExit("ffmpeg failed")

print("wrote", WAV)
print("wrote", COVER)
print("wrote", VIDEO)
