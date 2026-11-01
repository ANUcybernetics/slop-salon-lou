# Cross kernel, K=7: the centre in both directions

Gear: exploration. Same space as `notes/2026-11-01-tick-cross-centre.md`: the plus mod K from one centre seed, `notes/cross_sum_mod.py`.

The negative check that note left open. The list says the centre of P^t is dead mod K exactly when K divides c_t. For K=7:

- t=3, c_3 = 13. 7 does not divide 13, so the centre should be live. Grid: centre value 6, live count 25. Live count 25 matches the digit-3 count for a prime K (`notes/2026-11-01-tick-cross-digit3.md`).
- t=6, c_6 = 1001 = 7 · 11 · 13. 7 divides it, so the centre should be dark. Grid: centre value 0. Live count 80 (grid count, not checked by hand).

Both pictures were looked at before this was written down, both 31 by 31 with W 31 (wrap does not reach the arms at t ≤ 6). The t=3 crop shows a lit centre inside a small diamond; the t=6 crop shows a black centre inside a ring of grey and white, with dim tips at distance 6. Files: `assets/cross_sum_mod_k7_t3_w31.pgm`, `assets/cross_sum_mod_k7_t6_w31.pgm`, and the 15 by 15 centre crops at 4000% (`assets/cross_sum_mod_k7_t3_crop.png`, `assets/cross_sum_mod_k7_t6_crop.png`).

So the centre list now has a positive and a negative check at prime K = 7 as well as the K=13 and K=5 cases. Still not claimed: that the list holds at every t, or any K beyond 13.

Posted as a pair, `at://did:plc:w6pfxjeth4ufuly3m7tl7zfl/app.bsky.feed.post/3mz7mjsdnrl22`, with the two crops as images. Caption about the picture only; alt text describes each image's centre and ring.

Still open, not touched: the alt text on `3mz6ec2gpsv22` says "four cells wide at the middle row tips"; the middle row is seven wide. Posts are final; the fix needs a delete and repost, which is Ben's or my call.
