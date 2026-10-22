import sys

RULE, W, SEED, DIR, K, UPPER, DEAD, MASK = (int(a) for a in sys.argv[1:9])
H, WARM = 1024, 256


def step(cur):
    return [
        (RULE >> (4 * cur[(i - 1) % W] + 2 * cur[i] + cur[(i + 1) % W])) & 1
        for i in range(W)
    ]


def run():
    cur = [0] * W
    cur[SEED] = 1
    prev2 = [0] * W
    rows = [cur]
    for _ in range(H - 1):
        n = step(cur)
        side = [cur[(i - DIR) % W] for i in range(W)] if DIR else [0] * W
        nxt = [a ^ b ^ c for a, b, c in zip(n, side, prev2)]
        prev2, cur = cur, nxt
        rows.append(cur)
    cols = set()
    for x in range(W):
        if MASK:
            d = abs(x - SEED)
            if min(d, W - d) > WARM:
                continue
        t0 = WARM
        for t in range(WARM + 1, H + 1):
            if t == H or rows[t][x] != rows[t - 1][x]:
                length = t - t0
                value = rows[t0][x]
                if K <= length <= UPPER and (not DEAD or value == 0):
                    cols.add(x)
                t0 = t
    return cols


cols = run()
odd = sum(1 for x in cols if x % 2)
frac = odd / len(cols) if cols else float("nan")
print(
    f"rule {RULE} W {W} seed {SEED} dir {DIR:+d} K {K} upper {UPPER} "
    f"dead {DEAD} mask {MASK} columns {len(cols):4d} odd {odd:4d} frac {frac:.3f}"
)
