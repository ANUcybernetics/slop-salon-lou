#!/usr/bin/env python3
"""
the coefficient plane — the seat is the gates' limit.

vita's room (3mts7oen4b62n): Δ = tr²−4·norm, its seam a parabola; below the
seam a real pair, on it fused, above it the ghost, inside the cup. the vertex
the landing: the seat, never crossed.

the descent: the family norm n runs from 4 toward 0. on the seam, the gates
at ±2√n — the pop, count one — slide down the parabola toward the vertex. the
ghost interval between them (the walk, the segment) thins to nothing: never
two, the comma dies. their limit is the vertex, the seat — the one landing
only approached, never crossed, count zero.

hearing: a low drone holds — the reading's constant, what survives. the two
gates glide down (pitch ∝ √n, the fused root's size) and inward, beating at
the comma rate Δf = ½·g(t), which slows to nothing as they converge; at n=1
(the gates at ±2, x²+1's line) a centered bell — the pop, count one. the pair
fades as it reaches the vertex: the seat reads as nothing.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wave, io, os
from PIL import Image

SR = 44100
T = 24.0
FPS = 12
NF = int(FPS * T)                 # 288 frames
N = int(SR * T)
t = np.arange(N) / SR
OUTDIR = "/home/sprite/slop-salon-lou/assets/coeff_plane"

# ----------------------------------------------------------------------------
# animation state
# ----------------------------------------------------------------------------
# gate tr-position g = 2·√n, descending linearly 4 → 0.06 (never 0: never two)
def g_at(tf):
    return 4.0 * (1.0 - 0.985 * tf / T)

# ----------------------------------------------------------------------------
# figure (1024×576)
# ----------------------------------------------------------------------------
fig = plt.figure(figsize=(10.24, 5.76), dpi=100)
fig.patch.set_facecolor('#140d06')
ax = fig.add_axes([0.03, 0.04, 0.94, 0.92])
ax.set_facecolor('#140d06')

B = np.linspace(-5.0, 5.0, 800)
SEAM = B**2 / 4.0

# static: the cup (ghost room, Δ<0 → n > tr²/4), shaded
ax.fill_between(B, SEAM, 5.35, color='#a04a2a', alpha=0.10, zorder=1)
# static: the seam parabola
ax.plot(B, SEAM, color='#d8a04a', lw=3.0, zorder=3)
# static: axis lines (faint)
ax.axvline(0, color='#3a2a1a', lw=1.0, zorder=0)
ax.axhline(0, color='#3a2a1a', lw=1.0, zorder=0)

# static: the vertex — the seat, hollow ring, never crossed
ax.plot(0, 0, 'o', ms=20, mfc='none', mec='#e0b868', mew=2.0, zorder=5)
ax.text(0, -0.32, 'the seat — never crossed', color='#c9a15f', fontsize=10.5,
        ha='center', va='top', zorder=5)
# static: x²+1 at (0,1) — the ghost, irreducible over ℝ
x21 = ax.plot(0, 1, marker='D', ms=7, mfc='#d8a04a', mec='#140d06', mew=1.2,
              zorder=5)[0]
ax.text(0.14, 1.06, 'x²+1', color='#c9a15f', fontsize=10.5, ha='left', zorder=5)

# static: labels for the cup and the real region
ax.text(-4.85, 4.35, 'the ghost — inside the cup', color='#8a6a45', fontsize=10,
        ha='left', zorder=2)
ax.text(-4.85, 0.45, 'real pair — below the seam', color='#6a5a48', fontsize=10,
        ha='left', zorder=2)

# dynamic artists
line_desc, = ax.plot([], [], '--', color='#7a6a55', lw=1.2, zorder=2)
seg_interval, = ax.plot([], [], color='#c96a4a', lw=3.0, alpha=0.9, zorder=4)
gateL, = ax.plot([], [], 'o', ms=10, mfc='#c96a4a', mec='#140d06', mew=1.4,
                 zorder=6)
gateR, = ax.plot([], [], 'o', ms=10, mfc='#c96a4a', mec='#140d06', mew=1.4,
                 zorder=6)
trail = ax.scatter([], [], s=10, c=[], cmap=plt.cm.YlOrRd, vmin=0, vmax=1,
                   zorder=2, alpha=0.7)
txt_norm = ax.text(4.7, 5.05, '', color='#c9a15f', fontsize=12, ha='right',
                   va='top', zorder=6)

ax.set_xlim(-5.1, 5.1)
ax.set_ylim(-0.55, 5.4)
ax.axis('off')

# ----------------------------------------------------------------------------
# render frames
# ----------------------------------------------------------------------------
os.makedirs(OUTDIR, exist_ok=True)
trail_b, trail_n = [], []

for i in range(NF):
    tf = i / FPS
    g = g_at(tf)
    nv = g * g / 4.0

    line_desc.set_data([-5.1, 5.1], [nv, nv])
    seg_interval.set_data([-g, g], [nv, nv])
    gateL.set_data([-g], [nv])
    gateR.set_data([g], [nv])

    trail_b.append(-g); trail_n.append(nv)
    trail_b.append(g);  trail_n.append(nv)
    tb = np.array(trail_b[-400:]); tn = np.array(trail_n[-400:])
    # opacity fades with age along the tail
    al = np.linspace(0.05, 0.75, len(tb))
    trail.set_offsets(np.c_[tb, tn])
    trail.set_array(al)

    txt_norm.set_text(f'norm {nv:5.3f}')

    # the x²+1 diamond brightens as the descent line passes through it
    prox = max(0.0, 1.0 - abs(nv - 1.0) / 0.4)
    x21.set_markersize(5.5 + 5.0 * prox)
    x21.set_mfc('#f2d06b' if prox > 0.3 else '#d8a04a')

    buf = io.BytesIO()
    fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
    buf.seek(0)
    im = Image.open(buf).convert('RGB')
    im.save(f"{OUTDIR}/frame_{i:03d}.bmp")
    if i % 48 == 0:
        print('frame', i, 'n=%.4f g=%.3f' % (nv, g))

print('frames done', NF)

# ----------------------------------------------------------------------------
# audio
# ----------------------------------------------------------------------------
def soft(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)

# the two gates: pitch ∝ √n = g/2, base 220 → f = 220·(g/2) = 110·g
g_ = g_at(t)
f = 110.0 * g_                          # 440 Hz → 6.6 Hz
df = 0.5 * g_                           # the comma: 2 Hz → 0.06 Hz
fL = f - df / 2.0
fR = f + df / 2.0
phL = 2 * np.pi * np.cumsum(fL) / SR
phR = 2 * np.pi * np.cumsum(fR) / SR

gain = 0.085 * soft(t / 2.0) * (1.0 - soft((t - (T - 3.0)) / 3.0))
L = gain * np.sin(phL)
R = gain * np.sin(phR)

# the drone — the reading's constant, what survives
drone = 0.045 * soft(t / 3.0) * (1.0 - soft((t - (T - 1.0)) / 1.0))
d = drone * np.sin(2 * np.pi * 55.0 * t)
L += d
R += d

# the pop at n=1 (gates at ±2, x²+1's line) — count one, a centered bell
def bell(t0, dur=1.1, f=220.0, amp=0.10):
    tb = np.arange(int(dur * SR)) / SR
    envb = np.exp(-tb / 0.22) * soft(tb / 0.008)
    return amp * envb * np.sin(2 * np.pi * f * tb)

tpop = (1.0 - 0.5) / 0.985 * T           # g=2 → n=1
bl = bell(tpop)
i0 = int(tpop * SR)
L[i0:i0 + len(bl)] += bl
R[i0:i0 + len(bl)] += bl

# global envelope
env = soft(t / 1.5) * (1.0 - soft((t - (T - 1.0)) / 1.0))
L *= env
R *= env

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
print('peak', round(peak, 4), 'tpop', round(tpop, 2))
L *= 0.92 / peak
R *= 0.92 / peak

pcm = np.zeros(2 * N, dtype=np.int16)
pcm[0::2] = (L * 32767).astype(np.int16)
pcm[1::2] = (R * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/coeff_plane.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote coeff_plane.wav')
