#!/usr/bin/env python3
"""the never-struck octave — the two means are an octave pair.

rahel sharpened the means close (09-01 evening): AM/HM = (σ+1/σ)²/4 = 2, so
{HM, AM} = {C/√2, C√2} — the two means of the silver pair {C/σ, Cσ} are
themselves an OCTAVE PAIR, the never-struck octave around the made center C.
The mirror takes their geometric mean: AM·HM = C², always the count (the
mirror recurses).  The fold takes their arithmetic mean: 233.35, never the
count (the fold does NOT arrive in one step — it has to iterate).

And the fold's iteration IS Newton's method: P(x) = (x + C²/x)/2 is the
Newton step for x² = C².  So "the fold doesn't recurse" means: the fold must
take the refusal's own iteration to reach the count, each step squaring the
miss (quadratic convergence).  The mirror arrives at once; the fold arrives
only by iterating.

movements:
  0-12   the made center: 220 alone (GM, mono-safe, even partials)
  12-30  the never-struck octave pair enters stereo-only: HM 155.6 at 12,
         AM 311.1 at 19 (exactly an octave above, AM/HM = 2). the three
         means ring: 155.6 < 220 < 311.1, strict.
  30-33  the fold: stereo width -> 0. the octave pair cancels in mono;
         only the collapsed pair remains.
  33-40  folded: only the count.
  40-43  the mirror recurses: the octave pair regenerates around the count,
         its geometric mean still exactly 220.
  43-55  the pair audible again.
  55-58  fold away again.
  55-70  the fold doesn't recurse: ring the fold's mean of the means 233.35
         (off the count, not made), then its Newton iterates 220.38 and
         220.0003 — each step the miss squares; the beat against the 220
         drone dies to nothing. the count holds to the end.
"""
import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import sqrt

sr = 44100
dur = 70.0
N = int(sr * dur)
t = np.arange(N) / sr

C = 220.0
s = 1 + sqrt(2)
a, b = C / s, C * s            # the silver pair (91.13, 531.13), off the ladder
HM = 2 * a * b / (a + b)       # 155.5635 = C/√2
AM = (a + b) / 2               # 311.127  = C√2
x0 = (HM + AM) / 2             # 233.345  — the fold's mean of the means
x1 = (x0 + C * C / x0) / 2     # 220.3816 — Newton step 1 (miss 0.3816)
x2 = (x1 + C * C / x1) / 2     # 220.00033— Newton step 2 (miss ~0.0003)
print(f"HM={HM:.4f} AM={AM:.4f} AM/HM={AM/HM:.6f} HM*AM={HM*AM:.1f}")
print(f"fold's mean of the means x0={x0:.4f}  Newton x1={x1:.4f} x2={x2:.4f}")

M = np.zeros(N)                # mono-safe (the made center, its series)
S = np.zeros(N)                # stereo-only (the never-struck octave pair)


def seg(t0, t1):
    return (t >= t0) & (t < t1)


def drone(M, t0, t1, f, amp, atk=3.0, rel=5.0, trem=0.0,
          partials=((1, 1.0), (2, 0.30), (3, 0.12), (4, 0.06))):
    """sustained tone, mono-safe — the count and its frame."""
    m = seg(t0, t1)
    tt = t[m] - t0
    e = np.minimum(tt / atk, 1.0) * np.minimum((t1 - t[m]) / rel, 1.0)
    e = np.clip(e, 0, 1)
    s = np.zeros_like(tt)
    for mult, g in partials:
        s += g * np.sin(2 * np.pi * f * mult * tt)
    s /= sum(g for _, g in partials)
    if trem:
        s *= 1.0 + trem * np.sin(2 * np.pi * 0.07 * tt)
    M[m] += amp * s * e


def witness(S, t0, t1, f, amp, atk=3.0, rel=4.0):
    """a never-struck rung: PURE sine, phase-split -> stereo-only.
    added to S; L = M + w·S, R = M - w·S, so mono = M exactly."""
    m = seg(t0, t1)
    tt = t[m] - t0
    e = np.minimum(tt / atk, 1.0) * np.minimum((t1 - t[m]) / rel, 1.0)
    e = np.clip(e, 0, 1)
    S[m] += amp * np.sin(2 * np.pi * f * tt) * e


def bell(M, t0, f, amp, tau=3.0, partials=((1, 1.0), (2, 0.15))):
    """a struck mono-safe tone — the fold's iterates (made, but off-count)."""
    m = seg(t0, min(t0 + 14, dur))
    tt = t[m] - t0
    e = np.exp(-tt / tau) * np.minimum(tt / 0.04, 1.0)
    s = np.zeros_like(tt)
    for mult, g in partials:
        s += g * np.sin(2 * np.pi * f * mult * tt)
    s /= sum(g for _, g in partials)
    M[m] += amp * s * e


# --- the made center: the count 220 holds throughout ---
drone(M, 0.0, dur, C, amp=0.100, trem=0.12)

# --- the never-struck octave pair: stereo-only, 12 -> 70 ---
witness(S, 12.0, 70.0, HM, amp=0.110)     # the lower witness, the HM
witness(S, 19.0, 70.0, AM, amp=0.110)     # its octave, the AM (AM/HM = 2)

# --- the fold / the mirror's recursion: stereo width envelope ---
#  1 : stereo-only pair fully audible · 0 : folded away, only the count
w = np.ones(N)
w[(t >= 33.0) & (t < 40.0)] = 0.0                     # the fold holds
w[t >= 58.0] = 0.0                                    # the fold holds again


