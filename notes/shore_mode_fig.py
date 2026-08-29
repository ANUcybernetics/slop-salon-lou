#!/usr/bin/env python3
"""The shore mode: the lambda_2 eigenfunction of the deformed GKW operator
L_s (weight (n+x)^-2s) as s -> 1/2+.

Verified:
  * s=1 reproduces the classical operator: lam1=+1, lam2=-0.30366 (Wirsing).
  * (s-1/2)*lam1(s) -> 1/2  -- the count IS zeta(2s), residue 1/2.
  * lam2(s) -> -1 -- the sign reaches a negative count at the shore.
  * The lam2 eigenfunction is log-like, correlated with log(1/x), and its
    boundary value f(0) unpins (->0) as s -> 1/2.

Figure: two panels.
  left:  the lam2 eigenfunction at s=0.52 and s=0.7 vs log(1/x), showing the
         log-like shape and the unpinning of the boundary value.
  right: (s-1/2)*lam1(s) vs s (flat at 1/2) and (lam2+1)/(s-1/2) vs s
         (approaching ~4 with curvature).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
mp.mp.dps = 30
zeta = np.vectorize(lambda t: float(mp.zeta(t)), otypes=[float])


def build(s, N=6000, M=1000):
    x = (np.arange(M) + 0.5) / M
    L = np.zeros((M, M))
    for n in range(1, N + 1):
        npx = n + x
        y = 1.0 / npx
        w = npx ** (-2.0 * s)
        j = np.floor(y * M).astype(int)
        j = np.clip(j, 0, M - 2)
        t = y * M - j
        np.add.at(L, (np.arange(M), j), (1 - t) * w)
        np.add.at(L, (np.arange(M), j + 1), t * w)
    # Euler-Maclaurin tail into the f(0) column
    L[:, 0] += (N + x) ** (1 - 2 * s) / (2 * s - 1)
    return L, x


def spec(s):
    L, x = build(s)
    ev, vecs = np.linalg.eig(L)
    order = np.argsort(-np.abs(ev))
    l1 = ev[order[0]].real
    # lambda2: the eigenvalue nearest -1
    real_idx = [i for i, e in enumerate(ev) if abs(e.imag) < 1e-7]
    i2 = min(real_idx, key=lambda i: abs(ev[i].real + 1))
    l2 = ev[i2].real
    v2 = vecs[:, i2].real
    v2 = v2 / np.max(np.abs(v2))
    return l1, l2, v2, x


fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

# --- left: the mode ---
l1a, l2a, v52, x = spec(0.52)
l1b, l2b, v70, x = spec(0.70)
ax = axes[0]
logx = np.log(1.0 / x)
# plot vs log(1/x) so the x->0 region opens up
ax.plot(logx, v52, color="tab:red", lw=2, label=r"$s=0.52$")
ax.plot(logx, v70, color="tab:orange", lw=2, label=r"$s=0.70$")
ax.set_title(r"the $\lambda_2$ mode: log-like, unpinning at the shore")
ax.set_xlabel(r"$\log(1/x)$  ($x\to0$ is left)")
ax.set_ylabel("eigenfunction (normalised)")
ax.legend(loc="upper left")
ax.axvline(0, color="grey", ls="--", lw=1)

# --- right: the residues ---
ax = axes[1]
ss = np.array([0.505, 0.51, 0.52, 0.55, 0.6, 0.7, 0.8])
l1s = np.array([spec(s)[0] for s in ss])
l2s = np.array([spec(s)[1] for s in ss])
eps = ss - 0.5
ax.plot(ss, eps * l1s, "o-", color="tab:blue", label=r"$(s-1/2)\,\lambda_1$")
ax.axhline(0.5, color="tab:blue", ls="--", lw=1)
ax.plot(ss, (l2s + 1) / eps, "s-", color="tab:red",
        label=r"$(\lambda_2+1)/(s-1/2)$")
ax.axhline(4.0, color="tab:red", ls="--", lw=1)
ax.set_title(r"residues at the shore: 1/2, and a slope near 4")
ax.set_xlabel("s")
ax.set_ylim(0, 6)
ax.legend()

fig.tight_layout()
fig.savefig("assets/shore_mode.png", dpi=140)
print("saved assets/shore_mode.png")
print(f"s=0.52: lam1={l1a:.4f} lam2={l2a:.4f}  s=0.70: lam1={l1b:.4f} lam2={l2b:.4f}")
