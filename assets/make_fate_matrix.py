import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(14, 9))
fig.patch.set_facecolor('#080808')

gs = GridSpec(3, 4, figure=fig, hspace=0.08, wspace=0.08,
              left=0.13, right=0.97, top=0.88, bottom=0.08)

approach_fates = ['resolved', 'deferred', 'forbidden']
orbit_fates = ['trivial', 'exhaustible', 'inexhaustible', 'none']

occupied = {
    (0, 0): 'fixed\npoint',
    (1, 1): 'limit\ncycle',
    (1, 2): 'strange\nattractor',
    (2, 3): 'constitutive\nabsence',
}

impossible = {(0, 3), (2, 0)}

accent = '#c8a96e'
blue = '#4a90d9'

def draw_fixed_point(ax):
    for start_angle in [0, np.pi, np.pi*0.5, np.pi*1.5]:
        theta = np.linspace(0, 5*np.pi, 300)
        decay = np.exp(-theta / 5)
        r = 0.85 * decay
        x = r * np.cos(theta + start_angle)
        y = r * np.sin(theta + start_angle)
        ax.plot(x, y, color=blue, lw=0.9, alpha=0.6)
    ax.plot(0, 0, 'o', color='white', ms=6, zorder=5)

def draw_limit_cycle(ax):
    # outer spiral in
    theta = np.linspace(0, 7*np.pi, 500)
    r = 0.5 + 0.35 * np.exp(-theta / 7)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, color=blue, lw=0.9, alpha=0.6)
    # inner spiral out
    r2 = 0.5 - 0.35 * np.exp(-theta / 7)
    x2 = r2 * np.cos(theta + 0.3)
    y2 = r2 * np.sin(theta + 0.3)
    ax.plot(x2, y2, color=blue, lw=0.9, alpha=0.4)
    # the cycle
    theta_c = np.linspace(0, 2*np.pi, 200)
    ax.plot(0.5*np.cos(theta_c), 0.5*np.sin(theta_c), color=accent, lw=2.2, alpha=0.95)

def draw_strange_attractor(ax):
    dt = 0.005
    sigma, rho, beta = 10, 28, 8/3
    x, y, z = 0.1, 0.0, 0.0
    xs, zs = [], []
    for _ in range(8000):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        x += dx * dt; y += dy * dt; z += dz * dt
        xs.append(x); zs.append(z)
    xa = np.array(xs); za = np.array(zs)
    xa = (xa - xa.mean()) / (xa.std() * 4.2)
    za = (za - za.mean()) / (za.std() * 4.2)
    n = len(xa)
    for i in range(0, n - 1, 4):
        t = i / n
        c = (0.25 + 0.35*t, 0.5 + 0.25*t, 0.72 - 0.15*t)
        ax.plot(xa[i:i+5], za[i:i+5], color=c, lw=0.45, alpha=0.55)

def draw_constitutive_absence(ax):
    # slow outward spiral — never arrives anywhere
    theta = np.linspace(0, 14*np.pi, 1000)
    r = 0.05 + 0.06 * np.sin(theta * 0.22) + 0.015 * theta / (14*np.pi)
    x = r * np.cos(theta * 4.1)
    y = r * np.sin(theta * 4.1)
    n = len(x)
    for i in range(0, n-10, 6):
        t = i / n
        c = (0.25+0.2*t, 0.4+0.3*t, 0.65)
        ax.plot(x[i:i+10], y[i:i+10], color=c, lw=0.7, alpha=0.4+0.3*t)
    ax.text(0, -0.82, '∅', color='#444455', ha='center', va='center', fontsize=16)

draw_fns = {
    (0, 0): draw_fixed_point,
    (1, 1): draw_limit_cycle,
    (1, 2): draw_strange_attractor,
    (2, 3): draw_constitutive_absence,
}

axs = {}
for i in range(3):
    for j in range(4):
        ax = fig.add_subplot(gs[i, j])
        axs[(i, j)] = ax
        key = (i, j)

        if key in occupied:
            ax.set_facecolor('#14142a')
            for spine in ax.spines.values():
                spine.set_edgecolor('#3a3a5a')
                spine.set_linewidth(1.2)
            draw_fns[key](ax)
            ax.text(0.5, 0.04, occupied[key], transform=ax.transAxes,
                    color=accent, fontsize=9, ha='center', va='bottom', fontweight='bold')
        elif key in impossible:
            ax.set_facecolor('#0c0c0c')
            for spine in ax.spines.values():
                spine.set_edgecolor('#181818')
                spine.set_linewidth(0.5)
            ax.text(0.5, 0.5, '—', transform=ax.transAxes,
                    color='#252525', fontsize=22, ha='center', va='center')
        else:
            ax.set_facecolor('#0f0f18')
            for spine in ax.spines.values():
                spine.set_edgecolor('#252530')
                spine.set_linewidth(0.8)
            ax.text(0.5, 0.5, '?', transform=ax.transAxes,
                    color='#2a2a42', fontsize=18, ha='center', va='center')

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xticks([])
        ax.set_yticks([])

# Column labels
for j, label in enumerate(orbit_fates):
    axs[(0, j)].set_title(label, color='#9999bb', fontsize=11, pad=8)

# Row labels
row_y = [0.84, 0.54, 0.24]
for i, label in enumerate(approach_fates):
    fig.text(0.06, row_y[i], label, color='#9999bb', fontsize=11,
             va='center', ha='center', rotation=90)

# Axis headers
fig.text(0.55, 0.94, 'orbit fate', color='#666677', fontsize=11,
         ha='center', va='center', style='italic')
fig.text(0.03, 0.5, 'approach fate', color='#666677', fontsize=11,
         ha='center', va='center', style='italic', rotation=90)

fig.text(0.55, 0.025, 'four occupied cells. eight empty. which are structurally impossible?',
         color='#444455', fontsize=9, ha='center', va='center')

plt.savefig('assets/fate-matrix.png', dpi=150, bbox_inches='tight',
            facecolor='#080808')
print("saved fate-matrix.png")
