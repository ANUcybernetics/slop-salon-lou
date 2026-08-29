#!/usr/bin/env python3
"""Sharpen the shore mode: does the lambda_2 mode's boundary value v(0)
unpin (->0) as s -> 1/2+? And does the slope (lambda_2+1)/(s-1/2) settle?

Deformed GKW operator L_s, weight (n+x)^-2s. s=1 classical GKW, s=1/2 shore.
"""
import numpy as np


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
    L[:, 0] += (N + x) ** (1 - 2 * s) / (2 * s - 1)
    return L, x


def spec(s, N=6000, M=1000):
    L, x = build(s, N, M)
    ev, vecs = np.linalg.eig(L)
    order = np.argsort(-np.abs(ev))
    l1 = ev[order[0]].real
    real_idx = [i for i, e in enumerate(ev) if abs(e.imag) < 1e-7]
    i2 = min(real_idx, key=lambda i: abs(ev[i].real + 1))
    l2 = ev[i2].real
    v2 = vecs[:, i2].real
    v2 = v2 / np.max(np.abs(v2))
    return l1, l2, v2, x


ss = [0.5015, 0.502, 0.503, 0.505, 0.51, 0.515, 0.52, 0.53, 0.55, 0.6, 0.7]
print(f"{'s':>7} {'lam1':>8} {'lam2':>8} {'slope':>7} {'v(0)':>8} {'v(0)/eps^0.5':>12}")
for s in ss:
    l1, l2, v2, x = spec(s)
    eps = s - 0.5
    slope = (l2 + 1) / eps
    v0 = v2[0]
    print(f"{s:7.4f} {l1:8.4f} {l2:8.4f} {slope:7.3f} {v0:8.4f} {v0/np.sqrt(eps):12.4f}")
