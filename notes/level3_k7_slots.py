from collections import defaultdict
import sys

K, C, Rr = (int(a) for a in sys.argv[1:4]) if len(sys.argv) > 3 else (7, 2, 4)
LEVEL = 3
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


PR = power(P, Rr)
terms = sorted(power(P, C).items())

print(f"t = {C}*{K} + {Rr} = {C * K + Rr}, mod {K}; carriers P^{C} spacing {K}, rest P^{Rr}")
print()

tuples = defaultdict(list)
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        vec = tuple(PR.get((x - K * qx, y - K * qy), 0) for (qx, qy), _ in terms)
        val = sum(w * v for ((qx, qy), w), v in zip(terms, vec)) % K
        if val == LEVEL:
            tuples[vec].append((x, y))

for vec, pos in sorted(tuples.items(), key=lambda kv: min(kv[1])):
    pos = sorted(pos)
    x, y = pos[0]
    print(f"cells {pos[:8]}{' ...' if len(pos) > 8 else ''} (n={len(pos)})")
    for ((qx, qy), w), v in zip(terms, vec):
        if v:
            k = (x - K * qx, y - K * qy)
            print(f"  slot q={(qx, qy)} w={w} P{Rr}{k}={v} product={w * v % K}")
    print()

print(f"distinct slot vectors: {len(tuples)}, cells: {sum(len(p) for p in tuples.values())}")
