import band_seed_shape as b

b.SIDEWAYS = True
b.MIRROR = False
rows = b.run([b.CENTRE])

for d in (38, -38):
    x = b.CENTRE + d
    states = [b.bit(r, x) for r in rows]
    runs = []
    t = 0
    while t < len(states):
        if states[t] == 0:
            s = t
            while t < len(states) and states[t] == 0:
                t += 1
            runs.append((t - s, s, t - 1))
        else:
            t += 1
    long = [r for r in runs if r[0] >= 100]
    print(f"offset {d:+d} (x={x}): runs >=100 rows (length, start, end):")
    for length, s, e in long:
        print(f"  {length} rows, {s} to {e}")
    first_live = states.index(1) if 1 in states else None
    print(f"  first live row: {first_live}")
    flips = [t for t in range(1, len(states)) if states[t] != states[t - 1]]
    print(f"  flip rows: {flips[:40]}")
    print(f"  196-family end for |d|: {abs(d) + 198}")
