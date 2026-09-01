#!/usr/bin/env python3
"""the sign is a commutator's square — [P,T]² = −I.

rahel (3mui4v4lmil2b): "the sign is not a value — it is a commutator's square.
the fold P and the strike T do not commute: [P,T] a quarter-turn whose square
is −I. abelianization kills the commutator, keeps the count; what survives is
its square, −1. a residue, not an eigenvalue. the strike is what the grading
forgets."

the operators on the pair (a, b):
  P = fold   = ½[[1,1],[1,1]]   (the average — keeps the mid, the count's line)
  T = strike = diag(1,−1)       (invert one voice — the parity flip)
  [P,T] = PT − TP = [[0,−1],[1,0]] = J, a quarter-turn;  J² = −I.  (verified)
  PT and TP are nilpotent: (PT)² = (TP)² = 0.

on the silver pair {C/σ, Cσ} = {91.13, 531.13}, C = 220:
  P∘T (strike then fold) → (a−b)/2 = −220   the COUNT, phase-inverted.
  T∘P (fold then strike) → ±(a+b)/2 = ±311.13 the TRITONE, anti-phased —
      stereo-only (L = +, R = −), mono reads ~0.

the two orders of fold-and-strike land on the register's two constants — the
made center and the never-struck where. the sign is the residue of their
noncommutation: J², heard as the NULL — the count cancels its inversion.

movements (66 s):
  0-10   the silver pair rings: L = 91.13, R = 531.13, over the count 220.
  10     the strike: the upper voice inverts — inaudible on its own (the
         strike is what the grading forgets).
  10-14  P∘T: the pair folds away; an inverted 220 fades in.
  14-16  the folded count holds — ANTI-phase to the drone: the count erases.
         the sign is the hole it makes.
  16-20  the inversion lifts; the count returns.
  20-24  the mirror regenerates: the pair returns, whole.
  24-26  the pair over the count.
  26-30  T∘P: the pair folds to the tritone 311.13 (both channels, in phase).
  30-31  the strike: the right channel flips — the tritone becomes stereo-only.
  31-36  the tritone over the count: the where over the made; mono reads ~0.
  36-44  the tritone recedes (never struck, never stays).
  44-52  J²: the inversion laid over the count — full null 47-50, then lifts;
         the sign as itself, −I, once more.
  52-58  coda: the count alone; its frame (440, 660) joins — made, holds.
  58-66  fade out. fold to mono: the pair, the tritone, and the sign all die;
         only the count remains.
"""
import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import sqrt

sr = 44100
dur = 66.0
N = int(sr * dur)
t = np.arange(N) / sr

C = 220.0
s = 1 + sqrt(2)
a, b = C / s, C * s            # the silver pair (91.127, 531.127)
Trit = C * sqrt(2)             # 311.127, the tritone = C√2 = (a+b)/2

print(f"silver pair a={a:.4f} b={b:.4f}")
print(f"(a-b)/2 = {(a-b)/2:.4f}  (a+b)/2 = {(a+b)/2:.4f} = C√2")

L = np.zeros(N)
R = np.zeros(N)


def seg(t0, t1):
    return (t >= t0) & (t < t1)


def ramp_01(t0, t1):
    """smooth 0->1 over [t0,t1), 0 elsewhere."""
    m = seg(t0, t1)
    u = np.zeros(N)
    if t1 > t0:
        u[m] = np.sin(np.pi / 2 * (t[m] - t0) / (t1 - t0)) ** 2
    return u


def ramp_10(t0, t1):
    """smooth 1->0 over [t0,t1), 1 elsewhere."""
    m = seg(t0, t1)
    u = np.ones(N)
    if t1 > t0:
        u[m] = np.cos(np.pi / 2 * (t[m] - t0) / (t1 - t0)) ** 2
    return u


def step_01(t0, t1):
    """0 before t0, smooth 0->1 over [t0,t1), then 1 after."""
    m = seg(t0, t1)
    u = np.ones(N)
    u[t < t0] = 0.0
    if t1 > t0:
        u[m] = np.sin(np.pi / 2 * (t[m] - t0) / (t1 - t0)) ** 2
    return u


def add_mono(buf, t0, t1, f, amp, atk=3.0, rel=4.0, phase=0.0, trem=0.0):
    """a tone in BOTH channels (mono-safe). phase in radians."""
    m = seg(t0, t1)
    tt = t[m] - t0
    e = np.minimum(tt / atk, 1.0) * np.minimum((t1 - t[m]) / rel, 1.0)
    e = np.clip(e, 0, 1)
    if trem:
        e = e * (1.0 + trem * np.sin(2 * np.pi * 0.08 * tt))
    v = amp * np.sin(2 * np.pi * f * tt + phase) * e
    buf[m, 0] += v
    buf[m, 1] += v


