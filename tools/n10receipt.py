import numpy as np, wave
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

# --- audio: hold spectrum, long window over the hold segment ---
w = wave.open('assets/n10.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768
seg = x[int(1.0*sr):]                      # the hold, whole
n = 1 << int(np.ceil(np.log2(len(seg))))
S = np.abs(np.fft.rfft(seg*np.hanning(len(seg)), n))
f = np.fft.rfftfreq(n, 1/sr)
band = (f > 780) & (f < 980)
fb, Sb = f[band], S[band]/S[band].max()

# --- ink: hold row profile with the breath (x 933-1678) ---
im = np.asarray(Image.open('assets/n10_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper-im, 0, None)/paper
top = np.full(W, np.nan)
for c in range(W):
    r = np.where(ink[:, c] > 0.02)[0]
    if len(r):
        top[c] = r.min()
prof = 250 - top                          # hold top edge, lift = up
prof = prof/np.median(prof[1000:1600])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6))
ax1.plot(fb, Sb, color='#1a1a1a', lw=1.2)
for e in (871.5, 888.6):
    ax1.axvline(e, color='#b3402a', lw=0.8, ls='--', alpha=0.8)
ax1.axvline(880.05, color='#3a6b4f', lw=0.8, ls='-', alpha=0.8)
ax1.set_xlim(820, 940)
ax1.set_xlabel('Hz')
ax1.set_title('air: two edges, mean 880.05', fontsize=10)
ax2.plot(prof, color='#1a1a1a', lw=1.0)
ax2.axvline(933, color='#888888', lw=0.6, ls=':')
ax2.axvline(1290, color='#b3402a', lw=0.8, ls='--', alpha=0.8)
ax2.axvline(1678, color='#888888', lw=0.6, ls=':')
ax2.set_xlim(0, 1700)
ax2.set_xlabel('x (canvas px)')
ax2.set_title('ink: the rest, one breath at mid-hold', fontsize=10)
for a in (ax1, ax2):
    a.set_yticks([])
fig.suptitle('the hill rest, read - lou 02.10', fontsize=11)
fig.tight_layout()
fig.savefig('assets/n10_receipt.png', dpi=140)
print('saved')
