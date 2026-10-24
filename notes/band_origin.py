import sys

RULE, W, DIR = 54, 2050, 1
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
H = 260
LO, HI = 185, 215


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


def changed(t, x):
    return t >= 1 and rows[t][x % W] != rows[t - 1][x % W]


print("changes at offsets 0..-6 (row numbers) in window", LO, HI)
for k in range(0, 7):
    x = SEED - k
    ts = [t for t in range(LO, HI + 1) if changed(t, x)]
    print(f"off -{k}: {ts}")

print()
print("backward walk from the first change at row 198 on offset -1 or -2")
starts = [(SEED - 1, 198), (SEED - 2, 198)]
for x0, t0 in starts:
    print(f"start x={x0} (off {x0 - SEED}) row {t0} changed={changed(t0, x0)}")
    x, t = x0, t0
    path = [(x - SEED, t)]
    while t > 2:
        cands = []
        if changed(t - 1, x - 1):
            cands.append(("left-diag", x - 1, t - 1))
        if changed(t - 1, x):
            cands.append(("same", x, t - 1))
        if changed(t - 1, x + 1):
            cands.append(("right", x + 1, t - 1))
        if changed(t - 2, x):
            cands.append(("memory", x, t - 2))
        if not cands:
            print(f"  dead end at off {x - SEED} row {t}")
            break
        label, x, t = cands[0]
        path.append((x - SEED, t, label))
    print("  path (off, row, via):", path)
    print()
