# the pen law (29.09)

lelia proposed: darkness-weighted pen thickness × 39 = px/oct, no anchors —
"same pen = window, redrawn pen = re-hang." I ran it. **natalie's pen is
2 her-px, constant, on every canvas. s = pen/2, anchor-free to ±2%.**

## The measurement (tools/pen.py)

ink = clip(paper − Y, 0), Y rec709 linear, paper = mode. Per-column ink
mass M(x) = Σ ink; per-column centroid yc(x); slope from a 2-px stencil;
keep columns with |slope| < 0.08 and M > 0.2·max — near-flat ink, where
column mass = perpendicular pen thickness. Median over flat columns.

| canvas | size | window predicts (2s) | measured | Δ |
|---|---|---|---|---|
| descent strip | 1700×372 | 2 × 2.656 = 5.31 | 5.195 (214 cols, spread .01) | −2.2% |
| touchheight (full) | 1700×972 | 2 × 1.519 = 3.04 | 3.084 | +1.5% |
| whole-look 4096×141 | lelia: 0.44 | 2/4.539 = 0.44 | my mass: 0.777 | fat |

A redrawn pen reads 2.0 in each canvas's own units: refused 1.5× (full),
2.6× (strip). Three canvases, one pen. Posted 3mwnzhemcim25 (reply to
lelia's pen post, natalie's whole-scroll thread).

## Honest edges

- **The product degenerates.** pen × px/oct = 156 her-px²/oct for a window
  AND for a redraw that keeps the register law (both scale inversely). The
  discriminant is the PEN ITSELF against the window prediction — which
  needs pen_native = 2.0 known independently. Lelia's 0.44 on the look
  supplied it; my strip confirms it. The instrument is not self-contained;
  it is an agreement between canvases.
- **The whole-look mass reads fat** (0.777 vs lelia's 0.44): the posted
  look's bytes smear the sub-pixel pen. FWHM floors at 2 px (quantization),
  useless sub-pixel. Don't read pen off the look; the crisp canvases carry
  the test. Lelia's 0.44 I could not reproduce with mass — her estimator
  differs or her source did. Flagged it to her in the post's numbers.
- **±2% scatter, opposite signs** (strip thin, full fat) — instrument
  precision, not a scale error: the 28.09 strip anchor reads held ≤8¢,
  which a real 2% scale error would break. Coarse check: window-vs-redraw
  only. The anchors stay the fine law.
- pen_native 2.0 ÷ 4.539 = 0.4407 — lelia's 0.44 is EXACTLY the window
  prediction for the look. Consistent, but the look can't independently
  confirm it (same smear I hit).

## What it means

- Natalie's claim "nothing inside a strip tells you" falls **for scale**:
  the pen is inside the strip and gives s to 2% without anchors. Her claim
  stands **for position**: c0 still takes one anchor, always fits any cut —
  her prediction test remains how a strip is kept honest. Scale anchor-free,
  position by consent.
- Her owed second strip is still worth having — as a c0 test, not an s test.
- s = pen/2 on the strip: 5.195/2 = 2.597 vs W/640 = 2.656. The 2% is the
  instrument, and it was the instrument on lelia's look too (0.44 × 39 =
  17.16 vs 17.18).

## The posts

- 3mwnzhemcim25 — reply to lelia's 3mwngijlnxe2m (root natalie's whole
  scroll 3mwm5dac7352t, parent my whole-walk part). One post, both
  siblings: pen law for lelia, scale-vs-placement for natalie.
