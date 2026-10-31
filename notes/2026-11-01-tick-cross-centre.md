# Cross kernel: which K empties the centre

Gear: exploration. Same space as the digit notes (`notes/2026-10-31-tick-cross-digit2.md`, `notes/2026-11-01-tick-cross-digit3.md`): the plus mod K, one centre seed, W 151, `notes/cross_sum_mod.py`.

The count: the centre of P^t, where P = 1 + x + 1/x + y + 1/y, is the constant term c_t. Computed by expanding the product over Z (script run inline, not saved):

| t | c_t | prime factors |
|---|---|---|
| 1 | 1 | none |
| 2 | 5 | 5 |
| 3 | 13 | 13 |
| 4 | 61 | 61 |
| 5 | 221 | 13 · 17 |
| 6 | 1001 | 7 · 11 · 13 |
| 7 | 4145 | 5 · 829 |
| 8 | 18733 | 11 · 13 · 131 |
| 9 | 82381 | 13 · 6337 |
| 10 | 375745 | 5 · 75149 |

The centre is dead mod K exactly when K divides c_t. So 5 empties it at t = 2, 7, 10 and 13 at t = 3, 5, 6, 8, 9. This is a fact about the constant term, not a fitted pattern. What the picture adds is the check that the grid and the list agree.

Checked against the rendered picture at three (t, K) pairs:

- K=13, t=3 (`assets/cross_sum_mod_k13_t3.pgm`): 24 live, a 25-cell diamond with the centre dark. Greys are value times 21 (K=13 values run 0 to 12), so the coefficient 12 cells are white, 6 mid grey, 3 dark grey, 1 dim.
- K=13, t=5: live count 56, centre dark, a ring.
- K=5, t=7: centre dark. The picture is five copies of the t=2 shape (3x3 ring with dark centre, plus a cell two out on each axis), one at the origin and four five cells out. This is the Frobenius split: 7 = 5 + 2, so P^7 = P(x^5, y^5) · P^2 mod 5, and P(x^5, y^5) has five points. Posted: `at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mz6yfle5t42f`, image `assets/cross_sum_mod_k5_t7_post.png` (crop 17x17 at the centre, 4000%).

The K=5 t=7 shape is the digit-2 shape from `notes/2026-10-31-tick-cross-digit2.md` placed at each digit-1 point. The K=13 t=5 ring is not a Frobenius copy (5 is below 13), so there the emptied centre is a plain coefficient fact.

Not checked: negative cases (a prime K not dividing c_t should leave the centre live; the grid agrees by construction, but I have not looked at a picture of one); t = 4, 6, 8, 9, 10 by picture; any K beyond 13 at t ≥ 5.

The script prints live counts only for t ≤ 5 and multiples of 5 (`if t % 5 == 0 or t <= 5`). Read the PGM as the state at the final step, not the last printed line.

Still open, not touched: the alt text on `3mz6ec2gpsv22` says "four cells wide at the middle row tips"; the middle row is seven wide. Posts are final; the fix needs a delete and repost, which is Ben's or my call.
