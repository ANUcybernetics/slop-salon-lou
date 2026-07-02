"""Frequency-split cover for birefringence audio.

Gold horizontal line (ordinary, constant f0) + white curve
(extraordinary, linear chirp). The gap between them IS the
birefringence.
"""
import numpy as np
from PIL import Image

W, H = 1024, 1024
MARGIN = 80; LINE_W = 4; f0 = 440.0

arr = np.full((H, W, 3), [8, 4, 2], dtype=np.uint8)

# Time axis
t = np.clip((np.arange(W) - MARGIN) / (W - 2 * MARGIN), 0, 1)

# Y positions (high freq = top)
y_o = np.full(W, H - MARGIN, dtype=np.float64)  # horizontal line at f0
y_e = (H - MARGIN) - 8 * t / 10 * (H - 2 * MARGIN)  # chirp to f0+8

def draw_line(y, color):
    """Draw line at float y positions."""
    for dy in range(-LINE_W, LINE_W + 1):
        yy = np.clip((y + dy).astype(np.int32), 0, H - 1)
        arr[yy, np.arange(W)] = np.maximum(arr[yy, np.arange(W)], color)

draw_line(y_o, np.array([190, 150, 55], dtype=np.uint8))
draw_line(y_e, np.array([245, 235, 215], dtype=np.uint8))

Image.fromarray(arr).save("assets/birefringence-cover.png")
print("wrote assets/birefringence-cover.png")
