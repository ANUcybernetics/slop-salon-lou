#!/usr/bin/env python3
"""
Holonomy as audio + cover.

Parallel transport around a spherical triangle: vector returns rotated.
The rotation angle becomes a frequency sweep over the tone's duration.

The cover is a spectrogram with a golden spiral — the cobweb of iterations
that accumulate into the holonomy.
"""
import numpy as np
import wave
import struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Audio params
SAMPLE_RATE = 44100
DURATION = 8.0
BASE_FREQ = 220  # A3

# Generate audio
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION))
holonomy_t = np.linspace(0, 1, len(t))

# Quadratic holonomy: slow accumulation, then acceleration
holonomy_angle = np.pi/2 * holonomy_t**2

# Frequency sweep encodes the rotation
freq_sweep = BASE_FREQ + (holonomy_angle / (2 * np.pi)) * 110

# Phase = integral of frequency
phase = np.cumsum(2 * np.pi * freq_sweep / SAMPLE_RATE)
carrier = np.sin(phase)

# Fade in/out to avoid clicks
fade = np.ones(len(t))
fade[:500] = np.linspace(0, 1, 500)
fade[-500:] = np.linspace(1, 0, 500)
carrier *= fade

# Write WAV
output = './assets/holonomy.wav'
with wave.open(output, 'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    samples = (carrier * 32767).astype(np.int16)
    w.writeframes(samples.tobytes())
print(f"Wrote {output}: {DURATION}s @ 44100Hz")

# Cover: spectrogram with golden spiral (cobweb)
fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
ax.specgram(carrier, NFFT=512, Fs=SAMPLE_RATE, cmap='viridis', mode='magnitude')

# Golden spiral overlay — the cobweb of Christoffel iterations
theta = np.linspace(0, 4*np.pi, 500)
r = np.exp(theta * np.log(0.02))  # growth factor
x = r * np.cos(theta)
y = r * np.sin(theta)

# Scale to axes
ax.plot(x * 0.5 + 0.5, y * 0.5 + 0.5, 'gold', alpha=0.6, linewidth=1.5, transform=ax.transAxes)

ax.set_xlabel('time (s)', fontsize=8, color='white')
ax.set_ylabel('frequency (Hz)', fontsize=8, color='white')
ax.tick_params(colors='white', labelsize=7)
for spine in ax.spines.values():
    spine.set_color('white')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

plt.tight_layout()
plt.savefig('./assets/holonomy-cover.png', dpi=100, facecolor='black', edgecolor='none')
print("Wrote holonomy-cover.png")
