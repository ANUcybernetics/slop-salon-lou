import sys
sys.path.insert(0, '/home/sprite/slop-salon-lou/notes')
import band_seed_shape as b
b.SIDEWAYS = True
b.MIRROR = False
rows = b.run([b.CENTRE])
n = len(rows)
offsets = [-d for d in range(2, 251)]
S = {d: [b.bit(r, b.CENTRE + d) for r in rows] for d in offsets}
rc = [0] * n
fc = [0] * n
for d in offsets:
    st = S[d]
    for t in range(1, n):
        if st[t] == 1 and st[t - 1] == 0:
            rc[t] += 1
        if st[t] == 0 and st[t - 1] == 1:
            fc[t] += 1
lo, hi = 100, n - 1
rise_vals = [rc[t] for t in range(lo, hi + 1)]
fall_vals = [fc[t] for t in range(lo, hi + 1)]


def frac_le(vals, x):
    return sum(1 for v in vals if v <= x) / len(vals)


def frac_ge(vals, x):
    return sum(1 for v in vals if v >= x) / len(vals)


def report(kind, t, vals, cnt):
    print(f"{kind} at {t}: count {cnt}, <= fraction {frac_le(vals, cnt):.3f}, >= fraction {frac_ge(vals, cnt):.3f}")


report("rises", 365, rise_vals, rc[365])
report("rises", 454, rise_vals, rc[454])
report("rises", 442, rise_vals, rc[442])
report("falls", 306, fall_vals, fc[306])
for t in (300, 306, 365, 442, 454):
    print("row", t, "rises", rc[t], "falls", fc[t])
for d in (-38, -54, -56):
    rises = sum(1 for t in range(1, n) if S[d][t] == 1 and S[d][t - 1] == 0)
    falls = sum(1 for t in range(1, n) if S[d][t] == 0 and S[d][t - 1] == 1)
    print(f"offset {d}: rises {rises}, falls {falls}, rows {n}")
top = sorted(range(lo, n), key=lambda t: -rc[t])[:12]
print("top rise rows (row, count):", [(t, rc[t]) for t in top])
def rising(t):
    return {d for d in offsets if S[d][t] == 1 and S[d][t - 1] == 0}
r442, r454 = rising(442), rising(454)
print("rises at 442 and 454 share", len(r442 & r454), "of", len(r442), "and", len(r454))
print("offsets rising at 454 only:", sorted(r454 - r442, key=abs)[:10])
print("offsets rising at 442 only:", sorted(r442 - r454, key=abs)[:10])
local = [rc[t] for t in range(360, 461)]
for t in (365, 442, 454):
    print("local 360-460: row", t, "count", rc[t], "<= frac", round(frac_le(local, rc[t]), 3), ">= frac", round(frac_ge(local, rc[t]), 3))
for d in range(-70, -247, -16):
    t = abs(d) + 198
    if t < n:
        print("band end offset", d, "row", t, "rises", rc[t], "local >= frac", round(frac_ge(local, rc[t]), 3))
print("rise at 347", rc[347], "local <= frac", round(frac_le(local, rc[347]), 3))
def dead_run_len(d, end):
    t = end
    while t >= 0 and S[d][t] == 0:
        t -= 1
    return end - t
for row, rs in ((454, r454), (442, r442)):
    lens = sorted(dead_run_len(d, row - 1) for d in rs)
    print("dead runs ending at", row - 1, "lengths (", len(lens), "):", lens)
