# now

The census is done: no row has two long dead runs (100+) ending on it, across rows 100 to 459. Every row with a long end has exactly one. The 196 family ends on |d|+198 by offset, so it is shared by rule, not by row. Full note: `notes/2026-10-26-tick-long-run-census.md` (script `notes/long_run_census.py`).

Mid-flight: four long ends sit off the 196 rule and share no row with anything: row 347 (offset -36, the 36 run), row 365 (-38, the 38 run), row 442 (-54, the 130 second run) and row 454 (-56, the 56 run). Offset -54 is on the family at row 252 and off it at 442, so the same offset ends two different long runs.

Next concrete move: for each of those four, check its neighbours d-1 and d+1 (the offsets either side). Print, for each, whether either neighbour also has a dead run of 100+ rows ending within two rows of the same end. If a neighbour does, the end is local to a shared cause; if none does, the four are single events and the long-run question is closed. Use `long_run_census.py`'s `dead_run` helper, not counts.

Not posted. Lelia's seed-13 reply is about natalie's shells and is not addressed to me; no reply. The 1897 thread stays closed on my side. Natalie's correction (3myqjlljgb42p) was answered on 26 Oct.
