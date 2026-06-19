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
hop = NFFT // 4
n_freqs = NFFT // 2 + 1
n_frames = max(0, len(data) - NFFT) // hop

spec = np.zeros((n_freqs, n_frames))
for i in range(n_frames):
    start = i * hop
    seg = data[start:start+NFFT] * np.hanning(NFFT)
    spec[:, i] = np.abs(np.fft.rfft(seg)) ** 2

spec = 10 * np.log10(spec + 1e-10)
freqs = np.fft.rfftfreq(NFFT, 1.0/sr)

fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
cax = ax.pcolormesh(np.arange(n_frames) * (hop/sr), freqs, spec, shading='gouraud',
                    cmap='inferno', vmin=0, vmax=20)
ax.set_ylim(0, 600)
ax.set_yticks([440, 447])
ax.set_yticklabels(['440', '447'])
ax.set_ylabel('frequency (Hz)', fontsize=12)
ax.set_xlabel('time (s)', fontsize=12)
ax.set_xticks(np.linspace(0, n_frames*(hop/sr), 4))
ax.set_xticklabels(['0', '4', '8', '12'])
fig.savefig("assets/interference-spectrogram.png", dpi=150, facecolor='black', edgecolor='none',
            bbox_inches='tight', pad_inches=0.1)
plt.close()
print("spectrogram saved")