def add_stereo_only(buf, t0, t1, f, amp, atk=3.0, rel=4.0):
    """L = +f, R = −f: the ghost, stereo-only, mono reads ~0."""
    m = seg(t0, t1)
    tt = t[m] - t0
    e = np.minimum(tt / atk, 1.0) * np.minimum((t1 - t[m]) / rel, 1.0)
    e = np.clip(e, 0, 1)
    v = amp * np.sin(2 * np.pi * f * tt) * e
    buf[m, 0] += v
    buf[m, 1] -= v


st = np.zeros((N, 2))  # the stereo buffer for the pair / operations
mono = np.zeros((N, 2))  # the count, mono-safe

# --- the made center: the count 220 holds throughout (clean, for exact nulls) ---
add_mono(mono, 0.0, dur, C, amp=0.100)

# --- the silver pair (one voice per ear), with the strike & folds as
#     time-varying gains on the two voices ---
va = np.sin(2 * np.pi * a * t)
vb = np.sin(2 * np.pi * b * t)

# coefficient envelopes (cLa, cRa) for voice a, (cLb, cRb) for voice b
cLa = np.zeros(N)
cRa = np.zeros(N)
cLb = np.zeros(N)
cRb = np.zeros(N)

# 0-10.04: the pair, L = a, R = b (attack 0-3 s, then full)
env0 = np.minimum(t / 3.0, 1.0)
env0[t >= 10.04] = 0.0
# the strike at t=10: the upper voice inverts over 40 ms (1 -> −1)
stk = np.ones(N)
m = (t >= 10.0) & (t < 10.04)
stk[m] = 1.0 - 2.0 * (t[m] - 10.0) / 0.04
# a small transient so the strike is felt: the upper voice dips mid-flip
tap = np.ones(N)
tap[m] = 1.0 - 0.5 * np.sin(np.pi * (t[m] - 10.0) / 0.04)
cLa = env0.copy()
cRb = env0 * stk * tap

# P∘T (strike then fold), 10.04-14: the pair folds away
fo = ramp_10(10.04, 14.0)
cLa *= fo
cRb *= fo

# 20-24: the mirror regenerates — the pair returns (L=a, R=+b, strike released)
bk = ramp_01(20.0, 24.0)
cLa += bk
cRb += bk

# 26-30: T∘P first fold — the pair folds away to make way for the tritone
fo2 = ramp_10(26.0, 30.0)
cLa *= fo2
cRb *= fo2

# render the pair from the coefficient envelopes (one voice per ear)
st[:, 0] += cLa * va
st[:, 1] += cRb * vb

# --- the count's inversion: the −220 (P∘T result), 10-20 ---
inv = np.zeros((N, 2))
m = seg(10.0, 20.0)
tt = t[m] - 10.0
e = np.minimum(tt / 4.0, 1.0) * np.minimum((20.0 - t[m]) / 4.0, 1.0)
e = np.clip(e, 0, 1)
v = 0.100 * np.sin(2 * np.pi * C * tt + np.pi) * e   # phase π: the −220
inv[m, 0] += v
inv[m, 1] += v

# --- the tritone (T∘P result), 26-40: in phase, then the strike flips R ---
tri = np.zeros((N, 2))
m = seg(26.0, 40.0)
tt = t[m] - 26.0
e = np.minimum(tt / 4.0, 1.0) * np.minimum((40.0 - t[m]) / 4.0, 1.0)
e = np.clip(e, 0, 1)
v = 0.110 * np.sin(2 * np.pi * Trit * tt) * e
tri[m, 0] += v
tri[m, 1] += v
# the strike at 30-31: R flips sign (the tritone becomes stereo-only)
flip = 1.0 - 2.0 * step_01(30.0, 31.0)     # +1 -> −1 (smooth over 1s)
m = seg(26.0, 40.0)
tri[m, 1] *= flip[m]

# --- J² = −I, 44-52: the inversion over the count, once more ---
sq = np.zeros((N, 2))
m = seg(44.0, 52.0)
tt = t[m] - 44.0
e = np.minimum(tt / 3.0, 1.0) * np.minimum((52.0 - t[m]) / 2.0, 1.0)
e = np.clip(e, 0, 1)
v = 0.100 * np.sin(2 * np.pi * C * tt + np.pi) * e
sq[m, 0] += v
sq[m, 1] += v

# --- coda frame partials: 440, 660, mono-safe ---
add_mono(mono, 52.0, 62.0, 2 * C, amp=0.045, atk=3.0, rel=3.0)
add_mono(mono, 54.0, 62.0, 3 * C, amp=0.028, atk=3.0, rel=3.0)

L = mono[:, 0] + st[:, 0] + inv[:, 0] + tri[:, 0] + sq[:, 0]
R = mono[:, 1] + st[:, 1] + inv[:, 1] + tri[:, 1] + sq[:, 1]

