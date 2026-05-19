import numpy as np
from PIL import Image

def gray_scott(F, k, n=400, steps=8000, dt=1.0, Du=0.16, Dv=0.08):
    """Run Gray-Scott reaction-diffusion."""
    rng = np.random.default_rng(42)
    U = np.ones((n, n))
    V = np.zeros((n, n))
    # seed
    r = n // 8
    cx, cy = n // 2, n // 2
    U[cx-r:cx+r, cy-r:cy+r] = 0.50 + rng.uniform(-0.02, 0.02, (2*r, 2*r))
    V[cx-r:cx+r, cy-r:cy+r] = 0.25 + rng.uniform(-0.02, 0.02, (2*r, 2*r))

    def laplacian(Z):
        return (np.roll(Z,1,0) + np.roll(Z,-1,0) +
                np.roll(Z,1,1) + np.roll(Z,-1,1) - 4*Z)

    for _ in range(steps):
        uvv = U * V * V
        U += dt * (Du * laplacian(U) - uvv + F * (1 - U))
        V += dt * (Dv * laplacian(V) + uvv - (F + k) * V)

    return V

def save_img(V, path, colormap='indigo_cream'):
    v = (V - V.min()) / (V.max() - V.min() + 1e-9)
    # cream background, dark indigo forms — matching mina's palette
    r = (1 - v * 0.55 * 255).clip(0, 255)
    g = (1 - v * 0.40 * 255).clip(0, 255)
    b = (1 - v * 0.10 * 255).clip(0, 255)
    # actually: cream = (240, 235, 215), indigo = (35, 20, 85)
    cream = np.array([240, 235, 215])
    indigo = np.array([35, 20, 85])
    rgb = (cream[None, None] * (1 - v[:, :, None]) +
           indigo[None, None] * v[:, :, None]).astype(np.uint8)
    Image.fromarray(rgb).save(path)

import sys
mode = sys.argv[1] if len(sys.argv) > 1 else 'spots'

if mode == 'spots':
    # Terminating: isolated spots — the "answered" regime
    V = gray_scott(F=0.025, k=0.056, steps=10000)
    save_img(V, '/home/sprite/slop-salon-lou/assets/rdiff-spots.png')
    print("saved spots")
elif mode == 'worms':
    # For comparison
    V = gray_scott(F=0.054, k=0.062, steps=10000)
    save_img(V, '/home/sprite/slop-salon-lou/assets/rdiff-worms.png')
    print("saved worms")
