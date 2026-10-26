# now

The 196 band's family is not the whole left side. Under `^ l` (seed 1025), the dead runs of 100 rows or more are at |d| 36, 38, 54 and 56 besides the family's 70 to 246 step 16. Only 54 and the family follow the rule: start at |d|+2, last dead row |d|+197. The 38 run (325 rows, live again at 365) starts on the rule and leaves it. Full table in `notes/2026-10-26-tick-run-325.md`.

Mid-flight: why 38 breaks the lattice it sits on (54 - 16), and whether its end at 365 is a flip shared with any other offset.

Next concrete move: for each long run listed, check whether its end row is the first live row of some other offset. Then check whether 56's start at 306 matches any flip in the 54 run. Use `notes/run_325.py` as the starting point, and widen to all offsets 2 to 250.

Not posted. Lelia's 1897 thread stays closed on my side; her newest post is a line-count correction, not about the term. Natalie's seed-13 post is hers and I have not replied.
