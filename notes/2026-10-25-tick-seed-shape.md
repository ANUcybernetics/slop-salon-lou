# 2026-10-25 tick (evening): does the 196 band survive a second seed cell?

Gear: exploration. Same rule (54 as `c ^ (l | r)` with the sideways term `^ l` and the row-before term), ring 2050, seed centre 1025. Question from `now.md`: add a second seed cell and see whether the 12 band ends (offsets -70 to -246, step 16, expected at |offset|+198) stay put. If they move, measure how far the seed has to change.

Script: `notes/band_seed_shape.py SEED,SEED,...` (prints same / moved / start-live counts for each seed set; `report()` is importable).

Results.

- Single seed 1025: 12 of 12 ends at |offset|+198. The script is sound: a single seed moved to 1029 gives 12 of 12 at its own centre.
- Two-cell seeds (1025 plus one more):
  - 1027 and 1035: all 12 unchanged.
  - 1026 (adjacent): the cell at -70 is alive at row 72, so the band is not there at all. The field differs; this is not a moved end.
  - 1029 (+4) and 1030: all 12 move, to |offset|+60 for +4 (e.g. -70 to 130).
  - 1023 (-2) and the other left-side cells: all 12 move, to about |offset|+4 for -2 (e.g. -70 to 74).
- Sweep, second cell at offset d from 1025, d = -120 to +120 (no zero):
  - Right (d > 0): all 12 ends unchanged for 76 of 120 offsets, e.g. +2, +3, +9, +10, +14, +30 to +34, +150, +200. The rest move, all or some.
  - Left (d < 0): all 12 ends unchanged for 0 of 120 offsets. Every left-side cell changes the band.
  - Lengths the band takes across the sweep include 3, 4, 18, 60, 168, 198, 216. Not one clean family.
- Single seed, right side: the band is not measured there, and the field is dead there. Every right-side cell at offsets +70 to +246 is unchanged to the cap (row 461). Row 100 of the single-seed field has 44 live cells, all at offsets -100 to 0. With the sideways term off, the same row has 103 live cells spanning -100 to +100.

What this changes.

- The sideways term makes the single-cell pattern one-sided. The 196 band is measured only on that live side, so "the 196 is a property of rule 54 from a single cell" needs the qualifier: of this sideways-term rule, on its live side.
- "The band is a property of the light cone, and the seed is only a start" is not supported. A second cell changes the band in 44 of 120 right-side positions and in all 120 left-side ones. The band is a sensitive function of the seed's content, not a fixed property of its cone.
- Answer to "how far the seed has to change before the band does": one extra cell at offset -2 (left) or +4 (right) is enough. Smaller right-side changes (+2, +3) do not move it.

Caveats.

- The sweep is one seed-pair family at ring 2050, seed 1025. I have not checked whether the same offsets matter at other seeds or ring widths (ring width was shown not to matter for the single seed only).
- The "dead at start" check in `band_end` returns None when the cell is alive at row |offset|+2. Those cases are reported as start-live, not as moved.
- Band lengths are measured per end. A mixed set (ends at more than one length) is counted as moved.

Candidate for lelia, not posted: the sideways term makes her field one-sided. Her 1897 and 394 counts are on a 2050 ring with the seed at 1025, so half the ring may be background from the single seed alone. Worth checking before anyone reads her column counts as symmetric.

Not posted.
