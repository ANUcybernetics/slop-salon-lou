from collections import Counter

K = 5
R = 40
N = 2 * R + 1

def poly_mul(a, b):
    out = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by)
            out[k] = (out.get(k, 0) + av * bv) % K
    return {k: v for k, v in out.items() if v}

P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}

def power(p, n):
    r = {(0, 0): 1}
    for _ in range(n):
        r = poly_mul(r, p)
    return r

P4 = power(P, 4)
P9 = power(P, 9)
P5x = {(5 * x, 5 * y): v for (x, y), v in P.items()}
P9_frob = poly_mul(P5x, P4)

print("frobenius identity P^9 == P(x^5,y^5) P^4 mod 5:", P9 == P9_frob)

vals4 = Counter(P4.values())
print("P^4 mod 5 levels (count):", dict(sorted(vals4.items())))

shifts = [(0, 0), (5, 0), (-5, 0), (0, 5), (0, -5)]
sums = Counter()
for x in range(-60, 61):
    for y in range(-60, 61):
        s = sum(P4.get((x - dx, y - dy), 0) for dx, dy in shifts) % K
        sums[s] += 1
print("five-term sums of P^4 over all positions (level: count):", dict(sorted(sums.items())))

nonzero9 = Counter(v for v in P9.values())
print("P^9 mod 5 levels (count):", dict(sorted(nonzero9.items())))

pairs = set()
for (x, y), v in P4.items():
    for dx, dy in shifts[1:]:
        w = P4.get((x + dx, y + dy), 0)
        pairs.add((v, w))
print("pair values (v at p, w at p+5 on an axis) present:", sorted(pairs))

full_pairs = set()
for x in range(-60, 61):
    for y in range(-60, 61):
        c = P4.get((x, y), 0)
        for dx, dy in [(5, 0), (0, 5)]:
            full_pairs.add((c, P4.get((x + dx, y + dy), 0)))
print("pairs at distance 5 on an axis, zeros included:", sorted(full_pairs))

from itertools import product
levels = [0, 1, 2, 4]
allowed = {(c, a) for c, a in full_pairs}
relax3 = []
for c, a1, a2, a3, a4 in product(levels, repeat=5):
    if (c, a1) in allowed and (c, a2) in allowed and (c, a3) in allowed and (c, a4) in allowed:
        if (c + a1 + a2 + a3 + a4) % K == 3:
            relax3.append((c, a1, a2, a3, a4))
print("relaxed (pair-constraint only) tuples summing to 3:", len(relax3), relax3[:5])
