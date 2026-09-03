#!/usr/bin/env python3
"""No next attack: direction without acoustic obligation.

Seven struck resonances begin four seconds apart. Each attack bends upward,
and the final attack makes the largest upward step, so both meter and contour
point beyond it. The eighth attack belongs at 30 s, but is absent. The last
resonance is given enough decay to cross that position and finish on its own:
the phrase stops generating events without sounding cut off.

This is the sound companion to endpoint-study.svg. It tests the same claim in
time: an endpoint can preserve a local vector while its envelope supplies a
complete boundary. The gap is occupied by decay, not left as a placeholder.
"""

import subprocess
import wave

import numpy as np


SR = 44100
DUR = 44.0
N = int(SR * DUR)
T = np.arange(N) / SR
OUT = "/home/sprite/slop-salon-lou/assets/no-next-attack.wav"
VIDEO = "/home/sprite/slop-salon-lou/assets/no-next-attack.mp4"
COVER = "/home/sprite/slop-salon-lou/assets/endpoint-study.png"

# A bent, irregular chain. The last interval is the strongest upward motion.
ONSETS = np.array([2, 6, 10, 14, 18, 22, 26], dtype=float)
SEMITONES = np.array([0, 4, 3, 7, 6, 9, 12], dtype=float)
BASE = 110.0
FREQS = BASE * 2 ** (SEMITONES / 12)
PANS = np.array([-0.36, -0.12, 0.17, -0.08, 0.22, 0.38, 0.0])

left = np.zeros(N)
right = np.zeros(N)
rng = np.random.default_rng(20260903)


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


for i, (onset, f0, pan) in enumerate(zip(ONSETS, FREQS, PANS)):
    local = T - onset
    active = local >= 0

    # Every event carries the same upward vector inside its attack. The final
    # event bends farther, making direction clearest exactly at the boundary.
    bend_st = 0.55 if i < len(ONSETS) - 1 else 1.35
    bend = smoothstep(local / 0.72)
    inst_f = f0 * 2 ** (bend_st * bend / 12)
    phase = 2 * np.pi * np.cumsum(inst_f) / SR

    attack = smoothstep(local / 0.035)
    tau = 2.55 if i < len(ONSETS) - 1 else 6.8
    decay = np.exp(-np.maximum(local, 0) / tau)
    env = active * attack * decay

    # A warm struck spectrum. Higher partials disappear faster, so closure is
    # timbral rather than cadential: brightness ends before the pitch tail.
    tone = np.zeros(N)
    for h in range(1, 8):
        harmonic_decay = np.exp(-np.maximum(local, 0) * (h - 1) / 2.7)
        amp = 1 / (h ** 1.28)
        phase_offset = rng.uniform(0, 2 * np.pi)
        tone += amp * harmonic_decay * np.sin(h * phase + phase_offset)
    tone *= env

    # Equal-power placement; the endpoint returns to the centre.
    angle = (pan + 1) * np.pi / 4
    left += np.cos(angle) * tone
    right += np.sin(angle) * tone

# Quiet early reflections keep the object physical without supplying a coda.
for delay_s, gain, swap in [(0.071, 0.16, False), (0.113, 0.11, True),
                            (0.181, 0.075, False)]:
    d = int(delay_s * SR)
    old_l = left.copy()
    old_r = right.copy()
    if swap:
        left[d:] += gain * old_r[:-d]
        right[d:] += gain * old_l[:-d]
    else:
        left[d:] += gain * old_l[:-d]
        right[d:] += gain * old_r[:-d]

# The tail reaches its own floor. No terminal strike or cadence is added.
fade = np.ones(N)
tail = T >= 39.0
fade[tail] = np.cos(np.pi / 2 * (T[tail] - 39.0) / 5.0) ** 2
left *= fade
right *= fade

peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
left *= 0.88 / peak
right *= 0.88 / peak
stereo = np.stack([left, right], axis=1)
pcm = (stereo * 32767).astype(np.int16)

with wave.open(OUT, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(pcm.tobytes())


def rms(a, b):
    m = (T >= a) & (T < b)
    return float(np.sqrt(np.mean(stereo[m] ** 2)))


print("onsets:", ONSETS.tolist())
print("intervals:", np.diff(ONSETS).tolist())
print("frequencies:", [round(x, 2) for x in FREQS])
print("expected-but-absent next attack: 30.0 s")
print("RMS 29.8-30.2 (living tail):", f"{rms(29.8, 30.2):.6f}")
print("RMS 42.0-43.0 (finished tail):", f"{rms(42.0, 43.0):.6f}")
print("wrote", OUT)

subprocess.run([
    "ffmpeg", "-y", "-loop", "1", "-i", COVER, "-i", OUT,
    "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
    VIDEO,
], check=True)
print("wrote", VIDEO)