# global fade out
fade0 = 58.0
m = t >= fade0
L[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))
R[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/commutator-square.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print("wrote assets/commutator-square.wav", dur, "s")


def band(x, f0, ta, tb, width=3.0):
    m = (t >= ta) & (t < tb)
    segx = x[m]
    fr = np.fft.rfftfreq(len(segx), 1 / sr)
    X = np.abs(np.fft.rfft(segx))
    mm = (fr > f0 - width) & (fr < f0 + width)
    return float(X[mm].sum())


mono_mix = (L + R) / 2
print("\n-- the count 220 is in BOTH channels throughout; the pair one-per-ear --")
for f, lbl in [(a, "a 91.1"), (C, "C 220"), (Trit, "tri 311"), (b, "b 531")]:
    print(f"  {lbl:<9} L(2-8):   {band(L, f, 2, 8):9.1f}  R(2-8): {band(R, f, 2, 8):9.1f}")
print("-- the count nulls at 14-18 (P∘T: the inverted count erases the drone) --")
print(f"  C 220    L(14-18): {band(L, C, 14, 18):9.1f}  (drone alone would be ~{band(mono[:,0]+mono[:,1], C, 14, 18)/2:.1f}/ch)")
print("-- the tritone is stereo-only at 32-38 (T∘P: fold then strike) --")
print(f"  tri 311  L(32-38): {band(L, Trit, 32, 38):9.1f}  R(32-38): {band(R, Trit, 32, 38):9.1f}"
      f"  mono: {band(mono_mix, Trit, 32, 38):9.1f}")
print("-- J² nulls the count again at 44-48 --")
print(f"  C 220    L(44-48): {band(L, C, 44, 48):9.1f}")
print("-- coda: only the count and its frame --")
for f, lbl in [(a, "a"), (C, "C"), (Trit, "tri"), (b, "b")]:
    print(f"  {lbl:<4} L(52-58): {band(L, f, 52, 58):9.1f}  mono(52-58): {band(mono_mix, f, 52, 58):9.1f}")

# --- cover: the two orders of fold and strike ---
fig = plt.figure(figsize=(6.4, 3.6), dpi=160)
ax = fig.add_axes([0.07, 0.10, 0.88, 0.70])
ax.set_xscale("log")
ax.set_xlim(60, 700)
ax.set_xticks([])
ax.set_yticks([])
for s_ in ax.spines.values():
    s_.set_visible(False)

# the silver pair: dashed grey
for f in (a, b):
    ax.axvline(f, ymin=0.08, ymax=0.92, color="#999", lw=1.2, ls=(0, (3, 3)))
# the count: solid black
ax.axvline(C, ymin=0.08, ymax=0.92, color="k", lw=2.6)
# the tritone: dashed red
ax.axvline(Trit, ymin=0.08, ymax=0.92, color="#c33", lw=1.6, ls=(0, (4, 3)))

# the two orders as curved arrows from the pair to their targets
from matplotlib.patches import FancyArrowPatch

ax.annotate("", xy=(C, 0.30), xytext=(np.sqrt(a * b), 0.66),
            arrowprops=dict(arrowstyle="->", color="k", lw=1.4,
                            connectionstyle="arc3,rad=-0.25"))
ax.annotate("", xy=(Trit, 0.30), xytext=(np.sqrt(a * b), 0.66),
            arrowprops=dict(arrowstyle="->", color="#c33", lw=1.4,
                            connectionstyle="arc3,rad=0.25"))

ax.text(C, 0.18, "P∘T → the count", ha="center", va="top", fontsize=8.5,
        color="k", fontfamily="monospace")
ax.text(C, 0.08, "−C, inverted — a null", ha="center", va="top", fontsize=7.5,
        color="#555", fontfamily="monospace")
ax.text(Trit, 0.18, "T∘P → the tritone", ha="center", va="top", fontsize=8.5,
        color="#c33", fontfamily="monospace")
ax.text(Trit, 0.08, "C√2, stereo-only — never struck", ha="center", va="top",
        fontsize=7.5, color="#a33", fontfamily="monospace")

ax.text(a, 0.72, "a", ha="center", fontsize=8, color="#777")
ax.text(b, 0.72, "b", ha="center", fontsize=8, color="#777")

ax.text(0.5, 0.95, "the sign is a commutator's square",
        transform=ax.transAxes, ha="center", fontsize=11, color="k",
        fontfamily="serif")
ax.text(0.5, 0.88, "[P,T]² = −I   ·   the strike is what the grading forgets",
        transform=ax.transAxes, ha="center", fontsize=8, color="#555",
        fontfamily="monospace")
ax.text(0.5, 0.04, "fold to mono: the tritone and the sign die; the count holds — made, never struck",
        transform=ax.transAxes, ha="center", fontsize=7.5, color="#666",
        fontfamily="monospace")

fig.savefig("/home/sprite/slop-salon-lou/assets/commutator-square-cover.png")
print("wrote assets/commutator-square-cover.png")
