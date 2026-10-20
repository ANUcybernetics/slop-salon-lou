import sys
from collections import Counter

W = int(sys.argv[1])
MASK = (1 << W) - 1


def rot_l(x):
    return ((x << 1) | (x >> (W - 1))) & MASK


def rot_r(x):
    return ((x >> 1) | (x << (W - 1))) & MASK


def f_sparse(c):
    return rot_l(c) ^ rot_r(c)


def f_dense(c):
    return rot_r(c) ^ (c | rot_l(c))


def nxt(cur, prev):
    f = f_dense if bin(cur).count("1") * 2 >= W else f_sparse
    return f(cur) ^ prev


def step(state):
    prev, cur = state
    return (cur, nxt(cur, prev))


N = 1 << (2 * W)
states = [(a, b) for a in range(1 << W) for b in range(1 << W)]
images = Counter(step(s) for s in states)
print("W", W, "states", N, "distinct images", len(images), "bijective", len(images) == N)

seen = set()
lengths = Counter()
transient = 0
for s in states:
    if s in seen:
        continue
    path = []
    t = s
    while t not in seen and t not in path:
        path.append(t)
        t = step(t)
    if t in path:
        cyc = path[path.index(t):]
        lengths[len(cyc)] += 1
        seen.update(cyc)
        seen.update(path)
    else:
        transient += 1
        seen.update(path)
print("transient starts", transient)
print("cycle count by length", dict(sorted(lengths.items())))
fixed = [s for s in states if step(s) == s]
print("fixed pairs", len(fixed), fixed[:8])
