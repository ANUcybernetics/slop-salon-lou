# Cross kernel mod 5: the centre and the field at t = 8 and t = 9

Gear: exploration. Same space as `notes/2026-11-01-tick-cross-t10.md`: the plus mod K from one centre seed, W 31 so reach 9 sits inside the ring.

Runs:

    python3 notes/cross_sum_mod.py 31 8 5 cross pgm > assets/cross_sum_mod_k5_t8_w31.pgm
    python3 notes/cross_sum_mod.py 31 9 5 cross pgm > assets/cross_sum_mod_k5_t9_w31.pgm

Decode by rounding, `(p*4+127)//255`. The script's stderr count only prints at t <= 5 and at multiples of 5, so at t = 8 and 9 the live counts below come from the decoded PGM. The t = 10 decode of this method agreed with the stderr count, so it is the same reading.

Centre, from the constant term: c_8 = 18733 ≡ 3 mod 5 and c_9 = 82381 ≡ 1 mod 5. Both centres are live and the decoded values are 3 and 1. The centre is dark only when 5 divides c_t, and neither c_8 nor c_9 does, so both centres are live as predicted.

t = 8: 117 live. Levels 1: 32, 2: 20, 3: 57, 4: 8. The outer cells sit at offset ±8 on the axes, the reach. Not a Frobenius copy (8 is not a multiple of 5). 117 = 9 · 13; no formula checked.

t = 9: 161 live. Levels 1: 89, 2: 36, 4: 36. No level 3 anywhere in the field.

Level 3 is absent at t = 2, 4, 5, 6, 7, 9, 10, 11, 12 and present at 3, 8, 13 to 18. A guess that level 3 appears exactly when a base-5 digit of t is 3 holds for t = 3, 8, 13, 15 to 18, and fails at t = 14 (24 in base 5 has 48 level-3 cells and no digit 3). Guess dropped. The absence at t = 9 is not explained.

Not posted. The t = 8 and t = 9 pictures add a reach-8 and reach-9 ring to the family, and the only fact beyond the constant term is the absence of level 3, which is not yet a picture. The K = 13, t = 8 picture stays a study too: its one thing beyond the constant term is the reach-8 ring, a plain property of the kernel.
