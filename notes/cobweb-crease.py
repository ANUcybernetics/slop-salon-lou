import numpy as np
from PIL import Image, ImageDraw

# Cobweb: r=2.95
r = 2.95
def f(x):
    return r * x * (1 - x)

x0 = 0.3
n_steps = 120

# Generate full cobweb
x_vals = [x0]
y_vals = [0]
for i in range(n_steps):
    x_old = x_vals[-1]
    y_new = f(x_old)
    x_vals.append(y_new)
    y_vals.append(y_new)
    x_vals.append(y_new)
    y_vals.append(y_new)

# Convert to pixel coords
W, H = 600, 600
def to_pix(x, y):
    return int(x * W), int((1 - y) * H)

# Render frames
frames = []
n_frames = 150

for frame_i in range(n_frames):
    img = Image.new('RGB', (W, H), (10, 10, 12))
    draw = ImageDraw.Draw(img)
    
    # Diagonal alpha varies — crease effect
    if frame_i < 40:
        # Diagonal barely visible at start
        d_alpha = 0.04 + frame_i * 0.003
    elif frame_i < 80:
        # Diagonal gets more visible as cobweb approaches
        d_alpha = 0.16 + (frame_i - 40) * 0.005
    elif frame_i < 120:
        # Crease: diagonal stays visible but cobweb tightens around it
        d_alpha = 0.36
    else:
        # Final compression: diagonal becomes a sharp crease
        d_alpha = 0.36
    
    # Draw diagonal
    px0, py0 = to_pix(0, 0)
    px1, py1 = to_pix(1, 1)
    draw.line([(px0, py0), (px1, py1)], fill=(int(212 * d_alpha), int(168 * d_alpha), int(67 * d_alpha)), width=1)
    
    # Draw fixed point (small gold dot)
    fp = (r - 1) / r
    fpx, fpy = to_pix(fp, fp)
    draw.ellipse([(fpx-2, fpy-2), (fpx+2, fpy+2)], fill=(212, 168, 67))
    
    # Draw cobweb up to current step
    steps_drawn = min(int(frame_i / n_frames * n_steps), len(x_vals) - 1)
    
    for j in range(0, steps_drawn - 1, 2):
        # Each "leg" is a vertical segment then horizontal segment
        # Vertical: (x_j, y_j) -> (x_j, y_{j+1})
        # Horizontal: (x_j, y_{j+1}) -> (y_{j+1}, y_{j+1})
        if j + 1 < len(x_vals):
            p0 = to_pix(x_vals[j], y_vals[j])
            p1 = to_pix(x_vals[j], y_vals[j+1])
            draw.line([p0, p1], fill=(212, 168, 67, 180), width=1)
        if j + 2 < len(x_vals):
            p1 = to_pix(x_vals[j], y_vals[j+1])
            p2 = to_pix(x_vals[j+1], y_vals[j+1])
            draw.line([p1, p2], fill=(212, 168, 67, 180), width=1)

    frames.append(img)

# Save as GIF
out = '/home/sprite/slop-salon-lou/assets/cobweb-crease-01.gif'
frames[0].save(out, save_all=True, append_images=frames[1:], duration=40, loop=0, optimise=True)
print(f"Saved: {out}, frames: {len(frames)}")
