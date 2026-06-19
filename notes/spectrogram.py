"""Generate a spectrogram of the interference pattern for visual accompaniment."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wave
import struct

# Read the WAV
with wave.open("assets/interference.wav", "rb") as wf:
    sr = wf.getframerate()
    nchannels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0

plt.figure(figsize=(8, 2.5), dpi=150)
nperseg = 2048
freqs, times, spec = plt.mlab.specgram(data, NFFT=2048, Fs=sr,
                                        noverlap=2048-1, cmap='inferno')

plt.pcolormesh(times, freqs, 10*np.log10(spec + 1e-10), shading='gouraud', cmap='inferno')
plt.yticks([440, 447], ['440', '447'])
plt.ylabel('frequency (Hz)')
plt.xlabel('time (s)')
plt.ylim(0, 500)
plt.tight_layout(pad=0.3)
plt.savefig("assets/interference-spectrogram.png", dpi=150, facecolor='black', edgecolor='none')
plt.close()
print("spectrogram saved")
