import sys

W = int(sys.argv[1])
CAP = int(sys.argv[2])
M = (1 << W) - 1


def rot_l(x):
    return ((x << 1) | (x >> (W - 1))) & M


def rot_r(x):
    return (x >> 1) | ((x & 1) << (W - 1))


def step(cur, prev):
    return (rot_l(cur) ^ (cur | rot_r(cur))) ^ prev


tortoise = (1 << (W // 2), 0)
hare = (step(tortoise[0], tortoise[1]), tortoise[0])
power = lam = 1
while tortoise != hare and lam < CAP:
    if power == lam:
        tortoise = hare
        power *= 2
        lam = 0
    hare = (step(hare[0], hare[1]), hare[0])
    lam += 1
if tortoise == hare and lam < CAP:
    print("W", W, "period", lam)
else:
    print("W", W, "no cycle within", CAP, "steps")
