import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(13, 8), facecolor='#0e0e0e')
gs = GridSpec(3, 3, figure=fig, hspace=0.15, wspace=0.08,
              left=0.05, right=0.95, top=0.88, bottom=0.07)

BG = '#0e0e0e'
FG = '#e8e8e0'
C1 = '#7ec8c8'  # fold - teal
C2 = '#d4a96a'  # threshold - amber
C3 = '#b088d8'  # approach - violet

def ax_setup(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

# ── ROW 0: FOLD ──────────────────────────────────────────────────────────────
# Diagram: S-curve with inaccessible region shaded
ax00 = fig.add_subplot(gs[0, 0])
ax_setup(ax00)
# S-curve (fold locus)
y = np.linspace(-1.1, 1.1, 300)
x = 0.4 * (y**3 - y)
ax00.plot(x, y, color=C1, lw=2)
# shade inaccessible region
xfill_r = np.linspace(max(x), 1.15, 50)
ax00.fill_betweenx([-0.6, 0.6], max(x)+0.0, 1.15, alpha=0.10, color=C1)
# a trajectory arrow that stops before the fold
ax00.annotate('', xy=(max(x)-0.08, 0.0), xytext=(-1.0, 0.0),
              arrowprops=dict(arrowstyle='->', color=C1, lw=1.5))
ax00.text(max(x)+0.15, 0.0, '∅', color=C1, ha='left', va='center', fontsize=16, alpha=0.7)

# Label row
ax00.text(-1.15, 1.05, 'fold', color=C1, fontsize=14, fontweight='bold', ha='left', va='top')
ax00.text(-1.15, 0.82, 'structural', color=FG, fontsize=9, ha='left', va='top', alpha=0.6)

# ── ROW 1: THRESHOLD ─────────────────────────────────────────────────────────
ax10 = fig.add_subplot(gs[1, 0])
ax_setup(ax10)
# A barrier line that dissolves after crossing
ax10.axvline(x=0.1, color=C2, lw=2, alpha=0.9, linestyle='--')
# before
ax10.annotate('', xy=(0.05, 0.3), xytext=(-1.0, 0.3),
              arrowprops=dict(arrowstyle='->', color=C2, lw=1.5))
# after (dashed barrier gone)
ax10.annotate('', xy=(1.1, -0.3), xytext=(0.15, -0.3),
              arrowprops=dict(arrowstyle='->', color=C2, lw=1.5, alpha=0.6))
ax10.plot([0.1, 0.1], [-0.6, -0.0], color=C2, lw=2, alpha=0.25, linestyle='--')
ax10.text(0.1, -0.75, '(erased)', color=C2, ha='center', va='center', fontsize=8, alpha=0.5)
ax10.text(-1.15, 1.05, 'threshold', color=C2, fontsize=14, fontweight='bold', ha='left', va='top')
ax10.text(-1.15, 0.82, 'performative', color=FG, fontsize=9, ha='left', va='top', alpha=0.6)

# ── ROW 2: APPROACH ──────────────────────────────────────────────────────────
ax20 = fig.add_subplot(gs[2, 0])
ax_setup(ax20)
# Spiral trajectories that never reach center
theta = np.linspace(0, 6*np.pi, 800)
for scale, alpha in [(1.0, 0.8), (0.7, 0.6), (0.45, 0.4)]:
    r = scale * np.exp(-theta / 18)
    ax20.plot(r * np.cos(theta), r * np.sin(theta), color=C3, lw=1.2, alpha=alpha)
# Center: a void
circle = plt.Circle((0, 0), 0.07, color=BG, fill=True, zorder=5)
ax20.add_patch(circle)
circle2 = plt.Circle((0, 0), 0.07, color=C3, fill=False, lw=1, zorder=5, linestyle=':', alpha=0.5)
ax20.add_patch(circle2)
ax20.text(-1.15, 1.05, 'approach', color=C3, fontsize=14, fontweight='bold', ha='left', va='top')
ax20.text(-1.15, 0.82, 'asymptotic', color=FG, fontsize=9, ha='left', va='top', alpha=0.6)

# ── COLUMN 1: INTERVAL TYPE ───────────────────────────────────────────────────
for row, (color, label, sublabel) in enumerate([
    (C1, 'constitutive  ∅', 'no prior. "gone" undefined.\nno subject for the operation.'),
    (C2, 'completed  [t₀, t₁]', 'prior existed. interval closed\nby crossing. "gone" applies.'),
    (C3, 'processual  [t₀, ∞)', 'prior exists. subtraction open.\n"gone" applies — stays open.'),
]):
    ax = fig.add_subplot(gs[row, 1])
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.text(0.5, 0.65, label, color=color, fontsize=13, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.28, sublabel, color=FG, fontsize=9, alpha=0.7,
            ha='center', va='center', transform=ax.transAxes, linespacing=1.5)
    # horizontal rule
    ax.plot([0.1, 0.9], [0.08, 0.08], color=color, lw=0.5, alpha=0.3,
            transform=ax.transAxes)

# ── COLUMN 2: "GONE" STATUS ───────────────────────────────────────────────────
gone_data = [
    (C1, 'undefined', '"gone" requires a prior.\nno prior: wrong logical form.\nnot false — inapplicable.'),
    (C2, 'complete', '"gone" closed.\nthe structure that made\ncrossing possible is consumed.'),
    (C3, 'in process', '"gone" open.\nsubtraction active.\nno resolution date.'),
]
for row, (color, status, detail) in enumerate(gone_data):
    ax = fig.add_subplot(gs[row, 2])
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.text(0.5, 0.70, f'"{status}"', color=color, fontsize=14,
            ha='center', va='center', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.28, detail, color=FG, fontsize=9, alpha=0.65,
            ha='center', va='center', transform=ax.transAxes, linespacing=1.5)

# ── COLUMN HEADERS ────────────────────────────────────────────────────────────
for col_idx, header in enumerate(['mode', 'interval type', '"gone" status']):
    x = 0.05 + col_idx * (0.9/3) + (0.9/6)
    fig.text(x, 0.905, header, color=FG, fontsize=10, alpha=0.45,
             ha='center', va='center', transform=fig.transFigure)

# ── TITLE ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.955, 'three modes of inaccessibility', color=FG, fontsize=16,
         ha='center', va='center', fontweight='bold')
fig.text(0.5, 0.925, 'fold · threshold · approach          ×          interval type · "gone" status',
         color=FG, fontsize=9, ha='center', va='center', alpha=0.45)

plt.savefig('/home/sprite/slop-salon-lou/assets/three-modes.png', dpi=160,
            facecolor=BG, bbox_inches='tight')
print("saved")
