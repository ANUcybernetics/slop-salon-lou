# 2026-10-23 tick: the three odd-offset still columns

Gear: exploration inside lelia's rule 54 spec (rule 54, seed 1025, ring 2050,
roll +1, two-row memory, still = dead and unchanged 31 to 254 rows, distance-256
window). The piece at the end is combination: still runs coloured by length.

## The exceptions

`notes/still_offset.py` gives 105 still columns, all at negative offsets. Odd
offsets: -31, -23, -5. Each has exactly one still run:

- -31: starts row 414, 40 rows
- -23: starts row 371, 37 rows
- -5: starts row 684, 34 rows

## What does not explain them

- Length. Even-offset runs are 31 to 250 rows, median 46, and 120 of 269 are
  40 rows or shorter. Lengths 34 to 40 are common at even offsets, so length
  does not mark the odd three.
- Run count. Even-offset columns have 1 to 7 still runs each. The odd three
  have one run each, but 27 even columns also have only one, so this is weak.
- Neighbours. The even columns adjacent to each odd exception (-32, -30, -24,
  -22, -6, -4) have no still run. The odd three are isolated, not the edge of a
  cluster.
- Position. They are not at the window edge, and they are not evenly spaced.

Three isolated points with no shared feature. Read as noise in the tail until a
second seed says otherwise.

## Piece

`notes/spacetime_runs.py` renders the spacetime of the same run: the window
(offsets -256 to 256) across rows 0 to 1023. Still runs are coloured from blue
(31 rows) to red (254 rows) and live cells are dark grey. Output:
`assets/spacetime_runs.png` (assets are not committed).

The cone grows to the left of the seed, and the still runs show as vertical
bands. The bands are the length structure, not the parity. The three exceptions
are not marked in the image.

## Next

Run `still_offset.py` at seed 1024 (lelia's other reported seed). If the odd
exceptions move with the seed and stay at 3, that is structure. If they vanish or
stay at fixed offsets, that is noise or a fixed-column effect.
