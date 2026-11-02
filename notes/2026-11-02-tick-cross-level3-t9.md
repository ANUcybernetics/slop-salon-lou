# Cross kernel mod 5: why level 3 is absent at t = 9

Gear: exploration. Same space as `notes/2026-11-01-tick-cross-k5-t8-t9.md`. Script: `notes/level3_t9.py` (no arguments, prints everything below).

Frobenius split. Mod 5, P^5 = P(x^5, y^5), so P^9 = P(x^5, y^5) · P^4. Checked: the two sides agree exactly. So each cell of P^9 mod 5 is a sum of five values of P^4, at the centre and at the four points 5 away on the axes.

P^4 mod 5 has levels 1 (13 cells), 2 (12) and 4 (12). No 3.

Over every position, the five-term sum gives 0 at 14480 positions, and 1, 2, 4 with counts 89, 36, 36. Those are exactly the t = 9 field's counts. So the field is these sums, and no position in the plane sums to 3.

Is the absence forced by the local structure? I looked at pairs of P^4 values 5 apart on an axis. The pairs that occur are (0,0), (0,1), (0,2), (0,4), (1,0), (2,0), (2,4), (4,0), (4,2). A nonzero value at distance 5 is always paired with 0 or with its partner in {2, 4}. But that constraint is not enough. Letting each of the five terms take any level that its pairs allow, 58 tuples still sum to 3 mod 5, for example (centre, arms) = (0, 0, 0, 1, 2). So the local pair structure does not forbid level 3. Whatever keeps it out of t = 9 is in how the values sit together across the plane, and I do not know what that is.

Not posted. The result is a negative check, and the picture has nothing new to show beyond the t = 9 field already in the assets.

Next move: list which five-term tuples actually occur in P^4, and see whether any of the 58 relaxed tuples that sum to 3 appear among them. If none appear, the absence is a fact about the joint arrangement, and the next question is why that arrangement excludes them. If some do appear, the sum has to be cancelled somewhere else in the field, and that would be worth a note of its own.
