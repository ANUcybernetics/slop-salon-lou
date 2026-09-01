#!/usr/bin/env python3
"""The tail is one law; the records are five signatures.

Walk five just intervals to N=50000, save strike tables + records to JSON.
"""
import sys, json
sys.path.insert(0, "/home/sprite/slop-salon-lou/notes")
from cf_walk_fast import walk

N = 50000
M = 500
intervals = [(3,2), (5,4), (6,5), (9,8), (16,15)]

out = {}
for (p, q) in intervals:
    res = walk(p, q, N, collect=range(1, M + 1))
    out[f"{p}/{q}"] = {
        "records": res["records"],
        "strikes": {str(k): len(v) for k, v in res["strikes"].items()},
    }
    print(f"done {p}/{q}: {len(res['records'])} records", flush=True)

json.dump(out, open("/tmp/grid_tail.json", "w"))
print("saved /tmp/grid_tail.json", flush=True)
