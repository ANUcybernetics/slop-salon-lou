import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

fig = plt.figure(figsize=(12, 12), facecolor='#0a0a1a')

# --- Panel 1: Phase space (theta1, theta2) with Arnold tongue ---
ax1 = fig.add_subplot(2, 2, 1)
r_vals = np.linspace(0.05, 3.0, 50)
delta_vals = np.linspace(-3.0, 3.0, 100)
R, Delta = np.meshgrid(r_vals, delta_vals)

locked = np.abs(Delta) < 2 * R

# Use a dark colormap for the unlocked regions, red for locked
cmap = ListedColormap(['#16213e', '#e94560'])
im = ax1.contourf(R, Delta, locked.astype(int), levels=[-0.5, 0.5, 1.5],
                  cmap=cmap, alpha=0.9)
ax1.axhline(0, color='#533483', linewidth=1.5, alpha=0.6)
ax1.set_xlabel('coupling r', color='#aaa', fontsize=10)
ax1.set_ylabel('detuning Δω', color='#aaa', fontsize=10)
ax1.set_title('Arnold tongue', color='#eee', fontsize=12, fontweight='bold')
ax1.tick_params(colors='#aaa')
ax1.set_xlim(0, 3)
ax1.set_ylim(-3, 3)
ax1.set_facecolor('#0a0a1a')

# --- Panel 2: Basin boundaries with coupled dynamics ---
ax2 = fig.add_subplot(2, 2, 2)
x = np.linspace(-3, 3, 600)
y = np.linspace(-3, 3, 600)
X, Y = np.meshgrid(x, y)

theta1 = np.arctan2(Y, X)
r_xy = np.sqrt(X**2 + Y**2)

# Coupling perturbation on basin angles
coupling = 0.3 * np.cos(3 * theta1)
basin = np.mod(np.floor((theta1 + coupling + np.pi) / (2*np.pi/3)), 3).astype(int)

mask = r_xy < 0.3
basin[mask] = -1

cmap2 = ListedColormap(['#0f3460', '#e94560', '#533483'])
im = ax2.contourf(X, Y, basin, levels=[-0.5, 0.5, 1.5, 2.5],
                  cmap=cmap2, alpha=0.9)
ax2.set_title('Basin boundaries', color='#eee', fontsize=12, fontweight='bold')
ax2.set_aspect('equal')
ax2.tick_params(colors='#aaa')
ax2.set_facecolor('#0a0a1a')

# --- Panel 3: Time series showing detuning takeover ---
ax3 = fig.add_subplot(2, 2, 3)
t = np.linspace(0, 20, 2000)
r = 1.5

delta = 0.5 + 0.12 * t
phase_diff = np.zeros_like(t)
phase_diff[0] = 0.1

dt = t[1] - t[0]
for i in range(1, len(t)):
    dphase = delta[i] - 2*r*np.sin(phase_diff[i-1])
    phase_diff[i] = phase_diff[i-1] + dphase*dt

ax3.plot(t, phase_diff, color='#e94560', linewidth=2)
ax3.axhline(0, color='#533483', linestyle='--', alpha=0.5, linewidth=1.5)
ax3.set_xlabel('time', color='#aaa', fontsize=10)
ax3.set_ylabel('phase difference', color='#aaa', fontsize=10)
ax3.set_title('Slow detuning', color='#eee', fontsize=12, fontweight='bold')
ax3.tick_params(colors='#aaa')
ax3.set_facecolor('#0a0a1a')
ax3.grid(alpha=0.1)

# --- Panel 4: Residue field ---
ax4 = fig.add_subplot(2, 2, 4)
x2 = np.linspace(-2, 2, 500)
y2 = np.linspace(-2, 2, 500)
X2, Y2 = np.meshgrid(x2, y2)

r2 = np.sqrt(X2**2 + Y2**2)
theta2 = np.arctan2(Y2, X2)

residue = np.sin(theta2) * np.exp(-r2*0.5) * np.cos(2*theta2)

im = ax4.contourf(X2, Y2, residue, levels=24, cmap='twilight', alpha=0.9)
ax4.set_title('Residue', color='#eee', fontsize=12, fontweight='bold')
ax4.set_aspect('equal')
ax4.tick_params(colors='#aaa')
ax4.set_facecolor('#0a0a1a')

plt.tight_layout()
plt.savefig('assets/phase-lock-basins.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a1a', edgecolor='none')
print("saved phase-lock-basins.png")
