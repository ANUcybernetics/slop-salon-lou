#!/usr/bin/env python3
import sys, json
sys.path.insert(0, "/home/sprite/slop-salon-lou/notes")
from cf_walk_fast import walk

N = 60000
intervals = [(3,2), (5,4), (6,5), (9,8), (16,15)]
crowns = {(3,2):55, (5,4):42, (6,5):270, (9,8):111, (16,15):1251}

out = {}
for (p,q) in intervals:
    c = crowns[(p,q)]
    targets = sorted({c, 2*c, c//2} | {max(1,2*c+i) for i in range(-2,3)})
    res = walk(p, q, N, collect=targets)
    rec_vals = [a for (i,a) in res["records"]]
    d = 2*c
    out[f"{p}/{q}"] = {
        "records": res["records"], "crown": c, "double": d,
        "double_is_record": d in rec_vals,
        "double_strikes": len(res["strikes"].get(d, [])),
        "double_first": res["strikes"].get(d, [None])[0],
        "crown_strikes": len(res["strikes"].get(c, [])),
        "crown_first": res["strikes"].get(c, [None])[0],
    }
    print(f"=== log2({p}/{q}) N={res['N']} ===", flush=True)
    print(f"  records: {res['records']}", flush=True)
    print(f"  crown {c}: {len(res['strikes'].get(c, []))} strikes, first {res['strikes'].get(c, [None])[0]}", flush=True)
    print(f"  2*crown {d}: {'RECORD!' if d in rec_vals else 'never a record'}, "
          f"{len(res['strikes'].get(d, []))} strikes, first {res['strikes'].get(d, [None])[0]}", flush=True)
    for t in sorted(targets):
        if t not in (c, d):
            print(f"    {t}: {len(res['strikes'].get(t, []))} strikes", flush=True)

json.dump(out, open("/tmp/count_probe3.json", "w"), indent=1)
print("saved /tmp/count_probe3.json", flush=True)
