import numpy as np, wave, math

sr = 44100
C = 220.0
sig = 1.0 + math.sqrt(2)          # silver constant
pair_l = C / sig                  # 91.127
pair_r = C * sig                  # 531.127
diff  = pair_r - pair_l           # 440.0
am    = (pair_l + pair_r) / 2     # 311.127 = C*sqrt2  (tritone up)
hm    = 2.0*C*C / (pair_l+pair_r) # 155.563 = C/sqrt2  (tritone down)

T = 45.0
n = int(sr * T)
t = np.arange(n) / sr
L = np.zeros(n); R = np.zeros(n)

def env(ts, a, r):
    # raised-cosine attack a, release r, 1 inside
    e = np.ones_like(ts)
    if a > 0:
        e &= (ts < a)
        e = np.where(ts < a, 0.5 - 0.5*np.cos(np.pi*ts/a), e)
    # handle via arithmetic
    e = np.ones_like(ts)
    mask_a = ts < a
    e = np.where(mask_a, 0.5 - 0.5*np.cos(np.pi*np.minimum(ts,a)/a), e)
    mask_r = ts > (T_local := ts[-1] if False else (ts if False else np.inf))  # placeholder
    return e

def env_window(ts, t0, t1, a=0.7, r=0.7):
    e = np.zeros_like(ts)
    m = (ts >= t0) & (ts <= t1)
    x = ts[m] - t0
    dur = t1 - t0
    e[m] = 1.0
    e[m] *= np.minimum(1.0, x / a)
    e[m] *= np.minimum(1.0, (dur - x) / r)
    # smooth the ramp ends
    e[m] = np.minimum(1.0, 0.5 - 0.5*np.cos(np.pi*np.minimum(x/a,1.0)))
    e[m] *= np.minimum(1.0, 0.5 - 0.5*np.cos(np.pi*np.minimum((dur-x)/r,1.0)))
    return e

def tone(f, t0, t1, amp, pan=0.0, phase=0.0, partials=((1,1.0),)):
    """pan -1 hard left, +1 hard right, 0 center. returns (l,r)"""
    e = env_window(t, t0, t1)
    s = np.zeros(n)
    for mult, g in partials:
        s += g * np.sin(2*np.pi*f*mult*t + phase)
    s = s / len(partials) * amp * e
    gl = math.cos((pan+1)*math.pi/4); gr = math.sin((pan+1)*math.pi/4)
    return gl*s, gr*s

# Section A (0-10): the mirror pair in stereo + soft count drone (GM)
for f, pan in ((pair_l, -1.0), (pair_r, 1.0)):
    l, r = tone(f, 0, 10, 0.28, pan=pan)
    L += l; R += r
# count drone 220 (the GM, mirror's fixed point) holds throughout 0-45
l, r = tone(220, 0, 45, 0.10, partials=((1,1.0),(2,0.35),(3,0.15),(4,0.08)))
L += l; R += r

# Section B (10-18): the pair's distance, 440 = 2*count — "half of it is the count"
l, r = tone(diff, 10, 18, 0.20)
L += l; R += r

# Section C (18-26): fold to mono — pair leaves (cross-pan to center then out),
# the count's even series holds
for f, pan in ((pair_l, -1.0), (pair_r, 1.0)):
    l, r = tone(f, 18, 26, 0.22, pan=pan)
    L += l; R += r
for f, g in ((440, 0.10), (660, 0.06), (880, 0.04)):
    l, r = tone(f, 18, 30, g)
    L += l; R += r

# Section D (26-38): the means as stereo-only tritones — AM 311.1, HM 155.6
l, r = tone(am, 26, 32, 0.30, pan=0.0, phase=math.pi/2)
L += l; R += -r  # phase-split: stereo-only
l, r = tone(hm, 32, 38, 0.30, pan=0.0, phase=math.pi/2)
L += l; R += -r

# Section E (38-45): fade everything, only the count remains
l, r = tone(220, 38, 45, 0.08)
L += l; R += r

# master: normalize, soft clip
mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L/mx*0.85; R = R/mx*0.85
L = np.tanh(1.6*L); R = np.tanh(1.6*R)
data = np.stack([L, R], axis=1)
pcm = (data * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-lou/assets/silver-means.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print("wav written", T, "s")
print("pair", round(pair_l,2), round(pair_r,2), "diff", round(diff,2), "AM", round(am,2), "HM", round(hm,2), "GM", C)
