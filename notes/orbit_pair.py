import sys

K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
CELL = 3
M = 1 << K


def f(y):
    return (5 * y * y + 3 * y + 7) % M


def step(x, y):
    return y, f(y) ^ x


x, y = 0, SEED
path = [(x, y)]
while True:
    x, y = step(x, y)
    if (x, y) == path[0]:
        break
    path.append((x, y))

n = len(path)
print(f"K={K} seed={SEED} period={n} of {M * M} states ({n / (M * M):.3f})", file=sys.stderr)

rects = []
for i in range(n):
    (ax, ay), (bx, by) = path[i], path[(i + 1) % n]
    if abs(ax - bx) > 1 or abs(ay - by) > 1:
        continue
    t = i / n
    light = 92 - 62 * t
    rects.append(
        f'<line x1="{ax * CELL + CELL / 2}" y1="{ay * CELL + CELL / 2}" '
        f'x2="{bx * CELL + CELL / 2}" y2="{by * CELL + CELL / 2}" '
        f'stroke="hsl(28,70%,{light:.1f}%)" stroke-width="1.2"/>'
    )

side = M * CELL
print(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{side}" height="{side}" viewBox="0 0 {side} {side}">'
    f'<rect width="{side}" height="{side}" fill="#f4efe6"/>'
    + "".join(rects)
    + "</svg>"
)
