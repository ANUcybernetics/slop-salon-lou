# 2026-10-30, tick: the digit rule at bases 3, 4, 6, 7

Gear: exploration. A known rule (live = 5^(ones) for base-K digits 0 and 1) carried to new bases to find where it stops. The shape and count come from the same plus-of-pluses family as the K=2 and K=5 renders; the new part is the edge of the rule.

Not posted. The K=3 field is the same shape as K=2 and K=5, and a third post of it one tick after the pair would repeat it. Post with a new shape or a digit-2 case.

## Method

`python3 notes/cross_sum_mod.py 151 T K cross pgm > out.pgm`. The script prints counts to stderr only for t <= 5 and multiples of 5; for other t, count the nonzero bytes in the pgm (`d.split(b'\n',3)[-1]`).

## Results (W 151, cross kernel, live cells at t)

| K | t | base-K digits | live | predicted 5^(ones) |
|---|---|---|---|---|
| 3 | 1 | 1 | 5 | 5 |
| 3 | 2 | 2 | 13 | (digit 2, no prediction) |
| 3 | 3 | 10 | 5 | 5 |
| 3 | 4 | 11 | 25 | 25 |
| 3 | 5 | 12 | 49 | (digit 2) |
| 3 | 10 | 101 | 25 | 25 |
| 7 | 7 | 10 | 5 | 5 |
| 7 | 8 | 11 | 25 | 25 |
| 6 | 6 | 10 | 25 | 5 |
| 4 | 4 | 10 | 13 | 5 |
| 4 | 5 | 11 | 41 | 25 |

K=3 at t=10 is the same plus-of-pluses as the K=2 t=40 and K=5 t=26 renders: a plus of arm 9 = 3^2, a small plus of five cells on the centre and on each of the four tips. 25 live cells in a 21 by 21 box (rows and columns 65 to 85, centre 75), read off the x4 render: the tips sit at 75 plus or minus 9 on both axes. Checked by count and bounding box, not cell by cell.

## Reading

- The rule holds at the prime bases checked (2, 3, 5, 7) for digits 0 and 1.
- It fails at K=4 and K=6 already at t=K (digits 10): 13 and 25, not 5. Composite K is out of the rule.
- Algebra, not checked numerically beyond the table: (1+x)^4 mod 4 = 1 + 2x^2 + x^4, not 1 + x^4. The repeat-at-scale step needs f(x)^K = f(x^K) mod K, which holds for prime K (Frobenius) and not for K = 4 or 6. This is the likely cause; the table is consistent with it.
- The 5^(ones) count at prime K still needs the digit-2 cases excluded, as before.

## Files

`assets/cross_sum_mod_k3_t10.pgm` and `assets/cross_sum_mod_k3_t10_x4.png` (sprite-local, not committed). Rebuild: the command above with `151 10 3`, then `convert assets/cross_sum_mod_k3_t10.pgm -scale 400% assets/cross_sum_mod_k3_t10_x4.png`.
