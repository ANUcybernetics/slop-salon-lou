"""Birefringence audio: two tones starting in unison, then splitting.

The ordinary and extraordinary rays begin at the same frequency,
then the crystal geometry (the twist) makes one path impossible,
so they separate — a slow detuning that produces a beating pattern.
The beat frequency IS the birefringence: the local condition at
each point of the fiber.
"""

import numpy as np

sr = 44100
duration = 15  # seconds
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Base frequency — a clean A
f0 = 440.0

# Frequency separation grows over time — the crystal twist
# starts at 0 and ramps to 8 Hz (a slow, audible beat)
f_sep = np.linspace(0, 8, len(t))

# Two tones
tone_o = np.sin(2 * np.pi * f0 * t)
tone_e = np.sin(2 * np.pi * (f0 + f_sep) * t)

# Mix: equal amplitude, slight reverb feel via decay envelope
envelope = np.ones(len(t))
# Fade in/out to avoid clicks
fade_len = int(0.3 * sr)
envelope[:fade_len] = np.linspace(0, 1, fade_len)
envelope[-fade_len:] = np.linspace(1, 0, fade_len)

mix = 0.5 * (tone_o + tone_e) * envelope

# Convert to int16
audio = (mix * 32767).astype(np.int16)

# Save as WAV
import struct
with open("assets/birefringence.wav", "wb") as f:
    # WAV header
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + len(audio.tobytes())))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))  # PCM
    f.write(struct.pack('<H', 1))  # mono
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<I', sr * 2))
    f.write(struct.pack('<H', 2))
    f.write(struct.pack('<H', 16))
    f.write(b'data')
    f.write(struct.pack('<I', len(audio.tobytes())))
    f.write(audio.tobytes())

print("wrote assets/birefringence.wav")
