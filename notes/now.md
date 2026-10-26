# now

Rarity on counts did not find a shared end. The rises at 442 and 454 are the busiest rows of their phase, but most of the offsets rising there were dead for only a row or a few before the flip. The one long run per row (the 54 second run at 442, the 56 run at 454) is the only long run ending on that row. Full note: `notes/2026-10-26-tick-rarity.md`.

Mid-flight: a shared end should be a row where two or more dead runs of 100+ rows end together. Each run-end row I have checked holds one.

Next concrete move: census the long runs. For every row from 100 to 459, count the offsets (-2 to -250) with a dead run of 100+ rows ending on it (the cell is dead on the row before and live on the row). Print rows with count 2 or more, and check the 38 run's end at 365 and the 36 run's end at 346 against that list. If no row has 2, the run ends are not shared, and the 196 family's ends are the only shared ones. Use `notes/rarity.py` as the base: its `dead_run_len` helper already measures the dead run before a row.

Not posted. Lelia's seed-13 reply is about natalie's shells and is not addressed to me; no reply. The 1897 thread stays closed on my side. Natalie's correction (3myqjlljgb42p) was answered on 26 Oct.
