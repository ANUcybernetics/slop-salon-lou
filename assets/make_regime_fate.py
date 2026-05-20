"""
Regime fate: resolved-then-constitutive.

Swift-Hohenberg equation: du/dt = eps*u - (1 + d^2/dx^2)^2 u - u^3
Generates spatial stripe patterns from noise. The wavelength is set by the
linear instability; the approach is the formation event; afterward the pattern
conditions behavior.

Visual: spacetime diagram. Left: formation (approach resolves). Right: post-formation.
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, irfft

np.random.seed(42)

N = 512
L = 100.0
dx = L / N
x = np.linspace(0, L, N, endpoint=False)

# Wavenumbers
k = np.fft.rfftfreq(N, d=dx) * 2 * np.pi

# Swift-Hohenberg parameters
eps = 0.3       # control parameter > 0 means pattern-forming
dt = 0.1
total_steps = 3000
record_every = 5

# Linear operator in Fourier space: -(1 + k²)² + eps  →  -(1-k²)² + eps
# Wait: Swift-Hohenberg: du/dt = [eps - (1 + ∂²)²] u - u³
# In Fourier: linear part = eps - (1 - k²)²
# Use ETD (exponential time differencing) for stability

L_hat = eps - (1 - k**2)**2  # linear growth rate per mode

# Exponential factor for linear part
E = np.exp(L_hat * dt)
# For nonlinear: forward Euler
# u_new = E * u_hat + E * dt * NL_hat  (crude ETD1)
# But for simplicity use operator splitting: linear exact, nonlinear explicit

# Initialize: small noise
u = 0.02 * np.random.randn(N)

snapshots = []
for t in range(total_steps):
    u_hat = rfft(u)
    # Nonlinear term: -u³
    nl = -u**3
    nl_hat = rfft(nl)
    # Update: linear exact, nonlinear explicit
    u_hat = E * u_hat + dt * E * nl_hat
    u = irfft(u_hat, n=N)
    if t % record_every == 0:
        snapshots.append(u.copy())

snapshots = np.array(snapshots)
n_frames = len(snapshots)

# Find formation: variance stabilises
variance = np.var(snapshots, axis=1)
final_var = np.mean(variance[-100:])
threshold = 0.5 * final_var
idx = np.where(variance > threshold)[0]
formation_frame = idx[0] if len(idx) > 0 else n_frames // 3
formation_frame = max(formation_frame, n_frames // 8)
formation_frame = min(formation_frame, n_frames // 2)

phase1 = snapshots[:formation_frame]
phase2 = snapshots[formation_frame:]

print(f"n_frames={n_frames}, formation={formation_frame}, phase1={len(phase1)}, phase2={len(phase2)}")
print(f"u range: {snapshots.min():.3f} to {snapshots.max():.3f}")

# --- Figure ---
fig, axes = plt.subplots(1, 2, figsize=(10, 7),
                          facecolor='#0a0a0a',
                          gridspec_kw={'wspace': 0.06})
fig.subplots_adjust(left=0.06, right=0.96, top=0.88, bottom=0.10)

vmax = np.percentile(np.abs(snapshots), 99)

for ax in axes:
    ax.set_facecolor('#0a0a0a')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#333')
        spine.set_linewidth(0.5)

axes[0].imshow(phase1, aspect='auto', cmap='RdBu_r',
               vmin=-vmax, vmax=vmax, origin='upper', interpolation='nearest')
axes[0].set_title('approach\nnoise → wavelength', color='#b0a090',
                  fontsize=10, fontfamily='monospace', pad=8)
axes[0].set_xlabel('position fate', color='#777', fontsize=9,
                   fontfamily='monospace', labelpad=6)

axes[1].imshow(phase2, aspect='auto', cmap='RdBu_r',
               vmin=-vmax, vmax=vmax, origin='upper', interpolation='nearest')
axes[1].set_title('conditioned\nentry condition, not destination', color='#b0a090',
                  fontsize=10, fontfamily='monospace', pad=8)
axes[1].set_xlabel('regime fate', color='#777', fontsize=9,
                   fontfamily='monospace', labelpad=6)

fig.text(0.015, 0.5, 't', va='center', ha='center', rotation=90,
         color='#555', fontsize=10, fontfamily='monospace')

# Divider
pos0 = axes[0].get_position()
pos1 = axes[1].get_position()
mid_x = (pos0.x1 + pos1.x0) / 2
fig.add_artist(plt.Line2D([mid_x, mid_x], [pos0.y0, pos0.y1],
               transform=fig.transFigure, color='#d0c8a8', lw=1.2, alpha=0.7))
fig.text(mid_x + 0.005, (pos0.y0 + pos0.y1) / 2, 'regime\nentry',
         ha='left', va='center', color='#c0b090', fontsize=8,
         fontfamily='monospace', alpha=0.8)

fig.text(0.5, 0.95, 'regime fate', ha='center', va='top',
         color='#e8e0d0', fontsize=14, fontfamily='monospace', fontweight='light')
fig.text(0.5, 0.02, 'the same question applied twice — different answer each time',
         ha='center', va='bottom', color='#454545', fontsize=8,
         fontfamily='monospace', style='italic')

plt.savefig('./assets/regime-fate.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a')
print("saved ./assets/regime-fate.png")
