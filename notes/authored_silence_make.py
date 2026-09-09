#!/usr/bin/env python3
"""Cut generated sound into brief objects and give the rests their own clock."""

from __future__ import annotations

import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SR = 48_000
DURATION = 44.0
FPS = 24
SIZE = (1024, 576)


def decode(path: Path) -> np.ndarray:
    raw = subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le",
            "-ac", "2", "-ar", str(SR), "-",
        ]
    )
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)


def envelope(length: int, attack: float, release: float) -> np.ndarray:
    env = np.ones(length, dtype=np.float32)
    a = max(2, min(length // 2, int(attack * SR)))
    r = max(2, min(length - a, int(release * SR)))
    env[:a] = np.sin(np.linspace(0, np.pi / 2, a, endpoint=True)) ** 2
    env[-r:] = np.cos(np.linspace(0, np.pi / 2, r, endpoint=True)) ** 2
    return env


def main() -> None:
    flux = decode(ASSETS / "room-without-meter.opus")
    musicgen = decode(ASSETS / "room-without-meter-musicgen.mp3")

    # source, source start, length, destination, gain, pan (-1 left, +1 right)
    events = [
        (flux, 0.69, 0.31, 1.40, 0.58, -0.72),
        (flux, 2.29, 0.43, 5.95, 0.68, +0.44),
        (musicgen, 0.12, 0.27, 12.80, 0.38, -0.18),
        (flux, 4.72, 0.56, 20.35, 0.74, +0.78),
        (musicgen, 14.29, 0.34, 29.45, 0.31, -0.55),
        (flux, 8.20, 0.72, 38.15, 0.62, +0.12),
    ]

    mix = np.zeros((int(DURATION * SR), 2), dtype=np.float32)
    event_shapes = []
    for source, source_at, length, dest_at, gain, pan in events:
        n = int(length * SR)
        start = int(source_at * SR)
        clip = source[start : start + n].copy()
        peak = float(np.max(np.abs(clip))) or 1.0
        clip /= peak
        clip *= envelope(len(clip), min(0.035, length / 4), min(0.16, length / 2))[:, None]
        left = np.sqrt((1.0 - pan) / 2.0)
        right = np.sqrt((1.0 + pan) / 2.0)
        mono = clip.mean(axis=1)
        placed = gain * np.column_stack((mono * left, mono * right))
        out_start = int(dest_at * SR)
        mix[out_start : out_start + len(placed)] += placed
        event_shapes.append((dest_at, length, pan, gain))

    peak = float(np.max(np.abs(mix)))
    if peak > 0.92:
        mix *= 0.92 / peak

    audio_path = ASSETS / "the-room-keeps-the-rests.opus"
    video_path = ASSETS / "the-room-keeps-the-rests.mp4"
    cover_path = ASSETS / "the-room-keeps-the-rests-cover.png"

    with tempfile.TemporaryDirectory(prefix="lou-rests-") as tmp:
        wav_path = Path(tmp) / "mix.wav"
        pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
        with wave.open(str(wav_path), "wb") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(SR)
            wav.writeframes(pcm.tobytes())

        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(wav_path),
             "-c:a", "libopus", "-b:a", "160k", str(audio_path)],
            check=True,
        )

        video = subprocess.Popen(
            [
                "ffmpeg", "-y", "-v", "error", "-f", "rawvideo",
                "-pix_fmt", "rgb24", "-s", f"{SIZE[0]}x{SIZE[1]}",
                "-r", str(FPS), "-i", "-", "-i", str(wav_path),
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", str(video_path),
            ],
            stdin=subprocess.PIPE,
        )

        cover = None
        for frame_no in range(round(DURATION * FPS)):
            t = frame_no / FPS
            image = Image.new("RGB", SIZE, (237, 232, 219))
            draw = ImageDraw.Draw(image)
            draw.line((84, 288, 940, 288), fill=(189, 181, 163), width=1)
            draw.ellipse((507, 283, 517, 293), fill=(62, 58, 52))

            for index, (at, length, pan, gain) in enumerate(event_shapes):
                age = t - at
                if 0 <= age <= length + 0.45:
                    life = max(0.0, 1.0 - age / (length + 0.45))
                    x = int(512 + pan * 300)
                    radius = int(12 + age * 180)
                    color = (150 + index * 9, 62 + index * 8, 48)
                    width = max(1, int(6 * life))
                    draw.arc(
                        (x - radius, 288 - radius, x + radius, 288 + radius),
                        202, 338, fill=color, width=width,
                    )
                    dot = max(2, int(9 * gain * life))
                    draw.ellipse((x - dot, 288 - dot, x + dot, 288 + dot), fill=color)

            if frame_no == int(20.5 * FPS):
                cover = image.copy()
            assert video.stdin is not None
            video.stdin.write(np.asarray(image, dtype=np.uint8).tobytes())

        assert video.stdin is not None
        video.stdin.close()
        if video.wait() != 0:
            raise RuntimeError("ffmpeg video encode failed")

    if cover is None:
        raise RuntimeError("cover frame was not made")
    cover.save(cover_path)
    print(audio_path)
    print(video_path)
    print(cover_path)


if __name__ == "__main__":
    main()
