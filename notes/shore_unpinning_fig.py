#!/usr/bin/env python3
"""The unpinning figure: at the shore s -> 1/2+, the ODD mode's boundary
value vanishes linearly, v(0) ~ -4 (s-1/2); the EVEN (count) mode stays
pinned at the boundary (|v(0)| = 1). The constant is 4 = 2^2, the same 4
as the eigenvalue slope (lambda_2 + 1 ~ 4(s-1/2)).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, "notes")
from shore_unpinning import spec

ss = [0.5015, 0.502, 0.503, 0.505, 0.51, 0.515, 0.52, 0.53, 0.55]
eps, v_odd, v_even = [], [], []
for s in ss:
    l1, l2, v2, x = spec(s)
    e = s - 0.5
    # even (count) mode, first eigenvector
    L, _ = __import__("shore_unpinning", fromlist=["build"]).build(s)
    ev, vecs = np.linalg.eig(L)
    order = np.argsort(-np.abs(ev))
    v1 = vecs[:, order[0]].real
    v1 = v1 / np.max(np.abs(v1))
    eps.append(e)
    v_odd.append(v2[0])
    v_even.append(abs(v1[0]))

eps = np.array(eps)
v_odd = np.array(v_odd)
v_even = np.array(v_even)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

# left: log-log, the linear unpinning vs the pinned even mode
ax = axes[0]
ax.loglog(eps, -v_odd, "o", color="tab:red", label=r"odd mode $|v_2(0)|$")
ax.loglog(eps, eps * 4, "r--", lw=1.5, label=r"$4\,(s-1/2)$")
ax.loglog(eps, v_even, "s", color="tab:blue", label=r"even mode $|v_1(0)|$")
ax.axhline(1, color="tab:blue", ls="--", lw=1)
ax.set_xlabel(r"$s-1/2$")
ax.set_ylabel(r"boundary value $|v(0)|$")
ax.set_title(r"at the shore the odd unpins, the even holds")
ax.legend()

# right: the mode shape near the shore, and the slope
l1, l2, v52, x = spec(0.52)
l1b, l2b, v70, x = spec(0.70)
ax = axes[1]
logx = np.log(1.0 / x)
ax.plot(logx, v52, color="tab:red", lw=2, label=r"$s=0.52$")
ax.plot(logx, v70, color="tab:orange", lw=2, label=r"$s=0.70$")
ax.set_title(r"the odd mode vs $\log(1/x)$: log-like, unpinning")
ax.set_xlabel(r"$\log(1/x)$  ($x\to0$ is left)")
ax.axvline(0, color="grey", ls="--", lw=1)
ax.legend()

fig.tight_layout()
fig.savefig("assets/shore_unpinning.png", dpi=140)
print("saved assets/shore_unpinning.png")
print("v(0)/eps for the odd mode:")
for e, v in zip(eps, v_odd):
    print(f"  eps={e:7.4f}  v(0)={v:8.4f}  v(0)/eps={v/e:7.3f}")
