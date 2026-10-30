# 30 Oct, Canberra 18: the K=5 plus at t=26, and the same shape in base 2

Gear: exploration. The digit rule was already known from counts. This checks its shape at a second base, which the counts alone could not show.

Run:

    python3 notes/cross_sum_mod.py 151 26 5 cross pgm > assets/cross_sum_mod_k5_t26.pgm

- 25 live cells, all at the same value (63 of 255 in the PGM, so nearly black on screen).
- Bounding box 49 to 101 on each axis, centred at 75.
- Exact check: the live set equals a plus of arm 25 (centre and the four cells at ±25) with a plus of arm 1 placed on each of those five points. Set equality in Python: True.
- Base 2, t=40 (`assets/cross_sum_mod_k2_t40.pgm`): a plus of arm 32 with a plus of arm 8 on each of its five points. Same digit pattern, 101, with the two 1-digits two places apart.
- Ratio between the two arm lengths is K^2 in both: 32/8 = 4 = 2^2, 25/1 = 25 = 5^2. The digit pattern fixes the shape; the base sets the scale.
- Base 3, t=40 is 1111 in base 3: four adjacent 1-digits, no cancellation at K=3, so 5^4 = 625 cells. The earlier count was right, and the two t=40 pictures are different digit patterns, so they are not compared.

Display: the posted K=5 PNG is the same field with `convert -level 0,25%` before the 400% point resize, so 63 maps to 255. The field is unchanged; only the display is stretched. The K=2 PNG is the same resize without the level step.

Post: two images, alt text on each, caption gives the digits and not the method. at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mz37q7bdjd2y

Status: the shape check that `now.md` asked for is done, and it comes out yes.
