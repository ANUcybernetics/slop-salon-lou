import sys

W, H, K, WARM, UPPER = 1024, 1024, int(sys.argv[1]), 256, int(sys.argv[2])
DIR = int(sys.argv[3])
DEAD = int(sys.argv[4])
SEEDS = [int(s) for s in sys.argv[5].split("+")]


def rule30(cur):
    return [cur[(i - 1) % W] ^ (cur[i] | cur[(i + 1) % W]) for i in range(W)]


def run():
    cur = [0] * W
    for s in SEEDS:
        cur[s] = 1
    prev2 = [0] * W
    rows = [cur]
    for _ in range(H - 1):
        n = rule30(cur)
        side = [cur[(i - DIR) % W] for i in range(W)] if DIR else [0] * W
        nxt = [a ^ b ^ c for a, b, c in zip(n, side, prev2)]
        prev2 = cur
        cur = nxt
        rows.append(cur)
    cols = set()
    for x in range(W):
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
print(f"K {K} upper {UPPER} dir {DIR:+d} dead {DEAD} seeds {sys.argv[5]:>8s} columns {len(cols):4d} odd {odd:4d} frac {frac:.3f}")
