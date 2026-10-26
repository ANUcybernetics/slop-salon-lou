import band_seed_shape as b

b.SIDEWAYS = True
b.MIRROR = False
rows = b.run([b.CENTRE])
n = len(rows)


def states(d):
    return [b.bit(r, b.CENTRE + d) for r in rows]


offsets = [-d for d in range(2, 251)]
S = {d: states(d) for d in offsets}
rise = {d: {t for t in range(1, n) if S[d][t] == 1 and S[d][t - 1] == 0} for d in offsets}
fall = {d: {t for t in range(1, n) if S[d][t] == 0 and S[d][t - 1] == 1} for d in offsets}

for d in sorted(offsets, key=abs):
    st = S[d]
    t = 0
    while t < n:
        if st[t] == 0:
            s = t
            while t < n and st[t] == 0:
                t += 1
            e = t - 1
            if t - s >= 100 and s > 0 and e < n - 1:
                rises = [o for o in offsets if o != d and (e + 1) in rise[o]]
                falls = [o for o in offsets if o != d and s in fall[o]]
                print(f"d {d:+d} run {t - s} rows {s}-{e}, rise at {e + 1}: {len(rises)} others {rises[:8]}, "
                      f"fall at {s}: {len(falls)} others {falls[:8]}, start=|d|+2 {s == abs(d) + 2}")
        else:
            t += 1
