"""VOICE BEHIND THE METRONOME — the second movement.

The metronome is e's count: exact, never fading, centred (mono — the count).
The voice is the where: wide stereo, breathing at the same 75 bpm — the thing
that keeps time with the count. Present from the first pulse of the fade.

The cut: at 25.3s the metronome's recording ends, the count does not. The
voice carries on alone, still breathing the count's tempo, then fades — the
recording ends; the count continues as breath.
"""

import numpy as np
import wave

SR = 44100
CUT = 25.3          # where the metronome recording is cut
TAIL = 6.0          # the voice alone after the cut
FADE_OUT = 3.0      # voice fades over the last seconds

def load_stereo(path, sr):
    w = wave.open(path)
    n = w.getnframes(); osr = w.getframerate()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    L = d[::2]; R = d[1::2]
    if osr != sr:
        idx = np.round(np.arange(len(L) * sr / osr) / (sr / osr)).astype(int)
        idx = np.clip(idx, 0, len(L) - 1)
        L = L[idx]; R = R[idx]
    return L, R

met_L, met_R = load_stereo('assets/metronome.wav', SR)
voc_L, voc_R = load_stereo('assets/metronome-voice-32.wav', SR)

total = CUT + TAIL
N = int(total * SR)
out_L = np.zeros(N); out_R = np.zeros(N)

# metronome: centred, full length of its recording
n_met = len(met_L)
out_L[:n_met] += met_L
out_R[:n_met] += met_R

# voice: wide (stereo as generated), present throughout, then alone
G_BED = 0.55            # under the metronome
G_ALONE = 0.78          # after the cut, forward
n_voc = len(voc_L)
t = np.arange(N) / SR

gain = np.ones(N) * G_BED
# fade in
f_in = int(1.5 * SR)
gain[:f_in] *= np.linspace(0, 1, f_in)
# after the cut the voice steps forward
after = t >= CUT
gain[after] = G_ALONE
# crossfade the step over 0.4s so it does not click
step = int(0.4 * SR)
i0 = int(CUT * SR)
gain[i0:i0 + step] = G_BED + (G_ALONE - G_BED) * np.linspace(0, 1, step)
# final fade-out
f_out = int(FADE_OUT * SR)
gain[-f_out:] *= np.linspace(1, 0, f_out)

n_v = min(n_voc, N)
out_L[:n_v] += voc_L[:n_v] * gain[:n_v]
out_R[:n_v] += voc_R[:n_v] * gain[:n_v]

# the metronome's own ground drone is inside metronome.wav; the voice rides above.

# normalise peak
pk = max(np.max(np.abs(out_L)), np.max(np.abs(out_R)))
out_L /= pk; out_R /= pk
out = np.empty(N * 2, dtype=np.float32)
out[::2] = out_L; out[1::2] = out_R
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)

with wave.open('assets/metronome-voice-piece.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('written', total, 's; peak', round(pk, 3))
