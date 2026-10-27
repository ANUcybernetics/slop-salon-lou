import io
import contextlib
import subprocess
import sys

sys.path.insert(0, '/home/sprite/slop-salon-lou/notes')
with contextlib.redirect_stdout(io.StringIO()):
    from rarity import S, offsets, n

MIN = 100
ROW_LO, ROW_HI = 100, 459
K_MAX = 250
SX, SY = 3, 2
L, T = 70, 40
W = L + K_MAX * SX + 30
H = T + (ROW_HI - ROW_LO + 1) * SY + 50

PAPER = (0xfc, 0xfc, 0xfb)
GRID = (0xe1, 0xe0, 0xd9)
AXIS = (0xc3, 0xc2, 0xb4)
INK2 = (0x52, 0x51, 0x4e)
FAMILY = (0x2a, 0x78, 0xd6)
SINGLE = (0xeb, 0x68, 0x34)

canvas = bytearray(PAPER * (W * H))


def put(x, y, col):
    if 0 <= x < W and 0 <= y < H:
        i = 3 * (y * W + x)
        canvas[i:i + 3] = bytes(col)


def square(x, y, r, col):
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            put(x + dx, y + dy, col)


def hline(x0, x1, y, col):
    for x in range(x0, x1 + 1):
        put(x, y, col)


def vline(x, y0, y1, col):
    for y in range(y0, y1 + 1):
        put(x, y, col)


def px(k):
    return L + (K_MAX - k) * SX


def py(t):
    return T + (t - ROW_LO) * SY


x_left, x_right = px(K_MAX), px(2)
y_top, y_bot = py(ROW_LO), py(ROW_HI)

for row in range(ROW_LO, ROW_HI + 1, 50):
    hline(x_left, x_right, py(row), GRID)
for k in range(50, K_MAX + 1, 50):
    vline(px(k), y_top, y_bot, GRID)
hline(x_left, x_right, y_bot, AXIS)
vline(x_left, y_top, y_bot, AXIS)

for k in range(2, K_MAX + 1):
    t = k + 198
    if ROW_LO <= t <= ROW_HI:
        put(px(k), py(t), INK2)

counts = {'family': 0, 'single': 0}
rows_out = []
for d in offsets:
    st = S[d]
    for t in range(ROW_LO, ROW_HI + 1):
        if st[t] == 1 and st[t - 1] == 0:
            u = t - 1
            while u >= 0 and st[u] == 0:
                u -= 1
            length = (t - 1) - u
            if length >= MIN and u >= 0:
                k = -d
                on_family = length == 196 and t == k + 198
                kind = 'family' if on_family else 'single'
                counts[kind] += 1
                rows_out.append((d, t, length, kind))
                square(px(k), py(t), 2, FAMILY if on_family else SINGLE)

print('ends (100+ rows) in frame:', len(rows_out), counts)
for d, t, length, kind in sorted(rows_out, key=lambda r: (r[3], r[0])):
    if kind == 'single':
        print('single: offset', d, 'row', t, 'length', length)
fam_at = {d: (t, l) for d, t, l, kind in rows_out if kind == 'family'}
for d in (-70, -54, -38, -36, -56):
    print('offset', d, 'family end?', fam_at.get(d))

ppm = b'P6\n%d %d\n255\n' % (W, H) + bytes(canvas)
out = '/home/sprite/slop-salon-lou/assets/end_map.png'
labels = [
    '-annotate', '+%d+%d' % (L, 24), 'Long dead-run ends (100+ rows), seed 1025, sideways on',
    '-annotate', '+%d+%d' % (L, H - 12), 'offset from seed: -250 (left) to -2 (right)',
    '-annotate', '+8+%d' % (T + 6), 'row 100',
    '-annotate', '+8+%d' % (y_bot), 'row 459',
]
subprocess.run(['convert', 'ppm:-', '-font', 'DejaVu-Sans', '-pointsize', '13',
                '-fill', '#0b0b0b'] + labels + [out], input=ppm, check=True)
print('wrote', out, W, H)
