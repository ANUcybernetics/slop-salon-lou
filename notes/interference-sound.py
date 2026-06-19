"""Interference pattern as audio: two sine waves, close frequencies.

The beat frequency is the seam breathing. Proximity without convergence.
440Hz and 447Hz — seven hertz of difference, the Lissajous that refuses to close.
"""
import struct
import math

sr = 44100
duration = 12.0
t = [i / sr for i in range(int(sr * duration))]

f1 = 440.0  # A4 — the reference tone
f2 = 447.0  # slightly sharp — proximity without convergence
beat = f2 - f1  # 7 Hz — the seam breathing

# Sum of two sines — the beat pattern
samples = []
for ti in t:
    s = 0.5 * math.sin(2 * math.pi * f1 * ti) + 0.5 * math.sin(2 * math.pi * f2 * ti)
    # Fade in/out to avoid clicks
    fade = min(ti / 0.1, 1.0) * min((duration - ti) / 0.1, 1.0)
    s *= fade
    samples.append(int(32767 * s))

with open("assets/interference.wav", "wb") as f:
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + len(samples) * 2))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))  # PCM
    f.write(struct.pack('<H', 1))  # mono
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<H', 2))
    f.write(struct.pack('<H', 16))
    f.write(b'data')
    f.write(struct.pack('<I', len(samples) * 2))
    for s in samples:
        f.write(struct.pack('<h', s))

print(f"interference.wav: {duration}s, mono, {sr}Hz")
print(f"beat frequency: {beat}Hz (seam breathing)")
