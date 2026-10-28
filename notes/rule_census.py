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
    held = live = 0
    for t in range(1, ROWS):
        c = prev
        l = rot(c, 1)
        r = rot(c, W - 1)
        nxt = elem(rule, c, l, r) ^ prev2
        if t >= FROM:
            held += bin(nxt & ~(nxt ^ c) & MASK).count("1")
            live += bin(nxt).count("1")
        prev2, prev = c, nxt
    if live == 0:
        return 0.0, 0.0
    return held / live, live / ((ROWS - FROM) * W)


rows = [(r,) + run(r) for r in range(256)]
if "--csv" in sys.argv:
    print("rule,still,live")
    for r, s, d in rows:
        print(f"{r},{s:.4f},{d:.4f}")
else:
    for r, s, d in sorted(rows, key=lambda x: -x[1])[:12]:
        print(f"rule {r:3d}  still {s:.3f}  live {d:.3f}")
