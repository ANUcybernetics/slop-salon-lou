from collections import Counter, defaultdict

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
occ = set()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        c = P4.get((x, y), 0)
        arms = tuple(P4.get((x + dx, y + dy), 0) for dx, dy in shifts)
        occ.add((c,) + arms)

print("distinct occurring 5-tuples:", len(occ))
by_c = defaultdict(list)
for t in sorted(occ):
    by_c[t[0]].append(t)

for c in sorted(by_c):
    print(f"\ncentre {c}: {len(by_c[c])} tuples")
    for t in by_c[c]:
        print("  arms", t[1:], "sorted", tuple(sorted(t[1:])), "sum", sum(t) % K)

multisets = {c: Counter(tuple(sorted(t[1:])) for t in by_c[c]) for c in by_c}
print("\narm multisets per centre:")
for c in sorted(multisets):
    print(" ", c, "->", len(multisets[c]), "multisets")

print("\nsum mod K of tuple, by centre:")
for c in sorted(by_c):
    print(" ", c, Counter(sum(t) % K for t in by_c[c]))

print("\nlevels present in arms, by centre:")
for c in sorted(by_c):
    s = set(v for t in by_c[c] for v in t[1:])
    print(" ", c, sorted(s))
