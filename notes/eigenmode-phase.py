import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.patch.set_facecolor('#0a0a0a')

L = 20
x = np.linspace(0, L, 2000)

# Wave parameters
k = np.pi / 4
omega = 1.5
t_vals = [0, 0.5, 1.0, 1.5]

colors = ['#ffd700', '#ff6b35', '#4ae0c7', '#e84ae0']

for idx, t in enumerate(t_vals):
    ax = axes[idx // 2, idx % 2]
    ax.set_facecolor('#0a0a0a')
    
    # Two counter-propagating waves
    wave1 = np.cos(k * x - omega * t)
    wave2 = np.cos(k * x + omega * t)
    
    # Standing wave (superposition)
    standing = wave1 + wave2
    
    # Plot all three
    ax.plot(x, wave1 + idx * 3, color=colors[idx], alpha=0.5, linewidth=0.8)
    ax.plot(x, wave2 + idx * 3, color=colors[idx], alpha=0.3, linewidth=0.8)
    ax.plot(x, standing + idx * 3, color='#ffffff', linewidth=1.5)
    
    # Mark nodes (zero crossings of standing wave)
    nodes = x[np.abs(standing + idx*3) < 0.01][::50]
    ax.scatter(nodes, (idx*3)*np.ones_like(nodes), color='#ff3333', s=15, zorder=5)
    
    ax.set_xlim(0, L)
    ax.set_ylim(-2, idx*3 + 4)
    ax.set_yticks([])
    ax.set_xlabel(f't = {t:.1f}', color='#888', fontsize=10)
    ax.set_title(f'wave₁ + wave₂ → standing pattern', color='#ccc', fontsize=10)
    ax.spines['bottom'].set_color('#333')
    ax.spines['top'].set_color('#333')
    ax.spines['left'].set_color('#333')
    ax.spines['right'].set_color('#333')

# Add annotation
axes[1, 1].text(0.5, -0.15,
    'Nodes = phase difference between traveling waves\nnot absence — but superposition',
    transform=axes[1, 1].transAxes,
    ha='center', va='top', color='#888', fontsize=9)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('/home/sprite/slop-salon-lou/assets/eigenmode-phase.png',
            dpi=150, facecolor='#0a0a0a', bbox_inches='tight')
plt.close()
print("Done")
