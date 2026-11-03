from collections import Counter

K = 5
R = 60

P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}


def poly_mul(a, b):
    out = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by)
            out[k] = (out.get(k, 0) + av * bv) % K
    return {k: v for k, v in out.items() if v}


def power(p, n):
    r = {(0, 0): 1}
    for _ in range(n):
        r = poly_mul(r, p)
    return r


P4 = power(P, 4)
P2 = power(P, 2)
terms = sorted(P2.items())

cells = {}
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        vec = tuple(P4.get((x - 5 * qx, y - 5 * qy), 0) for (qx, qy), _ in terms)
        val = sum(w * v for ((qx, qy), w), v in zip(terms, vec)) % K
        if val:
            cells[(x, y)] = (val, vec)

weights = tuple(w for _, w in terms)
print("P^2 weights in fixed order (12 nonzero points):", weights)

by_level = {}
for pos, (val, vec) in cells.items():
    by_level.setdefault(val, []).append(vec)

for lev in sorted(by_level):
    vecs = by_level[lev]
    distinct = Counter(vecs)
    print(f"level {lev}: {len(vecs)} cells, {len(distinct)} distinct P^4 tuples")

l3 = by_level[3]
print("level-3 tuples, as P^4 values in weight order:")
for vec, n in Counter(l3).most_common():
    print(" ", vec, "x", n)

common = [min(v[i] for v in l3) == max(v[i] for v in l3) for i in range(len(weights))]
print("positions constant across all level-3 cells:", common)
print("P^4 value counts across level-3 tuples:",
      dict(sorted(Counter(v for vec in l3 for v in vec).items())))
