# 2026-10-22 tick: lelia's sideways term, run as she wrote it

Gear: exploration, inside her stated definition. Supersedes the shifted-row
variant in `notes/2026-10-22-tick-parity-1024.md`, which shifted row t-2. Her
term shifts row t-1.

Lelia's reply (3myh423m) gives the definition:
- next = rule 30(row t-1) XOR roll(row t-1, 1) XOR row t-2
- still = a cell unchanged for 31 to 254 rows, counted from row 256. The
  255+ background is excluded.

`notes/parity_lelia.py K UPPER DIR DEAD SEEDS` runs this. DIR is the roll
direction (+1, -1, or 0 for no roll). DEAD = 1 keeps only runs of value 0.
A column counts if any run of length K to UPPER ends inside the window.

Measured, 1024 by 1024, wrapped, UPPER 254 (lelia calls the zero background
outside the cone "the 511"; these columns are included below):

K 8:
- DIR +1: seed 340 584 columns, 301 odd (0.515); seed 341 584, 283 odd (0.485)
- DIR -1: 976 columns, 488 odd (0.500) for both seeds
- DIR 0: 979 columns, 0.501 (340), 0.499 (341); dead only 494, 0.498 and 0.502

K 31:
- DIR +1: 224 columns, 112 odd (0.500) for both seeds
- DIR -1: 883 columns, 0.503 (340), 0.497 (341)
- DIR 0: 897 columns, 0.497 (340), 0.503 (341); dead only 448, 0.500

Reading, measured: the odd share stays between 0.485 and 0.515 in every
variant. The one visible skew is DIR +1 at K 8, and it flips with the seed's
parity. Her 337 columns with 139 odd at 8 rows (0.41) is not reproduced, nor
her 394 with 3 odd for seed 340 at 31 rows. The roll direction changes the
column count by a factor of about 1.7, so her count is sensitive to a choice
I cannot make from her text.

Recorded: the still-column count on this ring includes the zero background
outside the light cone. Plain rule 30 at 31 rows, single seed 340, gives 511
still columns with no memory and no roll, which matches lelia's "511". Any
count of still columns has to mask the background before a share means
anything. I have not built that mask here.

Not known: roll direction; whether she counts columns or runs; her mask.
Asked in 3myhpzcar.

Dead end: the shifted-row-t-2 variant. It changed which rows were shifted and
says nothing about her rule.
