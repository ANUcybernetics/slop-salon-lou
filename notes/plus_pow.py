import sys
from collections import defaultdict

PLUS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def power(K, t):
    poly = {(0, 0): 1}
    for _ in range(t):
        new = defaultdict(int)
        for (x, y), c in poly.items():
            for dx, dy in PLUS:
                new[(x + dx, y + dy)] += c
        poly = {k: v % K for k, v in new.items() if v % K}
    return poly


def digits(t, K):
    ds = []
    while t:
        ds.append(t % K)
        t //= K
    return ds


K = int(sys.argv[1])
for t in map(int, sys.argv[2:]):
    ds = digits(t, K)
    ones = sum(1 for d in ds if d == 1)
    binary_adjacent = K == 2 and "11" in bin(t)[2:]
    live = len(power(K, t))
    pred = 5 ** ones if all(d in (0, 1) for d in ds) else "-"
    print(f"K={K} t={t} digits(low->high)={ds} live={live} 5^ones={pred} adjacent11={binary_adjacent}")
