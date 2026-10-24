import sys

RULE, W, DIR = 54, 2050, 1
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
H = 600
OFFS = [-2, -1, 0, 1, 2]


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

for o in OFFS:
    x = SEED + o
    flips = [t for t in range(1, H) if rows[t][x] != rows[t - 1][x]]
    print(f"offset {o:+d}: flips at {flips[:12]}{' ...' if len(flips) > 12 else ''}")
