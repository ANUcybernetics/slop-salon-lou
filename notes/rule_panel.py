import sys

W = 301
ROWS = 240
MASK = (1 << W) - 1
CENTRE = 1 << (W // 2)
GAP = 8


def rot(x, k):
    return ((x << k) | (x >> (W - k))) & MASK


def elem(rule, c, l, r):
    out = 0
    for p in range(8):
        if not (rule >> p) & 1:
            continue
        a = l if p & 4 else ~l
        b = c if p & 2 else ~c
        d = r if p & 1 else ~r
        out |= a & b & d
    return out & MASK


def spacetime(rule):
    prev2, prev = 0, CENTRE
    rows = [prev]
    for _ in range(ROWS - 1):
        c = prev
        nxt = elem(rule, c, rot(c, 1), rot(c, W - 1)) ^ prev2
        rows.append(nxt)
        prev2, prev = c, nxt
    return rows


rules = [int(x) for x in sys.argv[1:]]
panels = [spacetime(r) for r in rules]
width = len(rules) * W + (len(rules) - 1) * GAP
out = sys.stdout.buffer
out.write(f"P5\n{width} {ROWS}\n255\n".encode())
for y in range(ROWS):
    line = bytearray()
    for i, p in enumerate(panels):
        if i:
            line += bytes([128]) * GAP
        row = p[y]
        line += bytes(255 if (row >> (W - 1 - x)) & 1 else 0 for x in range(W))
    out.write(bytes(line))
