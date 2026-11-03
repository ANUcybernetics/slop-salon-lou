import importlib.util, sys
sys.argv = ["x"]
K = 5
P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}
def mul(a, b):
    o = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by); o[k] = (o.get(k, 0) + av * bv) % K
    return {k: v for k, v in o.items() if v}
PT = {(0, 0): 1}
for _ in range(14):
    PT = mul(PT, P)
cells = sorted(k for k, v in PT.items() if v == 3)
print(len(cells))
print(cells)
