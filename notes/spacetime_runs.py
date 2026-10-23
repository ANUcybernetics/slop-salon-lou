import subprocess

RULE, W, SEED, DIR = 54, 2050, 1025, 1
H, WARM, K, UPPER = 1024, 256, 31, 254
HALF = 256
OUT = "assets/spacetime_runs.ppm"
PNG = "assets/spacetime_runs.png"


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


def still_length(rows):
    grid = [[0] * (2 * HALF + 1) for _ in range(H)]
    for x in range(W):
        off = (x - SEED + W // 2) % W - W // 2
        if abs(off) > HALF:
            continue
        col = off + HALF
        t0 = 0
        for t in range(1, H + 1):
            if t == H or rows[t][x] != rows[t - 1][x]:
                length = t - t0
                if rows[t0][x] == 0 and K <= length <= UPPER and t > WARM:
                    for u in range(t0, t):
                        grid[u][col] = length
                t0 = t
    return grid


def colour(value, live):
    if value == 0:
        return (255, 255, 255) if not live else (40, 40, 40)
    f = (value - K) / (UPPER - K)
    r = int(255 * f)
    b = int(255 * (1 - f))
    return (r, 60, b)


rows = run()
grid = still_length(rows)
width = 2 * HALF + 1
with open(OUT, "wb") as f:
    f.write(f"P6\n{width} {H}\n255\n".encode())
    for t in range(H):
        for c in range(width):
            x = (SEED + c - HALF) % W
            r, g, b = colour(grid[t][c], rows[t][x] == 1)
            f.write(bytes((r, g, b)))
subprocess.run(["convert", OUT, PNG], check=True)
print(f"wrote {PNG} width {width} height {H}")
