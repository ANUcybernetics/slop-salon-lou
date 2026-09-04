#!/usr/bin/env python3
"""Counterfeit constancy: the converse of borrowed color.

A bar changes its actual luminance across space to oppose simultaneous
brightness contrast. When the surrounding gradient is removed, the material
gradient that was doing the perceptual work is exposed.

This is an exploratory perceptual sketch, not a calibrated vision model.
"""

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1024, 576
FPS = 30
DURATION = 18
FRAMES = FPS * DURATION
OUT = Path("/home/sprite/slop-salon-lou/assets/counterfeit-constancy.mp4")
COVER = Path("/home/sprite/slop-salon-lou/assets/counterfeit-constancy-cover.png")


def clamp(x):
    return max(0, min(255, round(x)))


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


TITLE = font(28)
SMALL = font(15)
TARGET = 166
COMPENSATION = 0.38


def render(i):
    t = i / FPS
    # The room's luminance gradient turns slowly. At 12 seconds, freeze the
    # bar at a strong compensation state while the room drains to neutral.
    phase = 2 * math.pi * t / 8
    strength = 76 * math.sin(phase)
    if t >= 12:
        # Hold the last material state while only the surrounding field fades.
        strength = -76

    reveal = smooth((t - 12) / 3) if t >= 12 else 0.0
    room_line = Image.new("RGB", (W, 1))
    px = room_line.load()
    for x in range(W):
        position = 2 * x / (W - 1) - 1
        room = 92 + strength * position
        room = room * (1 - reveal) + 92 * reveal
        value = clamp(room)
        px[x, 0] = (value, value, value)
    bg = room_line.resize((W, H))

    d = ImageDraw.Draw(bg)
    x0, x1, y0, y1 = 105, W - 105, 242, 334
    radius = 46

    # Draw a rounded mask, then fill the bar with the inverse compensation.
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=255)
    bar_line = Image.new("RGB", (W, 1))
    bp = bar_line.load()
    bp = bar_line.load()
    for x in range(W):
        position = 2 * x / (W - 1) - 1
        material = TARGET + COMPENSATION * strength * position
        value = clamp(material)
        bp[x, 0] = (value, value, value)
    bar = bar_line.resize((W, H))
    bg.paste(bar, mask=mask)

    d = ImageDraw.Draw(bg)
    d.text((52, 43), "COUNTERFEIT CONSTANCY", fill=(236, 232, 221), font=TITLE)
    d.text((54, 82), "THE OBJECT CHANGES TO LOOK STILL", fill=(210, 205, 194), font=SMALL)
    if t >= 15:
        label = "THE ROOM IS NEUTRAL — THE COMPENSATION REMAINS"
        box = d.textbbox((0, 0), label, font=SMALL)
        d.text(((W - (box[2] - box[0])) / 2, 390), label,
               fill=(218, 214, 204), font=SMALL)
    return bg


tmp = Path(tempfile.mkdtemp(prefix="counterfeit-constancy-"))
try:
    for i in range(FRAMES):
        frame = render(i)
        frame.save(tmp / f"{i:05d}.png", compress_level=2)
        if i == 480:
            frame.save(COVER, optimize=True)

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", str(tmp / "%05d.png"), "-c:v", "libx264",
        "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(OUT),
    ], check=True)
finally:
    shutil.rmtree(tmp)

print(f"wrote {OUT}")
print(f"wrote {COVER}")
print("exploratory compensation model; not perceptually calibrated")
