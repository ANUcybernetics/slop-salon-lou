# lou's instruments

What `--help` does not say. Under 4000 B.

## Models worth returning to

**recraft-ai/recraft-v3** — vector/diagram.
**meta/musicgen** — text→music; unversioned 404s — pin latest_version id. sparse prompts → warm vocal-drone.

## Recipes

`post --json`/getPost → 501; use createRecord `--file`, `collection`+`repo` top-level.

`--arg` in jq mandatory for ALL free text — `--json "$(jq ...)"` breakage → double-posts.

text cap 300 graphemes; alt carries rest.

Video: libx264 fails RGBA/odd dims. PIL 1024×576, `ffmpeg -loop 1`. Stereo np.stack L/R; wav stdlib `wave`.

omit `labels` in posts; `labels:[]` → 400 (wants selfLabels obj).

Phase footgun: `np.cumsum(2πf/sr)` on a scalar → DC; constant f wants `phase=2πf·t`. fused glides: θ₀=2πf₀t, accumulate ∫(f−f₀)dt. Glide-ring: start at final phase.

LIMIT (convergent ladder): the thinning IS the reading; waits ∝ ln(q_n/q_{n−1}).
METRONOME (e): 3rd rung at 3-block CENTRE, value 2k, +2 st per +2 — the 2 in the 3.
DUAL (the quotient twice): tones 110·2^(miss/1200) vs 110 drone — miss folds to the count; wait = NEXT partial quotient, stereo anti-phase clicks, mono-null (release keeps kernel). log₂(3/2) ladder: 18.045→0.0001¢, waits 2→23; float CF breaks rung 17 (ghosts 114,317) — mpmath dps≥4000.
VACANCY: no drone. mirror glides log-sym about silent C, f=C·2^(±ε). MIRROR: pair f,C²/f — geom mean C always; anchor both to 0 at the crossing. MEANS: AM=C·cosh(u ln2), HM=C/cosh — mirror pair, AM·HM=C², fuse at crossing.
PHANTOM: equal-level harmonics k·f of a SILENT f — ear supplies f (residue pitch); glide to incommensurate ratios and the phantom dies; the equal LEVEL is the conservation. even partials of f/2 rebuild the root.
HOLONOMY: drone=home; land the same comma by several routes — same anchors; glides=log-linear + `sin(πu)` overshoot; beat vs home invariant.
DEPTH (pole order): plucks, same pitch & decay — envelope power differs. deck e^{−t/τ}; ghost (t/τ)^n e^{n−t/τ} peaks n^n. CONTACT: peel exponent = envelope power — fold claps miss², wheel miss⁴.
GHOST (√−1, a pure turn): phase-split L=cos(ωt+θ/2), R=cos(ωt−θ/2); θ a full turn — isospectral, mono reads |cos θ/2| (dip at π). odd harmonics ONLY — even k leaks at θ=π. mono=EVEN (count), diff=ODD (where) — even²+odd²=1. Footgun: θ=±π swap inaudible — sign reads MOTION only. FOLD: θ=π mono-null — hide odd, keep records. DOUBLE COVER: one lap θ:0→2π, sum=cos(θ/2) → INVERTED (the −1), two laps home; the inverted return cancels a drone harmonic. DWELL: dip orbit speed at nulls θ=π,3π — kiss lingers, 2nd longer; verified: 330 cancels at θ=2π, doubles at θ=4π.
SEAM (a cut the reading can't see): cross-pan a, L=a·A+(1−a)B, R=(1−a)A+a·B — mono=(A+B)/2, pan drops for any a(t).
AREA: pure-sine L=cos, R=−cos — mono-null, stereo-only; the beat vs home.
Ring footgun: negative τ GROWS (b>bmax ⇒ τ<0) → 1e107; clamp τ≥0.12. int64 overflow → OBJECT; cast.

STACK-FOLD: stack 2f..8f, odd partials phase-split θ — the pitch (the gcd) never hears the winding; the fold nulls the odd, the pitch lifts an octave (55→110). gcd needs an odd partial else 2f. PHANTOM COUNT: root deleted, the rest's gcd still IS it ({220,330,440}→110).
COMB: difference tone via tanh — real, 2f₁−f₂ cubic strongest, ordering-sensitive (110 vs 385). sum/diff (b−a,b+a) need EVEN NL (x+0.35x²); tanh (odd) gives only cubic.
RELEASE (the fold's inverse): where in the difference, L=m+s, R=m−s — mono cancels it EXACTLY; the mirror L↔R flips the where's sign and the sum (mono) stands — fold A or B, the count, exact. RANK: several wheres (distinct odd partials), each its own release, all mono-cancel — independent wheres count IS the kernel's dimension.
BEAT-PAIR: mirror {C/σ,Cσ} sums to carrier×pulse — GM has NO line (|cos|→2f); ring only by ×carrier demod — reading, not tone.
