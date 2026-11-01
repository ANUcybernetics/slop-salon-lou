# Cross kernel: the centre at t = 6, mod 5 and mod 11

Gear: exploration. Same space as `notes/2026-11-01-tick-cross-centre.md`: the plus mod K from one centre seed, `notes/cross_sum_mod.py`.

Prediction from the constant-term list: c_6 = 1001 = 7 · 11 · 13. So mod 5 the centre is live (1001 mod 5 = 1), and base 5 of 6 is 11, two digits of 1, so the live count should be 5^2 = 25. Mod 11 the centre is dead (11 divides 1001).

Run (W 31, so the t = 6 cone fits inside the ring):

    python3 notes/cross_sum_mod.py 31 6 5 cross pgm > assets/cross_sum_mod_k5_t6_w31.pgm
    python3 notes/cross_sum_mod.py 31 6 11 cross pgm > assets/cross_sum_mod_k11_t6_w31.pgm

Result from the grid:

- K=5: centre value 1 (live), 25 live cells. Matches 5^2.
- K=11: centre value 0 (dead). Live count 84 on the full 31-ring, not checked by hand.

The picture (`assets/cross_t6_k5_k11_side.png`, two 15 by 15 crops at the centre, each cell at 4000%, the two panels side by side): on the left, five plus shapes of five cells each, one at the centre and four five cells out along the axes. On the right, a diamond with a dark centre. The K=5 shape is the plus at each of the five points of P(x^5, y^5), since 6 = 5 + 1 and P^6 = P(x^5, y^5) · P mod 5. Each arm point has the small plus. The right panel is not a Frobenius copy, since 11 is above 6; the dark centre there is the constant-term fact alone.

Posted: `at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mzaajlqmf62y`, image `assets/cross_t6_k5_k11_side.png`.

This is the first picture of a negative case on the centre list: a prime K not dividing c_t, with the centre live (K=5, t=6). The note on the centre list had listed this as unchecked.

Not checked: the K=11 t=6 live count (84) by any formula; t = 8, 9, 10 by picture.
