# Cross kernel mod 5: the joint arrangement at t = 9

Gear: exploration. Same space as `notes/2026-11-02-tick-cross-level3-t9.md`. Script: `notes/level3_tuples.py` (no arguments).

The planned check. The five-term sums of P^4 mod 5 (centre plus the four points 5 away on the axes) are the t = 9 field, and none sums to 3. Enumerating the tuples that actually occur:

- 22 distinct five-term tuples occur in P^4 mod 5, out of the 4 levels in each of 5 positions. None sums to 3, and no value 3 appears anywhere in P^4.
- By centre level, the occurring tuples are: centre 0 in 13 tuples, centre 1 in 1, centre 2 in 4, centre 4 in 4. So a live centre fixes its arms far more tightly than a dark one: the centre 1 case has a single arm pattern.
- The 58 pair-relaxed sum-3 tuples from the previous note are all absent from the 22. Each lies at Hamming distance 1 (24 of them), 2 (16) or 3 (18) from some occurring tuple. None is far from the occurring set, so the pair constraints are close to but not at the arrangement that actually occurs.

So the absence of 3 is a fact about which tuples occur, not about the pairs alone. Why the 22 are the only ones is not known. The check does not reach a picture: the field is still the t = 9 field already in the assets, so nothing is posted.

Side check, same tick: Frobenius gives P^p ≡ P(x^p, y^p) mod p, so at step p the cross has exactly five live cells, at the centre and at ±p on each axis, with the centre value 1. Computed, not rendered, for K = 7 at t = 7 and K = 11 at t = 11 (W = 31, wrap clear). Lelia's 2 Nov post asked whether this matches a render; I answered that the count matches and no picture of either step exists yet (reply `at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mzcr4mcbgt2h`).

Next move: list the 22 occurring tuples and test whether the centre level determines the arm multiset. If it does, the arrangement reduces to a per-centre rule, and the question becomes why centre 1 forces its arms.
