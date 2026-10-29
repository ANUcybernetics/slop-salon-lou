import sys

W = int(sys.argv[1]) if len(sys.argv) > 1 else 151
STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 60
K = int(sys.argv[3]) if len(sys.argv) > 3 else 3
KERNEL = sys.argv[4] if len(sys.argv) > 4 else "cross"

if KERNEL == "cross":
    OFFS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
else:
    OFFS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]

g = [[0] * W for _ in range(W)]
g[W // 2][W // 2] = 1


def step(g):
    return [
        [sum(g[(y + dy) % W][(x + dx) % W] for dx, dy in OFFS) % K for x in range(W)]
        for y in range(W)
    ]


def rank_one(g):
    rows = [r for r in g if any(r)]
    if not rows:
        return True
    ref = rows[0]
    c0 = next(c for c, v in enumerate(ref) if v)
    for r in rows:
        k = r[c0] * pow(ref[c0], K - 2, K) % K
        if any((r[c] - k * ref[c]) % K for c in range(W)):
            return False
    return True


for t in range(1, STEPS + 1):
    g = step(g)
    if t % 5 == 0 or t <= 5:
        live = sum(1 for r in g for v in r if v)
        print(f"K={K} kernel={KERNEL} t={t} live={live} rank1={rank_one(g)}", file=sys.stderr)

if len(sys.argv) > 5 and sys.argv[5] == "pgm":
    sys.stdout.buffer.write(f"P5\n{W} {W}\n255\n".encode())
    sys.stdout.buffer.write(bytes(v * 255 // (K - 1) for row in g for v in row))
