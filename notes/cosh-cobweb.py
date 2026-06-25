import numpy as np
import matplotlib.pyplot as plt

# Clamp xs to avoid overflow
xs = np.linspace(-2.5, 2.5, 1000)

def f(x):
    return 0.9 * np.cosh(np.clip(x, -2.5, 2.5)) - 0.4

def f_continuous(x):
    return f(x) - x

fixed_pts = []
for i in range(len(xs)-1):
    if (f(xs[i]) - xs[i]) * (f(xs[i+1]) - xs[i+1]) < 0:
        fixed_pts.append((xs[i] + xs[i+1]) / 2)

x0 = 2.0
trajectory = [x0]
val = x0
for i in range(25):
    val = f(val)
    trajectory.append(val)
trajectory = np.array(trajectory)

t = np.linspace(0, 3, 200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: discrete cobweb on cosh-based curve
ax1.plot(xs, xs, 'k-', alpha=0.3, linewidth=1, label='diagonal y=x')
ax1.plot(xs, f(xs), color='#DAA520', linewidth=2.5, label='f(x) = 0.9·cosh(x) − 0.4')

for i in range(len(trajectory)-1):
    if i % 2 == 0:
        ax1.plot([trajectory[i], trajectory[i+1]], [trajectory[i+1], trajectory[i+1]], 
                color='#FFBF00', linewidth=1.2, alpha=0.7)
    else:
        ax1.plot([trajectory[i], trajectory[i]], [trajectory[i], trajectory[i+1]], 
                color='#FFBF00', linewidth=1.2, alpha=0.7)

for fp in fixed_pts:
    ax1.plot(fp, fp, 'o', color='#8B0000', markersize=8)

ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('f(x)', fontsize=12)
ax1.set_title('Discrete: cobweb iterations on cosh-based map', fontsize=13)
ax1.set_xlim(-2.8, 2.8)
ax1.set_ylim(-0.5, 4)
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.2)

# Right: continuous flow
for x_start in [2.0, 1.0, 0, -1.0, -2.0]:
    flow_x = [x_start]
    flow_t = [0]
    for i in range(len(t)-1):
        dx = f_continuous(flow_x[-1]) * (t[1] - t[0])
        flow_x.append(flow_x[-1] + dx)
        flow_t.append(flow_t[-1] + (t[1] - t[0]))
    flow_x = np.array(flow_x)
    flow_t = np.array(flow_t)
    ax2.plot(flow_x, flow_t, color='#FFBF00', linewidth=1.5, alpha=0.6)

arrow_xs = np.linspace(-2.5, 2.5, 12)
for ax_val in arrow_xs:
    dx = f_continuous(ax_val)
    if abs(dx) > 0.05:
        ax2.arrow(ax_val, 0, dx * 0.8, 0, head_width=0.08, head_length=0.15,
                 fc='#DAA520' if dx > 0 else '#8B4513', ec='#DAA520', 
                 alpha=0.7, linewidth=1.2)

ax2.axvline(x=0, color='white', alpha=0.3, linestyle='--')
ax2.set_xlabel('x', fontsize=12)
ax2.set_ylabel('t', fontsize=12)
ax2.set_title('Continuous: flow dx/dt = f(x) − x', fontsize=13)
ax2.set_xlim(-2.8, 2.8)
ax2.set_ylim(-0.1, 3)
ax2.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/cosh-cobweb-continuous.png', dpi=200, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()
print("Done")
