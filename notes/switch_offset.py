import subprocess
import sys

W, H, CELL, MARGIN = 301, 400, 2, 8
PAPER, INK, GREY = 244, 22, 150
SEED = int(sys.argv[1])
CAP = int(sys.argv[2])
M = (1 << W) - 1


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


def picture():
    seed = [0] * W
    seed[SEED] = 1
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
    subprocess.run(["convert", "-", "assets/switch_offset.png"], input=header + data, check=True)


def rot_l(x):
    return ((x << 1) | (x >> (W - 1))) & M


def rot_r(x):
    return (x >> 1) | ((x & 1) << (W - 1))


def bstep(cur, prev):
    if 2 * bin(cur).count("1") >= W:
        f = rot_l(cur) ^ (cur | rot_r(cur))
    else:
        f = rot_l(cur) ^ rot_r(cur)
    return f ^ prev


def period():
    tortoise = (1 << SEED, 0)
    hare = (bstep(tortoise[0], tortoise[1]), tortoise[0])
    power = lam = 1
    while tortoise != hare and lam < CAP:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = (bstep(hare[0], hare[1]), hare[0])
        lam += 1
    if tortoise == hare and lam < CAP:
        print("W", W, "seed", SEED, "period", lam)
    else:
        print("W", W, "seed", SEED, "no cycle within", CAP, "window")


picture()
period()
