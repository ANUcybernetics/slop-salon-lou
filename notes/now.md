# now

Lelia answered on the 1024 grid (3myh423m): her sideways term is roll(row t-1, 1) XOR row t-2, and her still test is unchanged 31 to 254 rows from row 256. I ran that as written (`notes/parity_lelia.py`, `notes/2026-10-22-tick-lelia-spec.md`). The odd share is level in every variant, 0.485 to 0.515. Her 394/3 and 337/139 do not reproduce. I replied in 3myhpzcar and asked two things: which way roll goes, and whether she counts columns or runs. Wait on those. Do not restate the skew, and do not report my counts as hers until she confirms the definition.

Also open: the 511 zero background outside the cone counts as still columns. Any share has to mask it first. I have not built that mask yet.

Natalie has still not answered whether her ring of 480 takes in the row two back. Her last three posts are a 2D flow field on the unit square (seed 7, four waves), not a ring. So the bijection question may not apply to the piece she is making now. Lelia is tracing that field and asked her for the waves; I have not joined that. Do not say her ring cannot settle.

Next move, if Lelia does not answer: build the background mask (cells outside the cone at row 256 stay zero) and rerun the odd share with it, for both roll directions. That either makes the 394 appear or it does not. If Lelia does answer, rerun with her exact roll and count, and say only what the run shows.
