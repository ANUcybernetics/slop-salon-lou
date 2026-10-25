import sys

import band_seed_shape as b


def post_live_dead(rows, x):
    states = [b.bit(r, x) for r in rows]
    best = (0, None, None)
    if 1 not in states:
        return best
    t = states.index(1)
    while t < len(states):
        if states[t]:
            t += 1
            continue
        s = t
        while t < len(states) and not states[t]:
            t += 1
        if t - s > best[0]:
            best = (t - s, s, t - 1)
    return best


if __name__ == "__main__":
    b.SIDEWAYS = "--no-sideways" not in sys.argv
    rows = b.run([b.CENTRE])
    print(f"sideways {b.SIDEWAYS}, seed {b.CENTRE}, rows 0-{b.H}")
    for side, sign in (("left", -1), ("right", 1)):
        runs = {d: post_live_dead(rows, b.CENTRE + sign * d) for d in range(2, 251)}
        long = {d: r for d, r in runs.items() if r[0] >= 100}
        worst = max(runs, key=lambda d: runs[d][0])
        print(f"  {side}: {len(long)} offsets with a dead run >=100 after going live; "
              f"max {runs[worst][0]} at |d|={worst}")
