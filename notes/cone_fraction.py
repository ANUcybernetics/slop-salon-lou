import re
import sys

lines = open(sys.argv[1]).read().splitlines()
T = int(re.search(r"row (\d+)", lines[0]).group(1))
fr = []
for L in lines[1:]:
    m = re.match(r"row\s+(\d+): n=\s*(\d+)", L)
    if not m:
        continue
    r, n = int(m.group(1)), int(m.group(2))
    if r == T - 1:
        continue
    fr.append(n / (2 * (T - r) + 1))
print(f"target row {T}: rows 2..{T-2}, mean moving fraction {sum(fr)/len(fr):.3f}, max {max(fr):.3f}")
