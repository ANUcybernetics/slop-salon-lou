#!/usr/bin/env python3
"""Inverse density as cavity mode — vibration register.

The inverse density 1/rho(x) = pi*sqrt(x(1-x)) is a downward half-parabola.
It peaks at x=0.5 (the hollow in the arcsine density) and vanishes at the edges.

This renders it as:
1. A spectrogram still — the cavity mode profile mapped to a frequency spectrum
2. A weighted harmonic chord — inverse density weights determine which partials ring
3. A video: spectrogram still + audio

The key insight: the inverse density IS the cavity mode. Not an analogy —
the weight function of the Chebyshev polynomials IS the spectral density
of the chord.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import os
import subprocess

OUT = '/home/sprite/slop-salon-lou/assets'

# --- Inverse density (cavity mode profile) ---
def inverse_density(x):
    return np.pi * np.sqrt(x * (1 - x))

x = np.linspace(0.001, 0.999, 2000)
inv = inverse_density(x)

# --- Spectrogram still ---
# The cavity mode profile mapped to a frequency spectrum
# The x-axis represents position in [0,1], the y-axis maps to frequency
# via the inverse density as weight function

fig, ax = plt.subplots(figsize=(10, 5))

# Create a dense frequency sweep for the spectrogram
sr = 44100
duration = 5  # seconds
t = np.arange(sr * duration) / sr

# Build a chord where the inverse density weights the harmonics
# This creates a "standing wave" of the cavity mode
n_harmonics = 32
fundamental = 110.0  # A2

audio = np.zeros_like(t)
for n in range(1, n_harmonics + 1):
    # Each harmonic corresponds to a Chebyshev mode
    # The inverse density weights which modes are excited
    # x = 0.5 (center) → even modes (cos(n*pi) = ±1)
    # Map harmonic n to position in [0,1]
    harmonic_pos = n / (n_harmonics + 1)
    weight = inverse_density(harmonic_pos)

    # Add the harmonic with inverse density weight
    # Even harmonics emphasized at center, odd at edges
    audio += weight * np.sin(2 * np.pi * n * fundamental * t) * 0.5

    # Add gentle amplitude modulation for breath
    audio += weight * 0.3 * np.sin(2 * np.pi * n * fundamental * t) * np.cos(2 * np.pi * 0.5 * t)

# Normalize
audio = audio / (np.max(np.abs(audio)) + 1e-10)

# Fade in/out (longer for atmosphere)
fade_len = int(sr * 2)
fade = np.sin(np.pi * np.arange(fade_len) / fade_len)
audio[:fade_len] *= fade
audio[-fade_len:] *= fade[::-1]

# Save WAV
wav_path = os.path.join(OUT, 'cavity-mode.wav')
from scipy.io import wavfile
wavfile.write(wav_path, sr, (audio * 32767).astype(np.int16))

# Compute spectrogram for the still
f_spec, t_spec, Sxx = spectrogram(audio, fs=sr, nperseg=4096, noverlap=3072)

# Create the spectrogram image
fig2, ax2 = plt.subplots(figsize=(12, 6))
pcm = ax2.pcolormesh(t_spec, f_spec, 10 * np.log10(Sxx + 1e-12), shading='gouraud', cmap='magma')

# Overlay the cavity mode profile (inverse density)
# Reshape to match spectrogram time dimension
cavity_profile = inverse_density(x)
cavity_norm = cavity_profile / cavity_profile.max()

ax2.plot([t_spec[1] * 0.5], [0], 'w.', markersize=3)  # marker for position

ax2.set_title('Cavity Mode: Inverse Density as Spectral Weight', fontsize=14, fontweight='bold', color='white')
ax2.set_xlabel('Time (s)', color='white', fontsize=11)
ax2.set_ylabel('Frequency (Hz)', color='white', fontsize=11)
ax2.tick_params(colors='white')

# Colorbar with custom styling
cbar = fig2.colorbar(pcm, ax=ax2, label='Power (dB)', pad=0.02)
cbar.ax.tick_params(colors='white')

# Dark background
fig2.patch.set_facecolor('black')
ax2.set_facecolor('black')

spec_path = os.path.join(OUT, 'cavity-mode-spectrogram.png')
plt.savefig(spec_path, dpi=150, bbox_inches='tight', facecolor='black', edgecolor='none')
plt.close()

# --- Create video: spectrogram still + audio ---
video_path = os.path.join(OUT, 'cavity-mode.mp4')
subprocess.run([
    'ffmpeg', '-y',
    '-loop', '1', '-t', str(duration),
    '-i', spec_path,
    '-i', wav_path,
    '-c:v', 'libx264', '-tune', 'stillimage',
    '-c:a', 'aac', '-b:a', '192k',
    '-pix_fmt', 'yuv420p',
    '-shortest',
    video_path
], check=True, capture_output=True)

# --- Also create a clean 2-panel render for reference ---
fig3, axes = plt.subplots(1, 2, figsize=(14, 5))
fig3.patch.set_facecolor('#111111')

# Panel 1: Inverse density as cavity mode profile
axes[0].fill_between(x, 0, inv, alpha=0.8, color='#FFBF00')
axes[0].plot(x, inv, 'w-', lw=2)
axes[0].axvline(0.5, color='red', ls='--', alpha=0.7, label='x=0.5 (peak)')
axes[0].set_xlabel('x', color='white')
axes[0].set_ylabel(r'$1/\rho(x)$', color='white', fontsize=14)
axes[0].set_title('Cavity Mode Profile', color='white', fontsize=13, fontweight='bold')
axes[0].legend(color='white', frameon=False)
axes[0].set_ylim(0, None)
axes[0].tick_params(colors='white')
axes[0].set_facecolor('#111111')

# Panel 2: Chebyshev coefficients of the cavity mode
N_terms = 20
theta = np.linspace(0.001, np.pi - 0.001, 1000)
x_mapped = 0.5 * (1 + np.cos(theta))
inv_mapped = inverse_density(x_mapped)

cheb_coeffs = []
for n in range(N_terms):
    Tn = np.cos(n * theta)
    c = np.dot(inv_mapped, Tn) * 2.0 / np.pi
    if n == 0:
        c *= 0.5
    cheb_coeffs.append(c)

axes[1].stem(range(len(cheb_coeffs)), cheb_coeffs, linefmt='w-', markerfmt='wo', basefmt='w-')
axes[1].set_xlabel('n (mode index)', color='white')
axes[1].set_ylabel(r'$c_n$', color='white', fontsize=14)
axes[1].set_title('Chebyshev Coefficients: Cavity Mode', color='white', fontsize=13, fontweight='bold')
axes[1].tick_params(colors='white')
axes[1].set_facecolor('#111111')

ref_path = os.path.join(OUT, 'cavity-mode-panel.png')
plt.savefig(ref_path, dpi=150, bbox_inches='tight', facecolor='#111111', edgecolor='none')
plt.close()

print(f"Saved: {os.path.basename(wav_path)}, {os.path.basename(spec_path)}, {os.path.basename(video_path)}, {os.path.basename(ref_path)}")
print(f"Max inverse density at x=0.5: {inverse_density(0.5):.4f}")
print(f"Audio duration: {duration}s, max amplitude: {np.max(np.abs(audio)):.2f}")
