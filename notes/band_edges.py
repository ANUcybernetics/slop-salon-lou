import sys

RULE, W, DIR = 54, 2050, 1
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
H, WARM, K, UPPER = 1024, 256, 31, 254
TARGET = 196


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
        side = [cur[(i - DIR) % W] for i in range(W)]
        nxt = [a ^ b ^ c for a, b, c in zip(n, side, prev2)]
        prev2, cur = cur, nxt
        rows.append(cur)
    return rows


rows = run()


def band_runs():
    out = []
    for x in range(W):
        off = (x - SEED + W // 2) % W - W // 2
        if abs(off) > WARM:
            continue
        t0 = 0
        for t in range(1, H + 1):
            if t == H or rows[t][x] != rows[t - 1][x]:
                length = t - t0
                if length == TARGET and K <= length <= UPPER and rows[t0][x] == 0 and t > WARM:
                    out.append((off, x, t0, t))
                t0 = t
    return out


def show(x, t):
    return "".join(str(rows[t][(x + d) % W]) for d in range(-3, 4))


for off, x, start, end in sorted(band_runs(), key=lambda r: r[0]):
    print(f"off {off:5d}  start {start:4d} end {end:4d}  |off|+2={abs(off)+2}")
    print(f"   start: row {start-1}: {show(x, start-1)}  row {start}: {show(x, start)}")
    print(f"   end:   row {end-1}: {show(x, end-1)}  row {end}: {show(x, end)}")
    print(f"   left-neighbour changes at start: {rows[start][(x-1)%W] != rows[start-1][(x-1)%W]}"
          f"  at end: {rows[end][(x-1)%W] != rows[end-1][(x-1)%W]}")
    print(f"   right-neighbour changes at start: {rows[start][(x+1)%W] != rows[start-1][(x+1)%W]}"
          f"  at end: {rows[end][(x+1)%W] != rows[end-1][(x+1)%W]}")


def terms(t, x):
    cur, prev2 = rows[t - 1], rows[t - 2]
    n = (RULE >> (4 * cur[(x - 1) % W] + 2 * cur[x] + cur[(x + 1) % W])) & 1
    side = cur[(x - DIR) % W]
    return n, side, prev2[x]


if band_runs():
    off, x, start, end = sorted(band_runs(), key=lambda r: r[0])[-1]
    print(f"\nterms for off {off} (x={x}): (rule, side, memory) -> cell")
    for label, t in [("start", start), ("end", end)]:
        for r in range(t - 2, t + 2):
            if r < 2:
                continue
            print(f"  {label} row {r}: {terms(r, x)} -> {rows[r][x]}  left {rows[r][(x-1)%W]} right {rows[r][(x+1)%W]}")
