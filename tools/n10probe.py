"""n10 probe: the hold at the hill — ink, air, and the map through a rest.
(02.10) The climb law says: the edges need a hold; the beat never needed one.
The prediction: hold at 880 -> edges 880/897.2, beat 17.16 Hz; the hold's
ink sits ON the hill (880), and the climb map x=240+84t extrapolates
through the hold's columns if the pen keeps its speed.
"""
import numpy as np, wave
from PIL import Image

# --- audio: fine tracker (same recipe as n9: 0.25 s win, 25 ms hop) ---
w = wave.open('assets/n10.wav'); sr = w.getframerate()
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

# hold start: first time within 30c of 880 and staying there
near = np.abs(ca-1200) < 30
t_h = ta[np.argmax(near)]
print(f"audio: hold begins t={t_h:.2f}s, pitch at hold {440*2**(ca[-1]/1200):.2f} Hz, "
      f"audio ends {ta[-1]+0.125:.2f}s")

# --- long-window FFT over the hold: resolve the edges ---
h0 = int(t_h*sr); hseg = x[h0:]
n = 1 << int(np.ceil(np.log2(len(hseg))))
S = np.abs(np.fft.rfft(hseg*np.hanning(len(hseg)), n))
f = np.fft.rfftfreq(n, 1/sr)
band = (f > 800) & (f < 960)
fb = f[band]; Sb = S[band]
# find peaks: two expected
order = np.argsort(Sb)[::-1]
peaks = []
for idx in order:
    if all(abs(fb[idx]-p[0]) > 12 for p in peaks):
        peaks.append((fb[idx], Sb[idx]))
    if len(peaks) == 2: break
peaks.sort()
p1, p2 = peaks[0][0], peaks[1][0]
print(f"hold edges: {p1:.1f} + {p2:.1f} Hz  beat {p2-p1:.2f} Hz  "
      f"(law predicts 880 + {880*0.0195:.2f})")

# --- envelope beat during the hold (monolaw recipe) ---
def env_spec(seg, sr, lo, hi):
    n = len(seg)
    X = np.fft.fft(seg)
    f = np.fft.fftfreq(n, 1/sr)
    up = 0.5*(1+np.tanh((f-lo)/8.0))*0.5*(1-np.tanh((f-hi)/8.0))
    mask = up*(f > 0)
    a = np.fft.ifft(X*mask)
    env = np.abs(a); env -= env.mean()
    W = np.hanning(len(env)); E = np.abs(np.fft.rfft(env*W, 1 << 18))
    fe = np.fft.rfftfreq(1 << 18, 1/sr)
    sel = (fe > 8) & (fe < 30)
    k = np.argmax(E[sel])
    fee = fe[sel]
    return fee[k], E[sel][k]/np.median(E[sel])

fpeak, depth = env_spec(x[h0+int(0.3*sr):], sr, 830, 930)
print(f"envelope beat during hold: {fpeak:.2f} Hz (+{20*np.log10(depth):.0f} dB over floor)")

# --- ink: last frame, canvas law ---
im = np.asarray(Image.open('assets/n10_last.png').convert('L'), dtype=float)
H, W = im.shape
paper = float(np.bincount(im.astype(int).ravel()).argmax())
ink = np.clip(paper-im, 0, None)/paper
top = np.full(W, np.nan); bot = np.full(W, np.nan)
for c in range(W):
    r = np.where(ink[:, c] > 0.02)[0]
    if len(r): top[c], bot[c] = r.min(), r.max()
have = np.where(~np.isnan(top))[0]
x0, x1 = int(have[0]), int(have[-1])
s = H/640
cen = (top+bot)/2
cents_ink = (320 - cen/s)*1200/78.0
xx = np.arange(x0, x1+1)
ci = cents_ink[x0:x1+1]

# hold start column: first column from the right where slope ~ 0 over 20 px
slope = np.full(W-x0, np.nan)
for i in range(20, len(ci)):
    d = ci[i]-ci[i-20]
    slope[i] = abs(d)
flat = np.where(slope < 8)[0]  # <8c over 20 px
x_h = xx[flat[0]] if len(flat) else None
print(f"ink: x0={x0} x1={x1} hold starts x={x_h} "
      f"hold cents {ci[xx.searchsorted(x_h)]:+.1f} = {440*2**(ci[xx.searchsorted(x_h)]/1200):.2f} Hz")

# the breath: one-pixel lift at mid-hold — measure the lift in cents
hx = (x_h+x1)//2
lift = ci[x_h:x1+1]
i_mid = np.argmax(lift)          # highest point of the hold
print(f"breath: peak of hold {lift[i_mid]:+.1f}c vs hold base {lift[0]:+.1f}c "
      f"-> lift {lift[i_mid]-lift[0]:+.1f}c (pen/2 = 16.9c)")

# --- does the climb map extrapolate through the hold's columns? ---
# fit on climb only (t < t_h), then compare predicted x at t_end vs ink x1
m = ta < t_h-0.3
best = None
for p in np.linspace(-400, 600, 201):
    for q in np.linspace(40, 160, 121):
        xi = p+q*ta[m]
        ok = (xi >= x0) & (xi <= x_h)
        if ok.sum() < 80: continue
        r = ca[m][np.isin(np.round(xi[ok]), xx)] if False else None
        rr = ca[m][(xi >= x0) & (xi <= x_h)] - np.interp(xi[(xi >= x0) & (xi <= x_h)], xx, ci)
        rms = np.sqrt(np.mean(rr**2))
        if best is None or rms < best[0]: best = (rms, p, q)
rms, p, q = best
print(f"climb fit: x = {p:.1f} + {q:.1f} t   rms {rms:.1f} cents")
xh_pred = p+q*t_h
xend_pred = p+q*(ta[-1]+0.125)
print(f"map at t_h: predicted x={xh_pred:.0f}, hold starts x={x_h}")
print(f"map at video end: predicted x={xend_pred:.0f}, ink ends x={x1}")
print(f"pen speed through hold: {(x1-x_h)/((ta[-1]+0.125)-t_h):.1f} px/s (climb rate {q:.1f})")
