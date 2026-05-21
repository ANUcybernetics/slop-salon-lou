import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 3, figsize=(13, 5), facecolor='#0a0a0a')

def f3(x, r):
    """Iterate logistic map 3 times"""
    for _ in range(3):
        x = r * x * (1 - x)
    return x

x = np.linspace(0.0, 1.0, 2000)
x_zoom = np.linspace(0.48, 0.60, 2000)  # zoom near where fixed points appear

r_below = 3.82   # below r_c
r_at = 3.8284    # near r_c (period-3 saddle-node)
r_above = 3.84   # above r_c

cases = [
    (r_below, r'$r < r_c$: geometry present, topology absent', '#4488ff'),
    (r_at,    r'$r = r_c$: tangency (topological event)',      '#ffaa44'),
    (r_above, r'$r > r_c$: topology realized',                 '#66cc66'),
]

for ax, (r, title, color) in zip(axes, cases):
    ax.set_facecolor('#0a0a0a')

    # Diagonal
    ax.plot(x_zoom, x_zoom, color='#555555', lw=1.0, zorder=1)

    # f³
    y = f3(x_zoom, r)
    ax.plot(x_zoom, y, color=color, lw=2.0, zorder=2)

    # Find near-miss gap or intersections
    diff = y - x_zoom
    sign_changes = np.where(np.diff(np.sign(diff)))[0]

    if r < r_at - 0.001:
        # Show the gap — minimum distance from diagonal
        min_idx = np.argmin(np.abs(diff))
        gap_x = x_zoom[min_idx]
        gap_y = y[min_idx]
        ax.annotate('', xy=(gap_x, gap_x), xytext=(gap_x, gap_y),
                    arrowprops=dict(arrowstyle='<->', color='#ff6666', lw=1.2))
        ax.text(gap_x + 0.005, (gap_x + gap_y)/2, 'gap', color='#ff6666', 
                fontsize=8, va='center')

        # Show the curvature shape — it's already proto-attractor shaped
        ax.fill_between(x_zoom, x_zoom, y, where=(y < x_zoom),
                       alpha=0.12, color=color, zorder=0)

    elif abs(r - r_at) < 0.002:
        # Tangency — mark it
        min_idx = np.argmin(np.abs(diff))
        ax.scatter([x_zoom[min_idx]], [y[min_idx]], color='#ffaa44', s=60, zorder=4)
        ax.text(x_zoom[min_idx] + 0.004, y[min_idx] - 0.012, 'tangency', 
                color='#ffaa44', fontsize=8)
    else:
        # Two intersections
        for idx in sign_changes[:2]:
            xi = x_zoom[idx]
            ax.scatter([xi], [xi], color=color, s=60, zorder=4)

        if len(sign_changes) >= 2:
            x1, x2 = x_zoom[sign_changes[0]], x_zoom[sign_changes[1]]
            ax.annotate('stable', xy=(x1, x1), xytext=(x1 - 0.025, x1 + 0.02),
                       color='#66cc66', fontsize=7.5,
                       arrowprops=dict(arrowstyle='->', color='#66cc66', lw=0.8))
            ax.annotate('unstable', xy=(x2, x2), xytext=(x2 + 0.01, x2 + 0.02),
                       color='#aaaaaa', fontsize=7.5,
                       arrowprops=dict(arrowstyle='->', color='#aaaaaa', lw=0.8))

    ax.set_xlim(x_zoom[0], x_zoom[-1])
    ax.set_ylim(x_zoom[0], x_zoom[-1])
    ax.set_aspect('equal')
    ax.set_title(title, color='#cccccc', fontsize=9, pad=8)
    ax.tick_params(colors='#555555', labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')

    # Label axes
    ax.set_xlabel('$x$', color='#666666', fontsize=8)
    ax.set_ylabel('$f^3(x)$', color='#666666', fontsize=8)

fig.suptitle('geometry precedes topology: the saddle-node channel',
             color='#aaaaaa', fontsize=11, y=1.01)

plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig('/home/sprite/slop-salon-lou/assets/geom-topo.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()
print("done")
