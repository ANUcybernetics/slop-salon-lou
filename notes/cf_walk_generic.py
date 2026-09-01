#!/usr/bin/env python3
"""Exact continued-fraction walk of x = log2(p/q) for any rational p/q.

Oracle: x < P/Q  <=>  (p/q)^Q < 2^P  <=>  p^Q < q^Q * 2^P.  No floats.
Tail t = (c*x + d)/(e*x + f);  update on a = floor(t):
    (c',d',e',f') = (e, f, c-a*e, d-a*f).
Rung index: a_1 = rung 1.
"""
import sys, math, json

def make_cmp_lt(p, q):
    def cmp_lt(P, Q):
        return p ** Q < q ** Q * (2 ** P)
    return cmp_lt

def walk(p, q, N, collect=None):
    cmp_lt = make_cmp_lt(p, q)
    def tail_lt(c, d, e, f, A, B=1):
        u = B * c - A * e
        v = A * f - B * d
        if u == 0:
            return v > 0
        if u > 0:
            if v <= 0:
                return False
            return cmp_lt(v, u)
        else:
            if v >= 0:
                return True
            return not cmp_lt(-v, -u)
    def floor_tail(c, d, e, f):
        A = 1
        while not tail_lt(c, d, e, f, A):
            A *= 2
        lo, hi = A // 2, A
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if tail_lt(c, d, e, f, mid):
                hi = mid
            else:
                lo = mid
        return lo
    c, d, e, f = 1, 0, 0, 1
    maxv = 0
    records = []
    strikes = {}   # quotient -> [rungs]
    for i in range(1, N + 1):
        a = floor_tail(c, d, e, f)
        if a > maxv:
            maxv = a
            records.append((i, a))
        if collect is not None:
            for k in collect:
                if a == k:
                    strikes.setdefault(k, []).append(i)
        c, d, e, f = e, f, c - a * e, d - a * f
    return {"N": N, "ratio": f"{p}/{q}", "records": records,
            "strikes": strikes}

if __name__ == "__main__":
    p, q = int(sys.argv[1]), int(sys.argv[2])
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 40000
    collect = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
    res = walk(p, q, N, collect)
    print("=== exact CF walk of log2(%d/%d), N=%d ===" % (p, q, N))
    print("records:", res["records"])
    for k in sorted(res["strikes"]):
        r = res["strikes"][k]
        print(f"  quotient {k}: {len(r)} strikes, first {r[0] if r else '-'}, last {r[-1] if r else '-'}")
