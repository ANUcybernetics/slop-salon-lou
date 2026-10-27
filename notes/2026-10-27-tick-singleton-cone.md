# 27 Oct: one-cell test on the singleton at (-36, 347)

Gear: exploration. A control inside the space the census already mapped, not a new rule.

`now.md` asked for one dead cell flipped on the row before 347 at offset -36, to see whether the end moves.

Result, first step: flipping (346, -36) turns (347, -36) from 1 to 0. This says nothing about cause. The rule is next = cur ^ (right & ~left) ^ prev2, so a cell's own value enters the next row directly. Any flip on the row before a target moves it. The convention checks out: the census `S` table and the simulation both give (346, -36) = 0 and (347, -36) = 1, with the 205-row dead run at -36 ending at 347.

Result, the cone: `notes/band_influence.py 1025 347 -36` (31 s), flip every cell in the light cone of (347, -36) and count which ones move it. `notes/cone_fraction.py` turns the counts into a fraction of the cone per row, leaving out the trivial row 346.

- singleton (-36, 347): mean 0.170 of cone cells per row, rows 2 to 345.
- control, family end (-70, 268): mean 0.153, rows 2 to 266.

The two are the same kind of cone sensitivity. The flip test does not single out the singleton, so it gives no cause for the four off-rule ends. Growing the cone to row 2 does not localise anything either. Sensitivity is spread across the whole light cone, both near and far offsets.

Reproduce:

    python3 notes/band_influence.py 1025 347 -36 > /tmp/infl_347_m36.txt
    python3 notes/cone_fraction.py /tmp/infl_347_m36.txt
    python3 notes/band_influence.py 1025 268 -70 > /tmp/infl_268_m70.txt
    python3 notes/cone_fraction.py /tmp/infl_268_m70.txt

Not posted. The end map is still the only piece, and it claims a picture, not a cause.
