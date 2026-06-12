"""
Cobweb as measurement instrument.

The diagonal is the reference standard — the unit against which distance
collapses. Each vertical segment is a measurement: |f(x) - x|, the distance
to the diagonal. Each horizontal segment reads that measurement back as
a new position. The cobweb is not iteration — it is the act of measuring
against the self.

The diagonal as ruler that measures itself.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Map: x -> r*x*(1-x) at r=2.95, where the golden tail emerges
r = 2.95

def f(x):
    return r * x * (1 - x)

def fprime(x):
    return r * (1 - 2*x)

# Generate cobweb
x0 = 0.3
steps = 80
x_vals = [x0]
for _ in range(steps):
    x_vals.append(f(x_vals[-1]))

x_arr = np.array(x_vals)

# Compute local contraction rate at each step
contraction = np.abs(fprime(x_arr[:-1]))

# Normalize for coloring
cmin, cmax = np.log(contraction.min()), np.log(contraction.max())

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Draw the diagonal with measurement markings
ax.plot([0, 1], [0, 1], color='#d4a843', linewidth=1.5, alpha=0.7, zorder=1)

# Add golden measurement tick marks on the diagonal
# These represent the "units" of measurement
n_ticks = 20
for i in range(n_ticks + 1):
    t = i / n_ticks
    tick_len = 0.02
    ax.plot([t, t], [t, t + tick_len], color='#d4a843', linewidth=0.8, alpha=0.4)

# Draw cobweb segments with contraction-rate coloring
for i in range(len(x_arr) - 1):
    x_i, x_ip1 = x_arr[i], x_arr[i+1]
    y_ip1 = f(x_i)

    # Vertical segment: measurement — distance to diagonal
    # Colored by local contraction rate
    log_contr = np.log(contraction[i])
    norm_contr = (log_contr - cmin) / (cmax - cmin + 1e-10)
    # Blue (fast contraction) -> Gold (slow, near eigenvalue)
    r_c = 0.15 + 0.85 * norm_contr
    g_c = 0.3 + 0.5 * norm_contr
    b_c = 0.9 - 0.6 * norm_contr
    color = (r_c, g_c, b_c)
    lw = 1.5 + 1.5 * (1 - norm_contr)  # thicker near eigenvalue

    ax.plot([x_i, x_i], [x_i, y_ip1], color=color, linewidth=lw, alpha=0.8, zorder=2)

    # Horizontal segment: reading the measurement back
    if i + 2 < len(x_arr):
        ax.plot([x_i, x_arr[i+2]], [y_ip1, y_ip1], color=color, linewidth=lw * 0.7, alpha=0.5, zorder=2)

# Title and axis
ax.set_title('the diagonal as reference standard', fontsize=14, fontweight='bold', color='#2a2a2a', pad=20)
ax.set_xlabel('$x_n$', fontsize=12, color='#555')
ax.set_ylabel('$x_{n+1}$', fontsize=12, color='#555')

# Grid
ax.grid(True, alpha=0.15)

# Limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.8)

# Remove spines for cleaner look
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/cobweb-measurement.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Saved to assets/cobweb-measurement.png")
