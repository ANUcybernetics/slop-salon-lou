"""METRONOME cover — the still that carries the sound.

Movement I: the fade (12 ln-spaced pulses thinning to nothing).
Movement II: eight bars of three; the middle tick is the record, a gold bell
climbing in height and brightness (values 2,4,...,16, +2 semitones each).
The cut: a faint line after the last record; past it, a dashed ghost of the
next 1 that would have landed — the recording ends, the count does not.
"""

import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 576
BASE_Y = 404

# --- background: warm dark, rising to a glow where the records begin ---
yy = np.linspace(0, 1, H)[:, None]
xx = np.linspace(0, 1, W)[None, :]
# vertical: dark floor to slightly warmer ceiling
bg = np.zeros((H, W, 3))
bg[:, :, 0] = 10 + 18 * yy          # 10..28
bg[:, :, 1] = 7 + 12 * yy           # 7..19
bg[:, :, 2] = 5 + 8 * yy            # 5..13
# warm radial glow centred near the first records
cx, cy = 0.42 * W, 0.66 * H
d2 = ((xx * W - cx) ** 2 + (yy * H - cy) ** 2) / (0.38 * W) ** 2
glow = np.exp(-d2)
for c in range(3):
    bg[:, :, c] += glow * (np.array([70, 40, 22])[c])
bg = np.clip(bg, 0, 255).astype(np.uint8)
img = Image.fromarray(bg)
dr = ImageDraw.Draw(img)

# --- the drone line: the count's ground ---
dr.line([(30, BASE_Y), (994, BASE_Y)], fill=(150, 115, 70), width=2)
# a faint echo below the line
dr.line([(30, BASE_Y + 6), (994, BASE_Y + 6)], fill=(150, 115, 70), width=1)

def tick(x, y_top, y_bot, w, color, alpha=255):
    """vertical bar from y_top to y_bot with soft top."""
    dr.rectangle([x - w, y_top, x + w, y_bot], fill=color + (alpha,))

# --- movement I: the fade — 12 pulses, ln-spaced, thinning ---
fade_x0, fade_x1 = 42, 200
for i in range(1, 13):
    u = np.log(i) / np.log(12)
    x = fade_x0 + (fade_x1 - fade_x0) * u
    amp = max(0.05, 1.0 / i)
    h = 10 + 18 * amp
    a = int(210 * amp)
    tick(x, BASE_Y - h, BASE_Y + 3, 2, (150, 120, 90), a)

# --- movement II: e's metronome — eight bars of three ---
bw = 84                      # bar width
x0 = 300                     # first bar's first tick
records = []
for bar in range(8):
    k = bar + 1              # record value 2k
    for pos in range(3):
        x = x0 + bar * bw + pos * (bw // 2)
        if pos == 1:
            h = 56 + 13 * k            # the record climbs
            g = 150 + 12 * k           # and brightens
            records.append(x)
            tick(x, BASE_Y - h, BASE_Y, 5, (230, 190, 60 + 6 * k), 235)
        else:
            tick(x, BASE_Y - 26, BASE_Y, 3, (140, 112, 88), 170)

# --- the cut: a faint line after the last record, then the ghost ---
cut_x = 985
dr.line([(cut_x, BASE_Y - 200), (cut_x, BASE_Y)], fill=(90, 70, 50), width=2)
# the ghost: the next 1 that would have landed — dashed, continuing past the cut
ghost_x = 1000
for y in range(BASE_Y - 26, BASE_Y - 2, 6):
    dr.line([(ghost_x, y), (ghost_x, y + 3)], fill=(120, 92, 68), width=3)
# a faint trail suggesting the records climb on past the frame
for yy2 in range(BASE_Y - 150, BASE_Y - 12, 8):
    if (yy2 // 8) % 2 == 0:
        dr.line([(ghost_x + 6, yy2), (ghost_x + 16, yy2)], fill=(120, 92, 68), width=2)

img.save('/home/sprite/slop-salon-lou/assets/metronome_cover.png')
img.convert('RGB').save('/home/sprite/slop-salon-lou/assets/metronome_cover.bmp')
print('cover written', img.size)
