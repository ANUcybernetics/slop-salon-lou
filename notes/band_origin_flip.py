import sys

RULE = 54
W = int(sys.argv[4]) if len(sys.argv) > 4 else 2050
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else W // 2
FLIP_T = int(sys.argv[2]) if len(sys.argv) > 2 else 198
FLIP_OFF = int(sys.argv[3]) if len(sys.argv) > 3 else 0
H = 460
MASK = (1 << W) - 1
OFFS = list(range(-70, -247, -16))


def rot_up(x):
    return ((x << 1) | (x >> (W - 1))) & MASK


def rot_down(x):
    return (x >> 1) | ((x & 1) << (W - 1))


def step(cur, prev2):
    left, right = rot_up(cur), rot_down(cur)
    return cur ^ (left | right) ^ left ^ prev2


def run(flip):
    rows = [1 << SEED]
    prev, cur = 0, 1 << SEED
    for t in range(1, H + 1):
        prev, cur = cur, step(cur, prev)
        if flip and t == FLIP_T:
            cur ^= 1 << (SEED + FLIP_OFF)
        rows.append(cur)
    return rows


def bit(x, i):
    return (x >> (i % W)) & 1


def band_end(rows, off):
    x = SEED + off
    start = abs(off) + 2
    if bit(rows[start], x) != 0:
        return None
    for t in range(start + 1, H + 1):
        if bit(rows[t], x) != bit(rows[t - 1], x):
            return t
    return H + 1


base = run(False)
pert = run(True)
moved = []
for off in OFFS:
    b, p = band_end(base, off), band_end(pert, off)
    print(f"off {off:5d}: base end {b}  flipped end {p}  expected {abs(off) + 198}")
    if b != p:
        moved.append(off)
print(f"flip (row {FLIP_T}, off {FLIP_OFF}); ends moved: {len(moved)} of {len(OFFS)} {moved}")
