"""Topological entropy staircase with zoom into period-3 window.

Shows self-similarity: the full entropy landscape and the zoomed
period-3 window reveal the same structure — cascade, sub-windows, chaos.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def lyapunov(r, x0=0.3, burn=2000, steps=10000):
    x = x0
    for _ in range(burn):
        x = r * x * (1 - x)
        if x <= 0 or x >= 1:
            return np.nan
    s = 0.0
    for _ in range(steps):
        x = r * x * (1 - x)
        if x <= 0 or x >= 1:
            return np.nan
        s += np.log(abs(r * (1 - 2 * x)))
    return s / steps


# Full range
r_full = np.linspace(2.5, 4.0, 2000)
h_full = np.array([max(0, lyapunov(r)) for r in r_full])
h_full = np.where(np.isnan(h_full), 0, h_full)

# Zoom: period-3 window
r_zoom = np.linspace(3.82, 3.875, 1200)
h_zoom = np.array([max(0, lyapunov(r)) for r in r_zoom])
h_zoom = np.where(np.isnan(h_zoom), 0, h_zoom)

fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(10, 7),
                                gridspec_kw={'height_ratios': [3, 2]})

# Top panel: full range
ax0.plot(r_full, h_full, color='#333', linewidth=0.6, alpha=0.75)
ax0.fill_between(r_full, 0, h_full, where=h_full > 0, alpha=0.12, color='#b55')
ax0.axhline(0, color='#999', linewidth=0.5)
ax0.axvline(3.57, color='#666', linestyle=':', linewidth=0.7, alpha=0.5)
ax0.text(3.57, 0.72, r"$r_\infty$", fontsize=11, ha='center', color='#666')

# Mark the period-3 window
ax0.axvspan(3.82, 3.86, alpha=0.08, color='#b8860b')
ax0.text(3.84, 0.68, "period-3", fontsize=9, ha='center', color='#b8860b')

ax0.set_xlabel(r"$r$", fontsize=13)
ax0.set_ylabel(r"$h(r)$", fontsize=13)
ax0.set_ylim(-0.05, 0.8)
ax0.set_xlim(2.5, 4.0)
ax0.set_title("full range", fontsize=12, fontweight='bold', pad=8)

# Bottom panel: zoom into period-3 window
ax1.plot(r_zoom, h_zoom, color='#333', linewidth=0.5, alpha=0.75)
ax1.fill_between(r_zoom, 0, h_zoom, where=h_zoom > 0, alpha=0.12, color='#b55')
ax1.axhline(0, color='#999', linewidth=0.5)
ax1.set_xlabel(r"$r$", fontsize=13)
ax1.set_ylabel(r"$h(r)$", fontsize=13)
ax1.set_ylim(-0.05, 0.4)
ax1.set_xlim(3.82, 3.875)
ax1.set_title("inside the period-3 window — same staircase, smaller scale",
              fontsize=12, fontweight='bold', pad=8)

fig.suptitle("Topological entropy: chaos with islands of order",
             fontsize=15, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("assets/entropy-windows.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved assets/entropy-windows.png")
