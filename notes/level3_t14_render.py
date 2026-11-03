import sys

K = 5
T = 14
R = 20
HI = 3

P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}


def poly_mul(a, b):
    out = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by)
            out[k] = (out.get(k, 0) + av * bv) % K
    return {k: v for k, v in out.items() if v}


def power(p, n):
    r = {(0, 0): 1}
    for _ in range(n):
        r = poly_mul(r, p)
    return r


PT = power(P, T)
W = 2 * R + 1
hits = []
rows = []
for y in range(R, -R - 1, -1):
    row = []
    for x in range(-R, R + 1):
        v = PT.get((x, y), 0)
        if v == HI:
            hits.append((x, y))
            row.append(255)
        else:
            row.append(60 if v else 0)
    rows.append(row)

print(f"P^{T} mod {K}: level {HI} cells in window R={R}: {len(hits)}", file=sys.stderr)
sys.stdout.buffer.write(f"P5\n{W} {W}\n255\n".encode())
sys.stdout.buffer.write(bytes(v for row in rows for v in row))
