#!/usr/bin/env python3
"""Borrowed color: a motion study in simultaneous contrast.

One uninterrupted RGB-neutral bar crosses two fields whose hues and luminance
change independently. The bar never changes. Near the end, both fields drain
to the same neutral ground, making the material continuity plain.
"""

import colorsys
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1024, 576
FPS = 30
DURATION = 22
FRAMES = FPS * DURATION
BAR = (166, 166, 166)
OUT = Path("/home/sprite/slop-salon-lou/assets/borrowed-color.mp4")
COVER = Path("/home/sprite/slop-salon-lou/assets/borrowed-color-cover.png")


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def mix(a, b, u):
    return tuple(round(x * (1 - u) + y * u) for x, y in zip(a, b))


def field(hue, light, saturation=0.56):
    rgb = colorsys.hls_to_rgb(hue % 1.0, light, saturation)
    return tuple(round(255 * c) for c in rgb)


def font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


TITLE = font(28)
SMALL = font(15)


def render(i):
    t = i / FPS
    # The fields turn slowly through opposing hues while their brightnesses
    # breathe out of phase. The bar itself is never interpolated or shaded.
    hue = 0.02 + 0.055 * t
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t / 9)
    left = field(hue, 0.31 + 0.13 * pulse)
    right = field(hue + 0.5, 0.66 - 0.13 * pulse)

    # From 16–19 s, remove the context. Hold the proof, then let color return.
    if 16 <= t < 19:
        u = smooth((t - 16) / 3)
        left = mix(left, (92, 92, 92), u)
        right = mix(right, (92, 92, 92), u)
    elif 19 <= t:
        left = right = (92, 92, 92)

    im = Image.new("RGB", (W, H), left)
    d = ImageDraw.Draw(im)
    d.rectangle((W // 2, 0, W, H), fill=right)

    # One continuous object, deliberately drawn in a single operation.
    d.rounded_rectangle((105, 242, W - 105, 334), radius=46, fill=BAR)

    d.text((52, 43), "BORROWED COLOR", fill=(236, 232, 221), font=TITLE)
    d.text((54, 82), "THE OBJECT DOES NOT CHANGE", fill=(210, 205, 194), font=SMALL)
    if 19 <= t:
        label = "RGB 166 / 166 / 166 — ONE UNINTERRUPTED BAR"
        box = d.textbbox((0, 0), label, font=SMALL)
        d.text(((W - (box[2] - box[0])) / 2, 390), label,
               fill=(218, 214, 204), font=SMALL)
    return im


tmp = Path(tempfile.mkdtemp(prefix="borrowed-color-"))
try:
    for i in range(FRAMES):
        frame = render(i)
        frame.save(tmp / f"{i:05d}.png", compress_level=2)
        if i == 300:
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
print(f"bar RGB is constant: {BAR}")
