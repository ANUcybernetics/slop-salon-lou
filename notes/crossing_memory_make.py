#!/usr/bin/env python3
"""Render two identical boundary-rate pulse trains reached from opposite sides."""

from __future__ import annotations

import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FPS = 24
SR = 48_000
DURATION = 29.0
W, H = 1024, 576
BOUNDARY = 18.0


def smooth(u: np.ndarray) -> np.ndarray:
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def event_rate(t: np.ndarray) -> np.ndarray:
    r = np.zeros_like(t)
    a = (t >= 1.0) & (t < 9.0)
    r[a] = 3.0 * np.power(6.0, smooth((t[a] - 1.0) / 8.0))
    a = (t >= 9.0) & (t < 13.0)
    r[a] = BOUNDARY
    a = (t >= 16.0) & (t < 24.0)
    r[a] = 54.0 * np.power(1.0 / 3.0, smooth((t[a] - 16.0) / 8.0))
    a = (t >= 24.0) & (t < 28.0)
    r[a] = BOUNDARY
    return r


def envelope(t: np.ndarray) -> np.ndarray:
    env = np.zeros_like(t)
    for start, end in ((1.0, 13.0), (16.0, 28.0)):
        inside = (t >= start) & (t < end)
        env[inside] = np.minimum(1.0, (t[inside] - start) / 0.45) * np.minimum(
            1.0, (end - t[inside]) / 0.45
        )
    return np.clip(env, 0.0, 1.0)


def make_audio() -> Path:
    t = np.arange(round(SR * DURATION), dtype=np.float64) / SR
    r = event_rate(t)
    cycles = np.cumsum(r) / SR
    wrapped = (cycles + 0.5) % 1.0 - 0.5
    width = 0.055
    pulse = np.exp(-0.5 * (wrapped / width) ** 2)
    pulse -= math.sqrt(2.0 * math.pi) * width
    y = pulse * envelope(t)
    # The two plateaus are physically the same pulse train; only their lead-in differs.
    delay = int(0.031 * SR)
    room = y.copy()
    room[delay:] += 0.16 * y[:-delay]
    y = room / max(1e-9, np.max(np.abs(room))) * 0.82
    stereo = np.stack([y, y], axis=1)
    pcm = np.int16(np.clip(stereo, -1.0, 1.0) * 32767)
    path = ASSETS / "crossing-memory.wav"
    with wave.open(str(path), "wb") as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SR)
        out.writeframes(pcm.tobytes())
    return path


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def rate_scalar(sec: float) -> float:
    return float(event_rate(np.array([sec]))[0])


def centered(d: ImageDraw.ImageDraw, text: str, y: int, size: int, color: tuple[int, int, int]) -> None:
    f = font(size)
    box = d.textbbox((0, 0), text, font=f)
    d.text(((W - (box[2] - box[0])) / 2, y), text, font=f, fill=color)


def frame_at(sec: float) -> Image.Image:
    bg = (8, 10, 15)
    ivory = (226, 222, 205)
    faint = (55, 61, 71)
    coral = (239, 103, 84)
    blue = (93, 175, 231)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)

    d.text((70, 52), "CROSSING MEMORY", font=font(24), fill=ivory)
    d.line((70, 94, 954, 94), fill=(36, 41, 49), width=2)

    if sec < 14.5:
        active_start, active_end = 1.0, 13.0
        direction = "FROM APART"
        direction_color = coral
        progress = np.clip((sec - active_start) / (active_end - active_start), 0.0, 1.0)
        local_sec = sec
    else:
        active_start, active_end = 16.0, 28.0
        direction = "FROM FUSED"
        direction_color = blue
        progress = np.clip((sec - active_start) / (active_end - active_start), 0.0, 1.0)
        local_sec = sec

    centered(d, direction, 129, 25, direction_color)
    left, right, yy = 112, 912, 286
    d.line((left, yy, right, yy), fill=faint, width=3)
    # Log rate ruler, with the shared plateau marked as the central door.
    for value in (3, 6, 12, 18, 27, 54):
        x = left + math.log(value / 3.0, 18.0) * (right - left)
        h = 22 if value == 18 else 10
        d.line((x, yy - h, x, yy + h), fill=ivory if value == 18 else faint, width=2)
        label = str(value)
        box = d.textbbox((0, 0), label, font=font(17))
        d.text((x - (box[2] - box[0]) / 2, yy + 32), label, font=font(17), fill=ivory if value == 18 else faint)

    r = rate_scalar(local_sec)
    if r > 0:
        x = left + math.log(r / 3.0, 18.0) * (right - left)
        pulse = 0.5 + 0.5 * math.cos(2 * math.pi * r * sec)
        radius = 8 + int(5 * pulse)
        d.ellipse((x - radius, yy - radius, x + radius, yy + radius), fill=direction_color)
        if abs(r - BOUNDARY) < 0.01:
            d.rounded_rectangle((382, 354, 642, 411), radius=8, outline=ivory, width=2)
            centered(d, "18 / SECOND", 366, 25, ivory)

    d.text((70, 492), "RHYTHM", font=font(21), fill=coral)
    tone = "TONE"
    tw = d.textbbox((0, 0), tone, font=font(21))[2]
    d.text((954 - tw, 492), tone, font=font(21), fill=blue)

    if 13.4 <= sec < 15.6:
        fade = min(1.0, (sec - 13.4) / 0.5, (15.6 - sec) / 0.5)
        centered(d, "SAME RATE", 218, 32, tuple(int(c * fade) for c in ivory))
        centered(d, "DIFFERENT ARRIVAL", 269, 32, tuple(int(c * fade) for c in ivory))
    if sec >= 27.0:
        fade = min(1.0, sec - 27.0, DURATION - sec)
        centered(d, "DOES THE NAME ARRIVE AT THE SAME TIME?", 438, 22, tuple(int(c * max(0.0, fade)) for c in ivory))
    return im


def render_video(wav_path: Path) -> Path:
    silent = ASSETS / "crossing-memory-silent.mp4"
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-crf", "20", str(silent),
    ], stdin=subprocess.PIPE)
    assert proc.stdin is not None
    for idx in range(round(DURATION * FPS)):
        proc.stdin.write(frame_at(idx / FPS).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("video render failed")
    out = ASSETS / "crossing-memory.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(wav_path),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out),
    ], check=True)
    silent.unlink()
    return out


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    wav = make_audio()
    video = render_video(wav)
    frame_at(24.8).save(ASSETS / "crossing-memory-cover.png")
    wav.unlink()
    print(video)


if __name__ == "__main__":
    main()
