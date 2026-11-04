# Cross power level 3: does the K = 5 pair alignment hold at K = 7?

Gear: exploration (same level-3 slot space, new modulus and digits).

Script: `notes/level3_k7_slots.py K C R` for t = C·K + R, carriers P^C at spacing K, rest P^R. Control: `level3_k7_slots.py 5 2 4` reproduces `level3_t14_slots.py` (48 cells, 12 slot vectors).

## Results

- **K = 7, t = 11** (the planned P(x^7,y^7)·P^4): no level-3 cells. P^11 mod 7 takes values {1, 4, 5, 6} only. Same kind of absence as K = 5, t = 9. Dead end as specified.
- **K = 7, t = 18** (digits 2, 4, the analogue of K = 5, t = 14): 120 level-3 cells, 24 slot vectors.
  - 8 lone clusters of 13 cells: one slot, weight 2 on P^4 value 5 (2·5 ≡ 3).
  - 16 mixed singletons, one cell each. Each has two slots: weight 2 on P^4 value 4 and weight 2 on value 1, where the two P^4 support points are 7 apart on an axis (for example (0, 3) = 4 and (0, −4) = 1). 2·4 + 2·1 ≡ 3.
  - No 8-cell mixed bars. The K = 5 bars do not reappear at K = 7.
- **K = 11, t = 26** (digits 2, 4): 48 cells, 12 lone clusters, no mixed entries. Prediction held: P^4 spans ±4, so no two of its support points are 11 apart on an axis.

## Reading

The pair alignment is general for this carrier and K ≤ 8, since P^4's axis extent is 8. It does produce mixed level-3 entries at K = 7. The bar shape is not general: at K = 7 the same alignment gives isolated cells. The K = 5 bars are K = 5 specific, at least for this carrier and digits.

Not yet checked: K = 3 or other digit pairs at K = 7. Whether the K = 7 singletons arrange into any larger form at higher t.
