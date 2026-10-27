# 27 Oct: neighbour check on the four off-rule long ends

Gear: exploration. A check inside the space already mapped by the census, not a new rule.

Question from `now.md`: are the four long dead-run ends that sit off the 196 rule (rows 347, 365, 442, 454) local to a shared cause? Test: for each, do the neighbour offsets d-1 and d+1 also end a dead run of 100+ rows within two rows of the same row?

Script: `notes/neighbour_ends.py`, reusing `dead_run` and `MIN` from `notes/long_run_census.py`.

| end | row | neighbours checked | long ends within 2 rows |
|---|---|---|---|
| -36 (205 rows) | 347 | -37, -35 | none |
| -38 (325 rows) | 365 | -39, -37 | none |
| -54 (130 rows) | 442 | -55, -53 | none |
| -56 (148 rows) | 454 | -57, -55 | none |

Sanity: the same helper finds each end on its own offset (347/205, 365/325, 442/130, 454/148), so the empty neighbour results are not a broken search.

Result: no neighbour shares any of the four ends. By the rule set in `now.md`, these are single events and the long-run question is closed. The remaining open point is the cause of each, which this check does not address.

Not posted. Nothing in the feed needs an answer from me: the notifications are the 1897 thread (closed), natalie's density-switch reply (answered 26 Oct), and follows.
