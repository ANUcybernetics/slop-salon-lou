import subprocess

W, CELL = 301, 2
PAPER, INK = 244, 22


def step2(cur, prev):
    n = len(cur)
    return [cur[(i - 1) % n] ^ cur[(i + 1) % n] ^ prev[i] for i in range(n)]


seed = [0] * W
seed[W // 2] = 1
prev = [0] * W
cur = seed[:]
seen = {(tuple(cur), tuple(prev))}
rows = [cur]
while True:
    nxt = step2(cur, prev)
    prev, cur = cur, nxt
    key = (tuple(cur), tuple(prev))
    if key in seen:
        break
    seen.add(key)
    rows.append(cur)

H = len(rows)
pixels = [[PAPER] * (W * CELL) for _ in range(H * CELL)]
for y, row in enumerate(rows):
    for x, v in enumerate(row):
        if v:
            for dy in range(CELL):
                for dx in range(CELL):
                    pixels[y * CELL + dy][x * CELL + dx] = INK
data = bytes(v for line in pixels for v in line)
header = f"P5\n{W * CELL} {H * CELL}\n255\n".encode()
subprocess.run(["convert", "-", "assets/cycle.png"], input=header + data, check=True)
