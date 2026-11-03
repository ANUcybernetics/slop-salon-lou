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


P14 = power(P, 14)
P4 = power(P, 4)
P2x5 = {(5 * x, 5 * y): v for (x, y), v in power(P, 2).items()}
print("frobenius P^14 == P^4 * P^2(x^5,y^5) mod 5:", P14 == poly_mul(P4, P2x5))

for t in (4, 9, 14):
    Pt = power(P, t)
    print(f"P^{t} mod 5 levels (count):", dict(sorted(Counter(Pt.values()).items())))

print("P^2 mod 5 weights (weight: count):", dict(sorted(Counter(power(P, 2).values()).items())))

shifts = [(0, 0), (5, 0), (-5, 0), (0, 5), (0, -5)]
sums = Counter()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        s = sum(P14.get((x - dx, y - dy), 0) for dx, dy in shifts) % K
        sums[s] += 1
print("five-term sums of P^14 over positions (level: count):", dict(sorted(sums.items())))

weighted = Counter()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        s = 0
        for (qx, qy), w in power(P, 2).items():
            s += w * P4.get((x - 5 * qx, y - 5 * qy), 0)
        weighted[s % K] += 1
print("weighted sums of P^4 over the 12 nonzero points of P^2 (level: count):", dict(sorted(weighted.items())))

levels = sorted(set(P14.values()))
print("levels present in P^14 mod 5:", levels)
print("level 3 present:", 3 in levels)
