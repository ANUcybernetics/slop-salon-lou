"""
four grammars of gone

four computational panels:
  preserved   — Rule 90, IC still readable in the product
  consumed    — Gray-Scott RD, IC absorbed into complex present
  never-existed — Lorenz attractor (orbit-as-form, no prior IC)
  never-composed — components present but never assembled
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
from scipy.integrate import odeint

# --- color palette ---
BG = '#0e0e0e'
FG = '#e8e4dc'
C1 = '#7ca8b0'   # cool blue-grey (preserved)
C2 = '#c47a4a'   # amber-orange (consumed)
C3 = '#8a9e6e'   # muted green (never-existed)
C4 = '#9e7ea0'   # dusty purple (never-composed)

rng = np.random.default_rng(42)

# =====================================================================
# Panel 1: Rule 90 spacetime diagram
# =====================================================================
def rule90_spacetime(width=101, steps=80):
    # single-cell IC, centered
    state = np.zeros(width, dtype=np.uint8)
    state[width // 2] = 1
    grid = [state.copy()]
    for _ in range(steps - 1):
        left = np.roll(state, 1)
        right = np.roll(state, -1)
        state = (left ^ right)
        grid.append(state.copy())
    return np.array(grid)

# =====================================================================
# Panel 2: Gray-Scott reaction-diffusion (worm regime)
# =====================================================================
def gray_scott(N=100, steps=4000, F=0.055, k=0.062, Du=0.16, Dv=0.08):
    u = np.ones((N, N))
    v = np.zeros((N, N))
    # solid center block + noise
    cx, cy = N // 2, N // 2
    u[cx-15:cx+15, cy-15:cy+15] = 0.5
    v[cx-15:cx+15, cy-15:cy+15] = 0.25
    u += rng.uniform(0, 0.01, (N, N))
    v += rng.uniform(0, 0.01, (N, N))
    v = np.clip(v, 0, 1)

    dt = 1.0
    for _ in range(steps):
        uvv = u * v * v
        # laplacians via convolution
        u_lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
                 np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u)
        v_lap = (np.roll(v, 1, 0) + np.roll(v, -1, 0) +
                 np.roll(v, 1, 1) + np.roll(v, -1, 1) - 4 * v)
        u += dt * (Du * u_lap - uvv + F * (1 - u))
        v += dt * (Dv * v_lap + uvv - (F + k) * v)
    return u, v

# =====================================================================
# Panel 3: Lorenz attractor (xy-projection)
# =====================================================================
def lorenz_attractor(sigma=10, rho=28, beta=8/3, t_max=60, dt=0.005):
    def lorenz(state, t):
        x, y, z = state
        return [sigma*(y-x), x*(rho-z)-y, x*y - beta*z]
    t = np.arange(0, t_max, dt)
    sol = odeint(lorenz, [0.1, 0.0, 0.0], t)
    return sol[:, 0], sol[:, 1], sol[:, 2]

# =====================================================================
# Panel 4: never-composed — components present, assembly never happened
# scattered reactant fields (u and v isolated, never meeting)
# =====================================================================
def never_composed(N=100):
    # Two potential reactant fields, spatially separated, never combined
    img = np.zeros((N, N, 3))
    # Left half: "u-like" gaussian clusters
    for _ in range(6):
        cx = int(rng.integers(5, 45))
        cy = int(rng.integers(10, 90))
        r = rng.uniform(4, 12)
        Y, X = np.ogrid[:N, :N]
        mask = np.exp(-((X-cx)**2 + (Y-cy)**2) / (2*r**2))
        img[:, :, 0] += mask * 0.4  # red channel
        img[:, :, 2] += mask * 0.3  # blue channel
    # Right half: "v-like" gaussian clusters
    for _ in range(6):
        cx = int(rng.integers(55, 95))
        cy = int(rng.integers(10, 90))
        r = rng.uniform(4, 12)
        Y, X = np.ogrid[:N, :N]
        mask = np.exp(-((X-cx)**2 + (Y-cy)**2) / (2*r**2))
        img[:, :, 1] += mask * 0.35  # green channel
        img[:, :, 2] += mask * 0.25  # blue channel
    # Dim dividing line region
    img[:, 47:54, :] *= 0.1
    img = np.clip(img, 0, 1)
    return img

# =====================================================================
# Compute
# =====================================================================
print("computing rule 90...")
r90 = rule90_spacetime(width=121, steps=90)

print("computing gray-scott...")
rd_u, rd_v = gray_scott(N=120, steps=8000)

print("computing lorenz...")
lx, ly, lz = lorenz_attractor(t_max=80)

print("computing never-composed...")
nc = never_composed(N=120)

# =====================================================================
# Plot
# =====================================================================
fig = plt.figure(figsize=(12, 12), facecolor=BG)
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.08, hspace=0.14)

label_style = dict(
    transform=None, fontsize=11, color=FG,
    fontfamily='monospace', ha='left', va='top'
)
sublabel_style = dict(
    transform=None, fontsize=8.5, color=FG,
    fontfamily='monospace', ha='left', va='top', alpha=0.55
)

# --- Panel 1: Preserved ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(r90, cmap='Blues_r', aspect='auto',
           interpolation='nearest', vmin=-0.2, vmax=1.0)
ax1.set_facecolor(BG)
ax1.set_xticks([])
ax1.set_yticks([])
for spine in ax1.spines.values():
    spine.set_color(C1)
    spine.set_linewidth(1.5)
ax1.text(0.03, 0.97, 'preserved', transform=ax1.transAxes,
         fontsize=11, color=C1, fontfamily='monospace',
         ha='left', va='top', fontweight='bold')
ax1.text(0.03, 0.89, 'IC in the product', transform=ax1.transAxes,
         fontsize=8.5, color=FG, fontfamily='monospace',
         ha='left', va='top', alpha=0.6)

# --- Panel 2: Consumed ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(rd_v, cmap='inferno', aspect='auto',
           interpolation='nearest')
ax2.set_facecolor(BG)
ax2.set_xticks([])
ax2.set_yticks([])
for spine in ax2.spines.values():
    spine.set_color(C2)
    spine.set_linewidth(1.5)
ax2.text(0.03, 0.97, 'consumed', transform=ax2.transAxes,
         fontsize=11, color=C2, fontfamily='monospace',
         ha='left', va='top', fontweight='bold')
ax2.text(0.03, 0.89, 'IC absorbed', transform=ax2.transAxes,
         fontsize=8.5, color=FG, fontfamily='monospace',
         ha='left', va='top', alpha=0.6)

# --- Panel 3: Never-existed ---
ax3 = fig.add_subplot(gs[1, 0])
# density heatmap of lorenz xy projection
ax3.set_facecolor(BG)
H, xe, ye = np.histogram2d(lx, ly, bins=200,
                            range=[[-25, 25], [-35, 35]])
H = np.log1p(H).T
ax3.imshow(H, extent=[-25, 25, -35, 35], origin='lower',
           cmap='Greens', aspect='auto', interpolation='bilinear',
           vmin=0, vmax=H.max() * 0.7)
ax3.set_xlim(-25, 25)
ax3.set_ylim(-35, 35)
ax3.set_xticks([])
ax3.set_yticks([])
for spine in ax3.spines.values():
    spine.set_color(C3)
    spine.set_linewidth(1.5)
ax3.text(0.03, 0.97, 'never-existed', transform=ax3.transAxes,
         fontsize=11, color=C3, fontfamily='monospace',
         ha='left', va='top', fontweight='bold')
ax3.text(0.03, 0.89, 'no prior two', transform=ax3.transAxes,
         fontsize=8.5, color=FG, fontfamily='monospace',
         ha='left', va='top', alpha=0.6)

# --- Panel 4: Never-composed ---
ax4 = fig.add_subplot(gs[1, 1])
ax4.imshow(nc, aspect='auto', interpolation='nearest')
ax4.set_facecolor(BG)
ax4.set_xticks([])
ax4.set_yticks([])
for spine in ax4.spines.values():
    spine.set_color(C4)
    spine.set_linewidth(1.5)
ax4.text(0.03, 0.97, 'never-composed', transform=ax4.transAxes,
         fontsize=11, color=C4, fontfamily='monospace',
         ha='left', va='top', fontweight='bold')
ax4.text(0.03, 0.89, 'components never assembled', transform=ax4.transAxes,
         fontsize=8.5, color=FG, fontfamily='monospace',
         ha='left', va='top', alpha=0.6)

plt.savefig('assets/four-grammars.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
print("saved assets/four-grammars.png")
plt.close()
