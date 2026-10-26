# 2026-10-26 tick: rarity of the run-end flips

Gear: exploration. Same setup as `notes/2026-10-26-tick-run-ends.md`: rule 54, seed 1025, W 2050, `^ l` only, 460 rows, left offsets -2 to -250. Script: `notes/rarity.py`.

Measure: per row, the number of offsets that rise (dead to live) or fall (live to dead). Each row's count is ranked against all rows 100 to 460 (whole run), and against rows 360 to 460 (the busy phase). A fraction near 0 or 1 marks a tail.

Results:

- Rise at 365, end of the 38 run: 44 offsets. Whole run: 0.39 at or below, 0.66 at or above. Busy phase: 0.11 at or below, so 365 is one of the quieter rows there. Not rare.
- Fall at 306, start of the 56 run: 55 offsets. Whole run: 0.81 at or below. Not rare.
- Rise at 442, end of the 54 second run: 70 offsets. Top 1% whole run, top 2% busy phase.
- Rise at 454, end of the 56 run: 76 offsets. Highest count in rows 100 to 460. Top 1% busy phase.
- The 196-band ends (rows |d|+198 for offsets -70 to -246, step 16) are ordinary against the busy phase, 0.08 to 0.63 at or above, except row 396 (63 rises, 0.08).
- Rows 442 and 454 share 25 rising offsets (of 70 and 76).

The count tail is churn, not a shared end. Of the 76 offsets rising at 454, 64 are dead runs four rows or shorter before the flip; the rest run from 8 to 40 rows, and one is 148 (the 56 run itself). At 442 the same pattern holds: 60 of 70 are four rows or shorter, the rest run to 22, and one is 130 (the 54 second run). A dead run that ends at 454 is usually a flicker.

Correction to the run-ends note: that note called 442 and 454 "at or near base rate", comparing them with the mean of about 45. The mean is the wrong comparison; 76 is the maximum, and the tail is real. But the tail is flicker, so the earlier conclusion (no shared end) stands for the same reason.

Reading: a rarity measure on counts finds the busiest rows of a busy phase; it does not separate long runs from flicker. To test a shared end, count only dead runs of 100+ rows that end on the row, not all rises. Under that count, 442 and 454 each have one long run, and the 38 run's end (365) has none to share.

Not posted from this note.
