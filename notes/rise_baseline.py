import sys
sys.path.insert(0, '/home/sprite/slop-salon-lou/notes')
import band_seed_shape as b
b.SIDEWAYS = True
b.MIRROR = False
rows = b.run([b.CENTRE])
n = len(rows)
offsets = [-d for d in range(2, 251)]
S = {d: [b.bit(r, b.CENTRE + d) for r in rows] for d in offsets}
rc = [0] * n
for d in offsets:
    st = S[d]
    for t in range(1, n):
        if st[t] == 1 and st[t - 1] == 0:
            rc[t] += 1
vals = [rc[t] for t in range(100, 420)]
print("mean rises per row 100-419:", round(sum(vals) / len(vals), 1), "min", min(vals), "max", max(vals))
for t in (252, 268, 300, 348, 365, 396, 442, 454):
    print("rises at", t, rc[t])
