import subprocess

W, H, CELL, MARGIN = 301, 400, 2, 8
PAPER, INK, GREY = 244, 22, 150


def f_sparse(cur):
    n = len(cur)
    return [cur[(i - 1) % n] ^ cur[(i + 1) % n] for i in range(n)]


def f_dense(cur):
    n = len(cur)
    return [cur[(i - 1) % n] ^ (cur[i] | cur[(i + 1) % n]) for i in range(n)]


def step(cur, prev):
    dense = sum(cur) * 2 >= len(cur)
    f = f_dense if dense else f_sparse
    return [a ^ b for a, b in zip(f(cur), prev)], dense


seed = [0] * W
seed[W // 2] = 1
prev = [0] * W
cur = seed[:]
rows, flags = [cur], [False]
for _ in range(H - 1):
    nxt, dense = step(cur, prev)
    prev, cur = cur, nxt
    rows.append(cur)
    flags.append(dense)

width = MARGIN + W * CELL
pixels = [[PAPER] * width for _ in range(H * CELL)]
for y, (row, dense) in enumerate(zip(rows, flags)):
    for dy in range(CELL):
        for dx in range(MARGIN - 2):
            pixels[y * CELL + dy][dx] = GREY if dense else PAPER
    for x, v in enumerate(row):
        if v:
            for dy in range(CELL):
                for dx in range(CELL):
                    pixels[y * CELL + dy][MARGIN + x * CELL + dx] = INK
data = bytes(v for line in pixels for v in line)
header = f"P5\n{width} {H * CELL}\n255\n".encode()
subprocess.run(["convert", "-", "assets/switch.png"], input=header + data, check=True)
