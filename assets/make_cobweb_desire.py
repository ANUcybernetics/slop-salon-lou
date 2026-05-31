import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def logistic(x, r):
    return r * x * (1 - x)

def cobweb(x0, r, n_iters):
    traj = [x0]
    for _ in range(n_iters):
        traj.append(logistic(traj[-1], r))
    return np.array(traj)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

r = 3.0
x_star = 0.5
x0s = [0.1, 0.3, 0.7, 0.9]
colors = ['#4A90D9', '#D94A4A', '#4AD94A', '#D9D94A']

for ax, x0, color in zip(axes.flat, x0s, colors):
    x = np.linspace(0, 1, 500)
    ax.plot(x, logistic(x, r), 'k-', lw=1.5, alpha=0.3)
    ax.plot(x, x, 'k--', lw=1, alpha=0.5)

    traj = cobweb(x0, r, 50)
    ax.plot(traj[:39], traj[1:40], color=color, lw=1.2, alpha=0.7)

    ax.plot(x_star, x_star, 'o', color='gold', markersize=8, zorder=5, label=f'x₀={x0}')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect(1)
    ax.legend(loc='upper right', fontsize=8)
    ax.set_title(f'x₀={x0}', color=color)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig('assets/r3-cobweb-desire.png', dpi=200, bbox_inches='tight', facecolor='black')
print('saved r3-cobweb-desire.png')
