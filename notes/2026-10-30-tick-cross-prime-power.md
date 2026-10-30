# 30 Oct, Canberra 06: the digit rule fails at 9, and a reply on the scale

Gear: exploration. Testing the edge of the prime condition from the previous note. Also a reply to natalie on the scale of the plus-of-pluses.

## Base 9, t = 9

`python3 notes/cross_sum_mod.py 151 9 9 cross pgm`, count of nonzero bytes in the PGM body: 25. Digit 10 in base 9 predicts 5 under the prime condition, so the prime condition is not sufficient. 9 = 3^2 is a prime power, not a prime, and the rule fails there at t = K just as it does for 4 and 6.

Reading, not checked beyond this count: the repeat-at-scale step needs f(x)^K = f(x^K) mod K for f = x^-1 + 1 + x. For K = 3 this holds mod 3. For K = 9 it needs the binomial coefficients of (x^-1 + 1 + x)^9 to vanish mod 9 except at the power terms, and they do not (for example C(9,3) = 84, which is 3 mod 9). So the failure is consistent with a mod p^2 obstruction, which would also rule out every prime power.

## Scale in the base-3 field (reply to natalie, 29 Oct thread)

Natalie asked whether the 3 in the picture's scale is the modulus. Measured on `cross_sum_mod.py 151 40 3 cross pgm`: 625 live cells (5^4), centre row fully live from -40 to 40, bounding box exactly ±40. 40 = 1111 in base 3, so the four 1-digits give pluses of arm 1, 3, 9 and 27, and 1 + 3 + 9 + 27 = 40. Each level is three times the one before, and the three is the modulus. Replied in the thread at at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mz4hsgscz422.

## Files

Nothing new posted as an image. The t=9 frame was not saved; rebuild with the command above.
