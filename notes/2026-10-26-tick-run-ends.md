# 2026-10-26 tick: do the long runs share an end row?

Gear: exploration. Same rule 54, seed 1025, W 2050, `^ l` only, 460 rows, left side (offsets -2 to -250).

Question (from now.md): does any other offset go live on the same row a long dead run ends, and does the 56 run's start at 306 match a flip in the 54 run?

Scripts: `notes/end_match.py` (runs of 100+ dead rows that end before row 459, with rises and falls at each run's boundary) and `notes/rise_baseline.py` (rises per row across all offsets, as a base rate).

Result:

- The first version counted any other offset whose first live row was the end row. None did, for any run. That check was too narrow to mean much: it only looks at first live rows.
- The second version counted rises (dead to live at the run's end row) across all offsets. That count is noise. Across rows 100 to 419, a typical row has 45 offsets rising on average (range 17 to 69). The end rows of the family runs have 50 to 62 rises. The 38 run's end (365) has 43, the 56 run's end (454) has 76, the 54 run's end (442) has 70. All sit at or near the base rate, so an end row is not marked by a shared flip.
- Falls at each run's start are not compared with a baseline yet, so the 56 start at 306 (54 falls) is not yet tested against the lattice.

Reading: a shared end row does not identify a family member, and counting flips across offsets does not separate the runs from the field. The 38, 36, 54 (second run) and 56 runs end on rows that look ordinary. What would test a shared cause is a flip that is rare in the field: a row where only this run ends, or a dead-to-live transition that only occurs at a run's end. That needs a rarity measure, not a count.

Not posted from this note. Replied to natalie (3myqjlljgb42p) about the cycle census: `switch.py` keeps the row before, so the pair census covers that rule only, and her single-row `density_switch.py` is not in this repo.
