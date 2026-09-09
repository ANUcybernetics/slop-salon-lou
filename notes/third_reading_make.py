#!/usr/bin/env python3
"""Four sign chambers: every first and second reading cancels; the third rings."""

from __future__ import annotations

import math
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SR = 48_000
FPS = 24
W, H = 1024, 576
DURATION = 30.0
BLOCK = 2.5
STATES = np.array([
    [1, 1, 1],
    [1, -1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
], dtype=np.float32)
FREQS = (55.0, 89.0, 144.0)  # the third is the sum of the first two
COLORS = ((226, 83, 76), (63, 180, 177), (230, 174, 57))
BG = (13, 15, 20)
PANEL = (21, 24, 31)
TEXT = (230, 226, 214)
MUTED = (118, 125, 137)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


F_TITLE = font(35)
F_LABEL = font(21)
F_SMALL = font(16)
F_BIG = font(42)


def centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str,
             face: ImageFont.ImageFont, fill: tuple[int, int, int]) -> None:
    box = draw.textbbox((0, 0), text, font=face)
    draw.text((xy[0] - (box[2] - box[0]) / 2,
               xy[1] - (box[3] - box[1]) / 2), text, font=face, fill=fill)


def make_audio() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    n = round(BLOCK * SR)
    t = np.arange(n, dtype=np.float64) / SR
    taper = np.ones(n, dtype=np.float64)
    edge = round(0.025 * SR)
    ramp = np.sin(np.linspace(0, math.pi / 2, edge, endpoint=True)) ** 2
    taper[:edge] = ramp
    taper[-edge:] = ramp[::-1]
    voices = np.stack([
        np.cos(2 * math.pi * f * t) * taper for f in FREQS
    ])

    # These are the actual observers. The Hadamard columns make every order-one
    # and order-two mean identically zero, sample by sample. Their product is +1.
    singles = np.stack([
        np.mean(STATES[:, i, None] * voices[i][None, :], axis=0)
        for i in range(3)
    ])
    pairs = np.stack([
        np.mean((STATES[:, i] * STATES[:, j])[:, None]
                * (voices[i] * voices[j])[None, :], axis=0)
        for i, j in ((0, 1), (0, 2), (1, 2))
    ])
    triple = np.mean(
        np.prod(STATES, axis=1)[:, None] * np.prod(voices, axis=0)[None, :],
        axis=0,
    )

    total = round(DURATION * SR)
    mix = np.zeros((total, 2), dtype=np.float64)
    pans = ((1.0, 0.18), (0.28, 0.28), (0.18, 1.0))

    # First ten seconds: the four chambers themselves.
    for k, signs in enumerate(STATES):
        start = round(k * BLOCK * SR)
        for i, sign in enumerate(signs):
            left, right = pans[i]
            mix[start:start+n, 0] += 0.18 * sign * voices[i] * left
            mix[start:start+n, 1] += 0.18 * sign * voices[i] * right

    # Ten seconds of exact authored silence are the first- and second-order reads.
    # Last ten seconds: the third-order observer, repeated four times.
    third = triple / max(np.max(np.abs(triple)), 1e-12)
    for k in range(4):
        start = round((20.0 + k * BLOCK) * SR)
        mix[start:start+n, 0] = 0.42 * third
        mix[start:start+n, 1] = 0.42 * third

    assert float(np.max(np.abs(singles))) < 1e-12
    assert float(np.max(np.abs(pairs))) < 1e-12
    assert np.all(np.prod(STATES, axis=1) == 1)
    return mix, singles, pairs, triple


def frame_at(seconds: float) -> Image.Image:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    centered(draw, (W / 2, 43), "THE THIRD READING", F_TITLE, TEXT)

    xs = (96, 312, 528, 744)
    for k, x in enumerate(xs):
        active = seconds < 10 and int(seconds / BLOCK) == k
        outline = (77, 81, 91) if not active else (210, 204, 186)
        draw.rounded_rectangle((x, 105, x + 184, 250), radius=18,
                               fill=PANEL, outline=outline, width=3 if active else 1)
        centered(draw, (x + 92, 130), str(k + 1), F_SMALL, MUTED)
        for i, sign in enumerate(STATES[k]):
            centered(draw, (x + 48 + i * 44, 187), "+" if sign > 0 else "−",
                     F_BIG, COLORS[i])

    if seconds < 10:
        heading, formula, result = "FOUR CHAMBERS", "ABC = +  ·  +  ·  +  ·  +", ""
        result_color = MUTED
    elif seconds < 15:
        heading, formula, result = "EACH VOICE", "mean A   mean B   mean C", "0   0   0"
        result_color = MUTED
    elif seconds < 20:
        heading, formula, result = "EACH PAIR", "mean AB   mean AC   mean BC", "0   0   0"
        result_color = MUTED
    else:
        heading, formula, result = "ALL THREE", "mean ABC", "+1"
        result_color = COLORS[2]

    centered(draw, (W / 2, 314), heading, F_LABEL, MUTED)
    centered(draw, (W / 2, 367), formula, F_LABEL, TEXT)
    if result:
        centered(draw, (W / 2, 442), result, F_BIG, result_color)

    if 10 <= seconds < 20:
        centered(draw, (W / 2, 515), "silence is the exact reading", F_SMALL, MUTED)
    elif seconds >= 20:
        phase = (seconds - 20) * 2 * math.pi * 0.5
        points = []
        for px in range(180, 845, 4):
            u = (px - 180) / 665
            y = 510 + 15 * math.sin(2 * math.pi * 8 * u + phase)
            points.append((px, y))
        draw.line(points, fill=COLORS[2], width=2)
    return image


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    mix, singles, pairs, triple = make_audio()
    audio_path = ASSETS / "the-third-reading.opus"
    video_path = ASSETS / "the-third-reading.mp4"
    cover_path = ASSETS / "the-third-reading-cover.png"

    with tempfile.TemporaryDirectory(prefix="lou-third-") as tmp:
        wav_path = Path(tmp) / "third.wav"
        pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
        with wave.open(str(wav_path), "wb") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(SR)
            wav.writeframes(pcm.tobytes())

        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", str(wav_path),
            "-c:a", "libopus", "-b:a", "160k", str(audio_path),
        ], check=True)

        proc = subprocess.Popen([
            "ffmpeg", "-y", "-v", "error", "-f", "rawvideo",
            "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-", "-i", str(wav_path), "-c:v", "libx264",
            "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags",
            "+faststart", str(video_path),
        ], stdin=subprocess.PIPE)
        cover = None
        for frame_no in range(round(DURATION * FPS)):
            frame = frame_at(frame_no / FPS)
            if frame_no == round(23 * FPS):
                cover = frame.copy()
            assert proc.stdin is not None
            proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
        assert proc.stdin is not None
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError("ffmpeg video encode failed")

    assert cover is not None
    cover.save(cover_path, optimize=True)
    print(f"max solo residue: {np.max(np.abs(singles)):.3g}")
    print(f"max pair residue: {np.max(np.abs(pairs)):.3g}")
    print(f"triple peak: {np.max(np.abs(triple)):.3g}")
    print(video_path)


if __name__ == "__main__":
    main()
