import sys

RULE, W, SEED, DIR, K, UPPER = (int(a) for a in sys.argv[1:7])
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
    counted = set()
    for x in range(W):
        t0 = WARM
        for t in range(WARM + 1, H + 1):
            if t == H or rows[t][x] != rows[t - 1][x]:
                length = t - t0
                if K <= length <= UPPER and rows[t0][x] == 0:
                    counted.add(x)
                t0 = t
    return counted


counted = run()
print(f"rule {RULE} W {W} seed {SEED} dir {DIR:+d} unmasked columns {len(counted)} odd {sum(x % 2 for x in counted)}")
best = []
for R in range(0, W // 2 + 1):
    cols = [x for x in counted if min(abs(x - SEED), W - abs(x - SEED)) <= R]
    odd = sum(x % 2 for x in cols)
    if len(cols) == 394:
        best.append((R, len(cols), odd))
    if R % 64 == 0 or (len(cols) == 394):
        print(f"R {R:4d} columns {len(cols):4d} odd {odd:4d}")
print("R giving 394 columns:", best)
