import sys

W, H, K, WARM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])


def rule30(cur):
    n = len(cur)
    return [cur[(i - 1) % n] ^ (cur[i] | cur[(i + 1) % n]) for i in range(n)]


def still_hits(seed):
    cur = [0] * W
    cur[seed] = 1
    rows = [cur]
    for _ in range(H - 1):
        cur = rule30(cur)
        rows.append(cur)
    run = [0] * W
    even = odd = 0
    for t in range(1, H):
        for x in range(W):
            if rows[t][x] == rows[t - 1][x]:
                run[x] += 1
            else:
                run[x] = 0
            if run[x] >= K and t >= WARM:
                if x % 2 == 0:
                    even += 1
                else:
                    odd += 1
    return even, odd


seeds = [int(s) for s in sys.argv[5].split(",")]
for s in seeds:
    e, o = still_hits(s)
    tot = e + o
    frac = o / tot if tot else float("nan")
    print(f"W {W} seed {s:4d} ({'odd' if s % 2 else 'even'}) still hits {tot:6d} even {e:6d} odd {o:6d} odd-frac {frac:.3f}")
