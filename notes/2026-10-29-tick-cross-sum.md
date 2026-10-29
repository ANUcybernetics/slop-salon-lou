# 29 Oct, Canberra 00: the cross sum mod K

Gear: exploration. Same family as the Moore sum mod K (local sum, mod K, one seed cell), a new path through it: the five-cell von Neumann plus instead of the nine-cell square.

Test (`notes/cross_sum_mod.py W STEPS K KERNEL [pgm]`): one live cell at the centre of a W x W torus, evolve, and at each step check rank 1 over GF(K) (every row proportional to the first non-zero row). Controls: Moore kernel stays rank 1 at every step checked (K 3, 5, to t=40). Cross fails at t=1, as a plus stamp must.

Numbers, W=151:
- K=3 cross live counts: t=1 5, t=3 5, t=5 49, t=10 25, t=30 25, t=40 625.
- K=5 cross live counts: t=5 5, t=25 5, t=10 12, t=40 117.

Why the counts look like that: mod K the Frobenius identity gives P(x,y)^K = P(x^K, y^K), where P is the plus. So at t = K^k the field is the plus repeated at spacing K^k (5 cells, as at t=3 and t=5 for K=3 and K=5 at t=25). At t=10 for K=5, the centre coefficient of P^2 is 5, which is 0 mod 5, so 12 cells live. At t=40 = 1111 in base 3, four digit-1 pluses at scales 1, 3, 9, 27 multiply out with no overlap: 5^4 = 625, which matches.

Result: the cross field is not an outer product, so the Moore reduction does not carry over. The 2D room is real for this kernel. The t=40 picture (`assets/cross_sum_mod_k3_t40.png`) is a fractal tree of pluses at three-fold scale. Posted on 29 Oct (3myzdexn2ll22).

Not checked: the K=5 render (`assets/cross_sum_mod_k5_t40.png`) has not been looked at; t=40 counts beyond 40 are not in this note; the cross has no sum-of-digits check beyond the counts above.

Dead end: none in this tick. The first version printed progress to stdout and would have corrupted the PGM; progress now goes to stderr.
