"""
Fractal basin boundaries: Newton's method for z^3 - 1 = 0.
Three roots at the cube roots of unity. The basin boundary
is the fractal (a variant of the Julia set).

At low resolution (coarse grid), the boundary looks clean.
At high resolution (fine grid with perturbation), the boundary
is infinitely detailed — it THICKENS without bound.

This is the basin hesitation made geometric: at the boundary,
you cannot tell where one basin ends and another begins,
no matter how finely you measure.
"""
import math
import random
import subprocess

def newton_step(z_r, z_i):
    """One Newton step for z^3 - 1 = 0.
    z_new = z - (z^3 - 1)/(3z^2) = (2z^3 + 1)/(3z^2)
    """
    z2 = z_r * z_r - z_i * z_i + 1  # z^2 real part + 1? No...
    # z^2 = (a+bi)^2 = a^2-b^2 + 2abi
    zr2 = z_r * z_r - z_i * z_i
    zi2 = 2 * z_r * z_i
    # 2z^3 = 2z * z^2 = 2*(a+bi)*(a^2-b^2 + 2abi)
    zr3 = z_r * zr2 - z_i * zi2  # z^3 real
    zi3 = z_r * zi2 + z_i * zr2  # z^3 imag
    zr3 = 2 * zr3 + 1  # 2z^3 + 1
    zi3 = 2 * zi3
    # 3z^2
    zr_den = 3 * zr2
    zi_den = 3 * zi2
    # (zr3 + zi3*i) / (zr_den + zi_den*i)
    denom = zr_den * zr_den + zi_den * zi_den
    if denom < 1e-20:
        return z_r, z_i
    z_new_r = (zr3 * zr_den + zi3 * zi_den) / denom
    z_new_i = (zi3 * zr_den - zr3 * zi_den) / denom
    return z_new_r, z_new_i

def newton(z_r, z_i, max_iter=30):
    """Newton's method for z^3 - 1. Returns which root it converges to."""
    roots = [
        (1.0, 0.0),              # 1
        (-0.5, math.sqrt(3)/2),  # e^(2pi*i/3)
        (-0.5, -math.sqrt(3)/2), # e^(-2pi*i/3)
    ]

    for _ in range(max_iter):
        denom = z_r * z_r + z_i * z_i
        if denom < 1e-20:
            return -1
        z_r, z_i = newton_step(z_r, z_i)
        r2 = z_r * z_r + z_i * z_i
        if r2 > 100:
            return -1
        for ri, (rr, ir) in enumerate(roots):
            if (z_r - rr)**2 + (z_i - ir)**2 < 1e-6:
                return ri
    return -1  # didn't converge

# Use a seeded RNG
rng = random.Random(42)

def gauss():
    u1 = max(1e-10, rng.random())
    u2 = rng.random()
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

# Resolution 1: coarse grid, no perturbation
print("coarse (no perturbation)...")
N1 = 64
grid1 = []
for iy in range(N1 + 1):
    row = []
    for ix in range(N1 + 1):
        zr = -1.5 + ix * 3.0 / N1
        zi = -1.5 + iy * 3.0 / N1
        b = newton(zr, zi, max_iter=30)
        row.append(b)
    grid1.append(row)

# Resolution 2: fine grid, with perturbation
# For each pixel, perturb 10 times and count basin assignments
print("fine (10 perturbations)...")
N2 = 64
grid2 = []
for iy in range(N2 + 1):
    row = []
    for ix in range(N2 + 1):
        zr = -1.5 + ix * 3.0 / N2
        zi = -1.5 + iy * 3.0 / N2

        counts = [0, 0, 0]
        for _ in range(10):
            pzr = zr + 0.02 * gauss()
            pzi = zi + 0.02 * gauss()
            b = newton(pzr, pzi, max_iter=30)
            if 0 <= b <= 2:
                counts[b] += 1

        row.append(counts)
    grid2.append(row)

def root_color(root_idx):
    """RGB for each of the three roots."""
    if root_idx == 0:
        return (255, 100, 100)   # red
    elif root_idx == 1:
        return (100, 255, 100)   # green
    else:
        return (100, 100, 255)   # blue

# Write PPM for coarse
lines1 = [f"P3\n{N1+1} {N1+1}\n255\n"]
for row in grid1:
    for b in row:
        if 0 <= b <= 2:
            r, g, bl = root_color(b)
            lines1.append(f"{r} {g} {bl}\n")
        else:
            lines1.append("0 0 0\n")

with open("/tmp/basin-coarse.ppm", "w") as f:
    f.writelines(lines1)

# Write PPM for fine (mixed colours)
lines2 = [f"P3\n{N2+1} {N2+1}\n255\n"]
for row in grid2:
    for counts in row:
        total = sum(counts)
        if total == 0:
            lines2.append("0 0 0\n")
        else:
            r = int(counts[0] / total * 255)
            g = int(counts[1] / total * 255)
            b = int(counts[2] / total * 255)
            lines2.append(f"{r} {g} {b}\n")

with open("/tmp/basin-fine.ppm", "w") as f:
    f.writelines(lines2)

# Convert both
subprocess.run(["convert", "/tmp/basin-coarse.ppm", "assets/basin-coarse.png"], check=True)
subprocess.run(["convert", "/tmp/basin-fine.ppm", "assets/basin-fine.png"], check=True)

# Stitch: coarse | fine
subprocess.run([
    "convert",
    "/tmp/basin-coarse.ppm", "/tmp/basin-fine.ppm",
    "+append",
    "-scale", "300%x300%",
    "assets/basin-boundary.png"
], check=True)

# Count boundary cells in fine grid (cells that don't fully converge)
boundary = 0
total = 0
for row in grid2:
    for counts in row:
        total += 1
        s = sum(counts)
        if s > 0:
            frac = max(counts) / s
            if frac < 1.0:  # not 100% in one basin
                boundary += 1

print(f"Boundary cells (not 100% convergent): {boundary}/{total} ({100*boundary/total:.1f}%)")
print("Done: basin-boundary.png, basin-coarse.png, basin-fine.png")
