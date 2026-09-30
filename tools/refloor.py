#!/usr/bin/env python3
"""tools/refloor.py -- proof that the far settle = the near floor's note.
Rebuilds the lock cells for both parts of the whole-scroll canvas, finds the
frames where ONLY band 52 (the floor band) is lit, FFTs exactly those frames
in walk1.wav / walk2.wav, and prints both peaks. Keys are hers (floor 62.4);
the claim tested is relational: same note both ends of the scroll."""
import numpy as np
import wave
from PIL import Image

SR = 32000


def cells_for(img, crop0, crop1):
    a = np.asarray(Image.open(img).convert("RGB"), dtype=np.float64)[:, crop0:crop1, :] / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    Y = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
    vals, counts = np.unique(Y.round(4), return_counts=True)
    ink = np.clip(float(vals[counts.argmax()]) - Y, 0, None)
    SC = 141 / 640
    NB, BH = 64, 8.49
    nfr = (crop1 - crop0) // 4
    C = np.zeros((NB, nfr))
    for b in range(NB):
        yc = 320 + (b - 26) * BH
        r0 = int(round((yc - BH / 2) * SC))
        r1 = max(int(round((yc + BH / 2) * SC)), r0 + 1)
        for t in range(nfr):
            C[b, t] = ink[r0:r1, 4 * t:4 * (t + 1)].max()
    return C


def peak(path, f0, f1):
    w = wave.open(path)
    sr = w.getframerate()
    w.setpos(int(f0 * sr))
    n = int((f1 - f0) * sr)
    x = np.frombuffer(w.readframes(n), dtype="<i2") / 32768
    X = np.abs(np.fft.rfft(x * np.hanning(n)))
    f = np.fft.rfftfreq(n, 1 / SR)
    return f[np.argmax(X)]


C1 = cells_for("assets/scroll.png", 0, 2048)
C2 = cells_for("assets/scroll_p2.png", 0, 2048)


def solo(C, b=52):
    # dominant, not pure: the look's sub-pixel pen smears a little ink into
    # neighbour rows everywhere, so a strict 0.02-dark test kills every frame
    lo = C[b - 1] > 0.15 * C[b]
    hi = C[b + 1] > 0.15 * C[b]
    return np.where((C[b] > 0.3) & ~lo & ~hi)[0]


s1, s2 = solo(C1), solo(C2)
print("p1 band-52 solo:", len(s1), "frames, t", s1.min() * 0.25, "-", s1.max() * 0.25 + 0.25, "s")
print("p2 band-52 solo:", len(s2), "frames, t", s2.min() * 0.25, "-", s2.max() * 0.25 + 0.25, "s")
def last_run(s):
    br = np.where(np.diff(s) > 1)[0]
    return s[br[-1] + 1:] if len(br) else s


r1, r2 = last_run(s1), last_run(s2)
print("p1 final solo run:", r1.min(), "-", r1.max(), "t", r1.min() * 0.25, "-", r1.max() * 0.25 + 0.25)
print("p2 final solo run:", r2.min(), "-", r2.max(), "t", r2.min() * 0.25, "-", r2.max() * 0.25 + 0.25)
p1 = peak("assets/walk1.wav", r1.min() * 0.25, r1.max() * 0.25 + 0.25)
p2 = peak("assets/walk2.wav", r2.min() * 0.25, r2.max() * 0.25 + 0.25)
print(f"p1 floor note {p1:.2f} Hz | p2 settle note {p2:.2f} Hz | "
      f"delta {1200*np.log2(p2/p1):+.1f} cents")
print("her key: floor 62.4 (her file), settle 62.3 (lelia's strip relations)")
