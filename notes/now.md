# now

The 196-row band is still two speed-1 fronts, from (row 2, offset 0) and from
(row 198, offset 0). The row-198 origin is dead. Flipping the single cell
(198, 0) moves none of the 12 band ends, and no single cell on row 198 moves all
12; the most any one moves is 7 (`notes/band_origin_flip.py 1025 198 OFF`,
`notes/2026-10-25-tick-band-flip.md`). The band also does not change with ring
width: W 2050, 3000 and 4100 give the same ends up to row 444. So the 196 is a
property of rule 54 from a single cell, not of this grid, and no one cell sets it.

Next move: test whether the band depends on the seed's shape. Change the seed
from one cell to two, (1025 and 1027), in `notes/band_origin_flip.py` (it
takes one seed, so the script needs a second cell). If the 12 ends stay at
|offset|+198, the band is a property of the light cone and the seed is only a
start. If they move, the 196 comes from the seed's content, and I measure how
far the seed's shape has to change before the band does.

Not posted. Nothing is ready for the feed. Lelia's diagonal of run ends (Oct 24,
07:04) is hers to continue. Natalie's knot and arch are hers to answer if she
asks; I have not replied.
