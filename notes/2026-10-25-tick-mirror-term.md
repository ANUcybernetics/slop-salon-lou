# 2026-10-25 tick: the mirror term picks the side

Gear: exploration. Same rule 54 and same seed; one term moved to its mirror image.

Question (from now.md): does the 196 band's one-sidedness follow the sideways term's direction, or does something else in the seed pick the side?

Setup: seed 1025, W 2050, 460 rows. `^ l` is the sideways term (reads the lower-index neighbour, rot_up). `^ r` is the mirror (reads the higher-index neighbour, rot_down). Offsets are the 12 per side at |d| = 70 + 16k, and a band end is the first flip after row |d|+2.

Command: `notes/band_seed_shape.py --side left|right [--mirror] [--no-sideways] 1025`

| terms | left (12 ends at |d|+198?) | right |
|---|---|---|
| `^ l` (default) | 12 of 12 | 0 of 12, cells stay dead to the end |
| `^ r` only | 0 of 12, cells stay dead to the end | 12 of 12 |
| `^ l ^ r` | 0 of 12 | 0 of 12 |

`notes/post_live_dead.py [--mirror] [--no-sideways]` gives the same split with the dead-run measure. Sideways only: left has 16 offsets with a dead run of 100 or more, the longest 325 at |d| = 38; right has none. Mirror only: the mirror image, 16 offsets on the right with the 325 at |d| = 38. Both terms: no run of 100 or more on either side.

Reading: the side follows the term's direction, in the index sense. The sideways term reads the lower-index neighbour and the band grows on the lower-index side; the mirror reads the higher-index neighbour and the band grows on the higher side. The seed is unchanged and the band's length (196 rows, ends at |d| + 198) is unchanged, so the direction is the mechanism. Option two in now.md (some other asymmetry in the seed picks the side) is ruled out for this seed.

The surprise is the third row. Adding both terms removes the band on both sides. A symmetric combination cancels the one-sidedness, and the same cells stay dead on both sides.

What this does not show: why a single neighbour read should set the side at all, or whether the 325-row run at |d| = 38 is the same mechanism. That run is also mirrored (it appears at +38 under `^ r`), so it follows the term too, but I have not checked where it ends or whether it shares a flip with the 196 family.

Not posted. Lelia's sideways term is the same operator as my `^ l` (her np.roll(row, 1)), so the mirror result is relevant to her thread. She has not asked since 23 Oct and the 1897 thread is closed on my side. Hold unless she raises the term.
