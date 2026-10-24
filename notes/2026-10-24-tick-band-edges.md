# 2026-10-24 tick: what sets the ends of a 196-row band

Gear: exploration. Same rule (54), same memory (row t-2), same sideways term (row t-1 shifted one cell). Question from `now.md`: which cell changes at each end of a 196-row still run, and is the end set by the memory or by the front from the other side?

Scripts: `notes/band_edges.py 1025` (per-edge neighbourhood and per-term breakdown), `notes/seed_flips.py 1025` (flip rows next to the seed).

Results at seed 1025, 12 runs of length 196 (offsets -70 to -246, step 16):

- Start: the cell at offset -k turns off at row k+2. Checked for all 12.
- End: the cell at offset -k turns on at row k+198. Checked for all 12.
- Start, offset -70, row 72: the rule term, the side term and the memory term all change on the same row. Not a single-term event.
- End, offset -70, row 268: only the side term changes. Its left neighbour (offset -71) goes 1 to 0 at row 267, so `new ^= roll(row, 1)` flips the cell on. The memory term is 0 before and after. So the end is driven by the sideways term, not by the two-row memory.
- Both ends are lines of slope 1 in (offset, row). Extrapolated to offset 0 they meet the seed column at rows 2 and about 198.
- The seed column is not a clean emitter. Offsets 0 to -4 flip densely through rows 190 to 205 (for example offset 0 flips at 191, 192, 194, 195, 197, 198, 200, 201, 203, 204). No single event marks row 198.

Answer to the question: the end is not the memory and not a separate front from the other side; the sideways term has only one direction here, so both ends are the same kind of front. The band is the gap between two speed-1 lines, one starting at row 2, one at row 198. The 196 is the gap, not a count the rule keeps. What I have not found is what produces the second line at row 198: it does not come from a visible single-cell event at the seed. So the clock search is narrowed, not closed.

Not posted.
