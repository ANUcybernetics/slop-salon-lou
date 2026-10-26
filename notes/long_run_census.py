import sys
sys.path.insert(0, '/home/sprite/slop-salon-lou/notes')
import band_seed_shape as b
from rarity import S, offsets, n

MIN = 100


def dead_run(d, end):
    t = end
    while t >= 0 and S[d][t] == 0:
        t -= 1
    return end - t, t


census = {}
for t in range(100, 460):
    ends = []
    for d in offsets:
        if S[d][t] == 1 and S[d][t - 1] == 0:
            length, last_live = dead_run(d, t - 1)
            if length >= MIN and last_live >= 0:
                ends.append((d, length))
    if ends:
        census[t] = ends

print("rows 100-459 with any long run ending:", len(census))
for t in sorted(census):
    ends = census[t]
    if len(ends) >= 2:
        print("row", t, "count", len(ends), ends)
print("count histogram:", sorted({len(v) for v in census.values()}))
for t in (346, 347, 364, 365):
    print("row", t, "long runs ending on the row before:", census.get(t, []))
