import sys

W, H, K, WARM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])


def rule30(cur):
    n = len(cur)
    return [cur[(i - 1) % n] ^ (cur[i] | cur[(i + 1) % n]) for i in range(n)]


def run(seeds):
    cur = [0] * W
    for s in seeds:
        cur[s] = 1
    rows = [cur]
    for _ in range(H - 1):
        cur = rule30(cur)
        rows.append(cur)
    streak = [0] * W
    cols = set()
    hits = 0
    for t in range(1, H):
        for x in range(W):
            if rows[t][x] == rows[t - 1][x]:
                streak[x] += 1
            else:
                streak[x] = 0
            if streak[x] >= K and t >= WARM:
                cols.add(x)
                hits += 1
    odd_cols = sum(1 for x in cols if x % 2)
    odd_hits = 0
    return len(cols), odd_cols, hits


for spec in sys.argv[5].split(";"):
    seeds = [int(s) % W for s in spec.split("+")]
    ncols, ocols, hits = run(seeds)
    frac = ocols / ncols if ncols else float("nan")
    print(f"W {W} seeds {spec:>8s} still columns {ncols:4d} odd {ocols:4d} odd-frac {frac:.3f} hits {hits}")
