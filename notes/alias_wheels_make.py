from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


W, H = 1024, 576
FPS = 24
DURATION = 10
BG = (12, 15, 22)
INK = (224, 221, 205)
DIM = (91, 99, 112)
CORAL = (236, 103, 91)
CYAN = (83, 202, 207)


def font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F18 = font(18)
F24 = font(24)
F34 = font(34)


def center_text(draw, xy, text, face, fill):
    box = draw.textbbox((0, 0), text, font=face)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1]), text, font=face, fill=fill)


def wheel(draw, cx, cy, radius, teeth, theta, color):
    # Repetition is the measurement: orientations separated by 2pi/teeth
    # are visually identical, although the motor itself has not changed.
    draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=DIM, width=2)
    for k in range(teeth):
        a = theta + 2 * math.pi * k / teeth
        r0 = radius * 0.28
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + radius * math.cos(a), cy + radius * math.sin(a)
        draw.line((x0, y0, x1, y1), fill=color, width=5)
        tx, ty = cx + (radius + 8) * math.cos(a), cy + (radius + 8) * math.sin(a)
        draw.ellipse((tx-3, ty-3, tx+3, ty+3), fill=color)
    draw.ellipse((cx-13, cy-13, cx+13, cy+13), fill=BG, outline=INK, width=3)


def main():
    out = Path("assets/alias-wheels-frames")
    out.mkdir(parents=True, exist_ok=True)
    frames = FPS * DURATION
    step = math.radians(14)  # each sampled frame: same physical motor step

    for i in range(frames):
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        theta = i * step
        wheel(d, 282, 286, 150, 12, theta, CORAL)
        wheel(d, 742, 286, 150, 20, theta, CYAN)

        center_text(d, (W/2, 34), "ONE MOTOR", F34, INK)
        center_text(d, (282, 474), "12-fold wheel", F24, CORAL)
        center_text(d, (742, 474), "20-fold wheel", F24, CYAN)
        center_text(d, (282, 512), "the clock reads forward", F18, DIM)
        center_text(d, (742, 512), "the clock reads backward", F18, DIM)

        # A small absolute marker gives the hidden motor angle without dominating
        # the two symmetry-quotiented readings.
        mx = W/2 + 28 * math.cos(theta)
        my = 92 + 28 * math.sin(theta)
        d.ellipse((W/2-31, 61, W/2+31, 123), outline=DIM, width=1)
        d.line((W/2, 92, mx, my), fill=INK, width=3)

        im.save(out / f"f{i:04d}.png", compress_level=2)


if __name__ == "__main__":
    main()
