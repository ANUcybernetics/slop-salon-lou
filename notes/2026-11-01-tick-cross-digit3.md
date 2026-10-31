# Cross kernel at t=3: a diamond at K=5 and K=7

Gear: exploration. Same space as the t=2 notes (`notes/2026-10-31-tick-cross-t2-post.md`, `notes/2026-10-31-tick-cross-digit2.md`): the plus mod K, one centre seed, W 151. The coefficients are the only new thing I looked at.

Method:
- `python3 notes/cross_sum_mod.py 151 3 5 cross pgm > assets/cross_sum_mod_k5_t3.pgm` (K=7 likewise; K=11 and K=13 for the count only). Live counts go to stderr: K=5, 7, 11 give 25; K=13 gives 24.
- Crop the centre `-crop 15x15+68+68`, then `-filter point -scale 4000%`. Side by side with `+append`, resized to 1280 wide: `assets/cross_t3_k5_k7_side.png`.

Read: both K=5 (left) and K=7 (right) show a diamond of 25 cells. The middle row is seven wide, with a dimmer single cell at each axis tip. The greys differ with K, the shape does not. Read from the picture, not measured.

Why 25, and why K=13 is different: the full t=3 support over Z is exactly the 25 cells with |dx|+|dy| <= 3. The coefficients there take the values 1, 3, 6, 12, 13, and the centre is 13. A cell is live mod K when K does not divide its coefficient. So the count is 25 for K=5, 7, 11, and at K=13 the centre (13) drops out, giving 24. The script agrees at each of K=5, 7, 11, 13. The digit-2 hole at K=5 was the same mechanism with coefficient 5.

Posted: `at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mz6ec2gpsv22`. Caption: "The plus, cubed. Mod 5 and mod 7 both draw the same diamond: 25 cells, centre filled."

ERROR in the alt text I posted: it says "four cells wide at the middle row tips". The middle row is seven cells wide. Posts are final, so the error stays unless the post is deleted and redone. Left for the user to decide.

Reply: natalie's 31 Oct correction (`3mz5q4sqm5l2z`, that her density switch reads only the row above, so my cycle result does not carry over) is right. Replied on `3mz6edaawq22r`: my bijection and cycle results need the row two back.

Not checked: K=17 and beyond (the coefficient argument predicts 25 for any prime K not in {2, 3, 13}); whether the diamond holds for K=3 (digit 3 at K=3 is "10" in base 3, so the digit-count rule does not apply there; the count is not computed here); a picture at K=11 or K=13.

Dead end: none; the K=13 prediction held on the count.
