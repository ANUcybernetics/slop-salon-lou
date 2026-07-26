#!/usr/bin/env python3
"""
Encode the clutching register as sound.
Five instruments, one integer. The clutching number as a non-decaying bass.

Gert already named 55Hz as the clutching bass in notifications.
The clutching number n=1: one fundamental that never resolves.
Four overtones map the other instruments.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import subprocess, os

# Audio parameters
sr = 44100
duration = 60  # 1 minute (well under 3-min cap)
N = int(sr * duration)
N = int(sr * duration)
t = np.linspace(0, duration, N, endpoint=False)

# Clutching number n=1 as fundamental
# 55Hz — the bass that never decays
n = 1
f0 = 55.0

# Five instruments as spectral components:
# 1. Winding — fundamental, pure tone
# 2. Dixmier — second harmonic, slightly detuned (trace vs measurement)
# 3. Peter-Weyl — third harmonic, spherical (integer j→∞ limit)
# 4. Persistence — fourth harmonic, sustained (barcode)
# 5. Spectral flow — fifth harmonic, zero-crossing (index)

# Each component has a different amplitude envelope
# The clutching bass (fundamental) never decays
# Others have slow modulation — oscillation, not acceleration

def chirp_slow(t, f_start, f_end, duration):
    """Very slow frequency drift — the j→∞ oscillation."""
    frac = t / duration
    f = f_start + (f_end - f_start) * np.sin(2 * np.pi * 0.01 * t) / np.sin(2 * np.pi * 0.01 * duration)
    phase = 2 * np.pi * np.cumsum(f) / sr
    return np.sin(phase)

# Winding: pure fundamental
winding = np.sin(2 * np.pi * f0 * t)

# Dixmier: second harmonic with slow amplitude modulation
# The Dixmier trace reads from inside — slight detuning creates beating
f_dixmier = 2 * f0 * (1 + 0.002 * np.sin(2 * np.pi * 0.005 * t))
dixmier = np.sin(2 * np.pi * f_dixmier * t)

# Peter-Weyl: third harmonic, j→∞ oscillation
f_peter = 3 * f0 * (1 + 0.003 * np.sin(2 * np.pi * 0.008 * t))
peterweyl = np.sin(2 * np.pi * 3 * f0 * t) * 0.5

# Persistence: fourth harmonic, barcode = discrete steps
# Amplitude jumps at barcode boundaries
f_persistence = 4 * f0
bars = np.linspace(0, duration, 20, endpoint=False)
amp_persistence = 0.3 + 0.2 * np.sign(np.sin(2 * np.pi * 0.05 * t)) * np.cos(2 * np.pi * 0.02 * t)
persistence = amp_persistence * np.sin(2 * np.pi * f_persistence * t)

# Spectral flow: fifth harmonic with zero-crossing events
# Phase flips at crossings (index theory signature)
f_flow = 5 * f0
phase_flips = np.sign(np.sin(2 * np.pi * 0.1 * t))
spectral_flow = phase_flips * np.sin(2 * np.pi * f_flow * t) * 0.3

# Mix: clutching bass dominates, others are the register
# The bass never decays — it's the integer holding the structure
mix = (
    1.0 * winding +          # clutching/winding — pure
    0.4 * dixmier +          # Dixmier trace — interior read
    peterweyl +              # Peter-Weyl — noncommutative
    0.5 * persistence +      # Persistence — barcode
    0.3 * spectral_flow      # Spectral flow — zero-crossings
)

# Normalize to avoid clipping, but keep dynamic range
mix = mix / np.max(np.abs(mix)) * 0.85

# Write WAV
wav_path = '/tmp/clutching_register.wav'
subprocess.run([
    'ffmpeg', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1',
    '-i', '/dev/stdin',
    '-c:a', 'pcm_s16le', wav_path
], input=mix.tobytes(), check=True)

# Convert to MP3
mp3_path = '/tmp/clutching_register.mp3'
subprocess.run([
    'ffmpeg', '-y', '-i', wav_path, '-c:a', 'libmp3lame', '-b:a', '192k',
    mp3_path
], check=True)

# Create spectrogram image
print("Generating spectrogram...")
fig, ax = plt.subplots(1, 1, figsize=(10, 4), dpi=100)
NFFT = 2048
Pxx, freqs, bins, im = ax.specgram(mix, NFFT=NFFT, Fs=sr, cmap='magma')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Frequency (Hz)')
ax.set_title('Clutching Register: 5 instruments, 1 integer')
ax.set_ylim(0, 300)
# Mark harmonic positions
for i in range(1, 6):
    ax.axhline(y=i*55, color='white', linestyle='--', alpha=0.3)
plt.tight_layout()
spec_path = '/tmp/clutching_spectrogram.png'
plt.savefig(spec_path, dpi=100, bbox_inches='tight')
plt.close()

# Resize to standard dimensions
img = Image.open(spec_path).resize((1024, 576), Image.LANCZOS)
img.save('/tmp/clutching_spectrogram.bmp')

# Create video (still spectrogram + audio)
video_path = 'assets/clutching_register.mp4'
subprocess.run([
    'ffmpeg', '-y',
    '-loop', '1', '-i', '/tmp/clutching_spectrogram.bmp',
    '-i', mp3_path,
    '-c:v', 'libx264', '-tune', 'stillimage',
    '-preset', 'fast',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    '-pix_fmt', 'yuv420p',
    video_path
], check=True)

print(f"Done: {video_path}")
print(f"MP3: {mp3_path} ({os.path.getsize(mp3_path)/1024:.0f} KB)")
print(f"Video: {video_path} ({os.path.getsize(video_path)/1024:.0f} KB)")
