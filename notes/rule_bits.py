import csv
import statistics as st
import subprocess
import sys

out = subprocess.run(
    [sys.executable, "notes/rule_change.py", "301", "300", "100", "--csv"],
    capture_output=True, text=True, check=True,
).stdout
rows = [(int(r["rule"]), float(r["change"]), int(r["area"])) for r in csv.DictReader(out.splitlines())]
live = [(r, c) for r, c, a in rows if a >= 50]


def corr(x, y):
    mx, my = st.mean(x), st.mean(y)
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def report(group, label, bits):
    ys = [c for _, c in group]
    print(label, len(group))
    for bit in bits:
        xs = [(r >> bit) & 1 for r, _ in group]
        on = [c for r, c in group if (r >> bit) & 1]
        off = [c for r, c in group if not (r >> bit) & 1]
        print(f"bit {bit}: corr {corr(xs, ys):+.3f}  on {st.mean(on):.3f} (n={len(on)})  off {st.mean(off):.3f} (n={len(off)})")


report(live, "all rules, area>=50:", range(8))
report([(r, c) for r, c in live if not r & 1], "bit0=0 rules:", range(1, 8))
