# Cross kernel, digit 2: the count depends on the base

Gear: exploration. Same space as the digit-0/1 rule (plus mod K, one seed, W 151, periodic), a new digit, and the count does not fit the 5^(ones) pattern.

Counts (`notes/cross_sum_mod.py 151 T K cross pgm`, live cells at T):

- K=2, t=2: 5
- K=3, t=2: 13
- K=5, t=2: 12; t=10 (digit 20): 12
- K=7, t=2: 13
- K=11, t=2: 13

Why: at t=2 the plus is squared. The coefficients of (x^-1 + 1 + x + y + y^-1)^2 are: centre 5; four axis-1 offsets 2; four diagonals 2; four axis-2 offsets 1. Total 25, as expected. Mod K, a coefficient that is 0 is dead:

- K=3, 7, 11: no coefficient vanishes; 1 + 4 + 4 + 4 = 13.
- K=5: the centre 5 vanishes; 12.
- K=2: 2 vanishes (axis-1 and diagonals die), 5 is 1: centre plus four axis-2 cells = 5.

So the digit-2 count is set by which of {5, 2, 1} vanish mod K. Only K=5 (and K=2) differ from 13. The t=10 result at K=5 is the t=2 pattern scaled by 5, since (P^2)^5 = P^2(x^5, y^5) mod 5.

Not checked: K=13 and above, and digits 3 or 4 at prime K. The digit-2 count is not 5^(ones) and should not be stated as a digit rule.
