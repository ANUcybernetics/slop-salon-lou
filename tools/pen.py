#!/usr/bin/env python3
"""tools/pen.py -- lelia's pen instrument: anchor-free scale from pen thickness.
Darkness-weighted pen thickness w = column ink mass on near-flat ink
(vertical cut; slope-corrected by selection, not by formula). If natalie
draws with a constant pen, w x px/oct = 156 her-px^2/oct on ANY canvas --
windows keep the product, redraws refuse it.
usage: pen.py <image> [slope_max]
"""
import sys
import numpy as np
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im, dtype=np.float64) / 255.0
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
vals, counts = np.unique(Y.round(4), return_counts=True)
paper = float(vals[counts.argmax()])
ink = np.clip(paper - Y, 0.0, None)
H, W = ink.shape

smax = float(sys.argv[2]) if len(sys.argv) > 2 else 0.08
M = ink.sum(axis=0)                       # ink mass per column
ys = np.arange(H)[:, None]
tot = M.sum()
yc = (ink * ys).sum(axis=0) / np.maximum(M, 1e-12)   # per-column centroid
slope = (yc[2:] - yc[:-2]) / 2.0
flat = np.zeros(W, bool)
flat[1:-1] = np.abs(slope) < smax
flat &= M > 0.2 * M.max()                 # on the line, not paper
pen = float(np.median(M[flat]))
print(f"{sys.argv[1]}: paper {paper:.4f} flat_cols {flat.sum()} "
      f"pen {pen:.3f} px  (16-84%: "
      f"{np.percentile(M[flat],16):.2f}-{np.percentile(M[flat],84):.2f})")
