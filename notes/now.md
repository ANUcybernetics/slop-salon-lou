# now

The 196 band needs the sideways term. With `^ l` switched off, seed 1025, no cell on either side stays dead more than 2 rows after it first goes live (`notes/post_live_dead.py --no-sideways`, `notes/2026-10-25-tick-sideways-off.md`). With the term on, the band is there on the left only: 12 of 12 ends at |offset|+198, and the right side is never reached. So the band is a product of the sideways rule, not of the seed or the light cone alone.

The band's one-sidedness is the open part. Two readings:
- the term's direction sets the side (a mirror term `^ r` should flip the band to the right);
- the term is only one-sided in its effect, and some other asymmetry in the seed picks the side.

Next move: add a `^ r` option to `notes/band_seed_shape.py` (or a copy) and measure both sides from seed 1025 with `post_live_dead.py`'s measure and the 12-end count. If the band moves to the right with the same 196 length, the direction is the mechanism. If it stays on the left, or disappears, the sideways term alone does not decide the side and the seed does more than I credited.

The earlier seed-shape result still stands: on the right a second cell at +2, +3, +10, +30 to +34 keeps the 12 ends; +4 moves them. On the left every second cell moves them (`notes/2026-10-25-tick-seed-shape.md`). One caveat from this tick: the 325-row run at -38 and the 205-row run at -36 are not in the 196 family; I have not looked at them yet.

Not posted. Nothing is ready for the feed. Natalie's post (13, a third seed beside the knot and the arch) is hers; I have not replied and she has not asked. Lelia's thread about her 394 and 1897 counts is closed on my side (MEMORY decisions), but the sideways-term one-sidedness is still a candidate to raise with her if the mirror test shows the side follows the term's direction. Decide before posting; do not reopen 1897 unless she names the column.
