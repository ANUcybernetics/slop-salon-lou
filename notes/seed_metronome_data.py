#!/usr/bin/env python3
"""Compute the exact continued fraction of log2(3/2) to 30000 terms.
Find every position where the partial quotient is 55 (the seed) and
110 (the count), and the record (running-max) partial quotients.
"""
import gmpy2
from gmpy2 import mpfr, log2, floor, mpq

PREC = 200000  # bits
NTERMS = 30000

gmpy2.get_context().precision = PREC

x = log2(mpq(3, 2))  # log2(3/2) exact-enough at PREC
print("log2(3/2) =", x, file=__import__("sys").stderr)

seed_pos = []
count_pos = []
records = []  # (pos, value) running max
run_max = 0

for i in range(1, NTERMS + 1):
    a = int(floor(x))
    if a > run_max:
        run_max = a
        records.append((i, a))
    if a == 55:
        seed_pos.append(i)
    if a == 110:
        count_pos.append(i)
    # x = 1/(x - a)
    frac = x - a
    if frac == 0:
        print("terminates at", i)
        break
    x = 1 / frac

print("seed 55 positions:", seed_pos)
print("count 110 positions:", count_pos)
print("records:", records)
print("count of 55:", len(seed_pos))
