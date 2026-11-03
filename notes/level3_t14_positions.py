from collections import defaultdict

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

tuples = defaultdict(list)
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        vec = tuple(P4.get((x - 5 * qx, y - 5 * qy), 0) for (qx, qy), _ in terms)
        val = sum(w * v for ((qx, qy), w), v in zip(terms, vec)) % K
        if val == 3:
            tuples[vec].append((x, y))

for vec, pos in sorted(tuples.items(), key=lambda kv: kv[1][0]):
    xs = [p[0] for p in pos]
    ys = [p[1] for p in pos]
    print(vec, f"{len(pos)} cells", f"x {min(xs)}..{max(xs)}", f"y {min(ys)}..{max(ys)}", sorted(pos))
