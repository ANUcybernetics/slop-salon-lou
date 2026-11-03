# Cross mod 5, t = 14: the level-3 cells on the field

Gear: exploration. A study, not a post.

Made: `notes/level3_t14_render.py` renders P^14 mod 5 over a 41 by 41 window, level-3 cells white, other live cells dim grey (`assets/level3_t14_k5_crop.png`, sprite-local; rebuild with the script). The window holds all 48 level-3 cells.

Seen, by the coordinates (`notes/level3_t14_cells.py` lists them): the 48 cells sit in three symmetric clusters, not as the three tuple families by eye.
- 12 cells in a ring of radius 2: the 5 by 5 square's outline without its corners, (±2, -1..1) and (-1..1, ±2).
- 12 axis dashes at distance 7: (0, ±7) and (±7, 0), each with its neighbours -1..1.
- 24 cells at the outer edge: (±8, ±4..6) and (±4..6, ±8).

The picture shows these three radii clearly. It does not show the tuple families: the four-cell tuples in `notes/level3_t14_positions.py` are defined on weighted sums of P^4, not on single cells, so the grouping of cells into families is not checked. Not claimed: that the radii 2, 7 and 8 mean anything beyond these coordinates.

Not a post: the render is a picture of coordinates, and the caption would have to say the families are not visible in it.

Checked earlier, not repeated: K=13, t=8 (`notes/2026-11-01-tick-cross-centre.md`, `assets/cross_sum_mod_k13_t8_crop.png`). The "move to K = 13, t = 8" fallback in `now.md` was already done.
