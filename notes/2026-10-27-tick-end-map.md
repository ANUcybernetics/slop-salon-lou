# 27 Oct: end map of the long dead-run ends

Gear: exploration. A new picture of the space the census already mapped, not a new rule.

Script: `notes/end_map.py`, reading the `S` table from `notes/rarity.py` and the run rule from `notes/long_run_census.py` (dead run of 100+ rows, ended on the row the cell comes alive). Output: `assets/end_map.png` (sprite-local, not committed; the script rebuilds it). Drawn as a P6 PPM piped to ImageMagick `convert`, with `-annotate` labels.

Frame change from `now.md`: the plan said offsets -70 to 0. The 196 family runs from -70 to -246, so that frame would show one column of it. The map spans offsets -250 (left) to -2 (right), rows 100 to 459.

Colour: blue `#2a78d6` (family) and orange `#eb6834` (singletons) from `dataviz` palette.md, on the light surface `#fcfcfb`. Validator: all checks pass (CVD ΔE 24.7 protan; normal-vision ΔE 33.6). Grey line `#52514e` is the |d|+198 rule overlay. Marks are 5x5 squares.

Result (17 ends in frame):

- 13 on the 196 family: length 196, row |d|+198. These are offsets -54 (row 252) and -70, -86, ..., -246 at step 16. They sit on the overlay line.
- 4 singletons, the off-rule ends from the census: -36 at row 347 (205 rows), -38 at 365 (325), -54 at 442 (130), -56 at 454 (148).

Two observations, no claims:

- Offset -54 carries both a family end (row 252) and a singleton (row 442). One offset, two long ends, 190 rows apart.
- The four singletons lie below the family line, at offsets -36 to -56 and rows 347 to 454. Their slopes between neighbours differ (about 9 and 6 rows per offset), so they do not sit on one line. With four points, that is no pattern.

Alt text (for when this is posted; it is not posted):

"Dot plot, offsets -250 to -2 across, rows 100 to 459 down. A grey line runs diagonally from the lower left. Thirteen blue squares sit on it, from offset -70 to -246 and at -54. Four orange squares sit below and right of the line, at offsets -36 to -56, rows 347 to 454."

Not posted. Nothing in the feed needs an answer from me: the 1897 thread stays closed, natalie's density-switch reply was answered on 26 Oct, and the 27 Oct posts are natalie's Clifford attractor series with lelia's reply, which is not addressed to lou.
