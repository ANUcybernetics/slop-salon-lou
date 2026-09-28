#!/usr/bin/env python3
"""The touch-height control, face: natalie's canvas over the proof,
time-aligned, 1920x1920. Her canvas (1700x972) covers the full sound
(ink cols 0-860, sound 0-53.75 s, then empty paper / true silence).
Both layers full-length: the empty right half shows in both — paper
above, silence below. Receipt LUT: bright = loud, silence black."""
import numpy as np
from PIL import Image

W, H = 1920, 1920
spec = np.load("assets/touchheight_proof.npy")     # (232, nwin) dB, row 0 = top = high
canvas = Image.open("assets/touchheight_rgb.png").convert("RGB")

img = Image.new("RGB", (W, H), (10, 10, 12))

proof = Image.fromarray(
    ((np.clip((spec + 90.0) / 90.0, 0, 1)) * 255).astype(np.uint8), "L"
).convert("RGB").resize((W, 822), Image.NEAREST)
img.paste(proof, (0, 1098))

cw = canvas.resize((W, round(972 * W / 1700)), Image.LANCZOS)   # 1920x1098
img.paste(cw, (0, 0))

img.save("assets/touchheight_face.png")
print("wrote assets/touchheight_face.png", img.size)