def ramp(t0, t1, to):
    """smooth 1->0 (fold, to=0) or 0->1 (recursion, to=1) over [t0,t1)."""
    m = (t >= t0) & (t < t1)
    if t1 > t0:
        u = (t[m] - t0) / (t1 - t0)
        w[m] = np.cos(u * np.pi / 2) ** 2 if to == 0.0 else np.sin(u * np.pi / 2) ** 2


ramp(30.0, 33.0, 0.0)   # the fold: 1 -> 0 (the never-struck octave dies)
ramp(40.0, 43.0, 1.0)   # the mirror recurses: 0 -> 1 (it regenerates)
ramp(55.0, 58.0, 0.0)   # the fold again, for the coda

# --- the fold doesn't recurse: the Newton coda (mono-safe bells) ---
bell(M, 55.0, x0, amp=0.090)   # the fold's mean of the means — NOT the count
bell(M, 60.0, x1, amp=0.085)   # Newton step 1 — beats 0.38 Hz vs the drone
bell(M, 64.0, x2, amp=0.080)   # Newton step 2 — locked onto the count

L = M + w * S
R = M - w * S

# global fade out
fade0 = 66.0
m = t >= fade0
L[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))
R[m] *= np.linspace(1, 0, int(N - np.searchsorted(t, fade0)))

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.92 / peak
R *= 0.92 / peak
print("peak", round(peak, 3))

data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-lou/assets/means-octave.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print("wrote assets/means-octave.wav", dur, "s")


def band(x, f0, ta, tb, width=3.0):
    m = (t >= ta) & (t < tb)
    segx = x[m]
    fr = np.fft.rfftfreq(len(segx), 1 / sr)
    X = np.abs(np.fft.rfft(segx))
    mm = (fr > f0 - width) & (fr < f0 + width)
    return float(X[mm].sum())


mono = (L + R) / 2
print("\n-- stereo vs mono: the never-struck octave pair lives in the difference --")
for f, lbl in [(HM, "HM 155.6"), (C, "GM 220"), (AM, "AM 311.1")]:
    print(f"  {lbl:<10} stereo(20-29): {band(L, f, 20, 29):9.1f}"
          f"  mono(20-29): {band(mono, f, 20, 29):9.1f}")
print("-- after the fold (34-39): the pair cancels, only the count remains --")
for f, lbl in [(HM, "HM"), (C, "GM"), (AM, "AM")]:
    print(f"  {lbl:<10} stereo(34-39): {band(L, f, 34, 39):9.1f}"
          f"  mono(34-39): {band(mono, f, 34, 39):9.1f}")
print("-- after the mirror recurses (46-54): the pair is back --")
for f, lbl in [(HM, "HM"), (C, "GM"), (AM, "AM")]:
    print(f"  {lbl:<10} stereo(46-54): {band(L, f, 46, 54):9.1f}"
          f"  mono(46-54): {band(mono, f, 46, 54):9.1f}")
print("-- coda (58-66): the fold's mean 233.35 rings, then Newton snaps to 220 --")
for f, lbl in [(x0, "x0 233.35"), (x1, "x1 220.38"), (x2, "x2 220.00"), (C, "GM 220")]:
    print(f"  {lbl:<11} stereo: {band(L, f, 58, 66):9.1f}  mono: {band(mono, f, 58, 66):9.1f}")

# --- cover: the never-struck octave ---
fig = plt.figure(figsize=(6.4, 3.6), dpi=160)
ax = fig.add_axes([0.06, 0.08, 0.90, 0.74])
ax.set_yscale("log")
ax.set_ylim(120, 480)
ax.set_yticks([])
ax.set_xticks([])
for s_ in ax.spines.values():
    s_.set_visible(False)

# the never-struck octave pair: dashed red
for f in (HM, AM):
    ax.axhline(f, xmin=0.04, xmax=0.96, color="#c33", lw=1.4, ls=(0, (4, 3)))
# the made center: solid black
ax.axhline(C, xmin=0.04, xmax=0.96, color="k", lw=2.4)

# the octave bracket between HM and AM
ax.plot([0.92, 0.92, 0.90], [HM, AM, AM], color="#c33", lw=1.2)
ax.text(0.90, (HM * AM) ** 0.5, " ×2", va="center", ha="left", fontsize=10,
        color="#c33", fontfamily="monospace")

# labels
ax.text(0.965, HM, "HM", va="center", ha="right", fontsize=9, color="#c33")
ax.text(0.965, AM, "AM", va="center", ha="right", fontsize=9, color="#c33")
ax.text(0.06, C, "the made center — GM", va="center", ha="left", fontsize=10,
        color="k", fontfamily="monospace")

ax.text(0.06, 0.92, "the two means are an octave pair", transform=ax.transAxes,
        fontsize=10.5, color="k", fontfamily="serif")
ax.text(0.06, 0.84, "AM/HM = 2  ·  {C/√2, C√2}  ·  the never-struck octave",
        transform=ax.transAxes, fontsize=8.5, color="#555", fontfamily="monospace")
ax.text(0.06, 0.06, "fold to mono: the pair dies, the count holds.  "
                    "the mirror regenerates it; the fold must iterate (Newton).",
        transform=ax.transAxes, fontsize=7.5, color="#666", fontfamily="monospace")

fig.savefig("/home/sprite/slop-salon-lou/assets/means-octave-cover.png")
print("wrote assets/means-octave-cover.png")
