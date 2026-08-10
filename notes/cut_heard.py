#!/usr/bin/env python3
"""cut_heard — the seam register's two meetings, heard as one.

The neck (f'=0) is the fixed point: a shift moves the roots, never the critical
points. Two meetings happen at the neck, and they are the same meeting:

  A. THE POP  — the meeting has a time. At b=2 the double root fuses with the
     gate z=1: the ghost becomes a root for one instant — the crystal — then
     the pair goes complex and the crossing thins. Left ear: a beating pair
     closes on the gate, the beat stretches to zero, flashes the crystal, and
     the film is silent.

  B. THE CUT  — the place is a line. At the empty gate z=-1 (a neck with no
     root on it) a walk arrives and the map cuts: the step divides by zero, the
     walk is flung across the plane, and it lands ON the crystal at z=1.
     Right ear: tension rises, the cut flings (sweep + scatter), the return
     descends, and it lands — on the same note the pop flashed.

The drone underneath is the neck itself: 55 Hz, never changes. H^0, the
survivor. Both meetings leave it alone; the seam outlives the pop.
"""
import numpy as np
import wave

SR = 44100
T = 90.0
N = int(SR * T)
t = np.linspace(0, T, N, endpoint=False)
rng = np.random.default_rng(7)

LP = lambda a, pan: (a * np.cos((pan + 1) * np.pi / 4),
                     a * np.sin((pan + 1) * np.pi / 4))

L = np.zeros(N)
R = np.zeros(N)

# ---------------------------------------------------------------- the drone
# the neck: 55 Hz and its harmonics, steady, low, warm. never changes.
phD = 2 * np.pi * np.cumsum(55.0 * np.ones(N)) / SR
drone = (0.24 * np.sin(phD) + 0.055 * np.sin(2 * phD)
         + 0.02 * np.sin(3 * phD))
breath = 1.0 + 0.06 * np.sin(2 * np.pi * 0.06 * t)
drone *= breath * np.minimum(1.0, t / 5.0)
l_d, r_d = LP(drone, 0.0)
L += l_d; R += r_d

# ---------------------------------------------------------------- A. the pop
# the meeting has a time. a beating pair rides the S-curve into the gate,
# the beat stretches, at tPOP they fuse — the crystal flashes — then thin.
tPOP = 40.0
p = np.clip(t / tPOP, 0, 1) ** 0.9
f1 = 268.0 - 58.0 * p                      # descends toward the gate
det = 1.0 + 0.016 * (1.0 - p)              # beat -> 0 as the pair fuses
phA = 2 * np.pi * np.cumsum(f1) / SR
pair = 0.5 * np.sin(phA) + 0.5 * np.sin(phA * det)
swell = 1.0 + 0.25 * np.sin(2 * np.pi * 0.18 * t)   # the S-curve riding
envA = 0.30 * p ** 1.4 * swell
envA *= np.minimum(1.0, t / 4.0)
envA = np.where(t < tPOP, envA, 0.0)       # the pair is gone — thinned
l_a, r_a = LP(pair * envA, -0.62)
L += l_a; R += r_a

# the crystal — one instant: the ghost becomes a root. 440 Hz, bright.
pf = int(tPOP * SR)
flash_n = int(2.6 * SR)
ft = np.arange(flash_n) / SR
crys = (np.sin(2 * np.pi * 440 * ft) + 0.5 * np.sin(2 * np.pi * 880 * ft)
        + 0.22 * np.sin(2 * np.pi * 1320 * ft))
crys *= np.exp(-ft / 0.55) * np.minimum(1.0, ft / 0.02) * 0.34
l_f, r_f = LP(crys, -0.30)
L[pf:pf + flash_n] += l_f
R[pf:pf + flash_n] += r_f

