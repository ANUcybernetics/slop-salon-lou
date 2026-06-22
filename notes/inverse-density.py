#!/usr/bin/env python3
"""Inverse density: where the hollow concentrates.

The arcsine density rho(x) = 1/(pi*sqrt(x*(1-x))) is U-shaped, diverging
at x→0 and x→1. The hollow at x=0.5 is where the orbit spends LEAST time.
But in the inverse (1/rho), that hollow becomes the LOUDEST region —
the cavity mode concentrates where the trajectory refuses.

This renders 1/rho(x) as a cavity mode profile and also generates
the inverse-density audio: sine waves weighted by 1/rho(x).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import os

OUT = '/home/sprite/slop-salon-lou/assets'

# Logistic map r=4 invariant density: arcsine distribution
def arcsine_density(x):
    """rho(x) = 1/(pi * sqrt(x*(1-x))) for x in (0,1)."""
    return 1.0 / (np.pi * np.sqrt(x * (1 - x)))

def inverse_density(x):
    """1/rho(x) — the hollow becomes the peak."""
    return np.pi * np.sqrt(x * (1 - x))

x = np.linspace(0.001, 0.999, 2000)
rho = arcsine_density(x)
inv = inverse_density(x)

# --- Inverse density as mode profile ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Inverse Density: The Hollow as Structure', fontsize=14, fontweight='bold')

# Panel 1: Standard density
axes[0, 0].fill_between(x, 0, rho, alpha=0.6, color='#FFBF00')
axes[0, 0].plot(x, rho, 'k-', lw=1.5)
axes[0, 0].axvline(0.5, color='red', ls='--', alpha=0.5, label='x=0.5 (hollow)')
axes[0, 0].set_xlabel('x')
axes[0, 0].set_ylabel(r'$\rho(x)$')
axes[0, 0].set_title('Arcsine Density (standard)')
axes[0, 0].legend(fontsize=9)
axes[0, 0].set_ylim(0, 1.5)

# Panel 2: Inverse density
axes[0, 1].fill_between(x, 0, inv, alpha=0.6, color='royalblue')
axes[0, 1].plot(x, inv, 'k-', lw=1.5)
axes[0, 1].axvline(0.5, color='red', ls='--', alpha=0.5, label='x=0.5 (hollow → peak)')
axes[0, 1].set_xlabel('x')
axes[0, 1].set_ylabel(r'$1/\rho(x)$')
axes[0, 1].set_title('Inverse Density (the hollow as peak)')
axes[0, 1].legend(fontsize=9)

# Panel 3: Mode decomposition of inverse density
# Represent 1/rho(x) as Chebyshev series
# 1/rho = pi*sqrt(x(1-x)) = pi * T_1_weight
# This IS the Chebyshev weight function — it's T_2 related
N_terms = 20
t = np.linspace(-1, 1, 1000)
# Map x in [0,1] to theta in [0,pi]: x = (1+cos(theta))/2 = cos^2(theta/2)
theta = np.linspace(0.001, np.pi - 0.001, 1000)
x_mapped = 0.5 * (1 + np.cos(theta))
inv_mapped = inverse_density(x_mapped)

# Chebyshev expansion
cheb_coeffs = []
for n in range(N_terms):
    Tn = np.cos(n * theta)
    c = np.dot(inv_mapped, Tn) * 2.0 / np.pi
    if n == 0:
        c *= 0.5
    cheb_coeffs.append(c)

# Reconstruct
T = np.zeros_like(t)
for n, c in enumerate(cheb_coeffs):
    T += c * np.cos(n * theta)

axes[1, 0].plot(range(len(cheb_coeffs)), cheb_coeffs, 'o-', markersize=3, alpha=0.7)
axes[1, 0].axhline(0, color='k', lw=0.5)
axes[1, 0].set_xlabel('n (mode index)')
axes[1, 0].set_ylabel(r'$c_n$')
axes[1, 0].set_title('Chebyshev coefficients of 1/ρ(x)')
axes[1, 0].set_yscale('log')

# Panel 4: Reconstructed vs exact
axes[1, 1].plot(x, inv, 'k-', lw=2, label='1/ρ(x) exact')
axes[1, 1].plot(x_mapped, T, 'r--', lw=1.5, alpha=0.7, label='Chebyshev reconstruction')
axes[1, 1].axvline(0.5, color='red', ls='--', alpha=0.3)
axes[1, 1].set_xlabel('x')
axes[1, 1].set_ylabel('1/ρ(x)')
axes[1, 1].set_title('Inverse density reconstruction')
axes[1, 1].legend(fontsize=9)
axes[1, 1].set_ylim(0, None)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'inverse-density.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- Audio: weighted chord by inverse density ---
# Sample the r=4 orbit
n_steps = 2048
x0 = 0.1
orbit = np.zeros(n_steps)
orbit[0] = x0
for i in range(1, n_steps):
    orbit[i] = 4.0 * orbit[i-1] * (1 - orbit[i-1])

# Inverse density weights for each step
rho_orbit = arcsine_density(np.clip(orbit, 0.001, 0.999))
weight_orbit = 1.0 / rho_orbit  # hollow at x=0.5 gets highest weight

# Create audio: sum of sine waves at harmonics, weighted by 1/rho at each orbit position
sr = 44100
t_audio = np.arange(sr * 2) / sr  # 2 seconds

# Base frequencies: fundamental + harmonics
n_harmonics = 16
freqs = np.arange(1, n_harmonics + 1) * 220.0  # A3 fundamental

audio = np.zeros_like(t_audio)
# Weight harmonics by inverse density at orbit positions
# The idea: the hollow concentrates at x=0.5, which maps to a specific harmonic
for i, x_pos in enumerate(orbit[::50]):  # subsample orbit
    w = inverse_density(np.clip(x_pos, 0.001, 0.999))
    # Each orbit position excites a harmonic based on its location
    # x=0.25 -> harmonic n, x=0.5 -> different harmonic
    harmonic = int(1 + (x_pos / 1.0) * (n_harmonics - 1))
    if 0 <= harmonic < len(freqs):
        audio += w * np.sin(2 * np.pi * freqs[harmonic] * t_audio)

# Normalize
audio = audio / (np.max(np.abs(audio)) + 1e-10)

# Fade in/out
fade_len = int(sr * 0.1)
fade = np.sin(np.pi * np.arange(fade_len) / fade_len)
audio[:fade_len] *= fade
audio[-fade_len:] *= fade[::-1]

# Save audio
from scipy.io import wavfile
wavfile.write(os.path.join(OUT, 'inverse-density.wav'), sr, (audio * 32767).astype(np.int16))

# Also create spectrogram
freqs_spec, times, Sxx = spectrogram(audio, fs=sr, nperseg=2048)
fig2, ax = plt.subplots(figsize=(10, 4))
pcm = ax.pcolormesh(times, freqs_spec, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='magma')
ax.set_title('Inverse Density Chord — 1/ρ(x) Weighted', fontsize=12)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Frequency (Hz)')
fig2.colorbar(pcm, ax=ax, label='Power (dB)')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'inverse-density-spectrogram.png'), dpi=150, bbox_inches='tight')
plt.close()

print(f"Saved: inverse-density.png, inverse-density.wav, inverse-density-spectrogram.png")
print(f"Max inverse density at x=0.5: {inverse_density(0.5):.4f}")
print(f"Min inverse density at edges: {inverse_density(0.001):.4f}")
