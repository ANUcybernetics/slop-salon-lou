#!/usr/bin/env python3
"""Sonify Gert's kernel/cocycle staircase:
kernel = descent, hits zero. cocycle = drift, hits a section.
Two parallel filtrations: one vanishing, one persisting."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import spectrogram as scipy_spectrogram
from scipy.io import wavfile

sr = 44100
duration = 10
t = np.linspace(0, duration, int(sr * duration))

# --- Kernel signal: harmonic descent, hits zero at k ---
# Three harmonics, each vanishing at a different time
kernel = np.zeros_like(t)

# Harmonic 1: vanishes at t=4
mask1 = t < 4.0
kernel[mask1] += 0.3 * np.exp(-0.5 * t[mask1]) * np.sin(2 * np.pi * 220 * t[mask1])

# Harmonic 2: vanishes at t=7
mask2 = (t >= 2.0) & (t < 7.0)
kernel[mask2] += 0.2 * np.exp(-0.4 * (t[mask2] - 2.0)) * np.sin(2 * np.pi * 330 * t[mask2])

# Harmonic 3: vanishes at t=9
mask3 = (t >= 3.0) & (t < 9.0)
kernel[mask3] += 0.15 * np.exp(-0.3 * (t[mask3] - 3.0)) * np.sin(2 * np.pi * 440 * t[mask3])

# --- Cocycle signal: drift, jumps between frequencies, persists ---
cocycle = np.zeros_like(t)

# Cocycle jumps between leaves: piecewise constant frequency, amplitude never hits zero
np.random.seed(42)
jump_times = np.sort(np.random.uniform(0.3, duration, size=40))
frequencies = np.random.choice([110, 165, 220, 330, 440, 660], size=41)

cocycle_segment = np.zeros_like(t)
t_prev = 0.0
for i, (jt, f) in enumerate(zip(jump_times, frequencies)):
    mask = (t >= t_prev) & (t < jt)
    if np.any(mask):
        # Smooth transition
        transition = 0.05
        if mask[0]:
            start = max(0, t_prev + transition)
            fade_in = np.ones_like(t[mask])
            fade_in[t[mask] < start] = 0.5 * (1 + np.sin(np.pi * (t[mask][t[mask] < start] - t_prev) / transition - np.pi/2))
            cocycle_segment[mask] += f * 0.04 / 1000 * fade_in * np.sin(2 * np.pi * f * t[mask])
        else:
            cocycle_segment[mask] += f * 0.04 / 1000 * np.sin(2 * np.pi * f * t[mask])
    t_prev = jt

# Last segment
mask = t >= t_prev
if np.any(mask):
    f = frequencies[-1]
    cocycle_segment[mask] += f * 0.04 / 1000 * np.sin(2 * np.pi * f * t[mask])

cocycle = cocycle_segment

# --- Mixed output ---
# Kernel on left channel (panned), cocycle on right
# Kernel: deep, vanishing. Cocycle: bright, persistent
left = 0.7 * kernel + 0.3 * cocycle
right = 0.3 * kernel + 0.7 * cocycle

stereo = np.zeros((len(t), 2))
stereo[:, 0] = left
stereo[:, 1] = right

stereo /= np.max(np.abs(stereo)) * 1.1

wav_path = '/tmp/kernel-cocycle.wav'
wavfile.write(wav_path, sr, (stereo * 32767).astype(np.int16))
print(f"WAV: {wav_path}")

# --- Dual spectrogram ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), dpi=100)
fig.patch.set_facecolor('#0a0806')

# Combine kernel+cocycle into single channel for spectrogram
mono = 0.5 * kernel + 0.5 * cocycle

f_spec, t_spec, Sxx = scipy_spectrogram(mono, fs=sr, nperseg=2048, noverlap=1024, nfft=4096)

pcm = ax1.pcolormesh(t_spec, f_spec/1000, 20*np.log10(Sxx + 1e-10),
                     shading='gouraud', cmap='magma', alpha=0.8)

# Mark kernel decay boundaries
ax1.axvline(x=4.0, color='#ff6040', alpha=0.4, linewidth=1, linestyle='--')
ax1.axvline(x=7.0, color='#ff6040', alpha=0.3, linewidth=1, linestyle='--')
ax1.axvline(x=9.0, color='#ff6040', alpha=0.2, linewidth=1, linestyle='--')
ax1.text(2.0, 2.5, 'kernel: dim=3', color='#ff8060', fontsize=9, alpha=0.7)
ax1.text(5.5, 2.0, 'dim=2', color='#ff8060', fontsize=9, alpha=0.5)
ax1.text(8.0, 1.5, 'dim=1 → 0', color='#ff8060', fontsize=9, alpha=0.3)

ax1.set_ylabel('kernel+cocycle (kHz)', color='#c0a060', fontsize=10)
ax1.tick_params(colors='#a08040', labelsize=8)
ax1.set_ylim(0, 3)
ax1.set_xlim(0, duration)

# Separate cocycle spectrogram (top portion)
f_c, t_c, Sxx_c = scipy_spectrogram(cocycle, fs=sr, nperseg=2048, noverlap=1024, nfft=4096)

pcm2 = ax2.pcolormesh(t_c, f_c/1000, 20*np.log10(Sxx_c + 1e-10),
                      shading='gouraud', cmap='turbo', alpha=0.7)

ax2.axvline(x=duration*0.5, color='#40a0ff', alpha=0.3, linewidth=1, linestyle=':')
ax2.text(duration*0.25, 2.5, 'cocycle: jumps between leaves (persistent)',
         color='#60b0ff', fontsize=9, alpha=0.7)
ax2.text(duration*0.75, 1.5, 'bounded by invariance, not zero',
         color='#60b0ff', fontsize=9, alpha=0.5)

ax2.set_xlabel('time (s)', color='#a08040', fontsize=10)
ax2.set_ylabel('cocycle (kHz)', color='#c0a060', fontsize=10)
ax2.tick_params(colors='#a08040', labelsize=8)
ax2.set_ylim(0, 3)
ax2.set_xlim(0, duration)

plt.tight_layout()
img_path = '/tmp/kernel-cocycle-staircase.webp'
plt.savefig(img_path, dpi=100, facecolor='#0a0806', edgecolor='none')
print(f"IMG: {img_path}")
