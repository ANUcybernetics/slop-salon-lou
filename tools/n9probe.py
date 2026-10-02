"""n9 probe: does the air match the ink on natalie's climb? (02.10)"""
import numpy as np, wave
from PIL import Image

# --- audio: fine tracker (0.25 s window, 25 ms hop) ---
w = wave.open('assets/n9.wav'); sr = w.getframerate()
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
im = np.asarray(Image.open('assets/n9_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper - im, 0, None)/paper
top = np.full(W, np.nan); bot = np.full(W, np.nan)
for c in range(W):
    r = np.where(ink[:, c] > 0.02)[0]
    if len(r): top[c], bot[c] = r.min(), r.max()
have = np.where(~np.isnan(top))[0]
x0, x1 = int(have[0]), int(have[-1])
s = H/640
cen = (top+bot)/2
cents_ink = (320 - cen/s)*1200/78.0          # cents rel 440
xx = np.arange(x0, x1+1)
ci = cents_ink[x0:x1+1]

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

# --- home crossing both ways ---
x_home = np.interp(0.0, ci[::-1], xx[::-1])   # ink crosses 0c (440)
t_home = np.interp(0.0, ca, ta)
print(f"ink crosses home at x={x_home:.0f} -> t={(x_home-p)/q:.2f}s ; audio crosses 440 at t={t_home:.2f}s")
print(f"ink start {440*2**(ci[0]/1200):.1f} Hz (x={x0})  ink end {440*2**(ci[-1]/1200):.1f} Hz (x={x1})")
print(f"audio start {440*2**(ca[0]/1200):.1f} Hz  audio end {440*2**(ca[-1]/1200):.1f} Hz")
