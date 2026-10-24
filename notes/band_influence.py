import sys

RULE, W = 54, 2050
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
TARGET_OFF = int(sys.argv[3]) if len(sys.argv) > 3 else -1
TARGET_X = SEED + TARGET_OFF
TARGET_T = int(sys.argv[2]) if len(sys.argv) > 2 else 198
MASK = (1 << W) - 1


def rot_up(x):
    return ((x << 1) | (x >> (W - 1))) & MASK


def rot_down(x):
    return (x >> 1) | ((x & 1) << (W - 1))


def step(cur, prev2):
    left, right = rot_up(cur), rot_down(cur)
    return cur ^ (left | right) ^ left ^ prev2


def rows_upto(t_max):
    rows = [1 << SEED]
    prev, cur = 0, 1 << SEED
    for _ in range(t_max):
        prev, cur = cur, step(cur, prev)
        rows.append(cur)
    return rows


def bit(x, i):
    return (x >> (i % W)) & 1


rows = rows_upto(TARGET_T)
base = bit(rows[TARGET_T], TARGET_X)
print(f"seed {SEED}, target off {TARGET_X - SEED} row {TARGET_T}, value {base}")

for r in range(TARGET_T - 1, 1, -1):
    reach = TARGET_T - r
    infl = []
    for d in range(-reach, reach + 1):
        x = (TARGET_X + d) % W
        cur = rows[r] ^ (1 << x)
        prev, c = rows[r - 1], cur
        for _ in range(TARGET_T - r):
            prev, c = c, step(c, prev)
        if bit(c, TARGET_X) != base:
            infl.append(d + TARGET_X - SEED)
    near = [o for o in infl if o in (-1, -2)]
    print(f"row {r:3d}: n={len(infl):3d} min={min(infl) if infl else '-':>4} max={max(infl) if infl else '-':>4} offsets-1/-2 {near}")
