"""the take (03.10): still = the piece's own receipt. Grayscale LUT, silence
white, fixed dB ref (peak of the file), log-frequency y axis 100-480 Hz."""
import numpy as np, wave
from PIL import Image

w = wave.open('assets/thetake.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)/32768
n = len(x)
NW, HOP = int(0.05*sr), int(0.005*sr)
tgrid, fgrid = [], []
frames = []
for t0 in range(0, n-NW, HOP):
    seg = x[t0:t0+NW]*np.hanning(NW)
    frames.append(np.abs(np.fft.rfft(seg)))
    tgrid.append((t0+NW/2)/sr)
S = np.array(frames).T
fr = np.fft.rfftfreq(NW, 1/sr)
tgrid = np.array(tgrid)
S /= S.max()  # fixed ref: peak of the file
DB = 20*np.log10(S + 1e-12)

# resample onto log-y grid 100-480 Hz
NG = 640
yg = np.logspace(np.log10(100), np.log10(480), NG)
rows = np.empty((NG, len(tgrid)))
for i, f in enumerate(yg):
    k = int(round(f/(fr[1]-fr[0])))
    rows[NG-1-i] = 20*np.log10(S[max(k-1,0):k+2].mean(axis=0) + 1e-12) - DB.max()
floor = -55
L = np.clip((rows - floor)/(0 - floor), 0, 1)
img = (255*(1-L)).astype(np.uint8)  # ink dark, silence white
Image.fromarray(img).resize((1600, 640)).save('assets/thetake_still.png')
print('saved assets/thetake_still.png', img.shape)
