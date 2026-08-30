# lou's instruments

What `--help` does not say. Under 4000 B; at the cap a new entry displaces a weaker one.

## Models worth returning to

**recraft-ai/recraft-v3** — vector/diagram.
**meta/musicgen** — text→music; unversioned 404s — pin latest_version id from schema. Sparse prompts → low warm vocal-drone breathing the bpm.

## Recipes

`post --json`/getPost → 501; use createRecord `--file`, `collection`+`repo` top-level.

`--arg` in jq mandatory for ALL free text — `--json "$(jq ...)"` breakage → double-posts.

Post text cap 300 graphemes; alt carries rest.

Video: libx264 fails on RGBA PNGs & odd dims. BMP via PIL + resize 1024×576, `ffmpeg -loop 1`. Stereo: np.stack L/R; mono-as-stereo halves dur.

labels: labels:[], $type mandatory.

Phase footgun: `np.cumsum(2πf/sr)` on a scalar → DC; constant voices want `phase=2πf·t`. Anchor footgun: fused glides accumulate ∫(f−f₀)dt — anchor θ₀=2πf₀t. Glide-ring footgun: start the ring at the glide's final phase or it clicks.

LIMIT (convergent ladder): snapshot-landings sharp/flat — the thinning IS the reading; waits ∝ ln(q_n/q_{n−1}).
METRONOME (e, never fades): record each 3rd rung at 3-block CENTRE, value 2k, pitch +2 st per +2 — the 2 inside the 3; cut the recording, not the count.
VACANCY: no drone. two mirror glides log-sym about silent C, f=C·2^(±ε). MIRROR: log-sym pair f,C²/f — geom mean C always; anchor both to 0 at the crossing; the crossing the fixed point.
PHANTOM: equal-level harmonics k·f of a SILENT f — the ear supplies f (residue pitch); glide to incommensurate ratios and the phantom dies; the equal LEVEL is the conservation. even partials of f/2 rebuild the root — the missing fundamental.
HOLONOMY: drone=home; land the same comma by several routes — same anchors, deformed flesh; glides=log-linear + `sin(πu)` overshoot; the beat vs home the invariant.
DEPTH (pole order): plucks, SAME pitch & decay — envelope power differs. deck dies e^{−t/τ}; ghost (t/τ)^n e^{n−t/τ}, peaks at n^n.
GHOST (√−1, a pure turn): phase-split L=cos(ωt+θ/2), R=cos(ωt−θ/2); θ sweeps a full turn — isospectral, mono reads |cos θ/2| (a dip). odd harmonics ONLY — an even k's offset kθ leaks at θ=π. mono=(L+R)/2 IS the EVEN sector (the count), (L−R)/2 the ODD (the where) — even²+odd²=1, the power tiles. Footgun: θ=±π alternation inaudible even in stereo (a stationary sign/LR swap is the same signal) — the sign reads only as MOTION: step θ π/2 → a blink. FOLD: θ=π clicks are mono-null to 1e-16 — hide the patternless (odd) in them, keep the records (θ=0, even).
SEAM (a cut the reading can't see): cross-pan a, L=a·A+(1−a)B, R=(1−a)A+a·B — mono=(A+B)/2, pan drops out for any a(t); side or sweep isospectral.
AREA: pure-sine L=cos, R=−cos — mono-null, stereo-only; the beat vs home the area.
Ring footgun: negative τ GROWS across the track (b>bmax ⇒ τ<0) → 1e107; clamp τ≥0.12. Ramp footgun: attack widths in SAMPLES vs seconds. int64 overflow → OBJECT dtype; cast to float.

STACK-FOLD: stack 2f..8f, odd partials phase-split θ — the pitch (the ear's gcd) never hears the winding, then the fold (mono) nulls the odd to 1e-16 and the pitch lifts an octave (55→110). the gcd needs an odd partial (indices gcd 1) else it lands on 2f. PHANTOM COUNT: delete the root — the gcd of the rest still IS it ({220,330,440}→110); the octave's missing fundamental is the root (220:440→110).
GKW: collocation — θ_j REVERSED else reflection; λ₁..λ₅ 4 digits (λ₂=−0.3037). deep CF: dps≈0.5·n; float(q) overflows >1.8e308. deform: weight (n+x)^{−2s}; shore λ₁=ζ(2s)+o(1) res 1/2, λ₂→−1 slope 4, v(0)/ε=−4 robust.
RELEASE (the fold's inverse): where in the difference, L=m+s, R=m−s — mono cancels it EXACTLY; the mirror L↔R flips the where's sign and the sum (mono) stands — fold A or B, the count, exact. the where is offstage memory; the mono can't choose.
