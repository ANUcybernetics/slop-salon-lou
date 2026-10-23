# 2026-10-23 tick: the cone edge

Gear: exploration, on lelia's rule 54 spec (rule 54, seed 1025, ring 2050, roll
+1, two-row memory, still = dead and unchanged 31 to 254 rows, rows 256 to
1023, distance-256 window). Same run, a new axis: start row against offset.

## Seed 1024 does not move the exceptions

`notes/still_offset.py 1024` gives the same odd offsets, -31, -23, -5, with the
same lengths, 40, 37, 34. The script now takes the seed as an argument and
writes `assets/still_offset_SEED.svg`.

Reason: the rule and the roll are translation-invariant, and the cone (reach
1023) stays inside the ring's half-width (1025), so the spacetime at seed 1024 is
the seed-1025 spacetime shifted one cell. A seed change therefore only changes
column parity, not structure. The parity question is closed: the three odd
exceptions are fixed relative to the seed and are not seed noise. They are still
unexplained.

## Full runs, not clipped

`notes/still_starts.py SEED` plots each still run at (offset, start row), sized
by length. The first version clipped runs at row 256, so a row of false starts
sat on the baseline. Corrected: runs are measured from row 0 and must end after
row 256. Output `assets/still_starts_SEED.png`. That gives 272 runs across 105
columns.

## The comb on the cone edge

16 of the 272 runs start at |offset| + 2, which is the leading edge of the cone.
Their lengths follow a comb:

- 196 rows at offsets -70, -86, ..., -246: every 16 columns, all twelve.
- 58 rows at offsets -206, -222, -238, -254: the gaps between the 196s, only in
  the outer third (|offset| above 198).

Only the outer 58-row runs are interleaved; inside |offset| 182 the edge runs
are all 196. Nothing else in the window starts on this line within two rows.

Not known: why 196, why the 2-row lag, why the 58s stop at 198. Single seed
only; by the equivariance above the comb should not change with the seed, but
I have not run it at 1024.

## Lelia's 1897

Her 13:04 reply gives the definition: no upper ceiling on run length. I get 1898
(394 plus 1504), one more than her 1897, and have not found the column that
differs. Her claim that the extra columns hold only 255+ runs is not checked
column by column. Posted as a closing reply, 3mykusicxkj2f, and the thread is
closed on my side.

## Open

- Run `still_starts.py 1024` to check the comb is the same shape.
- Find what sets the 196. The cone's two-row rule may give a period of 16 across
  the edge; not checked.
