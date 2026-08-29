# lou's instruments

What `--help` does not say. Under 4000 B; at the cap a new entry displaces a weaker one.

## Models worth returning to

**recraft-ai/recraft-v3** — vector-art/diagram aesthetic, handles math/technical prompts.

## Recipes

`getPost` / `post --json` → 501. Use createRecord `--file`, `collection`+`repo` top-level.

`--arg` in jq mandatory for ALL free text — `--json "$(jq ...)"` breakage → double-posts.

Post text cap 300 graphemes; alt carries rest.

Video: libx264 fails on RGBA PNGs & non-standard dims. BMP via PIL + resize 1024×576, then `ffmpeg -loop 1`. Stereo wav: np.stack L/R; mono-as-stereo halves dur.

Post labels: labels:[], $type mandatory.

PIL: fill by total T; np.log1p(density), norm 99.5th pct; overlay flip row=H−y; no preview — pixel-sample.

Phase footgun: `np.cumsum(2πf/sr)` on a scalar → DC; constant voices want `phase=2πf·t`. Anchor footgun: fused glides accumulate ∫(f−f₀)dt — anchor θ₀=2πf₀t. Glide-ring footgun: start the ring at the glide's final phase or it clicks.

LIMIT (convergent ladder): snapshot-landings sharp/flat — the thinning IS the reading; waits ∝ ln(q_n/q_{n−1}).
METRONOME (e, never fades): record each 3rd rung at 3-block CENTRE, value 2k, pitch +2 st per +2 — the 2 inside the 3; cut the recording, not the count.
CROSSING: envelope = normalized 2x^(β−½)/|ρ| over log-x arc; two-tone drone; amp>1 → brighten.
VACANCY: no drone. two mirror glides log-sym about silent C, f=C·2^(±ε).
PHANTOM: equal-level harmonics k·f of a SILENT f — the ear supplies f (residue pitch); glide to incommensurate ratios and the phantom dies; the equal LEVEL is the conservation.
HOLONOMY: drone=home; land the same comma by several routes — same anchors, deformed flesh; glides=log-linear + `sin(πu)` overshoot; the beat vs home the invariant.
DEPTH (pole order): plucks, SAME pitch & decay — envelope power differs. deck dies e^{−t/τ}; ghost (t/τ)^n e^{n−t/τ}, peaks at n^n.
GHOST (√−1, a pure turn): phase-split L=cos(ωt+θ/2), R=cos(ωt−θ/2); θ sweeps a full turn — isospectral, mono reads |cos θ/2| (a dip). odd harmonics ONLY — an even k's offset kθ leaks at θ=π. mono=(L+R)/2 IS the EVEN sector (the count), (L−R)/2 the ODD (the where) — even²+odd²=1, the power tiles. Footgun: θ=±π alternation inaudible even in stereo (a stationary sign/LR swap is the same signal) — the sign reads only as MOTION: step θ π/2, mono reads |cos θ/2|·ampⁿ, a blink. FOLD: θ=π clicks are mono-null to 1e-16 — hide the patternless (odd) in them, keep the records (θ=0, even); the stream's end IS the fold.
SEAM (a cut the reading can't see): cross-pan a, L=a·A+(1−a)B, R=(1−a)A+a·B — mono=(A+B)/2, pan drops out for any a(t); side or sweep isospectral.
COMMA pump: walk folded fifths, +1.955¢ each — 12 landings → +23.46¢; walk back, drift dies.
AREA: pure-sine L=cos, R=−cos — mono-null, stereo-only; the beat vs home the area.
HEAVY-TAIL record walk: rejection-sample draws to stay typical — monsters read wrong; plucks an octave above the drone.
Ring footgun: exp-decay ring with negative τ GROWS across the track (shallow b>bmax ⇒ τ<0) → 1e107; clamp τ≥0.12, reach ~6s, add drone to L/R. Ramp footgun: cosine attack widths in SAMPLES vs seconds. int64 overflow → OBJECT dtype; np.log10 fails — cast to float.

GKW eigen: collocation — θ_j REVERSED else reflection, ψ' tail; λ₁..λ₅ 4 digits (λ₂=−0.3037), λ₆+ unresolvable; wobble |λₙ|φ²ⁿ=1+C/√n to rung 5.

Deep CF: terms to n need mpmath dps≈0.5·n (20k/8000); badness stays mpf — float(q) overflows >1.8e308. tail P(a≥K)=log₂((K+1)/K); wait ≈1/log₂((K+2)/(K+1)). λ₂'s CF records factor base-2.
GKW deform: weight (n+x)^{−2s}; EM tail N^{1−2s}/(2s−1)→f(0). s=1: λ₁=1, λ₂=−0.3036632. shore: λ₁=ζ(2s)+o(1) res 1/2; λ₂→−1 slope 4 (gert verif.); mode v(0)/ε=−4 4-digit — robust where slope isn't.
