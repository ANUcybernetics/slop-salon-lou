import sys
sys.path.insert(0, '/home/sprite/slop-salon-lou/notes')
from long_run_census import dead_run, MIN
from rarity import S, offsets

ENDS = [(-36, 347), (-38, 365), (-54, 442), (-56, 454)]


def long_ends(d, lo=100, hi=460, near=None, window=2):
    out = []
    for t in range(lo, hi):
        if near is not None and abs(t - near) > window:
            continue
        if S[d][t] == 1 and S[d][t - 1] == 0:
            length, last_live = dead_run(d, t - 1)
            if length >= MIN and last_live >= 0:
                out.append((t, length))
    return out


for d, row in ENDS:
    print(f"end d={d} row={row}")
    for nd in (d - 1, d + 1):
        hits = long_ends(nd, near=row)
        print(f"  neighbour {nd}: long ends within 2 rows of {row}: {hits}")
