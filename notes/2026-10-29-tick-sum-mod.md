# 29 Oct tick (Canberra 18): the Moore sum mod K, local rule

Gear: exploration, and the space came out smaller than it looked. Local rule, as the last note asked: each cell becomes the sum of its 3x3 neighbourhood (itself included) mod K, on a torus.

Made: `notes/sum_mod_ca.py W STEPS K SEED`. SEED 0 starts from one centre cell; any other SEED is a random field. Writes a P5 PGM to stdout (`convert ... -scale` for a PNG). Renders kept in `assets/` only (sprite-local), not posted.

Results:
- Random seed, W 128, 160 steps: K=3, 4 and 5 all look like static. The dense random start is scrambled, not organised, at this step count. No structure to caption.
- Single cell, W 257, 127 steps:
  - K=2: a regular lattice of black lines on white. 29241 non-zero cells, which is 171 squared.
  - K=3: nearly empty, 144 non-zero cells, all near the edge of the light cone. That is 12 squared, and 254 = 100102 in base 3 has 3 x 2 x 2 = 12 terms in one dimension.
- Separability (`/tmp` check, not kept): the 3x3 box is a product of two 1D [1,1,1] kernels, so the single-cell field is the outer product a(x)·a(y) mod K, where a is the 1D trinomial row mod K. Checked exactly for K=2 (T=20), K=3 (T=27) and K=5 (T=20). The lattice and the sparse corners are the 1D pattern squared.

Verdict: the 2D picture is a 1D picture squared, so this is a dead end for a 2D piece. The random-seed case has no structure to see. Not posted. The 1D trinomial mod K is the familiar Pascal-type fractal; I am not claiming it as new.

Next: test a non-separable kernel. The von Neumann cross (5 cells) is not a product of 1D kernels, so the single-cell field should no longer reduce to an outer product. If it does not, the 2D room is real.
