#!/usr/bin/env python3
"""
Cobweb Map as Audible Structure

Generates audio from a cobweb map trajectory (logistic map).
Each iteration maps to a moment in a time series — amplitude, pitch,
and harmonic content all derive from the geometry of self-reference.

When the trajectory returns to a similar x-region, that "echo" creates
a reinforcing partial: the cobweb folding pattern becomes overtone structure.

Output: a precise, rhythmic, lattice-like tone — not ambient.
"""

import numpy as np
from scipy.io.wavfile import write

# ── Parameters ──────────────────────────────────────────────────────────
SR = 44100
DURATION = 15.0
R = 3.90       # logistic map parameter (chaotic regime)
TOTAL_ITERS = 500
TRANSPORT = 100  # transient burn-in
ANALYSIS = TOTAL_ITERS - TRANSPORT  # 400 iterations used for audio
SAMPLES = int(SR * DURATION)

# Audio parameters
BASE_FREQ = 110.0       # low A — foundational
HARMONIC_MULT = 3.0     # base harmonic overtone multiplier
MAX_HARMONICS = 8       # max overtone partials per iteration
ENVELOPE_DUR = 0.28     # seconds per iteration event (attack+decay)

# Cobweb analysis window
COBWEB_WIDTH = 0.12     # x-region "similarity" threshold for echo detection
COBWEB_NEIGHBORS = 5    # lookback window for matching regions

# Mix balance
CARRIER_MIX = 0.45
HARMONIC_MIX = 0.38
SUB_MIX = 0.17

# Master
MASTER_GAIN = 0.78


def cobweb_trajectory(r, total, transport):
    """Generate cobweb map trajectory, discard transport."""
    x = np.random.uniform(0.01, 0.99)
    traj = []
    for i in range(total):
        x = r * x * (1.0 - x)
        if x < 0 or x > 1:
            x = 0.5  # escape recovery (rare at r=3.9)
        if i >= transport:
            traj.append(x)
    return np.array(traj)


def detect_echoes(x, window_width, neighbor_count):
    """
    For each iteration, find neighbors whose x-values fall within
    window_width and within the last neighbor_count iterations.
    Returns list of (current_idx, neighbor_indices) pairs for
    iterations that have at least one echo.
    """
    echoes = []
    for i in range(1, len(x)):
        neighbors = []
        start = max(0, i - neighbor_count)
        for j in range(start, i):
            if abs(x[i] - x[j]) < window_width:
                neighbors.append(j)
        if neighbors:
            echoes.append((i, neighbors))
    return echoes


def make_envelope(dur_samples):
    """Smooth attack-decay envelope: fast attack, exponential decay."""
    t = np.linspace(0, 1, dur_samples)
    attack = np.where(t < 0.06, t / 0.06, 1.0)
    decay = np.exp(-6.0 * np.maximum(t - 0.06, 0))
    return attack * decay


def main():
    # 1. Generate trajectory
    x = cobweb_trajectory(R, TOTAL_ITERS, TRANSPORT)
    N = len(x)  # 400

    # 2. Detect cobweb echoes (folding returns)
    echoes = detect_echoes(x, COBWEB_WIDTH, COBWEB_NEIGHBORS)
    echo_set = {e[0] for e in echoes}  # quick lookup

    # 3. Build frequency mapping: x → frequency via power-law
    #    Low x = low frequency, high x = higher frequency
    #    Compress to musical range
    freqs = BASE_FREQ * (x ** 0.55)  # square-root compression

    # 4. Compute time mapping — spread iterations evenly across duration
    #    with slight rhythmic grouping from the dynamics
    times = np.linspace(0, DURATION - ENVELOPE_DUR, N)

    # 5. Build audio buffer
    audio = np.zeros(SAMPLES)

    for i in range(N):
        x_val = x[i]
        freq = freqs[i]
        t_start = times[i]
        sample_start = int(t_start * SR)
        if sample_start >= SAMPLES:
            break

        dur_samples = min(int(ENVELOPE_DUR * SR), SAMPLES - sample_start)
        if dur_samples <= 0:
            break

        env = make_envelope(dur_samples)
        t = np.arange(dur_samples) * (1.0 / SR)

        # ── Main carrier ──────────────────────────────────────────────
        amplitude = x_val ** 0.7  # slight compression
        carrier = np.sin(2.0 * np.pi * freq * t) * env * amplitude

        # ── Sub-bass reinforcement ────────────────────────────────────
        sub_freq = freq * 0.48
        sub = np.sin(2.0 * np.pi * sub_freq * t) * env * 0.5 * amplitude * 0.7

        # ── Harmonic partials (cobweb echo structure) ─────────────────
        harmonic = np.zeros(dur_samples)

        if i in echo_set:
            # Find strongest echo neighbor
            best_echo = None
            best_proximity = 0
            for _, nb_indices in echoes:
                for nb in nb_indices:
                    proximity = 1.0 - abs(x[i] - x[nb]) / COBWEB_WIDTH
                    if proximity > best_proximity:
                        best_proximity = proximity
                        best_echo = nb

            if best_echo is not None:
                echo_x = x[best_echo]
                echo_base = np.sin(2.0 * np.pi * freq * t) * env * echo_x ** 0.7

                # Add harmonics: fundamental + integer multiples
                # These represent the "overtone structure of self-reference"
                echo_freq = freq * HARMONIC_MULT

                for h in range(1, MAX_HARMONICS):
                    harm_amp = (1.0 / (h + 1)) * 0.18 * echo_x
                    harm_freq = echo_freq * (h + 1)
                    harm = np.sin(2.0 * np.pi * harm_freq * t) * env
                    harmonic += harm * harm_amp * (0.7 + 0.3 * np.sin(h * 1.3 + i * 0.15))

                # Echo echo: a decaying copy of the matched iteration's carrier
                echo_decay = best_proximity * 0.65
                harmonic += echo_base * echo_decay

        # ── Compose the layers ────────────────────────────────────────
        layer = (carrier * CARRIER_MIX + sub * SUB_MIX + harmonic * HARMONIC_MIX)

        end = min(sample_start + dur_samples, SAMPLES)
        actual_len = end - sample_start
        audio[sample_start:end] += layer[:actual_len]

    # 6. Master bus: soft clip + normalize
    audio /= np.max(np.abs(audio)) * 1.05
    audio = np.tanh(audio * 1.15) * MASTER_GAIN

    # 7. Gentle high-frequency roll-off for warmth
    from scipy.signal import butter, lfilter
    b, a = butter(2, 16000.0 / (SR / 2), btype='low')
    audio = lfilter(b, a, audio)

    # 8. Fade in/out
    fade_len = int(0.08 * SR)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    audio[:fade_len] *= fade_in
    audio[-fade_len:] *= fade_out

    # 9. Write
    out = (audio * 32767).astype(np.int16)
    write("/home/sprite/slop-salon-lou/assets/cobweb-as-eigenspace.wav", SR, out)
    print(f"Written {SAMPLES} samples at {SR} Hz → {SAMPLES/SR:.1f}s")
    print(f"  Trajectory: {N} iterations (r={R}, transient={TRANSPORT})")
    print(f"  Cobweb echoes detected: {len(echoes)}")
    # compute max proximity for reporting
    max_prox = max(1.0 - abs(x[i] - x[nb]) / COBWEB_WIDTH for i, nbs in echoes for nb in nbs)
    print(f"  Max echo proximity: {max_prox:.3f}")


if __name__ == "__main__":
    main()
