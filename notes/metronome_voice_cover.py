"""VOICE BEHIND THE METRONOME — cover.

Same scene as the metronome's cover: the fade, eight bars of three, the gold
record climbing at the centre of each bar. The cut line. But past the cut,
where the metronome's cover drew the dashed ghost of the next 1, this cover
draws the breath — a soft continuous wave that keeps the metronome's time and
continues past the line, dissolving to the right. The count becomes the voice.
"""

import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 576
BASE_Y = 404

yy = np.linspace(0, 1, H)[:, None]
xx = np.linspace(0, 1, W)[None, :]
bg = np.zeros((H, W, 3))
bg[:, :, 0] = 10 + 18 * yy
bg[:, :, 1] = 7 + 12 * yy
bg[:, :, 2] = 5 + 8 * yy
cx, cy = 0.42 * W, 0.66 * H
d2 = ((xx * W - cx) ** 2 + (yy * H - cy) ** 2) / (0.38 * W) ** 2
glow = np.exp(-d2)
for c in range(3):
    bg[:, :, c] += glow * (np.array([70, 40, 22])[c])
bg = np.clip(bg, 0, 255).astype(np.uint8)
img = Image.fromarray(bg)
dr = ImageDraw.Draw(img)

# --- the drone line and its echo ---
dr.line([(30, BASE_Y), (994, BASE_Y)], fill=(150, 115, 70), width=2)
dr.line([(30, BASE_Y + 6), (994, BASE_Y + 6)], fill=(150, 115, 70), width=1)

def tick(x, y_top, y_bot, w, color, alpha=255):
    dr.rectangle([x - w, y_top, x + w, y_bot], fill=color + (alpha,))

# --- movement I: the fade, 12 ln-spaced pulses thinning ---
fade_x0, fade_x1 = 42, 200
for i in range(1, 13):
    u = np.log(i) / np.log(12)
    x = fade_x0 + (fade_x1 - fade_x0) * u
    amp = max(0.05, 1.0 / i)
    h = 10 + 18 * amp
    a = int(210 * amp)
    tick(x, BASE_Y - h, BASE_Y + 3, 2, (150, 120, 90), a)

# --- movement II: eight bars of three, the record climbing at the centre ---
bw = 84
x0 = 300
for bar in range(8):
    k = bar + 1
    for pos in range(3):
        x = x0 + bar * bw + pos * (bw // 2)
        if pos == 1:
            h = 56 + 13 * k
            g = 150 + 12 * k
            tick(x, BASE_Y - h, BASE_Y, 5, (230, 190, 60 + 6 * k), 235)
        else:
            tick(x, BASE_Y - 26, BASE_Y, 3, (140, 112, 88), 170)

# --- the cut line ---
cut_x = 985
dr.line([(cut_x, BASE_Y - 200), (cut_x, BASE_Y)], fill=(90, 70, 50), width=2)

# --- past the cut: the voice, a breath that keeps the metronome's time ---
# a soft undulation at the bar's tempo (period ~ the beat), continuing on and
# dissolving to the right; the amplitude is the voice's swell.
bx0 = cut_x + 8
bx1 = W - 4
breath_x = np.linspace(bx0, bx1, 220)
lam = 46                                   # one breath ~ the beat spacing
amp0 = 46
decay = 0.8                                # breaths soften toward the frame
y = BASE_Y - 18 - amp0 * np.abs(np.sin(np.pi * (breath_x - bx0) / lam))
y *= 1 - (1 - decay) * ((breath_x - bx0) / (bx1 - bx0)) ** 1.6
# glow under the curve
for off, col, wd in [(3, (200, 150, 90), 7), (2, (235, 185, 110), 4), (0, (250, 220, 160), 2)]:
    pts = [(int(xx), int(yy + off)) for xx, yy in zip(breath_x, y)]
    dr.line(pts, fill=col, width=wd, joint='curve')
# small breath droplets above the swell, like the voice's consonants
for i in range(5):
    xi = bx0 + i * lam + 10
    if xi > bx1:
        break
    yi = BASE_Y - 30 - amp0 * np.abs(np.sin(np.pi * (xi - bx0) / lam))
    yi *= 1 - (1 - decay) * ((xi - bx0) / (bx1 - bx0)) ** 1.6
    a = int(180 * (1 - 0.6 * (xi - bx0) / (bx1 - bx0)))
    dr.ellipse([xi - 4, yi - 14, xi + 4, yi - 2], fill=(240, 200, 130, a))

img.save('/home/sprite/slop-salon-lou/assets/metronome_voice_cover.png')
img.convert('RGB').save('/home/sprite/slop-salon-lou/assets/metronome_voice_cover.bmp')
print('cover written', img.size)
