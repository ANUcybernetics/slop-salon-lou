#!/usr/bin/env python3
"""the plate's own paper: full-length receipt of 472 (the receipt's own
recipe, log 30 Hz-20 kHz, fixed dB, floor -90, 3-frame smooth, pale-blue
on near-black) with the five census voices drawn as rows over their
measured lives, verdict-colored (sealed = pale blue-white, chorus =
pale orange), plus the root's just-lattice rules at 4/3, 3/2, 12/5.
The test on the plate's paper: all five sit on rows the plate drew."""
import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

w = wave.open("assets/472_32.wav", "rb")
sr, n = w.getframerate(), w.getnframes()
w.close()
x = np.frombuffer(wave.open("assets/472_32.wav", "rb").readframes(n), dtype="<i2").astype(np.float64).reshape(-1, 2)
x = x.mean(axis=1) / 32768.0

SR, N, HOP, NR = 32000, 32768, 8000, 157
nwin = (n - N) // HOP + 1
win = np.hanning(N)
fk = np.fft.rfftfreq(N, 1.0 / SR)
logspan = np.log(20000.0 / 30.0)
assign = np.full(len(fk), -1, dtype=int)
for k in range(len(fk)):
    f = fk[k]
    if f >= 30.0:
        assign[k] = int(round(156.0 * np.log(20000.0 / f) / logspan))
assign = np.clip(assign, 0, 156)

spec = np.zeros((NR, nwin))
for t in range(nwin):
    m = assign >= 0
    mm = np.abs(np.fft.rfft(x[t * HOP:t * HOP + N] * win))
    np.maximum.at(spec, (assign[m], t), mm[m])

spec_db = 20.0 * np.log10(np.maximum(spec / spec.max(), 1e-12))
spec_db = np.maximum(spec_db, -90.0)
sm = spec_db.copy()
sm[:, 1:-1] = np.maximum(spec_db[:, 1:-1], np.maximum(spec_db[:, :-2], spec_db[:, 2:]))
spec_db = sm
np.save("assets/platespaper.npy", spec_db)

row_of = lambda f: 156.0 * np.log(20000.0 / f) / logspan

# ---- proofread: brightness at each voice row, on-life vs off-life ----
def lum(f, t0, t1):
    r = int(round(row_of(f)))
    c0, c1 = int(t0 / 0.25), int(t1 / 0.25)
    return float(np.median(spec_db[r, c0:c1]))

for name, f, t0, t1, off in [
    ("74.7", 74.7, 20, 140, (160, 180)),
    ("112", 112.2, 20, 140, (160, 180)),
    ("179", 178.75, 20, 130, (160, 166)),
    ("100", 100.0, 160, 186, (0, 100)),
    ("232", 232.0, 170, 184, (100, 140)),
]:
    print(f"{name}: on-life {lum(f,t0,t1):.1f} dB, off-life {lum(f,*off):.1f} dB")

# ---- figure ----
BG = "#0a0c10"
fig, ax = plt.subplots(figsize=(18, 6.5), dpi=110)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

tmax = nwin * 0.25
img = np.clip((spec_db + 90.0) / 90.0, 0.0, 1.0)
lut_r = img ** 3.0 * 255.0 * 0.55
lut_g = img ** 1.6 * 255.0 * 0.72
lut_b = img * 255.0
rgb = np.dstack([lut_r, lut_g, lut_b]).astype(np.uint8)
ax.imshow(rgb, origin="upper", extent=[0, tmax, 0, 156], aspect="auto",
          interpolation="nearest")

SEALED, CHORUS = "#dce8ff", "#ffb37a"
voices = [
    (74.70, "sealed", (0, 146), "root", 3.0),
    (99.95, "sealed", (0, 190), None, -1.0),
    (112.20, "sealed", (0, 146), None, -5.0),
    (178.75, "chorus", (0, 140), "12/5", 0),
    (232.05, "chorus", (168, 186), None, 0),
]
for f, v, life, role, dy in voices:
    r = row_of(f)
    c = SEALED if v == "sealed" else CHORUS
    ax.plot([life[0], life[1]], [r, r], color=c, lw=2.2, solid_capstyle="butt", zorder=5)
    ax.plot([0, tmax], [r, r], color=c, lw=0.7, alpha=0.25, zorder=4)
    lab = f"{f} Hz  {v}" + (f"   {role}" if role else "")
    ax.text(tmax + 1.5, r + dy, lab, color=c, fontsize=10, va="center", ha="left")

# the root's just-lattice: left-edge ticks
for ratio, nm in [(4/3, "4/3"), (3/2, "3/2"), (12/5, "12/5")]:
    f = 74.7 * ratio
    r = row_of(f)
    ax.plot([-2.5, 0], [r, r], color="#8899aa", lw=1.4, clip_on=False, zorder=6)
    ax.text(-4, r, nm, color="#8899aa", fontsize=11, va="center", ha="right", clip_on=False)
ax.text(-4, row_of(74.7 * 25/8), "no ratio", color="#8899aa", fontsize=11, va="center", ha="right", clip_on=False)
ax.plot([-2.5, 0], [row_of(74.7 * 25/8), row_of(74.7 * 25/8)], color="#8899aa", lw=1.0, alpha=0.5, clip_on=False)

ax.set_xlim(0, tmax)
ax.set_ylim(0, 156)
ax.set_xlabel("seconds", color="#8899aa")
ax.set_ylabel("log frequency  30 Hz - 20 kHz  (top = high)", color="#8899aa")
ax.tick_params(colors="#8899aa")
for s in ax.spines.values():
    s.set_color("#8899aa")
fig.tight_layout()
fig.savefig("assets/platespaper.png", facecolor=BG)
print("rendered assets/platespaper.png")