# ---------------------------------------------------------------- B. the cut
# the place is a line. the walk winds toward the empty gate; tension rises;
# the map cuts; the return descends; it lands on the crystal.
tCUT = 66.0
q = np.clip((t - 40.0) / (tCUT - 40.0), 0, 1)
# approach: pitch rises with the step size, wobble = the winding
fB = 120.0 * (1.0 - q) ** 1.3 + 500.0 * q
wob = 1.0 + 0.09 * np.sin(2 * np.pi * (1.1 + 1.8 * q) * t)
phB = 2 * np.pi * np.cumsum(fB * wob) / SR
voice = np.sin(phB) + 0.30 * np.sin(2 * phB)
envB = 0.26 * np.clip((t - 40.0) / 3.0, 0, 1) * np.clip((tCUT - t) / 0.35, 0, 1)
l_b, r_b = LP(voice * envB, 0.62)
L += l_b; R += r_b

# the cut: the map flings — a bright upward sweep with a noise edge
cs = int(tCUT * SR)
fling_n = int(0.9 * SR)
ftt = np.arange(fling_n) / SR
fsw = 300.0 * np.exp(np.log(2600.0 / 300.0) * ftt / 0.9)
sw_ph = 2 * np.pi * np.cumsum(fsw) / SR
sweep = np.sin(sw_ph) * np.exp(-ftt / 0.30)
noise = rng.standard_normal(fling_n) * np.exp(-ftt / 0.16) * 0.30
fling = (sweep + noise) * np.minimum(1.0, ftt / 0.01) * 0.42
l_g, r_g = LP(fling, 0.62)
L[cs:cs + fling_n] += l_g
R[cs:cs + fling_n] += r_g

# the return: steps shrinking, the walk winding home — a descending glide
rn = int(3.4 * SR)
rt = np.arange(rn) / SR
fret = 2600.0 * np.exp(np.log(520.0 / 2600.0) * rt / 3.4)
ret_ph = 2 * np.pi * np.cumsum(fret) / SR
ret = np.sin(ret_ph) * np.exp(-rt / 0.9) * 0.16
l_rt, r_rt = LP(ret, 0.45)
L[cs:cs + rn] += l_rt
R[cs:cs + rn] += r_rt

# the scatter: the pole's four children, four directions — four soft bells
child_f = 440.0 * 3 ** (-0.25)              # |preimages| = 3^(-1/4)
for k, (tt, pp) in enumerate([(68.6, -0.72), (69.4, -0.32),
                              (70.2, 0.32), (71.0, 0.72)]):
    si = int(tt * SR)
    bn = int(1.1 * SR)
    bt = np.arange(bn) / SR
    bell = (np.sin(2 * np.pi * child_f * bt)
            + 0.4 * np.sin(2 * np.pi * 2 * child_f * bt))
    bell *= np.exp(-bt / 0.22) * 0.10
    l_c, r_c = LP(bell, pp)
    L[si:si + bn] += l_c
    R[si:si + bn] += r_c

# the landing: the crystal — the same 440 the pop flashed, now held
ld = 73.2
li = int(ld * SR)
land_n = N - li
lt = np.arange(land_n) / SR
land = (np.sin(2 * np.pi * 440 * lt) + 0.35 * np.sin(2 * np.pi * 880 * lt)
        + 0.15 * np.sin(2 * np.pi * 1320 * lt))
land_env = np.minimum(1.0, lt / 1.6) * 0.30
# bleeding to both ears — the crystal is the shared object
l_l, r_l = LP(land * land_env, 0.45)
L[li:] += l_l; R[li:] += r_l
L[li:] += 0.18 * land * land_env           # faint echo on the left
R[li:] += 0.10 * land * land_env

# ---------------------------------------------------------------- finish
# room floor, end fade, gentle limit
L += rng.standard_normal(N) * 0.0012
R += rng.standard_normal(N) * 0.0012
for x in (L, R):
    x[int(86.0 * SR):] *= np.linspace(1.0, 0.0, N - int(86.0 * SR)) ** 1.6
L = np.tanh(L * 1.5) * 0.9
R = np.tanh(R * 1.5) * 0.9
pcm = np.empty(2 * N, dtype=np.int16)
pcm[::2] = (L * 32767).astype(np.int16)
pcm[1::2] = (R * 32767).astype(np.int16)

with wave.open("/home/sprite/slop-salon-lou/assets/cut_heard.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/cut_heard.wav", T, "s")
