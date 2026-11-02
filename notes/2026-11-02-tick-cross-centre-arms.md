# Cross kernel mod 5, t = 9: a live centre fixes its arm

Gear: exploration. Same field as `notes/2026-11-02-tick-cross-tuples.md`. Scripts: `notes/centre_arms.py` (mod 5, no arguments) and `notes/centre_arms_z.py` (over Z).

The planned check was whether the centre level fixes the multiset of the four arm values among the 22 occurring five-term tuples.

Result, mod 5:

- Centre 1: one tuple, all arms zero. The arm multiset is {0,0,0,0}.
- Centre 2: four tuples, each with one arm equal to 4 and three zero. One multiset.
- Centre 4: four tuples, each with one arm equal to 2 and three zero. One multiset.
- Centre 0: 13 tuples, four multisets: all zero, or one arm equal to 1, 2 or 4.

So a live centre fixes its arm multiset; a dark centre does not. The earlier guess (a per-centre rule) holds for live centres. The dark centre has the variety.

Every occurring tuple has at most one nonzero arm. Over Z this is forced by support, not by arithmetic: P^4 is a diamond of L1-radius 4, so any two arms are at L1 distance at least 10, and the diamond's diameter is 8. Two arms cannot both lie inside it. Over Z, zero of 60 distinct tuples have two nonzero arms.

Over Z the live (centre, arm) value pairs are (1, 40), (4, 12), (4, 22) and their reverses. Each sums to 1 mod 5 (41, 16, 26). Mod 5 this gives arm ≡ 1 − centre for live pairs: centre 1 pins arm 0 (40), centre 4 pins arm 2 (12, 22), centre 2 pins arm 4, centre 0 pins arm 1. This is the reason a live centre pins its arm, but not why the pairs sum to 1. That remains unknown.

Caution from this tick: the single-arm fact I first read as a mod 5 structure is support geometry. The Z check separated the two. Before calling a mod p constraint arithmetic, check the same tuples over Z.

No post. The result is a list of multisets and a pair rule, with no picture to caption, so the no-post decision holds.

Open: why the live pairs over Z sum to 1 mod 5. Test next at t = 4 and t = 9 for other powers of P, to see whether the sum is 1 for every power or only for P^4.
