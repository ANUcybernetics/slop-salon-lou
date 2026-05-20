"""
IC legibility comparison.
Top row: Rule 90 with 4 different ICs — each IC leaves a distinct trace.
Bottom row: RD with 4 different ICs — ICs converge to same family.
The rule absorbs the IC, or it doesn't.
"""
import numpy as np
from PIL import Image, ImageDraw

# ---- Rule 90 ----

def rule90(ic, steps=150):
    """Run Rule 90 (XOR) for given steps. Returns 2D array (steps x n)."""
    n = len(ic)
    grid = np.zeros((steps, n), dtype=np.uint8)
    grid[0] = ic
    for t in range(1, steps):
        left = np.roll(grid[t-1], 1)
        right = np.roll(grid[t-1], -1)
        grid[t] = (left ^ right)
    return grid

def render_rule90(grid, cell=3):
    h, w = grid.shape
    img = np.where(grid[:, :, None], [20, 10, 60], [240, 235, 220]).astype(np.uint8)
    # Scale up
    img = np.repeat(np.repeat(img, cell, axis=0), cell, axis=1)
    return Image.fromarray(img)

n = 200
steps = 150

# Four different ICs for Rule 90
ics_90 = []
rng = np.random.default_rng(7)
# IC 1: single center point
ic1 = np.zeros(n, dtype=np.uint8); ic1[n//2] = 1
# IC 2: two points
ic2 = np.zeros(n, dtype=np.uint8); ic2[n//3] = 1; ic2[2*n//3] = 1
# IC 3: random sparse
ic3 = (rng.uniform(0, 1, n) < 0.05).astype(np.uint8)
# IC 4: block
ic4 = np.zeros(n, dtype=np.uint8); ic4[n//2-5:n//2+5] = 1

ics_90 = [ic1, ic2, ic3, ic4]
panels_90 = [render_rule90(rule90(ic, steps), cell=3) for ic in ics_90]

# ---- Gray-Scott RD ----

def gray_scott(seed, F=0.054, k=0.062, n=200, steps=5000, dt=1.0, Du=0.16, Dv=0.08):
    rng = np.random.default_rng(seed)
    U = np.ones((n, n))
    V = np.zeros((n, n))
    # Each seed gets a different IC: random scattered perturbations
    n_seeds = rng.integers(3, 10)
    for _ in range(n_seeds):
        cx = rng.integers(20, n-20)
        cy = rng.integers(20, n-20)
        r = rng.integers(5, 20)
        U[cx-r:cx+r, cy-r:cy+r] = 0.50 + rng.uniform(-0.05, 0.05, (2*r, 2*r))
        V[cx-r:cx+r, cy-r:cy+r] = 0.25 + rng.uniform(-0.05, 0.05, (2*r, 2*r))

    def laplacian(Z):
        return (np.roll(Z,1,0) + np.roll(Z,-1,0) +
                np.roll(Z,1,1) + np.roll(Z,-1,1) - 4*Z)

    for _ in range(steps):
        uvv = U * V * V
        U += dt * (Du * laplacian(U) - uvv + F * (1 - U))
        V += dt * (Dv * laplacian(V) + uvv - (F + k) * V)

    return V

def render_rd(V, size=450):
    v = (V - V.min()) / (V.max() - V.min() + 1e-9)
    cream = np.array([240, 235, 215])
    indigo = np.array([35, 20, 85])
    rgb = (cream[None, None] * (1 - v[:, :, None]) +
           indigo[None, None] * v[:, :, None]).astype(np.uint8)
    img = Image.fromarray(rgb)
    return img.resize((size, size), Image.NEAREST)

seeds = [17, 42, 99, 137]
panels_rd = [render_rd(gray_scott(s)) for s in seeds]

# ---- Compose ----

panel_w = panels_rd[0].width   # 450
panel_h = panels_90[0].height  # 150 * 3 = 450
label_h = 40
gap = 12
border = 20
n_panels = 4

total_w = border * 2 + n_panels * panel_w + (n_panels - 1) * gap
total_h = border * 2 + 2 * panel_h + gap + label_h * 2

canvas = Image.new('RGB', (total_w, total_h), (248, 245, 238))
draw = ImageDraw.Draw(canvas)

# Draw row labels
draw.text((border, border + (panel_h - 14) // 2), "Rule 90", fill=(60, 50, 100))
draw.text((border, border + panel_h + gap + label_h + (panel_h - 14) // 2), "RD", fill=(60, 50, 100))

label_w = 80
x_start = border + label_w

for i, p in enumerate(panels_90):
    x = x_start + i * (panel_w + gap)
    y = border
    # resize rule90 panel to match panel_w x panel_h
    p_resized = p.resize((panel_w, panel_h), Image.NEAREST)
    canvas.paste(p_resized, (x, y))

for i, p in enumerate(panels_rd):
    x = x_start + i * (panel_w + gap)
    y = border + panel_h + gap + label_h
    canvas.paste(p, (x, y))

# Row captions
draw.text((x_start, border + panel_h + 4), "IC persists. the origin is legible.", fill=(80, 70, 120))
draw.text((x_start, border + panel_h + gap + label_h + panel_h + 4), "IC absorbed. the rule erased it.", fill=(80, 70, 120))

canvas.save('/home/sprite/slop-salon-lou/assets/ic-legibility.png')
print(f"saved ic-legibility.png — {canvas.size}")
