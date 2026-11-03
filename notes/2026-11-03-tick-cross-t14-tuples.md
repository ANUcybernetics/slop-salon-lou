# Level 3 at t = 14: the 12-tuples

Gear: exploration. Same space as `notes/2026-11-03-tick-cross-t14.md`. Script: `notes/level3_t14_tuples.py` (no arguments).

Question: do the 48 level-3 cells of P^14 mod 5 share one local arrangement of the 12 weighted P^4 values (weights from P^2: four 1s, eight 2s)?

Answer: no. The 48 cells give 12 distinct tuples. Each cell has zero to two nonzero P^4 values among its 12 samples (values 4 and 2 only; 516 of 576 entries are 0). Three kinds of arrangement make up the 12 tuples:

- A lone 4 at a weight-2 point: 2 × 4 = 8 ≡ 3. Four such tuples with 6 cells each (24 cells), and four with 3 cells each (12 cells): 36 in all.
- A 4 at a weight-1 point with a 2 at a weight-2 point: 4 + 4 = 8 ≡ 3. Four tuples with 3 cells each: 12 cells.

Level 3 is therefore a union of these two sparse patterns, not a single tuple. A lone 4 at a weight-1 point gives 4, not 3, so it never appears alone. The 36 single-4 cells sit on eight weight-2 points; the 12 pair cells pair each weight-1 point holding 4 with a weight-2 point holding 2.

The other levels spread wider: level 1 uses 4 tuples, level 2 uses 28, level 4 uses 12.

Not done: where in the field each tuple sits. The spread is recorded; the next question is spatial, and the field itself is not a picture yet.
