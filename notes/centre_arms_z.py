from collections import Counter

R = 60

def poly_mul(a, b, mod=None):
    out = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by)
            out[k] = out.get(k, 0) + av * bv
    if mod:
        out = {k: v % mod for k, v in out.items()}
    return {k: v for k, v in out.items() if v}

P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}
P4 = {(0, 0): 1}
for _ in range(4):
    P4 = poly_mul(P4, P)

print("P^4 over Z support size:", len(P4), "max |x|+|y|:", max(abs(x) + abs(y) for x, y in P4))
print("P^4 over Z coefficient values:", sorted(set(P4.values())))

shifts = [(5, 0), (-5, 0), (0, 5), (0, -5)]
occ = Counter()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        c = P4.get((x, y), 0)
        arms = tuple(P4.get((x + dx, y + dy), 0) for dx, dy in shifts)
        occ[(c,) + arms] += 1

multi_arm = [t for t in occ if sum(1 for a in t[1:] if a) >= 2]
print("distinct 5-tuples over Z:", len(occ))
print("tuples over Z with two or more nonzero arms:", len(multi_arm))

pairs_both_nonzero = 0
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        for dx, dy in [(5, 0), (0, 5)]:
            if P4.get((x, y), 0) and P4.get((x + dx, y + dy), 0):
                pairs_both_nonzero += 1
print("centre-arm pairs at distance 5 with both nonzero over Z:", pairs_both_nonzero)

far = Counter()
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        c = P4.get((x, y), 0)
        if c == 0:
            continue
        for dx, dy in shifts:
            a = P4.get((x + dx, y + dy), 0)
            if a:
                far[(c, a)] += 1
print("live-centre, live-arm value pairs over Z (count):", len(far))
