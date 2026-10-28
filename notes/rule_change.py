import sys

W = int(sys.argv[1]) if len(sys.argv) > 1 else 301
ROWS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
FROM = int(sys.argv[3]) if len(sys.argv) > 3 else 100
MASK = (1 << W) - 1
CENTRE = 1 << (W // 2)


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


def run(rule):
    prev2, prev = 0, CENTRE
    occupied = 0
    flips = rows = 0
    for t in range(1, ROWS):
        c = prev
        l = rot(c, 1)
        r = rot(c, W - 1)
        nxt = elem(rule, c, l, r) ^ prev2
        if t >= FROM:
            occupied |= nxt | c
            flips += bin(nxt ^ c).count("1")
            rows += 1
        prev2, prev = c, nxt
    area = bin(occupied).count("1")
    if area == 0 or rows == 0:
        return 0.0, area
    return flips / (area * rows), area


rows = [(r,) + run(r) for r in range(256)]
if "--csv" in sys.argv:
    print("rule,change,area")
    for r, s, a in rows:
        print(f"{r},{s:.4f},{a}")
else:
    for r, s, a in sorted(rows, key=lambda x: -x[1])[:16]:
        print(f"rule {r:3d}  change {s:.3f}  area {a}")
    print("---")
    for r in (30, 90, 94, 126, 14, 46, 84, 116, 182, 62):
        s, a = run(r)[0], run(r)[1]
        print(f"rule {r:3d}  change {s:.3f}  area {a}")
