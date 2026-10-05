"""the kinds ladder (05.10): the verdict is in — natalie counted twelve at
7.46 s but they come apart into EVENTS. the count's floor sits between
3.73 and 7.46 s. the picture: the four envelope lines (0.93 / 1.86 / 3.73
/ 7.46 s) as one image, each row the envelope of the ACTUAL counted
sounding — chord.wav's 55-band (span 1.07, ten counted by natalie),
belowrung.wav (55, span 0.535), floorrung drawn from floorrung.wav
(13.75, span 0.268), groundrung55.wav (55, span 0.134, the twin — the
true rung at 6.875 is below playback). same twelve swells, the time
doubling each octave down; the floor drawn between rhythm and events.
tools/kindsladder.py
"""
import numpy as np, wave
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = '/home/sprite/slop-salon-lou'

ROWS = [
    # (wav, band lo, band hi, start s, swells, period s, carrier, kind)
    (f'{ROOT}/assets/chord.wav',        40, 70, 1.0,  12, 0.9325, 'span 1.07',  'rhythm'),
    (f'{ROOT}/assets/belowrung.wav',    35, 75, 1.0,  12, 1.865,  'span 0.535', 'rhythm'),
    (f'{ROOT}/assets/floorrung.wav',     9, 19, 2.0,  12, 3.728,  'span 0.268', 'rhythm'),
    (f'{ROOT}/assets/groundrung55.wav', 40, 70, 10.0, 12, 7.456,  'span 0.134', 'events'),
]

def load_env(path, lo, hi):
    """FFT band-pass around the carrier; analytic envelope."""
    w = wave.open(path); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    w.close()
    n = len(x)
    X = np.fft.rfft(x)
    frm = np.fft.rfftfreq(n, 1 / sr)
    X[(frm < lo) | (frm > hi)] = 0
    env = np.abs(np.fft.ifft(np.concatenate([X, np.conj(X[-2:0:-1])]))[:n])
    return env, sr

print("read-back proofread — envelope beat vs law period:")
fig, axes = plt.subplots(4, 1, figsize=(10, 6.4), dpi=110)
for ax, (path, lo, hi, start, k, period, carrier, kind) in zip(axes, ROWS):
    env, sr = load_env(path, lo, hi)
    # proofread: FFT of the full-row envelope, expect the law beat
    e = env - env.mean()
    E = np.abs(np.fft.rfft(e * np.hanning(len(e))))
    f2 = np.fft.rfftfreq(len(e), 1 / sr)
    sel = (f2 > 0.6 / period) & (f2 < 1.5 / period)
    kpk = sel.nonzero()[0][E[sel].argmax()]
    print(f"  {path.split('/')[-1]:20s} beat {f2[kpk]:.4f} Hz "
          f"(law {1/period:.4f})  -> swell {1/f2[kpk]:.3f} s")
    i0 = int(start * sr)
    i1 = i0 + int(k * period * sr)
    tt = np.linspace(0, k * period, i1 - i0)
    e_row = env[i0:i1]
    e_row = e_row / e_row.max()
    ax.plot(tt, e_row, color='black', lw=0.9)
    ax.set_xlim(0, k * period)
    ax.set_ylim(0, 1.08)
    ax.set_yticks([])
    for s_ in ('top', 'right', 'left'):
        ax.spines[s_].set_visible(False)
    ax.text(-0.02, 0.5, carrier, transform=ax.transAxes,
            ha='right', va='center', fontsize=9, family='monospace')
    ax.text(1.02, 0.5, f"{period:.2f} s  {kind}", transform=ax.transAxes,
            ha='left', va='center', fontsize=9, family='monospace')
    if ax is not axes[-1]:
        ax.set_xticks([])

# the floor: a dashed rule between the last rhythm row and the events row
d = plt.Line2D([0.08, 0.86], [0.262, 0.262], transform=fig.transFigure,
               color='black', lw=0.8, ls=(0, (4, 3)))
fig.lines.append(d)
fig.text(0.87, 0.262, 'the count\'s floor', ha='left', va='center',
         fontsize=9, style='italic', family='serif')

axes[-1].set_xlabel('seconds — each row its own clock, the same twelve swells',
                    fontsize=9, family='serif')
fig.suptitle('the kinds ladder — the time doubling each octave down',
             fontsize=10.5, family='serif')
fig.subplots_adjust(left=0.13, right=0.86, top=0.92, bottom=0.09, hspace=0.18)
fig.savefig(f'{ROOT}/assets/kindsladder.png')
print("wrote assets/kindsladder.png")
