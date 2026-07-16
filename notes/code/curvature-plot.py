"""Fisher curvature blow-up at pure states + tropical boundary."""
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
theta = np.linspace(0.01, 0.99, 400)
fisher = 1.0 / (theta * (1 - theta))
log_fisher = np.log(fisher)

# Panel 1: Fisher curvature strip via imshow
ax1 = axes[0]
z = np.tile(log_fisher / log_fisher.max(), (10, 1))  # (10, 400)
im = ax1.imshow(z, aspect='auto', cmap='magma', extent=[0, 1, -1, 1])
ax1.set_xlabel('θ')
ax1.set_ylabel('thickness')
ax1.set_title('Fisher blows up at pure states')
fig.colorbar(im, ax=ax1, label='norm. log I(θ)')

# Panel 2: Tropical min(θ, 1-θ)
ax2 = axes[1]
left = theta <= 0.5
right = ~left
ax2.plot(theta[left], np.minimum(theta[left], 1-theta[left]), color='blue', lw=3, label='min = θ')
ax2.plot(theta[right], np.minimum(theta[right], 1-theta[right]), color='gold', lw=3, label='min = 1−θ')
ax2.axvline(0.5, color='red', ls='--', alpha=0.5, label='switch')
ax2.set_xlabel('θ')
ax2.set_ylabel('min(θ, 1−θ)')
ax2.set_title('Tropical boundary: two patches')
ax2.legend(fontsize=8)

# Panel 3: log Fisher vs distance to boundary
ax3 = axes[2]
dist = np.minimum(theta, 1 - theta)
sc = ax3.scatter(dist, log_fisher, c=log_fisher, cmap='magma', s=15, alpha=0.8)
ax3.set_xlabel('Distance to boundary')
ax3.set_ylabel('log Fisher I(θ)')
ax3.set_title('Curvature → ∞ as d → 0')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.text(0.04, 6, 'boundary\nchooses', ha='center', fontsize=9, color='white', alpha=0.8, rotation=30)
ax3.text(0.35, 2, 'superposition\nrefuses', ha='center', fontsize=9, color='white', alpha=0.8)
fig.colorbar(sc, ax=ax3, label='log I(θ)')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/curvature-boundary.png', dpi=150, bbox_inches='tight')
print("OK")
