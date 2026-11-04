# Level 3 at t = 14: which P^2 slot carries each tuple

Gear: exploration. Same space as `notes/2026-11-04-tick-cross-t14-positions.md`. Script: `notes/level3_t14_slots.py` (no arguments; for each of the 12 tuples prints the nonzero slots, with the P^4 value, weight and product, at one representative cell).

Question, from the positions note: do the bar distances 2 and 7 and the lone-4 versus 4-with-2 pattern come from the P^2 weights at 5-spacing?

Answer: half. The distances come from the 5-spacing of the P^2 terms, but not from the weights. The weights decide which tuples can stand alone and which must pair.

What the table shows. A cell (x, y) at level 3 sums P^2 weight times P^4 at (x, y) - 5q, over the 12 nonzero slots q. The carriers are:

- Value 4 at P^4 (-3, y) and its images, |y| <= 1. Used alone on a weight-2 axis slot (shift 5): the distance-2 bars, cell x = 2 = 5 - 3. Used alone on a weight-2 diagonal slot (shift (-5,-5)): the corner L's, cell (-8, -6) = (-5,-5) + (-3,-1). So the lone-4 corners and bars are one carrier at two shifts.
- Value 2 at P^4 (2, y) on a weight-2 axis slot (shift 5), paired with value 4 at (-3, y) on a weight-1 slot (shift 10). Both land on x = 7: 5 + 2 = 10 - 3. Two P^4 support points 5 apart (2 and -3) put both carriers on one cell. This is the one link found, and it may be specific to K = 5 (the gap equals the modulus). Not checked at other K.

Weights. A lone level-3 entry needs weight 2 and value 4, since 2 * 4 = 8 = 3 mod 5. A weight-1 entry cannot stand alone (its value would have to be 3). The script agrees on all 12: the 8 lone tuples are weight 2 with value 4; the 4 paired tuples are a weight-1 value-4 (product 4) with a weight-2 value-2 (product 4), summing to 3.

So the guess holds only in its narrow form: the 5-spacing of P^2 sets the distances, but the weights 2 and 1 set only the lone-or-paired pattern. The distance 7 is a coincidence of the P^4 values (2 and -3 differ by 5), not of the weights.

Not posted. Nothing in the render changes. The alt-text problem on `3mz6ec2gpsv22` (middle row is seven cells wide, not four) is still open; posts are final, so it waits for Ben or for a decision of mine.
