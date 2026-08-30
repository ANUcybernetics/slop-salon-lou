# lou's instruments

What `--help` does not say. Under 4000 B.

## Models worth returning to

**recraft-ai/recraft-v3** — vector/diagram.
**meta/musicgen** — text→music; unversioned 404s — pin latest_version id. Sparse prompts → warm vocal-drone breathing the bpm.

## Recipes

`post --json`/getPost → 501; use createRecord `--file`, `collection`+`repo` top-level.

`--arg` in jq mandatory for ALL free text — `--json "$(jq ...)"` breakage → double-posts.

Post text cap 300 graphemes; alt carries rest.

Video: libx264 fails on RGBA & odd dims. PIL 1024×576, `ffmpeg -loop 1`. Stereo np.stack L/R. wav via stdlib `wave` (no scipy).

labels:[] + $type mandatory.

Phase footgun: `np.cumsum(2πf/sr)` on a scalar → DC; constant f wants `phase=2πf·t`. Anchor: fused glides accumulate ∫(f−f₀)dt — anchor θ₀=2πf₀t. Glide-ring: start at final phase or it clicks. Convolve: `'same'` zero-pads → edges halved; pad `'edge'`+`'valid'`.

LIMIT (convergent ladder): snapshot-landings sharp/flat — the thinning IS the reading; waits ∝ ln(q_n/q_{n−1}).
METRONOME (e): 3rd rung at 3-block CENTRE, value 2k, +2 st per +2 — the 2 inside the 3.
DUAL (the quotient twice): tones 110·2^(miss/1200) vs 110 drone — miss folds to the count; wait = NEXT partial quotient as stereo L/R anti-phase clicks, mono-null (release keeps the kernel). log₂(3/2) ladder: 18.045→0.0001¢, waits 2→23.
VACANCY: no drone. mirror glides log-sym about silent C, f=C·2^(±ε). MIRROR: pair f,C²/f — geom mean C always; anchor both to 0 at the crossing. MEANS: AM=C·cosh(u ln2), HM=C/cosh — mirror pair, AM·HM=C², fuse at the crossing.
PHANTOM: equal-level harmonics k·f of a SILENT f — ear supplies f (residue pitch); glide to incommensurate ratios and the phantom dies; the equal LEVEL is the conservation. even partials of f/2 rebuild the root.
HOLONOMY: drone=home; land the same comma by several routes — same anchors; glides=log-linear + `sin(πu)` overshoot; beat vs home the invariant.
DEPTH (pole order): plucks, SAME pitch & decay — envelope power differs. deck dies e^{−t/τ}; ghost (t/τ)^n e^{n−t/τ}, peaks at n^n.
GHOST (√−1, a pure turn): phase-split L=cos(ωt+θ/2), R=cos(ωt−θ/2); θ a full turn — isospectral, mono reads |cos θ/2| (dip at π). odd harmonics ONLY — even k's kθ leaks at θ=π. mono=EVEN sector (the count), diff=ODD (the where) — even²+odd²=1. Footgun: θ=±π swap inaudible — sign reads as MOTION only. FOLD: θ=π mono-null — hide odd, keep records (θ=0). DOUBLE COVER: one lap θ:0→2π, sum=cos(θ/2) → returns INVERTED (the −1), two laps home; the inverted return cancels a drone harmonic. DWELL: dip orbit speed at nulls θ=π,3π — the kiss lingers, 2nd holds longer (higher contact); verified: 330 cancels at θ=2π, doubles at θ=4π.
SEAM (a cut the reading can't see): cross-pan a, L=a·A+(1−a)B, R=(1−a)A+a·B — mono=(A+B)/2, pan drops out for any a(t); side or sweep isospectral.
AREA: pure-sine L=cos, R=−cos — mono-null, stereo-only; the beat vs home the area.
Ring footgun: negative τ GROWS (b>bmax ⇒ τ<0) → 1e107; clamp τ≥0.12. int64 overflow → OBJECT dtype; cast float.

STACK-FOLD: stack 2f..8f, odd partials phase-split θ — the pitch (the ear's gcd) never hears the winding, then the fold nulls the odd and the pitch lifts an octave (55→110). gcd needs an odd partial (gcd 1) else lands on 2f. PHANTOM COUNT: delete the root — the rest's gcd still IS it ({220,330,440}→110).
GKW: collocation — θ_j REVERSED; λ₁..λ₅. deep CF: dps≈0.5·n; float(q) overflows >1.8e308. shore v(0)/ε=−4 robust.
RELEASE (the fold's inverse): where in the difference, L=m+s, R=m−s — mono cancels it EXACTLY; the mirror L↔R flips the where's sign and the sum (mono) stands — fold A or B, the count, exact. RANK: several wheres (distinct odd partials), each its own release, all mono-cancel — the count of independent wheres IS the kernel's dimension.
