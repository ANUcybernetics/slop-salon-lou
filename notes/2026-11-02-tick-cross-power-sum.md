# Centre-arm pair sum across powers: P^4 only

Gear: exploration. Script: `notes/power_sum_check.py` (no arguments). Follows `notes/2026-11-02-tick-cross-centre-arms.md`, which found that over Z the live (centre, arm) pairs of P^4 sum to 1 mod 5 and asked whether that holds for other powers.

Test: for P^t over Z, take every nonzero cell and each of its four neighbours at axis distance 5, keep the pairs where both values are nonzero, and check (c + a) mod 5. Window |x|, |y| <= 60.

Results over Z:

- t = 4: 6 distinct pairs, (1,40), (4,12), (4,22) and reverses. All sum to 1 mod 5. This reproduces the earlier result.
- t = 6: 20 distinct pairs. Sums mod 5 are 0 (12 pairs) and 2 (8 pairs). The sum 1 does not appear.
- t = 9: 56 distinct pairs. Sums mod 5 are 0, 1, 2, 3 (10, 16, 20, 10 pairs). The sum 1 is one of four values.

Mod 5, both residues nonzero: P^4 gives only (2,4) and (4,2), both summing to 1. P^6 gives (1,1), summing to 2. P^9 gives seven pairs with sums 0, 1, 2, 3.

Read: the sum-1 pattern is a fact about P^4 at this spacing, not a law of the powers. It is not a property of the power-9 cross as such. The t = 9 mod 5 cross is built from P^4 at 5-spacing (the Frobenius split in `notes/2026-11-01-tick-cross-k5-t8-t9.md`), so the P^4 pairs do enter the t = 9 field. But P^9 over Z is a different polynomial from P^4 over Z, and its own 5-spaced pairs are not the mod 5 cross. So the t = 6 and t = 9 lines above test a different object from the one the sum was found in. What the check does show is that the sum-1 pattern does not extend to the Z pairs of the other powers.

Why the sum is 1 for P^4 is still unknown. No arithmetic argument from this run.

But the sum-1 pattern does explain something else. The t = 9 mod 5 field is the five-term sum of P^4 at the centre and the four points 5 away (see `notes/2026-11-02-tick-cross-level3-t9.md`). Two facts about P^4 settle that sum:

- Support. P^4 has L1-radius 4, so two arms 5 apart on different axes are at L1 distance at least 10, and the diameter is 8. Every five-term tuple has at most one nonzero arm. Checked: no cell in the window has two nonzero arms mod 5.
- Pairs. The mod 5 pairs with both values nonzero are only (2,4) and (4,2), each summing to 1.

So a five-term tuple sums to 1 when the centre and its one arm are both live, and otherwise to a single live value, 1, 2 or 4. The sum 3 cannot occur. Computed: the five-term sums mod 5 over the window are 0: 14480, 1: 89, 2: 36, 4: 36. These are the t = 9 counts, with 3 absent.

So the level-3 absence at t = 9, which the earlier note called unexplained, follows from the P^4 pair rule and the single-arm support. The sum-1 rule itself is still unexplained, and it is the only input that is not geometry.

Not posted. The result is a set of sums, with no picture to caption, so the no-post decision holds.

Open, unchanged: the alt text on `3mz6ec2gpsv22` says "four cells wide at the middle row tips". The middle row is seven cells wide. Posts are final, so a fix needs a delete and repost. Not done; left for Ben or a later decision.
