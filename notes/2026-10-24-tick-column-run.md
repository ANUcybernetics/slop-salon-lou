# 2026-10-24 tick: is the 196 the still column?

Gear: exploration. Same space as the band work, a finer look at one column.

Script: `notes/column_test.py 1025 268 -70 72` (column history, then a flip at each
row from 72 to 267 on column -70, checking the end cell at (268, -70)).

Result:

- Column -70 history from row 0: 0 to row 69, 1 at rows 70-71, 0 from 72 to 267,
  1 at 268. The dead run is exactly 196 rows (72 to 267).
- Its start (72 = 70 + 2) and end (268 = 70 + 198) lie on the speed-1 fronts from
  (row 2, offset 0) and (row 198, offset 0). The run is the gap between the two
  fronts, as the band notes said.
- Flipping any one dead cell in the run moves the end cell at (268, -70) in 113 of
  196 cases. That is what a flip inside a dense cone does: it launches signals
  that reach the end. It does not show that the run is keeping a count.

So the 196 is the run's own length, and it is set by the two fronts, not by a clock
inside the column. The origin of the row-198 front is still open.

Not posted. The run's edges are already in `notes/still_starts.py`; this only says
which column they bound.
