import sys

RULE = 54
W = 2050
CENTRE = 1025
H = 460
MASK = (1 << W) - 1
LEFT_OFFS = list(range(-70, -247, -16))
RIGHT_OFFS = list(range(70, 247, 16))
OFFS = LEFT_OFFS
SIDEWAYS = True
MIRROR = False


def rot_up(x):
    return ((x << 1) | (x >> (W - 1))) & MASK


def rot_down(x):
    return (x >> 1) | ((x & 1) << (W - 1))


def step(cur, prev2):
    left, right = rot_up(cur), rot_down(cur)
    new = cur ^ (left | right) ^ prev2
    if SIDEWAYS:
        new ^= left
    if MIRROR:
        new ^= right
    return new


def run(seeds):
    start = 0
    for s in seeds:
        start |= 1 << s
    rows = [start]
    prev, cur = 0, start
    for _ in range(H):
        prev, cur = cur, step(cur, prev)
        rows.append(cur)
    return rows


def bit(x, i):
    return (x >> (i % W)) & 1


def band_end(rows, off):
    x = CENTRE + off
    start = abs(off) + 2
    if bit(rows[start], x) != 0:
        return None
    for t in range(start + 1, H + 1):
        if bit(rows[t], x) != bit(rows[t - 1], x):
            return t
    return H + 1


def report(seeds):
    rows = run(seeds)
    same = moved = live = 0
    detail = []
    for off in OFFS:
        e = band_end(rows, off)
        x = abs(off) + 198
        if e is None:
            live += 1
        elif e == x:
            same += 1
        else:
            moved += 1
            detail.append((off, e))
    return same, moved, live, detail


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--no-sideways" in args:
        SIDEWAYS = False
        args.remove("--no-sideways")
    if "--mirror" in args:
        MIRROR = True
        args.remove("--mirror")
    side = "left"
    if "--side" in args:
        i = args.index("--side")
        side = args[i + 1]
        del args[i:i + 2]
    OFFS = {"left": LEFT_OFFS, "right": RIGHT_OFFS}[side]
    for arg in args:
        seeds = [int(s) for s in arg.split(",")]
        same, moved, live, detail = report(seeds)
        print(f"sideways {SIDEWAYS} mirror {MIRROR} side {side} seeds {arg}: same {same}, moved {moved}, start-live {live} {detail}")
