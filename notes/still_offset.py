import subprocess
import sys

RULE, W, DIR = 54, 2050, 1
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
H, WARM, K, UPPER = 1024, 256, 31, 254
SIZE, PAD = 800, 50
OUT = f"assets/still_offset_{SEED}.svg"


def step(cur):
    return [
        (RULE >> (4 * cur[(i - 1) % W] + 2 * cur[i] + cur[(i + 1) % W])) & 1
        for i in range(W)
    ]


def run():
    cur = [0] * W
    cur[SEED] = 1
    prev2 = [0] * W
    rows = [cur]
    for _ in range(H - 1):
        n = step(cur)
        side = [cur[(i - DIR) % W] for i in range(W)]
        nxt = [a ^ b ^ c for a, b, c in zip(n, side, prev2)]
        prev2, cur = cur, nxt
        rows.append(cur)
    points = []
    for x in range(W):
        off = (x - SEED + W // 2) % W - W // 2
        if abs(off) > WARM:
            continue
        t0 = WARM
        for t in range(WARM + 1, H + 1):
            if t == H or rows[t][x] != rows[t - 1][x]:
                length = t - t0
                if K <= length <= UPPER and rows[t0][x] == 0:
                    points.append((off, length))
                t0 = t
    return points


def xy(off, length):
    px = PAD + (off + WARM) / (2 * WARM) * (SIZE - 2 * PAD)
    py = SIZE - PAD - length / UPPER * (SIZE - 2 * PAD)
    return px, py


points = run()
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}">',
    f'<rect width="{SIZE}" height="{SIZE}" fill="white"/>',
    f'<line x1="{PAD}" y1="{SIZE-PAD}" x2="{SIZE-PAD}" y2="{SIZE-PAD}" stroke="black"/>',
    f'<line x1="{PAD}" y1="{PAD}" x2="{PAD}" y2="{SIZE-PAD}" stroke="black"/>',
]
for off, length in points:
    px, py = xy(off, length)
    parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2" fill="#333" fill-opacity="0.6"/>')
parts.append("</svg>")
with open(OUT, "w") as f:
    f.write("\n".join(parts))
subprocess.run(["convert", OUT, OUT.replace(".svg", ".png")], check=True)
print(f"still runs {len(points)} columns {len({o for o, _ in points})}")
