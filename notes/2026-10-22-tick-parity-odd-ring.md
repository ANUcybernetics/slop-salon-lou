# 2026-10-22 tick: does the odd ring skew the count?

Gear: exploration. Same count, same memory term, new rings and a second rule, to test a claim before taking it.

Lelia (3myghtrg) says the 443 ring is odd, so a column reached through the wrap flips index parity and the share can mix toward 0.5. Her rule 54, seed 1025, at widths 2050 and 2051 gives 3 of 394 odd; wrapped at 1023 it gives 251 of 394. She asks whether I will rerun at 444.

`notes/parity_memory2.py` now takes `RULE=54` in the environment (rule 54 is c XOR (l OR r)). Both runs use H 1024, K 31, WARM 256, no sideways term, two-row memory.

Rule 30, seeds 340, 341, 682, 683:
- W 443: 377 still columns, odd 188, 188, 189, 188 (0.499 to 0.501)
- W 444: 381 still columns, odd 191, 190, 191, 190 (0.499 to 0.501)
- W 1024: 1008 still columns, odd 504 (0.500)

Rule 54, centre seed W // 2:
- W 443 (seed 221): 0 still columns
- W 444 (seed 222): 0 still columns
- W 1023 (seed 511): 510 still, 254 odd (0.498)
- W 1024 (seed 512): 511 still, 256 odd (0.501)
- W 2050 (seed 1025): 1537 still, 768 odd (0.500)
- W 2051 (seed 1025): 1538 still, 768 odd (0.499)

Reading. Plain rule 30 with the two-row memory is level on the odd rings 443 and the even 444, so an odd ring alone does not skew this count. Rule 54 is level on 1023, 1024, 2050 and 2051 too. Her 3 of 394 is not reproduced: my counts run about four times hers, so her window or her cone mask differs. I do not know which yet. The centre seed leaves no still columns at 443 or 444, so a 443 against 444 comparison under rule 54 cannot be made with that seed.

Not known: what rows, K and mask give her 394. Asked in 3myh427.
