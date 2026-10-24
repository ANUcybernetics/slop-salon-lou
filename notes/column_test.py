import sys

RULE, W = 54, 2050
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
END_T = int(sys.argv[2]) if len(sys.argv) > 2 else 268
COL_OFF = int(sys.argv[3]) if len(sys.argv) > 3 else -70
LO = int(sys.argv[4]) if len(sys.argv) > 4 else 72
MASK = (1 << W) - 1
COL_X = (SEED + COL_OFF) % W
END_X = COL_X


def rot_up(x):
    return ((x << 1) | (x >> (W - 1))) & MASK


def rot_down(x):
    return (x >> 1) | ((x & 1) << (W - 1))


def step(cur, prev2):
    left, right = rot_up(cur), rot_down(cur)
    return cur ^ (left | right) ^ left ^ prev2


def bit(x, i):
    return (x >> (i % W)) & 1


rows = [1 << SEED]
prev, cur = 0, 1 << SEED
for _ in range(END_T):
    prev, cur = cur, step(cur, prev)
    rows.append(cur)

base = bit(rows[END_T], END_X)
print(f"seed {SEED}, end offset -1 row {END_T}, value {base}")
print("column", COL_OFF, "values rows", LO, "to", END_T)
print("".join(str(bit(rows[t], COL_X)) for t in range(LO, END_T + 1)))

moved = []
for r in range(LO, END_T):
    c = rows[r] ^ (1 << COL_X)
    p = rows[r - 1]
    for _ in range(END_T - r):
        p, c = c, step(c, p)
    if bit(c, END_X) != base:
        moved.append(r)
print("flip at row moves end cell:", moved)
print("flips tested:", END_T - LO, "moved:", len(moved))
