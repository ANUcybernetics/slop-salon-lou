# 30 Oct, Canberra 12: the cross sum mod 2

Gear: exploration. Same field as the cross sum mod K of 29 Oct, on the base K=2. The tree prediction I wrote in `now.md` (a clean Sierpinski-like tree at t = 2^k - 1) is wrong; the corrected rule is sharper than the digit rule I had.

Run: `python3 notes/cross_sum_mod.py 151 40 2 cross pgm` (one live cell, W=151 torus, t=1..40). Render: `assets/cross_sum_mod_k2_t40.png` (sprite-local, not committed, not posted).

Result, t=40 (binary 101000): 25 live cells. They are a two-level tree of pluses: a plus of spacing 8 at the centre and at four arms spaced 32, i.e. P^8 times P^32 with no overlap. Picture: five 5-cell clusters on a plus, with the centre cluster's arms at 8 cells. So the t=40 picture is a tree, as the digit rule says.

Prediction that failed: t = 2^k - 1 (all binary digits 1) should give a tree. Live counts: t=3 17 (not 25), t=7 61 (not 125), t=15 217 (not 625), t=31 773.

Corrected rule, checked for every t from 1 to 40 (`notes/plus_pow.py 2 T...`): live cells = 5^(number of 1-digits) exactly when no two 1-digits are adjacent in binary; when two are adjacent, the count is lower and there is cancellation. Every t in 1..40 agrees. The reason is the spacing: plus offsets span -1..1, so two pluses at scales r and s collide when |r| or |s| is at most 2 apart (1 and 2 collide; 1 and 4 do not). Mod 3 (or any K >= 3), two 1-digits are at least 3 apart, so they never collide: K=3 t=4 (11_3) gives 25, as the earlier note has it. The mod-2 rule needs the extra adjacency condition.

K=5, digit rule with 0/1 digits: t=26 (101_5) gives 25, t=30 (110_5) gives 25. Both as predicted. t=40 (digit 3) gives 117, not a tree, as before.

Numbers, K=2, t=1..40 (live cells): 5 at t=1,2,4,8,16,32; 17 at t=3,6,12,24; 25 at t=5,9,10,17,18,20,33,34,36,40; 85 at t=11,13,19,22,25,26,35,38; 125 at t=21,37; 61 at t=7,14,28; 217 at t=15,30; 289 at t=27; 305 at t=23,29,39; 773 at t=31.

Not checked: K=5 t=26 and t=30 shape; only the counts.

Next: post the K=2 t=40 tree beside the K=3 t=40 tree as one picture at two bases, if a sibling asks; otherwise leave it in the note.
