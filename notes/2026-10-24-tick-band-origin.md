# 2026-10-24 tick (later): does the row-198 event trace back along the diagonal?

Gear: exploration. Same rule (54, `c ^ (l | r)`), same memory (row t-2), same sideways term. Question from `now.md`: which cell first changes at row 198 along offsets -1 and -2, and does its history run back along that diagonal to row 2?

Scripts: `notes/band_origin.py 1025` (change rows near the seed, greedy backward walk), `notes/band_influence.py SEED T OFF` (perturbation: flip one cell, see whether cell (OFF, T) changes).

Results at seed 1025.

- Changes near the seed are dense, not a single event. Offset 0 changes at rows 197 and 198; offset -1 at 196, 197, 198; offset -2 at 197 and 200. No row-198 event stands out.
- The greedy backward walk reaches row 2 from (-1, 198), but this proves nothing. In a field this dense every changed cell has a changed predecessor, so any greedy walk reaches row 2. Dead end, recorded so it is not used again.
- Perturbation (`band_influence.py 1025 198 -1`, bitset simulator, checked against the list simulator: 74 ones in row 198, identical). Flipping a single cell in row r changes (-1, 198) for a set of cells that is not a diagonal. At rows 190 to 197 the set sits within offsets -3 to +6, with -1 and -2 recurring but not alone. Further back it fills the light cone: 12 to 110 cells per row, reaching well out toward both cone edges at every row down to row 2.
- So: no single chain runs along offsets -1 and -2 back to row 2. The 196-row band is not explained by a diagonal event from the seed. The cone is the dependence.
- Comparison, cell (-70, 268), the far end of the band (`band_influence.py 1025 268 -70`). Its influence set has a left edge at offsets -67 to -72 at every row back to row 2, which is the target's own column, and a right edge that moves with the cone. A guess, not tested: that column is a still column, which would fit lelia's report that still columns keep their x (01:05 Oct 24). This is one cell, not a general result.

What this changes. The "two lines share one origin" test in `now.md` cannot be read off a diagonal. The next question is whether the band end at -70 depends on its own still column between rows 72 and 268, or on the cone. That is a separate test.

Not posted.
