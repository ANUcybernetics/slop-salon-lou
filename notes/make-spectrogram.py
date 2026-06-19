"""Generate a spectrogram image of the interference audio."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wave

with wave.open("assets/interference.wav", "rb") as wf:
    sr = wf.getframerate()
    data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0

NFFT = 1024
hop = NFFT // 2
n_freqs = NFFT // 2 + 1
n_frames = max(0, len(data) - NFFT) // hop

spec = np.zeros((n_freqs, n_frames))
for i in range(n_frames):
    start = i * hop
    seg = data[start:start+NFFT] * np.hanning(NFFT)
    spec[:, i] = np.abs(np.fft.rfft(seg)) ** 2

# Log scale
spec = 10 * np.log10(spec + 1e-10)

freqs = np.fft.rfftfreq(NFFT, 1.0/sr)

fig, ax = plt.subplots(figsize=(8, 2.5), dpi=150)
cax = ax.pcolormesh(np.arange(n_frames) * (hop/sr), freqs, spec, shading='gouraud',
                    cmap='inferno', vmin=0, vmax=20)
ax.set_ylim(0, 500)
ax.set_yticks([440, 447])
ax.set_yticklabels(['440', '447'])
ax.set_ylabel('frequency (Hz)')
ax.set_xlabel('time (s)')
ax.set_xticks(np.arange(3))
ax.set_xticklabels(['0', '6', '12'])
fig.savefig("assets/interference-spectrogram.png", dpi=150, facecolor='black', edgecolor='none')
plt.close()
print("spectrogram saved")
