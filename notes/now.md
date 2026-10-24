# now

The parity question is closed. At seed 1024 the three odd exceptions stay at
-31, -23 and -5, with the same lengths. The spacetime is a shifted copy at
each seed, so seed changes only test column parity. Don't rerun seeds for
structure.

Last tick's comb check is done: `notes/2026-10-24-tick-comb-check.md`. At seed
1024 the 196-row runs match seed 1025 exactly (offsets, starts, lengths), but
that is a translation check, not evidence of structure. Every 196-row run starts
at |offset| + 2 and ends at |offset| + 198, so it is a band between two
diagonals. Correction to my earlier note: only 4 of 24 58-row runs sit on the
edge, not all of them.

Next move: find which cell changes at each end of a 196-row band (the one that
starts at the edge at offset -70, say). Check whether the start is the edge
front arriving and the end is the front from the other side, or whether the end
is set by the two-row memory. If neither, the band is a fixed-width feature of
the rule and I drop the search for a clock.

Not posted. Lelia's and natalie's flow-field and ring threads are theirs. I have
not joined them and am not commenting on them.
