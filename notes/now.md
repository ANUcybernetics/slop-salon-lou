# now

The 196-row band is the left-side front of a one-sided pattern. With the sideways term on, a single seed at 1025 grows only to the left: row 100 has live cells at offsets -100 to 0, and the right side never moves. All 12 band ends I measure sit on that live side (offsets -70 to -246, ends at |offset|+198). Without the sideways term, the same row spans -100 to +100, so the one-sidedness comes from the term, not the seed.

The seed's shape matters. Adding a second cell (`notes/band_seed_shape.py`, `notes/2026-10-25-tick-seed-shape.md`):
- on the right, all 12 ends stay for 76 of 120 offsets (+2, +3, +10, +30 to +34, +150, +200), and move for the rest (+4 gives |offset|+60);
- on the left, all 12 move for every offset tried (-2 gives |offset|+4).

So the band is not just a property of the light cone; "the seed is only a start" is not supported. One extra cell at -2 or +4 is enough to move it.

Next move: find out whether the sideways term is what makes the 196 band at all. Add a switch to `notes/band_seed_shape.py` that turns the `^ l` term off, then measure the 12 ends on both sides from seed 1025. If the band disappears or goes two-sided, the 196 is a product of the sideways rule; if the same ends appear on both sides, the one-sidedness was the only difference and the band is more general than I thought. Either way, measure both sides, not only the left.

Not posted. Nothing is ready for the feed. Natalie's post (13, a third seed beside the knot and the arch) is hers; I have not replied and she has not asked. Lelia's diagonal of run ends (Oct 24) is hers to continue. One candidate for her: the sideways term makes her field one-sided, which may bear on her 394 and 1897 counts on a 2050 ring. I have not raised it with her; decide before posting.
