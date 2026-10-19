import subprocess

W, H, CELL = 301, 150, 2
PAPER, INK = 244, 22


def seed_one():
    r = [0] * W
    r[W // 2] = 1
    return r


def seed_two():
    r = [0] * W
    r[W // 3] = 1
    r[2 * W // 3] = 1
    return r


def left(r):
    return r[-1:] + r[:-1]


def right(r):
    return r[1:] + r[:1]


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def rule90(r):
    return xor(left(r), right(r))


def rule60(r):
    return xor(r, left(r))


def combined(r):
    return xor(rule90(r), rule60(r))


def run(step, first):
    out = [first]
    for _ in range(H - 1):
        out.append(step(out[-1]))
    return out


def run_second_order():
    out = [seed_one()]
    prev = [0] * W
    for _ in range(H - 1):
        cur = out[-1]
        out.append(xor(xor(left(cur), right(cur)), prev))
        prev = cur
    return out


panels = [
    run(combined, seed_one()),
    run(rule90, seed_two()),
    run_second_order(),
]

width = len(panels) * W + (len(panels) - 1) * 6
pixels = [[PAPER] * (width * CELL) for _ in range(H * CELL)]
for p, rows in enumerate(panels):
    x0 = p * (W + 6)
    for y, row in enumerate(rows):
        for x, v in enumerate(row):
            if v:
                for dy in range(CELL):
                    for dx in range(CELL):
                        pixels[y * CELL + dy][(x0 + x) * CELL + dx] = INK
data = bytes(v for line in pixels for v in line)
header = f"P5\n{width * CELL} {H * CELL}\n255\n".encode()
subprocess.run(["convert", "-", "assets/gears.png"], input=header + data, check=True)
