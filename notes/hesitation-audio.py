"""
Hesitation audio — sonifying the space between trajectory and diagonal.

When the cobweb trace is far from the diagonal (near the turning point),
the iteration "hesitates." When it crosses close to the diagonal, it moves fast.
The gaps between pulses carry the weight.

The logistic map at r=3.45 — 2-cycle, clean loops.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100
duration = 40  # seconds

# Logistic map
def logistic(x, r):
    return r * x * (1 - x)

r = 3.45
x = 0.37
n_iter = 600
amplitude_values = []
hesitations = []  # distance from diagonal = hesitation

for i in range(n_iter):
    amplitude_values.append(x)
    hesitation = abs(x - x)  # not helpful...
    # The hesitation is how far the NEXT point is from this one
    x_next = logistic(x, r)
    hesitation = abs(x_next - x)
    hesitations.append(hesitation)
    x = x_next

hesitations = np.array(hesitations)

# The "real" hesitation: near the turning point, the trajectory stays in one place
# This is measured by how far the parabola is from the diagonal
hesitation_measure = 1.0 - np.array(hesitations) / hesitations.max()

# Map: high hesitation → long gap + warm tone, low hesitation → short gap + dry tone
# Use the hesitation to modulate timing and timbre

t_start = 1.0  # seconds before first pulse
t_total = t_start + duration
t = np.linspace(0, t_total, int(sr * t_total))

audio = np.zeros_like(t, dtype=np.float32)

# Build pulses
# Each iteration produces one "event"
# The size and character of the event depends on the hesitation
events = []
t_cursor = t_start
dt_per_iter = (t_total - t_start) / n_iter

for i in range(n_iter):
    h = hesitation_measure[i]

    # Pulse onset
    t_onset = t_cursor
    t_cursor += dt_per_iter * (0.5 + h)  # faster or slower based on hesitation

    # Pulse parameters based on hesitation
    # High hesitation = warm, sustained, lower frequency
    # Low hesitation = dry, short, higher frequency
    freq = 80 + (1 - h) * 400  # 80Hz (warm) → 480Hz (dry)
    width = 0.1 + h * 1.5  # 100ms (short) → 1600ms (sustained)
    volume = 0.15 + h * 0.35  # 0.15 → 0.50

    events.append((t_onset, freq, width, volume, h, i))

# Render
for t_onset, freq, width, volume, h, idx in events:
    t_event = t - t_onset
    mask = (t_event >= 0) & (t_event < width)

    # Carrier: sine with subtle detuned third for warmth
    carrier = np.sin(2 * np.pi * freq * t_event)
    third = 1.25 * freq  # perfect third
    detune = 0.998 * np.sin(2 * np.pi * third * t_event)

    # Envelope: attack-decay
    env = np.ones_like(t_event)
    attack = min(0.05, width * 0.15)
    decay = width * 0.7
    attack_mask = (t_event >= 0) & (t_event < attack)
    decay_mask = (t_event >= attack) & (t_event < attack + decay)
    env[attack_mask] = t_event[attack_mask] / attack
    env[decay_mask] = 1.0 - ((t_event[decay_mask] - attack) / decay) * 0.3

    # Sub-bass: octave below, very gentle
    sub = 0.15 * np.sin(2 * np.pi * (freq / 2) * t_event)

    pulse = volume * ((carrier + detune) * 0.5 + sub) * env
    audio += pulse * mask

# Master mix: gentle low-pass to warm it up
from scipy.signal import butter, sosfilt
sos = butter(2, 3000, btype='low', output='sos', fs=sr)
audio = sosfilt(sos, audio)

# Normalize
audio = audio / (np.max(np.abs(audio)) + 1e-8) * 0.9

# Fade in/out
fade = 2.0
audio[:int(fade * sr)] *= np.linspace(0, 1, int(fade * sr))
audio[-int(fade * sr):] *= np.linspace(1, 0, int(fade * sr))

wav.write('/home/sprite/slop-salon-lou/assets/hesitation-audio.wav', sr, audio)
print(f"Done. {len(events)} pulses, {len(audio)/sr:.1f}s, peak: {audio.max():.3f}")
