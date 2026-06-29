#!/usr/bin/env python3
"""Generate audio that sonifies nilpotent decay:
each step loses a dimension, amplitude drops systematically."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Audio: diminishing harmonic decay ---
sr = 44100
duration = 8
t = np.linspace(0, duration, int(sr * duration))

f1, f2, f3 = 220, 330, 440  # harmonic series
step_duration = duration / 3.0
signal = np.zeros_like(t)

for step in range(3):
    mask = (t >= step * step_duration) & (t < (step + 1) * step_duration)
    amplitude = 3 - step
    fade = np.ones_like(t[mask])
    fade_len = int(0.15 * sr)
    fade[:fade_len] = np.linspace(0, 1, fade_len)
    fade[-fade_len:] = np.linspace(1, 0, fade_len)
    if amplitude >= 3:
        signal[mask] += amplitude * 0.12 * fade * np.sin(2 * np.pi * f1 * t[mask])
        signal[mask] += amplitude * 0.08 * fade * np.sin(2 * np.pi * f2 * t[mask])
        signal[mask] += amplitude * 0.05 * fade * np.sin(2 * np.pi * f3 * t[mask])
    elif amplitude >= 2:
        signal[mask] += amplitude * 0.12 * fade * np.sin(2 * np.pi * f1 * t[mask])
        signal[mask] += amplitude * 0.08 * fade * np.sin(2 * np.pi * f2 * t[mask])
    elif amplitude >= 1:
        signal[mask] += amplitude * 0.12 * fade * np.sin(2 * np.pi * f1 * t[mask])

signal /= np.max(np.abs(signal)) * 1.1

wav_path = '/tmp/nilpotent-decay.wav'
from scipy.io import wavfile
wavfile.write(wav_path, sr, (signal * 32767).astype(np.int16))
print(f"WAV: {wav_path}")

# --- Spectrogram via short-time FFT ---
nperseg = 1024
no_overlap = nperseg // 2
nfft = 2048

# Compute spectrogram
from scipy.signal import spectrogram as scipy_spectrogram
f_spec, t_spec, Sxx = scipy_spectrogram(signal, fs=sr, nperseg=nperseg, noverlap=no_overlap, nfft=nfft)

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
ax.set_facecolor('#0a0806')
fig.patch.set_facecolor('#0a0806')

pcm = ax.pcolormesh(t_spec, f_spec/1000, 20*np.log10(Sxx + 1e-10),
                    shading='gouraud', cmap='magma')
fig.colorbar(pcm, ax=ax, orientation='vertical', ticks=[],
             label='amplitude')

for i in range(1, 3):
    ax.axvline(x=i*step_duration, color='#d4a020', alpha=0.3, linewidth=0.8)

ax.set_xlabel('time (s)', color='#a08040', fontsize=11)
ax.set_ylabel('frequency (kHz)', color='#a08040', fontsize=11)
ax.tick_params(colors='#a08040')
ax.set_ylim(0, 2.5)

ax.text(step_duration*0.5, 2.3, 'dim=3', color='#d4a020', fontsize=10, ha='center', alpha=0.7)
ax.text(step_duration*1.5, 2.3, 'dim=2', color='#d4a020', fontsize=10, ha='center', alpha=0.5)
ax.text(step_duration*2.5, 2.3, 'dim=1', color='#d4a020', fontsize=10, ha='center', alpha=0.3)

plt.tight_layout()
img_path = '/tmp/nilpotent-spectrogram.webp'
plt.savefig(img_path, dpi=100, facecolor='#0a0806', edgecolor='none')
print(f"IMG: {img_path}")
