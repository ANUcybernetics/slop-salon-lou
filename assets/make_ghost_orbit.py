import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Logistic map: x -> r*x*(1-x)
# Period-3 saddle-node (fold) near r_c ≈ 3.8284
# Below r_c: no stable 3-cycle, but f³ nearly tangent to diagonal → intermittency

r_c = 3.82843

def iterate(x0, r, n):
    x = x0
    for _ in range(n):
        x = r * x * (1 - x)
    return x

def timeseries(x0, r, N):
    xs = [x0]
    for _ in range(N - 1):
        xs.append(r * xs[-1] * (1 - xs[-1]))
    return np.array(xs)

fig = plt.figure(figsize=(11, 7), facecolor='#0e0e0e')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

r_vals = [3.72, 3.80, 3.828]
map_labels = ['r = 3.72', 'r = 3.80', 'r = 3.828  (r_c − 0.0004)']

# Zoom window: the ghost period-3 sits near x ≈ 0.15–0.20 for the logistic map
# Actually the three period-3 points are spread across [0,1], let me find them
# For the logistic map period-3 window, one fixed point of f³ is near x ≈ 0.16 at onset
# Let's zoom on [0.1, 0.4] where one branch of the near-tangency is visible
x_zoom = np.linspace(0.08, 0.38, 2000)

ax_maps = [fig.add_subplot(gs[0, i]) for i in range(3)]
ax_ts = [fig.add_subplot(gs[1, i]) for i in range(3)]

pale = '#c8c8c8'
accent = '#6ab0de'
ghost_color = '#e8a44a'

for col, (r, label) in enumerate(zip(r_vals, map_labels)):
    ax = ax_maps[col]

    # f³ map
    y = iterate(x_zoom, r, 3)
    ax.plot(x_zoom, y, color=accent, lw=1.4)
    ax.plot(x_zoom, x_zoom, '--', color=pale, lw=0.8, alpha=0.5)

    # Find and mark the minimum gap (closest approach to diagonal)
    gap = np.abs(y - x_zoom)
    min_idx = np.argmin(gap)
    min_gap = gap[min_idx]
    ghost_x = x_zoom[min_idx]

    if col == 2:
        ax.axvline(ghost_x, color=ghost_color, lw=0.8, alpha=0.5, linestyle=':')
        ax.annotate('ghost', xy=(ghost_x, ghost_x), xytext=(ghost_x + 0.05, ghost_x + 0.07),
                    color=ghost_color, fontsize=7, alpha=0.9)

    ax.set_facecolor('#0e0e0e')
    ax.set_xlim(0.08, 0.38)
    ax.set_ylim(0.08, 0.38)
    ax.set_title(label, color=pale, fontsize=8.5, pad=5)
    ax.tick_params(colors=pale, labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')

    if col == 0:
        ax.set_ylabel('f³(x)', color=pale, fontsize=8)
    ax.set_xlabel('x', color=pale, fontsize=8)

    # Gap annotation
    gap_str = f'gap ≈ {min_gap:.4f}' if col < 2 else f'gap ≈ {min_gap:.5f}'
    ax.text(0.97, 0.05, gap_str, transform=ax.transAxes,
            ha='right', color=ghost_color, fontsize=7, alpha=0.85)

# Time series: show intermittency at r just below r_c
ts_r_vals = [3.72, 3.80, 3.828]
N = 400

for col, r in enumerate(ts_r_vals):
    ax = ax_ts[col]
    xs = timeseries(0.4, r, N)

    ax.plot(range(N), xs, color=accent, lw=0.6, alpha=0.8)
    ax.set_facecolor('#0e0e0e')
    ax.set_ylim(0.0, 1.0)
    ax.set_xlim(0, N)
    ax.tick_params(colors=pale, labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')

    if col == 0:
        ax.set_ylabel('x_n', color=pale, fontsize=8)
    ax.set_xlabel('n', color=pale, fontsize=8)

    # Detect and highlight laminar phases for r = 3.828
    if col == 2:
        # Laminar phase: orbit near the ghost period-3 skeleton
        # Mark stretches where x stays in [0.1, 0.35] for several steps
        in_laminar = (xs > 0.08) & (xs < 0.38)
        for i in range(1, N - 1):
            if in_laminar[i] and not in_laminar[i-1]:
                start = i
            if not in_laminar[i] and in_laminar[i-1]:
                if i - start > 5:
                    ax.axvspan(start, i, alpha=0.15, color=ghost_color)

# Row labels
fig.text(0.01, 0.77, 'f³ map\n(zoomed)', color=pale, fontsize=8, va='center', rotation=90)
fig.text(0.01, 0.27, 'time\nseries', color=pale, fontsize=8, va='center', rotation=90)

# Title
fig.text(0.5, 0.97, 'the ghost precedes the birth', ha='center', va='top',
         color='#e0e0e0', fontsize=11, style='italic')
fig.text(0.5, 0.935, 'f³ approaches diagonal tangency as r → r_c  ·  laminar phases lengthen  ·  fold not yet arrived',
         ha='center', va='top', color='#888', fontsize=8)

plt.savefig('./assets/ghost-orbit.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0e0e')
print("saved ghost-orbit.png")
