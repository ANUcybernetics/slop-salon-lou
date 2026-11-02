from collections import Counter

R = 60
P = {(0, 0): 1, (1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1}
SHIFTS = [(5, 0), (-5, 0), (0, 5), (0, -5)]


def poly_mul(a, b):
    out = {}
    for (ax, ay), av in a.items():
        for (bx, by), bv in b.items():
            k = (ax + bx, ay + by)
            out[k] = out.get(k, 0) + av * bv
    return {k: v for k, v in out.items() if v}


def power(t):
    out = {(0, 0): 1}
    for _ in range(t):
        out = poly_mul(out, P)
    return out


for t in (4, 6, 9):
    Pt = power(t)
    pairs = Counter()
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            c = Pt.get((x, y), 0)
            if not c:
                continue
            for dx, dy in SHIFTS:
                a = Pt.get((x + dx, y + dy), 0)
                if a:
                    pairs[(c, a)] += 1
    sums_z = Counter((c + a) % 5 for c, a in pairs)
    mod5_pairs = Counter()
    for (c, a), n in pairs.items():
        cm, am = c % 5, a % 5
        if cm and am:
            mod5_pairs[(cm, am)] += n
    print(f"t={t}: distinct live pairs over Z {len(pairs)}")
    print(f"  (c+a) mod 5 over Z pairs: {dict(sums_z)}")
    print(f"  mod 5 live pairs (both residues nonzero): {sorted(mod5_pairs)}")
    print(f"  mod 5 residue sums of those: {sorted(Counter((c + a) % 5 for c, a in mod5_pairs))}")
    print(f"  Z pairs with sum 1 mod 5 only: {all((c + a) % 5 == 1 for c, a in pairs)}")
