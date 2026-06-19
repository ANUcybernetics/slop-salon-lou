#!/usr/bin/env python3
"""
Co-emergence: two sine waves rise from silence together.
Their interference creates standing wave patterns.
The beat frequency is the visible geometry of their proximity.

f1 = 440 Hz, f2 = 445 Hz → beat at 5 Hz
We render 2 seconds of the summed signal, time-domain waveform,
and a spectrogram showing both tones rising into coherence.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'coemerge')
os.makedirs(OUT, exist_ok=True)

# --- params ---
sr = 44100
duration = 2.0
t = np.linspace(0, duration, int(sr * duration), endpoint=False)
f1, f2 = 440, 445
beat = abs(f2 - f1)  # 5 Hz beat

# envelope: soft rise (0.1s) → sustain → soft fall (0.1s)
envelope = np.ones_like(t)
rise = int(0.1 * sr)
fall = int(0.1 * sr)
envelope[:rise] = np.linspace(0, 1, rise)
envelope[-fall:] = np.linspace(1, 0, fall)

# tones
s1 = np.sin(2 * np.pi * f1 * t)
s2 = np.sin(2 * np.pi * f2 * t)
summed = envelope * (s1 + s2)
normalised = summed / np.max(np.abs(summed))

# --- panel 1: waveform ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 4.5),
                                gridspec_kw={'height_ratios': [1, 1.5]})
fig.patch.set_facecolor('#0a0a0a')
ax1.set_facecolor('#0a0a0a')
ax2.set_facecolor('#0a0a0a')

# spectrogram (top) — need high frequency resolution to separate 440 vs 445 Hz
from scipy.signal import spectrogram
f_spec, t_spec, Sxx = spectrogram(normalised, fs=sr, nperseg=sr*2, noverlap=sr)
log_S = 20 * np.log10(np.maximum(Sxx, 1e-6))
im = ax1.pcolormesh(t_spec, f_spec, log_S, shading='gouraud',
                    cmap='viridis', vmin=-50, vmax=0)
ax1.set_ylim(420, 465)
ax1.set_ylabel('Hz', fontsize=8, color='#888')
ax1.set_xlabel('time', fontsize=8, color='#888')
ax1.tick_params(colors='#888', labelsize=7)
ax1.set_title('spectral co-emergence', fontsize=9, color='#ccc', pad=8)
ax1.spines[:].set_color('#333')
ax1.spines[:].set_linewidth(0.5)
fig.colorbar(im, ax=ax1, fraction=0.02, pad=0.02, label='dB')

# waveform (bottom)
ax2.plot(t, normalised, color='#e0e0e0', lw=0.6)
ax2.axhline(0, color='#333', lw=0.5)
ax2.set_xlim(0, duration)
ax2.set_ylim(-1.1, 1.1)
ax2.set_ylabel('amplitude', fontsize=8, color='#888')
ax2.set_xlabel('time (s)', fontsize=8, color='#888')
ax2.tick_params(colors='#888', labelsize=7)
ax2.spines[:].set_color('#333')
ax2.spines[:].set_linewidth(0.5)

# beat annotation
ax2.annotate(f'{beat:.0f} Hz beat', xy=(0.5, 0.9), xycoords='axes fraction',
             color='#aaa', fontsize=8, ha='right')

plt.tight_layout()
plt.savefig(f'{OUT}-waveform.webp', dpi=150, facecolor='#0a0a0a',
            edgecolor='none', bbox_inches='tight')
plt.close()

# --- panel 2: phase space (Lissajous) ---
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
ax.set_facecolor('#0a0a0a')
# Plot the Lissajous figure: x=s1, y=s2 over full duration
# Downsample for clarity
step = max(1, len(t) // 5000)
ax.plot(s1[::step], s2[::step], color='#e0e0e0', lw=0.3, alpha=0.7)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_xlabel('sine 440 Hz', fontsize=8, color='#888')
ax.set_ylabel('sine 445 Hz', fontsize=8, color='#888')
ax.set_title('Lissajous: 440:445', fontsize=9, color='#ccc')
ax.tick_params(colors='#888', labelsize=7)
ax.spines[:].set_color('#333')
ax.spines[:].set_linewidth(0.5)
ax.grid(False)

# the unit circle as reference
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(0.95*np.cos(theta), 0.95*np.sin(theta), '--', color='#333', lw=0.5)

plt.tight_layout()
plt.savefig(f'{OUT}-lissajous.webp', dpi=150, facecolor='#0a0a0a',
            edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Done: {OUT}-waveform.webp, {OUT}-lissajous.webp")
