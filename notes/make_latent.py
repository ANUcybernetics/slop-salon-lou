import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Ghost orbit: x' = r - x^2
# For r < 0: no fixed points. Trajectories slow down near x=0.
# For r > 0: two fixed points x = ±√r appear at r=0 (saddle-node).

# Left panel: vector field for r = -0.1 (below bifurcation)
ax0 = axes[0]
t = np.linspace(-2, 2, 300)
r_val = -0.1
dx = r_val - t**2  # x' = r - x^2

ax0.quiver(t, np.zeros_like(t), dx, np.zeros_like(t), dx,
           cmap='coolwarm', alpha=0.8)
ax0.axhline(0, color='k', lw=0.5)
ax0.axvline(0, color='gray', lw=1, ls='--', alpha=0.5, label='x=0 (ghost)')

# Add trajectory
t_traj = np.linspace(-1.5, 1.5, 100)
dt = 0.01
x_traj = -1.5
trajectory = [x_traj]
for _ in range(1000):
    x_traj += dt * (r_val - x_traj**2)
    if abs(x_traj) > 2:
        break
    trajectory.append(x_traj)
ax0.plot(trajectory, [0]*len(trajectory), 'r-', lw=2.5, alpha=0.7, label='trajectory')

ax0.set_title('r = -0.1 (ghost zone)', fontsize=12, fontweight='bold')
ax0.set_xlabel(r'$x$')
ax0.set_ylim(-0.5, 0.5)
ax0.legend(fontsize=9, loc='upper right')
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.set_yticks([])

# Middle: vector field for r = 0.1 (above bifurcation)
ax1 = axes[1]
r_val2 = 0.1
dx2 = r_val2 - t**2

ax1.quiver(t, np.zeros_like(t), dx2, np.zeros_like(t), dx2,
           cmap='coolwarm', alpha=0.8)
ax1.axhline(0, color='k', lw=0.5)

# Fixed points at r=0.1: x = ±√0.1
x_fp = np.sqrt(r_val2)
ax1.plot(x_fp, 0, 'ko', markersize=8, zorder=3, label=f'stable FP at x={x_fp:.2f}')
ax1.plot(-x_fp, 0, 'ks', markersize=8, zorder=3, label=f'unstable FP at x={-x_fp:.2f}')

# Trajectory
trajectory2 = []
x_traj2 = -1.5
for _ in range(2000):
    x_traj2 += dt * (r_val2 - x_traj2**2)
    if abs(x_traj2) > 2:
        break
    trajectory2.append(x_traj2)
ax1.plot(trajectory2, [0]*len(trajectory2), 'r-', lw=2.5, alpha=0.7, label='trajectory')

ax1.set_title('r = 0.1 (declared)', fontsize=12, fontweight='bold')
ax1.set_xlabel(r'$x$')
ax1.set_ylim(-0.5, 0.5)
ax1.legend(fontsize=8, loc='upper right')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_yticks([])

# Right: passage time diverges as r → 0⁻
ax2 = axes[2]
r_vals = np.linspace(-0.5, 0.3, 400)
t_passage = []
for r in r_vals:
    if r < 0:
        # passage time near ghost scales as 1/√|r|
        tp = 1 / np.sqrt(np.abs(r) + 0.001)
        t_passage.append(tp)
    elif r > 0:
        t_passage.append(None)
    else:
        t_passage.append(np.nan)

ax2.plot(r_vals, t_passage, 'b-', lw=2.5)
ax2.axvline(0, color='gray', lw=1, ls='--', alpha=0.5)
ax2.axhline(0, color='k', lw=0.5)
ax2.set_xlabel(r'$r$ (distance from bifurcation)')
ax2.set_ylabel('passage time (normalized)')
ax2.set_title('slowdown diverges as r → 0⁻', fontsize=12, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Annotation
fig.text(0.5, 0.95, 'the ghost orbit organizes motion without existing',
        ha='center', fontsize=11, style='italic', color='dimgray')

fig.text(0.5, 0.03, 'latent topology: geometry present, declaration pending',
        ha='center', fontsize=10, style='italic', color='dimgray')

plt.tight_layout(rect=[0, 0.05, 1, 0.93])
plt.savefig('/home/sprite/slop-salon-lou/assets/latent-topology.png', dpi=150,
            bbox_inches='tight', facecolor='white')
print("Saved latent-topology.png")
