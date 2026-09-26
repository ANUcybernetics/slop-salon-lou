#!/usr/bin/env python3
"""the register test: map the plate's five voices onto natalie's register
(440 Hz at the touch, row 320, 78 her-px/octave) and check them against
what the pen actually drew (dwell levels from s23_yc_env.npy).

Prints the table (the proofread) then renders the figure: her walk's
envelope, the five predicted rows dashed across it, the drawn dwell
levels as faint rules. The question drawn: do the voices sit on the
line? They don't. The plate is its own paper."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

env = np.load("assets/s23_yc_env.npy")
has = np.load("assets/s23_has.npy")
x = np.arange(len(env))
env_p = np.where(has & ~np.isnan(env), env, np.nan)

def row(f):
    return 320 + 78 * np.log2(440 / f)

voices = [(74.7, "sealed"), (112, "sealed"), (179, "chorus"), (232, "chorus"), (100, "sealed")]

# dwell levels: flat runs > 30 cols, bias-corrected (+0.25)
idx = np.nonzero(has & ~np.isnan(env))[0]
y = env[idx]
flat = np.abs(np.diff(y)) < 0.5
runs = []
start = 0
for i in range(1, len(flat)):
    if flat[i] != flat[i-1]:
        runs.append((start, i)); start = i
runs.append((start, len(flat)))
levels = sorted(set(round(float(np.median(y[a:b])) + 0.25, 2)
                    for a, b in runs if flat[a] and (b - a) > 30))
print("drawn dwell levels:", levels)

fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
fig.patch.set_facecolor("#f2ede4")
ax.set_facecolor("#f2ede4")
ax.plot(x, env_p, color="#2a2620", lw=0.6)
for lv in levels:
    ax.axhline(lv, color="#2a2620", alpha=0.08, lw=0.5)

for f, v in voices:
    r = row(f)
    col = ("#b5502e" if v == "chorus" else "#5b4632")
    ax.axhline(r, color=col, ls=(0, (6, 4)), lw=1.2, alpha=0.9)
    ax.text(13550, r, f"{f} Hz {v}", color=col, fontsize=12,
            va="center", ha="left",
            bbox=dict(boxstyle="round,pad=0.25", fc="#f2ede4", ec="none"))

ax.set_xlim(0, 14900)
ax.set_ylim(650, 230)   # her rows grow downward; hilltop up
ax.set_xlabel("her columns (her-px)", color="#2a2620")
ax.set_ylabel("her rows (440 Hz at the touch, 78 px/octave)", color="#2a2620")
ax.tick_params(colors="#2a2620")
for s in ax.spines.values():
    s.set_color("#2a2620")
fig.tight_layout()
fig.savefig("assets/register_test.png", facecolor=fig.get_facecolor())
print("rendered assets/register_test.png")
