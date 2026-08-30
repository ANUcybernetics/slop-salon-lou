#!/usr/bin/env python3
"""the band — the wheel seen as a turning, the turn is the sign.

One lap, 8 → 92 s (audio in assets/the_band.wav, 96 s).

The wheel is fixed: the rim (the osculating circle, centre the ghost 220,220,
radius 110√2), the count seated at (110,110) where the fold kisses the mirror,
the spoke from hub to count, the fold line dying at (220,0).  The ghost is the
hub — the centre, never a seat.

The WHERE turns: the triple (330,330) rides the rim one full lap.  It starts
antipodal to the count, in phase (bright).  At the seam — half a lap — it
passes THROUGH the count (110,110), and there it is anti-phase: the rim nulls
in mono, the sign in neither side (it dims to a ghost).  It rounds the far side
and returns to its antipodal seat — inverted: the colour flips to the fold's
blue, the −1, the Möbius return.  One lap flips it; two would bring it home.
The count never moves: bound where it fixes the seat, free where it turns.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np

C = 110.0
G = 220.0
T = 330.0
R = C * np.sqrt(2.0)

DUR = 96.0
T0 = 8.0
T1 = 92.0
FPS = 12
FRAMES = int(DUR * FPS)

BG = "#0c0c10"
GRID = "#3a3a44"
DIM = "#8a8a96"
TXT = "#c9c9d4"
DRONE = "#e05252"
FOLD = "#7fb3ff"     # the fold — on the grid; also the flipped triple
MIRR = "#e0b45c"     # the mirror / the triple before the flip
TANG = "#c792ea"     # the kiss / the count
ROSE = "#d16fa0"     # the wheel / the rim
GOLD = "#f0c26a"     # the ghost / the hub

fig, ax = plt.subplots(figsize=(10.24, 5.76), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=DIM, labelsize=8)
ax.set_aspect("equal")
ax.set_xlim(40, 400)
ax.set_ylim(-20, 400)
ax.set_xticks([110, 220, 330])
ax.set_xticklabels(["110", "220", "330"])
ax.set_yticks([110, 220, 330])
ax.set_yticklabels(["110", "220", "330"])

# --- static: the wheel ---
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(G + R * np.cos(th), G + R * np.sin(th), color=ROSE, lw=2.0,
        ls="--", zorder=2, alpha=0.9)
ax.plot([C, T], [C, T], color=ROSE, lw=2.2, zorder=2, alpha=0.7)  # the diameter
ax.plot([G, C], [G, C], color=GOLD, lw=1.6, ls=(0, (2, 2)), zorder=3)  # spoke
# the fold, dying at 220 (below the hub) — a line cannot turn
xf = np.linspace(104, 236, 2)
ax.plot(xf, 220 - xf, color=FOLD, lw=2.2, zorder=3)
ax.plot([236, 340], [220 - 236, 220 - 340], color=FOLD, lw=1.2,
        ls=(0, (4, 3)), zorder=3)
ax.plot(G, 0, "o", color=FOLD, ms=5, mec="none", zorder=4)
# the count — the seated kiss point, never moves
ax.plot(C, C, "o", color=TANG, ms=11, mec="none", zorder=6)
ax.text(C - 6, C + 22, "the count — bound", color=TANG, fontsize=9,
        ha="center")
# the hub — the ghost, the centre
ax.plot(G, G, "o", color=GOLD, ms=15, mec="none", alpha=0.15, zorder=5)
ax.plot(G, G, "o", color="none", mec=GOLD, mew=2.4, ms=13, zorder=6)
ax.text(G, G - 26, "the ghost — the hub", color=GOLD, fontsize=9,
        ha="center")

# --- the moving where: the triple, one lap 0→2π (u), inverted at the end ---
def u_of(t_):
    s = np.clip((t_ - T0) / (T1 - T0), 0.0, 1.0)
    return 0.5 * (1.0 - np.cos(np.pi * s))

# orbit: start at the antipode (330,330) i.e. angle 45°, one lap CCW
ang0 = np.pi / 4.0
triple_dot, = ax.plot([], [], "o", ms=13, mec="none", zorder=7)
trail, = ax.plot([], [], color=MIRR, lw=1.2, alpha=0.35, zorder=1)

CAP = ("the wheel is a band — the where turns once, nulls at the count, "
       "returns inverted: one lap flips the −1")
ax.text(0.5, -0.16, CAP, transform=ax.transAxes, color=TXT, fontsize=10,
        ha="center")

# trail: last ~10% of the lap
N_TRAIL = int(0.10 * FRAMES)

def init():
    triple_dot.set_data([], [])
    trail.set_data([], [])
    return triple_dot, trail

def frame(i):
    t_ = i / FPS
    u = u_of(t_)
    # dimming: the rim nulls in mono as |cos(θ/2)| → 0 at the count
    dim = np.cos(np.pi * u)          # +1 start, 0 at seam, −1 return
    flipped = u >= 1.0               # after the lap completes
    col = FOLD if flipped else MIRR
    # brightness: bright when in-phase, ghostly at the seam
    alpha = 0.25 + 0.75 * abs(dim)
    ang = ang0 - 2.0 * np.pi * u     # CCW orbit
    px = G + R * np.cos(ang)
    py = G + R * np.sin(ang)
    triple_dot.set_data([px], [py])
    triple_dot.set_color(col)
    triple_dot.set_alpha(alpha)
    # trail
    j0 = max(0, i - N_TRAIL)
    us = np.array([u_of(j / FPS) for j in range(j0, i + 1)])
    angs = ang0 - 2.0 * np.pi * us
    trail.set_data(G + R * np.cos(angs), G + R * np.sin(angs))
    trail.set_color(col)
    trail.set_alpha(0.4 * abs(np.cos(np.pi * us)).min())
    return triple_dot, trail

ani = anim.FuncAnimation(fig, frame, frames=FRAMES, init_func=init,
                         interval=1000.0 / FPS, blit=True)
ani.save("assets/the_band.mp4", writer="ffmpeg", fps=FPS,
         extra_args=["-pix_fmt", "yuv420p"])
print("wrote assets/the_band.mp4  %.0f s @ %d fps" % (DUR, FPS))
