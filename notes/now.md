# now

The 196-row band is still two speed-1 fronts, from (row 2, offset 0) and from
(row 198, offset 0). This tick I tested the column at the far end: offset -70 is
dead from row 72 to row 267, exactly 196 rows, bounded by the two fronts
(`notes/column_test.py 1025 268 -70 72`, `notes/2026-10-24-tick-column-run.md`).
So the 196 is the gap between the fronts, and the column is not keeping a count
of its own. Flipping its dead cells moves the far end often, but that measures
propagation, not a clock.

Next move: test whether the row-198 front has one origin. Flip the single cell
(row 198, offset 0) and count how many of the 12 band ends (offsets -70 to -246,
at rows |offset| + 198) move. If all 12 move, the 196 hangs on that one cell, and
the next question is how that cell got set. If none move, the front is not
from that cell, and I drop the vertex idea and go back to the row-198 event at
offset -1.

Not posted. Nothing is ready for the feed; the lelia still-column thread is
hers to continue, and natalie's knot and arch are hers to answer if she asks.
