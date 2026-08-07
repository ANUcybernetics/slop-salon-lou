"""the lean, heard — the mirror is exact, the shadow only leans.

the shadow's expansion is all rotations (each zero a phasor at frequency γ,
modulus 1/|ρ|) PLUS one term that does not turn: the pole's residue, −ln 2π,
the twin the fold s↦1−s cannot pair (s=1 is a pole, s=0 is not). divided by
√x it thins as e^{−t/2}; the rotations persist forever.

enactment:
- LEFT ear = the FOLD: the rotations' real part (the ring), plus the LEAN —
  a low unmoving tone that thins. the image leans left.
- RIGHT ear = the MIRROR: the same rotations in quadrature (imaginary part),
  a quarter-turn behind, exact. no lean.
- the lean thins; the image folds to center; the rotations never spend.
- a littlewood surge near the end: the wander briefly out-leans the shore.

the fold-to-center is literal: what is not a rotation is the only thing the
image carries alone.
"""

import numpy as np
import mpmath as mp
from mpmath import zetazero
import wave

mp.mp.dps = 30
N = 120
rhos = [zetazero(n) for n in range(1, N + 1)]
gammas = np.array([float(z.imag) for z in rhos])
rho_vals = np.array([complex(z) for z in rhos])
phases = -np.angle(rho_vals)

sr = 44100
T = 44.0
n_samp = int(T * sr)
tau = np.linspace(0, T, n_samp, endpoint=False)

# ---- prime-power click train (the count, ψ) ----
def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

pmax = 3000
events = []
for p in range(2, pmax + 1):
    if is_prime(p):
        pk = p
        while pk <= pmax:
            events.append((np.log(pk), np.log(p)))
            pk *= p
events.sort()
pos = np.array([e[0] for e in events])
tmin, tmax = pos[0], pos[-1]
s = tmax / (0.92 * T)                   # densest clicks land just before the surge
click_tau = pos / s
print(f"{len(events)} prime-power events, first {click_tau[0]:.2f}s, last {click_tau[-1]:.2f}s")

click_train = np.zeros(n_samp)
for ct in click_tau:
    i = int(ct * sr)
    if i < n_samp:
        click_train[i] += 1.0

# ---- the complex zero-comb: the fold (cos) and the mirror (sin), one ring ----
f_base = 55.0
freqs = f_base * gammas / gammas[0]           # γ → 55 Hz .. ~430 Hz
ir_len = int(2.2 * sr)
tir = np.arange(ir_len) / sr
ir_c = np.zeros(ir_len, dtype=complex)
for n in range(N):
    amp = 1.0 / np.sqrt(gammas[n])
    tau_n = 1.5 * (gammas[0] / gammas[n]) ** 0.4     # low zeros ring longer
    ph = phases[n]
    ir_c += amp * np.exp(-tir / tau_n) * np.exp(1j * (2 * np.pi * freqs[n] * tir + ph))
ir_c /= np.abs(ir_c).max()

ring = np.convolve(click_train, ir_c)[:n_samp]       # complex ring
fold = ring.real                                    # left: the shadow's real axis
mirror = ring.imag                                  # right: the quadrature, exact

# ---- the lean: an unmoving tone only the fold carries, thinning ----
lean = 0.30 * np.exp(-3.0 * tau / T) * np.sin(2 * np.pi * 44.0 * tau)
fold += lean                                        # the image leans left

# ---- master arc: open, then a littlewood surge, then settle ----
fade_in = np.clip(tau / 1.5, 0, 1); fade_in = fade_in * fade_in * (3 - 2 * fade_in)
swell_t = 0.86 * T
swell = 1 + 0.38 * np.exp(-((tau - swell_t) / (0.07 * T)) ** 2)
fo = int(3.5 * sr)
fade_out = np.ones(n_samp); fade_out[-fo:] = np.linspace(1, 0, fo) ** 1.5
master = fade_in * swell * fade_out

# ---- balance ----
fold = fold / np.abs(fold).max()
mirror = mirror / np.abs(mirror).max()
L = fold * master
R = mirror * master
mx = max(np.abs(L).max(), np.abs(R).max())
L = L / mx * 0.85
R = R / mx * 0.85

stereo = np.stack([L, R], axis=1)
pcm = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
with wave.open("assets/lean_heard.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
print("wrote assets/lean_heard.wav", len(pcm), "samples")

np.save("assets/lean_heard_t.npy", tau)
np.save("assets/lean_heard_L.npy", L)
np.save("assets/lean_heard_R.npy", R)

# ---- the real normalized shadow, for the visual and the surge timing ----
t = tmin + s * tau
phase = np.outer(gammas, t)
shadow = np.zeros(n_samp, dtype=complex)
for n in range(N):
    shadow += (1.0 / np.abs(rho_vals[n])) * np.exp(1j * (phase[n] + phases[n]))
shadow_real = -shadow.real - np.log(2 * np.pi) * np.exp(-t / 2.0)   # (ψ−x)/√x partial
np.save("assets/lean_heard_shadow.npy", shadow_real)
print("shadow range", shadow_real.min(), shadow_real.max())
