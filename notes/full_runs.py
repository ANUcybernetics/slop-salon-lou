import sys

SEED = int(sys.argv[1])
W = int(sys.argv[2]) if len(sys.argv) > 2 else 2050
RULE, DIR, H, WARM, K, UPPER = 54, 1, 1024, 256, 31, 254


def step(cur):
    return [
        (RULE >> (4 * cur[(i - 1) % W] + 2 * cur[i] + cur[(i + 1) % W])) & 1
        for i in range(W)
    ]


cur = [0] * W
cur[SEED] = 1
prev2 = [0] * W
rows = [cur]
for _ in range(H - 1):
    n = step(cur)
    side = [cur[(i - DIR) % W] for i in range(W)]
    nxt = [a ^ b ^ c for a, b, c in zip(n, side, prev2)]
    prev2, cur = cur, nxt
    rows.append(cur)

cols = set()
for x in range(W):
    t0 = 0
    for t in range(1, H + 1):
        if t == H or rows[t][x] != rows[t - 1][x]:
            length = t - t0
            if K <= length <= UPPER and rows[t0][x] == 0 and t > WARM:
                cols.add(x)
            t0 = t
print(f"seed {SEED} W {W} full-run columns {len(cols)} odd {sum(x % 2 for x in cols)}")
