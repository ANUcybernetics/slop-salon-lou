"""let-go probe (02.10): natalie's fall hill->home, no holds. Window paper:
her alt gives the keys - hill 880 at the ink's left flat, home 440 at the end.
cents_ink = 1200*(r1-cen)/(r1-r0)  (parameter-free given the two anchors)."""
import numpy as np, wave
from PIL import Image

# --- audio: fine tracker (0.25 s window, 25 ms hop) ---
w = wave.open('assets/letgo.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768
WA = int(0.25*sr); win = np.hanning(WA); hop = int(0.025*sr)
fa = np.fft.rfftfreq(WA, 1/sr)
ta, ca = [], []
for t0 in range(0, len(x)-WA, hop):
    S = np.abs(np.fft.rfft(x[t0:t0+WA]*win))
    k = S[1:].argmax()+1
    a, b, c = S[k-1], S[k], S[k+1]
    d = 0.5*(a-c)/(a-2*b+c)
    ta.append((t0+WA/2)/sr); ca.append(1200*np.log2((fa[k]+d*(fa[1]-fa[0]))/440))
ta = np.array(ta); ca = np.array(ca)

# --- ink: per-column centroid under canvas law ---
im = np.asarray(Image.open('assets/letgo_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper - im, 0, None)/paper
top = np.full(W, np.nan); bot = np.full(W, np.nan)
for c in range(W):
    r = np.where(ink[:, c] > 0.02)[0]
    if len(r): top[c], bot[c] = r.min(), r.max()
have = np.where(~np.isnan(top))[0]
x0, x1 = int(have[0]), int(have[-1])
cen = (top+bot)/2
# window: two alt anchors - hill 880 at ink start, home 440 at ink end
r0 = np.mean(cen[x0:x0+10]); r1 = np.mean(cen[x1-9:x1+1])
print(f"window fit: ink rows {r0:.1f} -> {r1:.1f}  ({r1-r0:.1f} px = 1200c)  s={(r1-r0)/78:.4f} px/her-px")
ci = 1200*(r1 - cen)/(r1 - r0)
xx = np.arange(x0, x1+1)
ci = ci[x0:x1+1]

# --- fit t->x map, wide ---
best = None
for p in np.linspace(-400, 600, 201):
    for q in np.linspace(50, 160, 111):
        xi = p + q*ta
        ok = (xi >= x0) & (xi <= x1)
        if ok.sum() < 100: continue
        r = ca[ok] - np.interp(xi[ok], xx, ci)
        rms = np.sqrt(np.mean(r**2))
        if best is None or rms < best[0]: best = (rms, p, q, ok.mean())
rms, p, q, cov = best
print(f"fit: x = {p:.1f} + {q:.1f} t   rms {rms:.1f} cents  coverage {cov:.2f}")

# --- residuals over time (structure check) ---
xi = p + q*ta
ok = (xi >= x0) & (xi <= x1)
r = ca[ok] - np.interp(xi[ok], xx, ci)
tt = ta[ok]
for lo in np.arange(tt.min(), tt.max(), 1.0):
    m = (tt >= lo) & (tt < lo+1)
    if m.sum() > 5:
        print(f"  t {lo:5.1f}-{lo+1:.1f}  mean resid {r[m].mean():+6.1f} cents  (n={m.sum()})")


# --- receipt plot ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# measured beats (2 s windows) and law curve 0.0195*f(t)
X = np.fft.rfft(x)
freqs = np.fft.rfftfreq(len(x), 1/sr)
Xb = X.copy(); Xb[(freqs < 350) | (freqs > 950)] = 0
env = np.abs(np.fft.ifft(np.concatenate([Xb, np.conj(Xb[-2:0:-1])]))[:len(x)])
bm, bt = [], []
for lo in np.arange(0, 22, 2.0):
    i0, i1 = int(lo*sr), int((lo+2)*sr)
    if i1 > len(env): break
    seg = env[i0:i1] - env[i0:i1].mean()
    E = np.abs(np.fft.rfft(seg*np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1/sr)
    band = (fr >= 5) & (fr <= 25)
    k = np.where(band)[0][E[band].argmax()]
    bm.append(fr[k]); bt.append(lo+1.0)
flaw = 0.0195*440*2**(ca/1200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6))
ax1.plot(ta, flaw, color='#3a6b4f', lw=1.4, label='law 0.0195·f(t)')
ax1.plot(bt, bm, 'o', color='#b3402a', ms=5, label='measured beat')
ax1.set_xlabel('t (s)'); ax1.set_ylabel('beat (Hz)')
ax1.set_title('air: the beat rides the fall, 17.0 -> 8.5 Hz', fontsize=10)
ax1.legend(fontsize=8, frameon=False)
ax2.plot(tt, r, '.', color='#1a1a1a', ms=2)
ax2.axhline(0, color='#888888', lw=0.6)
ax2.set_xlabel('t (s)'); ax2.set_ylabel('air - ink (cents)')
ax2.set_title('ink: surge then ease, one linear map', fontsize=10)
for a in (ax1, ax2):
    a.set_yticks if False else None
ax2.set_yticks([-20, -10, 0, 10, 20])
fig.suptitle('the let-go, read - lou 02.10', fontsize=11)
fig.tight_layout()
fig.savefig('assets/letgo_receipt.png', dpi=140)
print('saved')
