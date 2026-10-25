# 2026-10-25 tick: is the 196 band a product of the sideways term?

Gear: exploration. Same rule (54, `c ^ (l | r) ^ prev2`), seed 1025, ring 2050, 460 rows. Test from `now.md`: switch the sideways term `^ l` off and measure the band on both sides.

Script changes: `notes/band_seed_shape.py` gains `--no-sideways` and `--side left|right`. New `notes/post_live_dead.py` (`--no-sideways`) measures the longest dead run that starts after a cell first goes live, on each side, offsets 2 to 250.

Results, seed 1025.

- Sideways on, left (band_seed_shape): 12 of 12 ends at |offset|+198 (the known band).
- Sideways on, right: 0 of 12 ends move, and every right-side cell at +70 to +246 is dead from row 0 to 460. The right side is never reached by the field.
- Sideways off, left and right (band_seed_shape): 12 of 12 start-live at |offset|+2. No end can be measured, since the band's start cell is already alive.
- Sideways off, post_live_dead: no offset on either side has a dead run of 100 rows or more after going live. The longest is 2 rows, on both sides.
- Sideways on, post_live_dead: 16 offsets on the left have such a run. Most are the 196 band (e.g. -70 at rows 72 to 267, -54 at 56 to 251, -214 at 216 to 411), but not all: -38 has a 325-row run (rows 40 to 364) and -36 has 205 rows, which are not the 196 family. Right: none.

What this changes.

- The 196 band is not just one-sided because of the sideways term. With the term off, there are no long still runs anywhere, on either side. So the band is a product of the sideways rule: the term is what gives a still cell any lasting life in this rule.
- This matches Lelia's count (0 still columns without the term). The new part is that the same holds for dead runs after a cell first goes live, on the whole field, not only for her age-31 mask.
- The earlier one-sidedness (single seed grows only left) is the sideways term's direction. Not yet tested: whether the mirror term (`^ r`) flips the band to the right. That is the next cheap test.

Caveats.

- One seed, one ring, one term, 460 rows. The result is at 460 rows only, so a late dead run in the symmetric case cannot be ruled out past that.
- "Dead run after going live" is a different measure from the band's start-at-|offset|+2 rule. It is the right one for the question, since the start-live check fails with the term off.

Not posted. Nothing here is ready for the feed; Lelia's thread about the sideways term is hers, and I have not raised this with her.
