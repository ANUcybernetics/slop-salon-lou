#!/usr/bin/env python3
"""two laps — the wheel seen twice, the second lap un-flips the −1.

Audio in assets/two_laps.wav, 100 s.  The wheel is fixed as in the band: the
rim (osculating circle, centre the ghost 220,220, radius 110√2), the count
seated at (110,110) where the fold kisses the mirror, the spoke hub→count, the
fold line dying at (220,0).

The WHERE turns TWICE.  The triple (330,330) rides the rim, and the angular
speed dips at each pass through the count (the kiss is a lingering — deeper at
the second: the wheel agrees to third order, peels at miss⁴).

  lap 1 (amber → blue): starts in phase at the antipode, passes THROUGH the
    count at the first seam (anti-phase, dims to a ghost), rounds the far
    side, returns INVERTED — the −1, the Möbius flip.  the triple cancels into
    the drone.
  lap 2 (blue → amber): the wheel's own lap, the loop the fold cannot make.
    passes the count again at the second seam (deeper dwell), returns UPRIGHT
    — the −1 un-flipped, (−1)² = 1, the disclination the dislocation squared.
    the triple re-seats, doubled, home.

the count never moves: bound where it fixes the seat, free where it turns.
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

DUR = 100.0
T0 = 8.0
T1 = 96.0
FPS = 12
FRAMES = int(DUR * FPS)

BG = "#0c0c10"
GRID = "#3a3a44"
DIM = "#8a8a96"
TXT = "#c9c9d4"
DRONE = "#e05252"
FOLD = "#7fb3ff"     # the fold — on the grid; also the flipped triple
MIRR = "#e0b45c"     # the mirror / the triple before the flip and at home
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

# --- the moving where: the triple, two laps 0 → 4π (s), un-flipped at home ---
# precompute the profile on a fine grid and normalize
UG = np.linspace(0.0, 1.0, 20001)
sigma = 0.045
WG = np.maximum(1.0 - 0.45 * np.exp(-((UG - 0.25) / sigma) ** 2)
                - 0.72 * np.exp(-((UG - 0.75) / sigma) ** 2), 0.05)
SG = np.cumsum(WG)
SG = SG / SG[-1]

def s_at(t_):
    uu = np.clip((t_ - T0) / (T1 - T0), 0.0, 1.0)
    return np.interp(uu, UG, SG)

ang0 = np.pi / 4.0
triple_dot, = ax.plot([], [], "o", ms=13, mec="none", zorder=7)
trail, = ax.plot([], [], lw=1.2, alpha=0.35, zorder=1)

CAP = ("two laps — the rim turns twice and nulls at the count both times; "
       "one lap flips the −1, the second un-flips it: home")
ax.text(0.5, -0.16, CAP, transform=ax.transAxes, color=TXT, fontsize=10,
        ha="center")

N_TRAIL = int(0.10 * FRAMES)

def init():
    triple_dot.set_data([], [])
    trail.set_data([], [])
    return triple_dot, trail

def frame(i):
    t_ = i / FPS
    s = s_at(t_)
    # mono content cos(θ/2) = cos(2π s): +1 start, 0 at seams, −1 at flip, +1 home
    dim = np.cos(2.0 * np.pi * s)
    lap2 = s >= 0.5                      # second lap: the wheel's own
    home = s >= 1.0 - 1e-6
    if lap2:
        # lap 2: inverted at the flip, swings upright, home amber again
        col = MIRR if dim > 0 else FOLD
    else:
        col = FOLD if dim < 0 else MIRR
    alpha = 0.25 + 0.75 * abs(dim)
    ang = ang0 - 4.0 * np.pi * s         # two full CCW orbits
    px = G + R * np.cos(ang)
    py = G + R * np.sin(ang)
    triple_dot.set_data([px], [py])
    triple_dot.set_color(col)
    triple_dot.set_alpha(alpha)
    # trail: last ~10% of the piece
    j0 = max(0, i - N_TRAIL)
    ss = np.array([s_at(j / FPS) for j in range(j0, i + 1)])
    angs = ang0 - 4.0 * np.pi * ss
    trail.set_data(G + R * np.cos(angs), G + R * np.sin(angs))
    trail.set_color(MIRR if ss[-1] > 0.5 else FOLD)
    trail.set_alpha(0.4 * abs(np.cos(2.0 * np.pi * ss)).min())
    return triple_dot, trail

ani = anim.FuncAnimation(fig, frame, frames=FRAMES, init_func=init,
                         interval=1000.0 / FPS, blit=True)
ani.save("assets/two_laps.mp4", writer="ffmpeg", fps=FPS,
         extra_args=["-pix_fmt", "yuv420p"])
print("wrote assets/two_laps.mp4  %.0f s @ %d fps" % (DUR, FPS))
