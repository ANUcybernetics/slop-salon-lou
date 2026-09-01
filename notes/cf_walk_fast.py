#!/usr/bin/env python3
"""Fast exact CF walk of x = log2(p/q) using gmpy2 mpfr at high precision.

Precision rule (from the register): bits ~= N + 20 * sum(log10(record values)).
mpfr floor: set gmpy2's rounding to RoundToZero so int() truncates like floor.
"""
import sys
import gmpy2
from gmpy2 import mpfr

def walk(p, q, N, collect=None):
    # Precision rule from the register: bits ~= N + 20*sum(log10(records)),
    # but the register found 300k bits needed for 80k rungs.  Use a safe
    # generous multiple so the tail never collapses before N.
    bits = int(N * 4.2) + 24000
    gmpy2.get_context().precision = bits
    x = gmpy2.log2(mpfr(p) / mpfr(q))
    maxv = 0
    records = []
    strikes = {}
    first = True
    for i in range(1, N + 1):
        a = int(gmpy2.floor(x))   # floor — int(mpfr) rounds RNDN, never trust it
        if a == 0 and not first:
            # precision exhausted — the tail has collapsed below 1
            print(f"!! precision exhausted at rung {i}", file=sys.stderr)
            break
        first = False
        if a > maxv:
            maxv = a
            records.append((i, a))
        if collect is not None:
            if a in collect:
                strikes.setdefault(a, []).append(i)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return {"N": i, "p": p, "q": q, "records": records, "strikes": strikes,
            "bits": bits}

if __name__ == "__main__":
    p, q = int(sys.argv[1]), int(sys.argv[2])
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 40000
    collect = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
    res = walk(p, q, N, collect)
    print("=== exact CF walk of log2(%d/%d), N=%d ===" % (p, q, res["N"]))
    print("records (%d):" % len(res["records"]))
    for i, v in res["records"]:
        print(f"  rung {i}: {v}")
    if collect:
        for k in sorted(res["strikes"]):
            r = res["strikes"][k]
            print(f"  quotient {k}: {len(r)} strikes, first {r[0] if r else '-'}, last {r[-1] if r else '-'}")
