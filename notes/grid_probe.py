#!/usr/bin/env python3
"""Probe the strike tables of several just intervals for grid structure.

Question: is the fifth's grid (seed 55 -> letters 55*odd, frame 55*even,
count 110 = seed's self-sum) a law of CF walks or a convention of the A1
reference?  For each interval, walk N rungs and report:
  - records (the crowns)
  - most-recurring quotients
  - which quotients in a band appear at all (sparse grid check)
  - for a candidate seed s: do its multiples 2s,3s,... appear?
"""
import sys
sys.path.insert(0, "/home/sprite/slop-salon-lou/notes")
from cf_walk_fast import walk

N = 50000
M = 600   # collect strikes for quotients up to M
intervals = [(5,4), (6,5), (9,8), (16,15)]

def show(p, q, N=N, M=M):
    res = walk(p, q, N, collect=range(1, M + 1))
    rec = res["records"]
    s = res["strikes"]
    print(f"=== log2({p}/{q}) N={res['N']} ===", flush=True)
    print(f"  records ({len(rec)}): {rec[:12]}{'...' if len(rec) > 12 else ''}", flush=True)
    top = sorted(s.items(), key=lambda kv: -len(kv[1]))[:8]
    print(f"  most-recurring: {[(k, len(v)) for k, v in top]}", flush=True)
    # sparse grid check: which quotients in 20..240 appear at all
    appear = [k for k in range(20, 241) if s.get(k)]
    print(f"  quotients 20..240 present ({len(appear)}): {appear}", flush=True)
    # doubles/triples check around small seeds
    for seed in [10, 20, 25, 30, 40, 50, 55, 60, 80, 100]:
        mults = [seed * m for m in range(1, 7)]
        got = {k: len(s.get(k, [])) for k in mults}
        if sum(1 for v in got.values() if v > 0) >= 3:
            print(f"  grid candidate seed {seed}: {got}", flush=True)
    return res

for (p, q) in intervals:
    show(p, q)
