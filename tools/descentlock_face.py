#!/usr/bin/env python3
"""the descent re-locked, face: her strip (cols 0-480, the sounded 30 s) over
the montage proof of the crop-locked wav (first 120 windows = 30 s), both
stretched full width -- time-aligned. Grayscale receipt LUT.
Canvas 1920x2368: strip 1920x1488 on top, proof 1920x872 below."""
import numpy as np
from PIL import Image

spec = np.load("assets/descent_locked_proof.npy")[:, :120]   # 30 s
strip = Image.open("assets/descent.png").convert("RGB").crop((0, 0, 480, 372))

W = 1920
STH = round(372 * W / 480)          # 1488 strip height
PRH = 872
img = Image.new("RGB", (W, STH + PRH), (10, 10, 12))

proof = Image.fromarray(
    ((np.clip((spec + 90.0) / 90.0, 0, 1)) * 255).astype(np.uint8), "L"
).convert("RGB").resize((W, PRH), Image.NEAREST)
img.paste(proof, (0, STH))

sw = strip.resize((W, STH), Image.LANCZOS)
img.paste(sw, (0, 0))

img.save("assets/descentlock_face.png")
print("wrote assets/descentlock_face.png", img.size)
