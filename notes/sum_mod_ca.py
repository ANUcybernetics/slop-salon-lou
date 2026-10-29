import random
import sys

W = int(sys.argv[1]) if len(sys.argv) > 1 else 128
STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 160
K = int(sys.argv[3]) if len(sys.argv) > 3 else 4
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 1

rng = random.Random(SEED)
if SEED == 0:
    g = [[1 if (x, y) == (W // 2, W // 2) else 0 for x in range(W)] for y in range(W)]
else:
    g = [[rng.randrange(K) for _ in range(W)] for _ in range(W)]
total0 = sum(map(sum, g)) % K

for _ in range(STEPS):
    g = [
        [
            sum(g[(y + dy) % W][(x + dx) % W] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) % K
            for x in range(W)
        ]
        for y in range(W)
    ]

total1 = sum(map(sum, g)) % K
print(
    f"W={W} steps={STEPS} K={K} seed={SEED}: total mod K {total0} -> {total1}, "
    f"predicted 9^steps * total0 = {pow(9, STEPS, K) * total0 % K}",
    file=sys.stderr,
)

sys.stdout.buffer.write(f"P5\n{W} {W}\n255\n".encode())
sys.stdout.buffer.write(bytes(v * 255 // (K - 1) for row in g for v in row))
