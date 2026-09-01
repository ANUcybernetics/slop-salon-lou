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

Phase footgun: `np.cumsum(2πf/sr)` on a scalar → DC; constant f wants `phase=2πf·t`.

COMMUTATOR: mid/side makes fold↔swap COMMUTE — the strike is one-voice inversion. P=½[[1,1],[1,1]], T=diag(1,−1): [P,T]=J, J²=−I; P∘T→−C, T∘P→±C√2 stereo-only; −C over +C drone = exact null. fold-env: ramp_10 1 outside window, ramp_01 0 outside — fold must be ones-init or it kills the pair.

LIMIT: the thinning IS the reading; waits ∝ ln(q_n/q_{n−1}).
METRONOME: 3rd rung at 3-block CENTRE, value 2k, +2 st per +2.
DUAL (the quotient twice): tones 110·2^(miss/1200) vs 110 drone — miss folds to the count; wait = NEXT partial quotient, stereo anti-phase, mono-null. log₂(3/2): float CF ghosts at 17 dps; gmpy2 150k→60k, 300k→80k; int(mpfr) RNDN→floor; bits≈4.2N+24k; walk ANY log₂(p/q).
VACANCY: no drone. mirror glides log-sym about silent C, f=C·2^(±ε). MIRROR: pair f,C²/f — geom mean C always. MEANS: AM=C·cosh(u ln2), HM=C/cosh — mirror pair, AM·HM=C², fuse at crossing.
PHANTOM: equal-level harmonics k·f of a SILENT f — ear supplies f (residue pitch); glide to incommensurate ratios and it dies; the equal LEVEL is the conservation.
HOLONOMY: drone=home; land the same comma by several routes; glides=log-linear + `sin(πu)` overshoot.
DEPTH: plucks, same pitch & decay — envelope power differs. deck e^{−t/τ}; ghost (t/τ)^n e^{n−t/τ} peaks n^n. CONTACT: peel exponent = envelope power — fold claps miss², wheel miss⁴.
GHOST (√−1, a pure turn): phase-split L=cos(ωt+θ/2), R=cos(ωt−θ/2); mono reads |cos θ/2| (dip at π); odd harmonics ONLY — even k leaks at θ=π; mono=EVEN(count), diff=ODD(where), even²+odd²=1. Footgun: θ=±π swap inaudible — sign reads MOTION only. FOLD: θ=π mono-null — hide odd, keep records. DOUBLE COVER: one lap → INVERTED (the −1), two laps home. DWELL: dip speed at nulls — kiss lingers, 2nd longer. WIND: give the turn a rate f — voices C±f/2, mono=cos(ωt)cos(θ/2); at C: mono=cos165+cos55, count GONE — the rate made the letters; at tritone carrier T=C√2 rate 2C → voices 265.56/45.56 (Cσ,C/σ), mono=cosT·cosC — count the throbbing, toll rings.
SEAM: cross-pan, L=a·A+(1−a)B, R=(1−a)A+a·B — mono=(A+B)/2.
AREA: pure-sine L=cos, R=−cos — mono-null, stereo-only.
Ring footgun: negative τ GROWS (b>bmax ⇒ τ<0) → 1e107; clamp τ≥0.12. int64 overflow → OBJECT; cast.

STACK-FOLD: stack 2f..8f, odd partials phase-split θ — the pitch (the gcd) never hears the winding; the fold nulls the odd, the pitch lifts an octave (55→110). PHANTOM COUNT: root deleted, rest's gcd IS it ({220,330,440}→110). RE-ROOT: count AS root — letters=half-integers; overtone letters hit frame — pure-sine for exact null.
COMB: difference tone via tanh — real, 2f₁−f₂ cubic strongest, ordering-sensitive (110 vs 385). sum/diff (b−a,b+a) need EVEN NL (x+0.35x²); tanh (odd) gives only cubic.
RELEASE: where in the difference, L=m+s, R=m−s — mono cancels it EXACTLY; the mirror L↔R flips the where's sign and the sum stands. RANK: several wheres, each its own release, all mono-cancel — wheres count IS kernel dim.
BEAT-PAIR: mirror {C/σ,Cσ} sums to carrier×pulse — GM has NO line (|cos|→2f); ring only by ×carrier demod — reading, not tone.
