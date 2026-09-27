#!/usr/bin/env python3
"""the descent heard, face: her strip (cols 0-720, the sounded crop) over
the montage proof, time-aligned, 1920x1080. Grayscale receipt LUT (bright
= loud, silence black) — same image I read as proof."""
import numpy as np
from PIL import Image

W, H = 1920, 1920
spec = np.load("assets/descent_proof.npy")     # (232, 176) dB, row 0 = top = high
strip = Image.open("assets/descent.png").convert("RGB").crop((0, 0, 720, 372))

img = Image.new("RGB", (W, H), (10, 10, 12))

# proof: stretch 176x232 -> 1920x880
proof = Image.fromarray(
    ((np.clip((spec + 90.0) / 90.0, 0, 1)) * 255).astype(np.uint8), "L"
).convert("RGB").resize((W, 880), Image.NEAREST)
img.paste(proof, (0, 992))

# strip above, full width
sw = strip.resize((W, round(372 * W / 720)), Image.LANCZOS)
img.paste(sw, (0, 0))

img.save("assets/descent_face.png")
print("wrote assets/descent_face.png", img.size)
