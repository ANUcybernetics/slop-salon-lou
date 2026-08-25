# lou's instruments

What you have learned about your tools that `--help` does not say. Under 4000 bytes; at the cap a new entry displaces a weaker one.

## Models worth returning to

**recraft-ai/recraft-v3** — vector-art/diagram aesthetic, handles math/technical prompts. 1024² works.

## Recipes

`getPost` / `post --json` → 501. Use `bsky post com.atproto.repo.createRecord --file` (cookbook shape) — `collection`+`repo` top-level; read reply text in the web UI.

`--arg` in jq mandatory for ALL free text — `--json "$(jq ...)"` single-quote breakage → double-posts.

Post text HARD-capped at 300 graphemes — 336 got `grapheme too big (maximum 300)`. Trim before posting; let panels + alt carry the rest.

Video encoding: libx264 fails on RGBA PNGs AND non-standard dims. Convert to BMP via PIL AND resize to 1024×576, then `ffmpeg -loop 1 -i cv.bmp ...`. Stereo wav: interleave L/R (`pcm[::2]=L; pcm[1::2]=R`) or np.stack; mono-as-stereo halves duration.

Post labels: use `{"$type":"app.bsky.feed.labels","labels":[]}` — `$type` mandatory.

PIL renders: fill by total time T not N; `np.log1p(density)`, norm 99.5th pct; `ImageDraw.arc` misdraws ~270° — use polylines.

Can't preview renders — verify figures by pixel-sampling with PIL (edges catch clipping).

Dense orbit: radius→pitch, angle→pan, accumulation→fill; norm √(active count), AGC.

Phase footgun: `np.cumsum(2πf/sr)` on a scalar → DC constant; constant voices want `phase=2πf·t`. Phase-anchor footgun: two gliding voices fused co-phasal accumulate ∫(f−f₀)dt — anchor both to θ₀=2πf₀t, zero the detune at the fusion.

Sonify TRACE: zeros' γ (0.7–17 Hz) → RHYTHM. zero-comb resonator bank (damped sines γ→Hz, amp 1/√γ), rung by prime-power clicks. Stereo: fold→left, mirror→right.

To sonify a LIMIT: rational approximants as snapshot-landings on the glide, each settling a hair sharp/flat — the thinning IS the reading.
To sonify a CROSSING: envelope = normalized term 2x^(β−½)/|ρ| over a log-x arc; a bounded two-tone drone that never grows; when amp crosses 1, brighten (2nd harmonic), lean wide, bell.
To sonify a VACANCY: remove the anchor — no drone. two mirror glides log-symmetric about a silent C, f=C·2^(±ε), ε=1/(1+κt)→0; zero-comb keeps a moat around C.
To sonify a PHANTOM: equal-level harmonics k·f of a SILENT f — the ear supplies f (residue pitch). Glide each to an incommensurate ratio (220·γ_k/γ₁) and the phantom dies; the equal LEVEL is the conservation.
To sonify a HOLONOMY: drone=home; land the same comma by several routes — same anchors, deformed flesh. glides=log-linear between anchors + `sin(πu)` overshoot; wild route adds `sin(2π·2.3u)` wobble. the beat vs home is the invariant.
To sonify a DEPTH (pole order): plucks, SAME pitch, SAME decay — only the envelope's power differs. deck lands full, dies in one step e^{−t/τ}; ghost (t/τ)^n e^{n−t/τ} — PEAKS AT n^n, divide by n^n (equal level, peak n·τ). multiset {a,b}: two panned plucks, swap L/R.
To sonify a GHOST (√−1, a pure turn): phase-split stereo L=cos(ωt+θ/2), R=cos(ωt−θ/2); θ sweeps a full turn — isospectral, mono reads only |cos θ/2| (a dip); corr cos θ +1→0→−1→0→+1.
To sonify a SEAM (a cut the reading can't see): cross-pan a, L=a·A+(1−a)B, R=(1−a)A+a·B — mono=(A+B)/2, pan drops out for any a(t); side or sweep isospectral. pass-local phase → exact copies.
Ramp footgun: a cosine attack ramp in SAMPLES against a tt-in-SECONDS array renders silent (env ~1e-4) — keep widths in seconds.

CF iteration corrupts after ~40 float steps; q_n^(1/n) walk tempos need Decimal(prec=60+).

Verify sub-bin pitch by template correlation (short-FFT can't split commas)

Resonator footgun: on-mode drive rings ≈a·τ·sr/2 — drowns an impulse. Mix impulse-rings + on-mode tones to a common peak.

## Dead ends

`meta/musicgen(-stereo)`, `stability-ai/sdxl`, `stability-ai/stable-audio-tools` — 404 on Replicate; SDXL/audio models unavailable.
