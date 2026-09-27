#!/usr/bin/env python3
"""the descent heard backward, face: her strip (cols 0-720, the sounded
crop) FLOPPED to the reversed clock, over the reversed montage proof,
time-aligned, 1920x1920. Receipt LUT: bright = loud, silence black."""
import numpy as np
from PIL import Image

W, H = 1920, 1920
spec = np.load("assets/descent_back_proof.npy")   # (232, 176) dB, row 0 = top = high
strip = Image.open("assets/descent.png").convert("RGB").crop((0, 0, 720, 372))
strip = strip.transpose(Image.FLIP_LEFT_RIGHT)    # reversed clock: climb reads left-to-right

img = Image.new("RGB", (W, H), (10, 10, 12))

proof = Image.fromarray(
    ((np.clip((spec + 90.0) / 90.0, 0, 1)) * 255).astype(np.uint8), "L"
).convert("RGB").resize((W, 880), Image.NEAREST)
img.paste(proof, (0, 992))

sw = strip.resize((W, round(372 * W / 720)), Image.LANCZOS)
img.paste(sw, (0, 0))

img.save("assets/descent_back_face.png")
print("wrote assets/descent_back_face.png", img.size)
