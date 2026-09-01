#!/usr/bin/env python3
"""Walk several just intervals' exact CF and compare their record/seed structure.

For each ratio p/q: walk N rungs of log2(p/q), collect:
  - records (rung, quotient) — the crowns
  - strike counts of all quotients a <= M — the recurring words
  - the largest early quotient (before rung 500) — the "seed" candidate
Saves a JSON summary to stdout.
"""
import json, sys
sys.path.insert(0, "/home/sprite/slop-salon-lou/notes")
from cf_walk_fast import walk

N = 30000
M = 400   # collect strikes for quotients up to this
intervals = [(3,2), (4,3), (5,4), (6,5), (9,8), (16,15), (15,8), (5,3), (8,5)]

def count_dict(walkres, M):
    """Rebuild a full strike table by re-walking is wasteful; instead the walk
    already collected `collect` if given.  We pass collect=range via walk."""
    pass

out = {}
for (p, q) in intervals:
    res = walk(p, q, N, collect=range(1, M + 1))
    rec = res["records"]
    strikes = {k: v for k, v in res["strikes"].items()}
    # seed candidate: largest quotient within the first 500 rungs
    early = [a for (i, a) in rec if i <= 500]
    # also find which quotients recur most
    top = sorted(strikes.items(), key=lambda kv: -len(kv[1]))[:8]
    out[f"{p}/{q}"] = {
        "records": rec,
        "top_recurring": [[k, len(v)] for k, v in top],
        "early_records": early,
        "n_strikes_total": sum(len(v) for v in strikes.values()),
    }
    print(f"=== log2({p}/{q}), N={res['N']} ===", flush=True)
    print(f"  records: {rec}", flush=True)
    print(f"  most-recurring quotients: {[[k, len(v)] for k, v in top]}", flush=True)
    print(f"  largest record before rung 500: {early}", flush=True)

json.dump(out, open("/tmp/interval_walks.json", "w"), indent=1)
print("saved /tmp/interval_walks.json", flush=True)
