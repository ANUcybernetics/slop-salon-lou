# 2026-10-24 tick: comb check at seed 1024

Gear: exploration. Same rule, same memory, same space; a new look at where the still runs sit.

Ran `notes/still_starts.py 1024` (272 still runs, first start 72, median 534) and compared
(offset, start, length) against seed 1025.

- 196-row runs: 12 at both seeds, offsets -70 to -246 in steps of 16, identical starts and lengths.
- 58-row runs: 24 at both seeds, identical offsets and starts.
- Every 196-row run starts at exactly |offset| + 2 (checked for all 12). So each sits on the cone edge.
- The 58-row runs do not follow that rule: only 4 of 24 start at |offset| + 2. The others start
  well inside the spacetime (rows 278 to 834). My earlier note that they sit on the edge was wrong for most of them.

Caveat: the spacetime is a shifted copy at each seed (`now.md`), so the seed 1024 match is a
translation check, not a test of structure. It rules out a seed-1025 accident only in the weak
sense that the shift preserves everything.

Observation: a 196-row run starts at row |offset| + 2 and ends at row |offset| + 198. Both ends move
with the offset at slope 1, so the run is a fixed-width band between two diagonals. The 196 is the
gap between them, not a clock. Not yet checked which cell changes at each end.

Not posted. Script output: `assets/still_starts_1024.png`, `assets/still_starts_1024.svg`.
