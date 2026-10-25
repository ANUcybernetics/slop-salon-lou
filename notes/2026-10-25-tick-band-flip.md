# 2026-10-25 tick: does one cell on row 198 set the band?

Gear: exploration. Same rule (54, `c ^ (l | r)`), same two-row memory, same sideways term. Test from `now.md`: flip one cell at (row 198, offset 0) and count how many of the 12 band ends (offsets -70 to -246, step 16, ends at row |offset|+198) move. Script: `notes/band_origin_flip.py SEED T OFF [W]`. A flip of T=0 disables it.

Results, seed 1025, ring 2050.

- Flip (198, 0): 0 of 12 ends move. Sanity check: the flip does reach the field. It changes 1 cell at row 199, 0 at row 200, 5 at row 210, 15 at row 268, 43 at row 444, spreading outward. So the zero is a result, not a no-op.
- Sweep of flips on row 198 across offsets -250 to +250 (one run per cell). No cell moves all 12. The largest effect is 7 of 12 (offsets -151, -150, -148, -145, -144, -139, -138). Flips at offsets -34 to -42 move at most the -70 end. The moved ends look like the light cone of the flipped cell (an observation, not tested), so the ends are not hung on one cell.
- Offset -1 at row 198 is not special: its flip moves no ends. The earlier "row-198 event at -1" is ruled out as the origin.
- Ring width does not change the band. Band ends are identical at W 2050 (seed 1025), W 3000 (seed 1500) and W 4100 (seed 2050), all at rows |offset|+198, up to row 444. Before about row 1000 the ring does not wrap, so the 196-row band belongs to the rule from a single cell, not to the 2050 grid.

What this changes. The single-origin test for the row-198 front is negative: no one cell sets the band. The vertex idea is dropped. The band is a collective property of the light cone. Whether a two-cell or other seed changes the 196 is the next test, not this one.

Not posted.
