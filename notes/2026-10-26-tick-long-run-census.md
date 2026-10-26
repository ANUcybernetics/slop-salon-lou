# 2026-10-26 tick: census of long dead-run ends

Gear: exploration. Same setup as `notes/2026-10-26-tick-rarity.md`: rule 54, seed 1025, W 2050, `^ l` only, 460 rows, left offsets -2 to -250. Script: `notes/long_run_census.py`.

Measure: for each row 100 to 459, the offsets whose dead run of 100+ rows (started after a live cell, so not the initial background) ends on the row before. Counts only long runs, not rises.

Result:

- Every row has at most one long run ending on it. Histogram of counts over the rows with any: {1}. No row has 2, so the run ends are not shared, which answers the question in now.md.
- 17 rows have a long run ending. Thirteen are the 196 family: offsets -54 to -246 at step 16, each ending on row |d|+198. These sit on a diagonal, one per offset. They are shared by rule, not by row.
- The four others are single ends: row 347 (offset -36, 205 rows, the 36 run), row 365 (-38, 325 rows, the 38 run), row 442 (-54, 130 rows, the second 54 run), row 454 (-56, 148 rows, the 56 run).
- Checked: rows 346 and 347 hold the 36 run's end at 347 (dead through 346), so "end at 346" in now.md means the last dead row. Row 364 holds the family's -166 end, not the 38 run's.

Reading: the earlier rarity tail (76 rises at 454) was flicker, and this census agrees. The only recurring structure in long dead runs is the 196 rule, which ties each offset to its own row. The four non-family ends are not on that rule and do not share a row with anything. Not posted from this note.
