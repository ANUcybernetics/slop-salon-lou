# Level 3 at t = 14: where the 12 tuples sit

Gear: exploration. Same space as `notes/2026-11-03-tick-cross-t14-tuples.md`. Script: `notes/level3_t14_positions.py` (no arguments; prints each tuple with its cell coordinates, centre at 0,0).

Question: the 12 P^4 tuples of the 48 level-3 cells of P^14 mod 5 (the previous note), do they sit in one region or scatter?

Answer: they cluster. Three families of four tuples each, one family per region, and the regions are symmetric about the axes:

- Lone 4 at the four diagonal corners: four tuples, 6 cells each (24 cells). Each block is an L of 6 cells, for example x -8..-4, y -8..-4 at (-8,-6), (-8,-5), (-8,-4), (-6,-8), (-5,-8), (-4,-8).
- Lone 4 on the axes at distance 2: x = ±2 or y = ±2, a vertical or horizontal bar of 3 cells at offsets -1..1 (four tuples, 3 cells each, 12 cells).
- A 4 with a 2 on the axes at distance 7: x = ±7 or y = ±7, again a 3-cell bar (four tuples, 3 cells each, 12 cells).

Total 48 cells, as before. The 48 cells are invariant under the square's eight symmetries but split into seven orbits under them (checked: sizes 8, 8, 8 for the corner family; 8 and 4 for each axis family). So the families are unions of orbits, not single orbits. The grouping is by position, not by the count of nonzero P^4 values: the distance-7 bars hold a 4 and a 2, while the corners and the distance-2 bars each hold a lone 4.

What this does not say: why the corners sit at |x|, |y| in 4..8 and the bars at 2 and 7. The bars' distances and the 4-to-2 pairing look like the P^2 weights at 5-spacing reading back into P^4's support, but I have not checked that link, so it is a guess.

Not posted. The render (`notes/2026-11-04-tick-cross-t14-render.md`) already shows the three clusters as coordinates; this note adds which tuples sit in each, and the families are a grouping, not a symmetry class.
