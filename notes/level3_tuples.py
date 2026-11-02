from collections import Counter
from itertools import product

K = 5
R = 60

def poly_mul(a, b):
    out = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by)
            out[k] = (out.get(k, 0) + av * bv) % K
    return {k: v for k, v in out.items() if v}

P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}
P4 = {(0, 0): 1}
for _ in range(4):
    P4 = poly_mul(P4, P)

shifts = [(5, 0), (-5, 0), (0, 5), (0, -5)]
occurring = Counter()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        c = P4.get((x, y), 0)
        arms = tuple(P4.get((x + dx, y + dy), 0) for dx, dy in shifts)
        occurring[(c,) + arms] += 1

levels = [0, 1, 2, 4]
pairs = set()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        c = P4.get((x, y), 0)
        for dx, dy in [(5, 0), (0, 5)]:
            pairs.add((c, P4.get((x + dx, y + dy), 0)))
relax = [t for t in product(levels, repeat=5)
         if all((t[0], a) in pairs for a in t[1:]) and sum(t) % K == 3]

occ_set = set(occurring)
print("distinct occurring 5-tuples:", len(occ_set))
print("occurring tuples summing to 3:", sum(1 for t in occ_set if sum(t) % K == 3))
print("relaxed sum-3 tuples:", len(relax))
print("relaxed sum-3 tuples that occur:", sum(1 for t in relax if t in occ_set))
print("occurring tuples with a value 3 anywhere:", sum(1 for t in occ_set if 3 in t))

def dist(a, b):
    return min(sum(1 for i in range(5) if a[i] != b[i]) for b in [b])

best = []
for t in relax:
    d = min(sum(1 for i in range(5) if t[i] != o[i]) for o in occ_set)
    best.append(d)
print("min Hamming distance from each relaxed sum-3 tuple to an occurring tuple:", Counter(best))

by_centre = Counter()
for t in occ_set:
    by_centre[t[0]] += 1
print("occurring tuples by centre level:", dict(sorted(by_centre.items())))
