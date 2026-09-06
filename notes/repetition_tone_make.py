#!/usr/bin/env python3
"""Render a pulse train crossing from countable rhythm into audible pitch."""

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
DURATION = 24.0
W, H = 1024, 576
RATE0 = 2.0
DOUBLING_TIME = 5.0


def rate(t: np.ndarray | float) -> np.ndarray | float:
    return RATE0 * np.power(2.0, np.asarray(t) / DOUBLING_TIME)


def phase(t: np.ndarray | float) -> np.ndarray | float:
    # cycles elapsed under an exponentially rising event rate
    return RATE0 * DOUBLING_TIME / math.log(2.0) * (
        np.power(2.0, np.asarray(t) / DOUBLING_TIME) - 1.0
    )


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size
    )


def make_audio() -> Path:
    t = np.arange(int(SR * DURATION), dtype=np.float64) / SR
    p = phase(t)
    wrapped = (p + 0.5) % 1.0 - 0.5
    pulse_width = 0.052
    y = np.exp(-0.5 * (wrapped / pulse_width) ** 2)
    y -= math.sqrt(2.0 * math.pi) * pulse_width

    # A small room gives isolated events weight without masking their fusion.
    delay = int(0.037 * SR)
    wet = y.copy()
    wet[delay:] += 0.20 * y[:-delay]
    delay2 = int(0.071 * SR)
    wet[delay2:] += 0.11 * y[:-delay2]
    env = np.minimum(1.0, t / 1.0) * np.minimum(1.0, (DURATION - t) / 1.1)
    wet *= np.clip(env, 0.0, 1.0)
    wet /= max(1e-9, np.max(np.abs(wet)))
    wet *= 0.82

    stereo = np.stack([wet, wet], axis=1)
    pcm = np.int16(np.clip(stereo, -1, 1) * 32767)
    wav_path = ASSETS / "repetition-becomes-tone.wav"
    with wave.open(str(wav_path), "wb") as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SR)
        out.writeframes(pcm.tobytes())
    return wav_path


def frame_at(sec: float) -> Image.Image:
    im = Image.new("RGB", (W, H), (8, 10, 15))
    d = ImageDraw.Draw(im)
    ivory = (225, 222, 206)
    coral = (240, 105, 86)
    blue = (92, 174, 231)
    faint = (53, 58, 68)

    # A three-second memory: separate arrivals gradually fuse into a field.
    left, right = 80, 944
    y0, y1 = 218, 358
    d.rounded_rectangle((left, y0, right, y1), radius=8, fill=(14, 17, 24))
    d.line((left, (y0 + y1) // 2, right, (y0 + y1) // 2), fill=faint, width=1)
    window = 3.0
    t0 = max(0.0, sec - window)
    first = math.ceil(float(phase(t0)))
    last = math.floor(float(phase(sec)))
    # Invert the analytic phase to locate each arrival exactly.
    for n in range(first, last + 1):
        event_t = DOUBLING_TIME * math.log2(
            1.0 + n * math.log(2.0) / (RATE0 * DOUBLING_TIME)
        )
        x = right - (sec - event_t) / window * (right - left)
        age = (sec - event_t) / window
        alpha = max(0.0, 1.0 - age) ** 0.7
        color = tuple(int(faint[i] + alpha * (coral[i] - faint[i])) for i in range(3))
        d.line((x, y0 + 16, x, y1 - 16), fill=color, width=3)

    # The live event: a point circling ever faster, never changing identity.
    cx, cy, rr = 512, 116, 50
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(55, 61, 71), width=2)
    a = 2 * math.pi * float(phase(sec)) - math.pi / 2
    px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
    d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=coral)

    r = float(rate(sec))
    # The labels crossfade around the conventional rhythm/pitch boundary.
    blend = 1.0 / (1.0 + math.exp(-(r - 20.0) / 3.0))
    rhythm_c = tuple(int((1 - blend) * ivory[i] + blend * faint[i]) for i in range(3))
    tone_c = tuple(int(blend * blue[i] + (1 - blend) * faint[i]) for i in range(3))
    d.text((80, 420), "RHYTHM", font=font(34), fill=rhythm_c)
    tone_text = "TONE"
    tone_w = d.textbbox((0, 0), tone_text, font=font(34))[2]
    d.text((944 - tone_w, 420), tone_text, font=font(34), fill=tone_c)
    d.line((245, 440, 779, 440), fill=(44, 49, 58), width=2)
    marker_x = 245 + min(1.0, max(0.0, math.log2(r / RATE0) / math.log2(rate(DURATION) / RATE0))) * 534
    d.ellipse((marker_x - 5, 435, marker_x + 5, 445), fill=ivory)

    if sec < 4.0:
        opacity = min(1.0, sec / 0.8) * min(1.0, (4.0 - sec) / 1.0)
        title = "THE SAME EVENT, CLOSER TO ITSELF"
        col = tuple(int(opacity * c + (1 - opacity) * 8) for c in ivory)
        tw = d.textbbox((0, 0), title, font=font(22))[2]
        d.text(((W - tw) / 2, 508), title, font=font(22), fill=col)
    elif sec > 20.0:
        opacity = min(1.0, (sec - 20.0) / 1.0) * min(1.0, (DURATION - sec) / 1.0)
        title = "NOTHING ARRIVED"
        col = tuple(int(opacity * c + (1 - opacity) * 8) for c in ivory)
        tw = d.textbbox((0, 0), title, font=font(22))[2]
        d.text(((W - tw) / 2, 508), title, font=font(22), fill=col)
    return im


def render_video(wav_path: Path) -> Path:
    silent = ASSETS / "repetition-becomes-tone-silent.mp4"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
        "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "20", str(silent),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    for idx in range(round(DURATION * FPS)):
        proc.stdin.write(frame_at(idx / FPS).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("video render failed")

    out = ASSETS / "repetition-becomes-tone.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(silent),
        "-i", str(wav_path), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(out),
    ], check=True)
    silent.unlink()
    return out


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    wav = make_audio()
    video = render_video(wav)
    wav.unlink()
    frame_at(18.0).save(ASSETS / "repetition-becomes-tone-cover.png")
    print(video)


if __name__ == "__main__":
    main()
