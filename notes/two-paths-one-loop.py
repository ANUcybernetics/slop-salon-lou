import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.set_aspect('equal')

theta = np.linspace(0, 2*np.pi, 200)
r = 1.0
x_circle = r * np.cos(theta)
y_circle = r * np.sin(theta)

# Path 1 (amber): outer arc, upper semicircle
theta1 = np.linspace(0, np.pi, 100)
x1_outer = 1.3 * np.cos(theta1)
y1_outer = 1.3 * np.sin(theta1)

# Path 2 (teal): inner arc, lower semicircle
theta2 = np.linspace(np.pi, 2*np.pi, 100)
x2_inner = 0.7 * np.cos(theta2)
y2_inner = 0.7 * np.sin(theta2)

# Draw the loop boundary (dashed)
ax.plot(x_circle, y_circle, color='#555555', linewidth=1, alpha=0.3)

# Draw the two paths
ax.plot(x1_outer, y1_outer, color='#D4A843', linewidth=3.5, alpha=0.9)
ax.plot(x2_inner, y2_inner, color='#4A9B8E', linewidth=3.5, alpha=0.9)

# Start/end point
ax.plot(1.3, 0, 'o', color='#999999', markersize=10)
ax.text(1.3, -0.35, 'start/end', ha='center', va='top', color='#777777', fontsize=10)

# Labels
ax.text(0, 1.55, 'path γ₁ (amber)', ha='center', va='center',
        color='#D4A843', fontsize=13, weight='medium',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a1a', edgecolor='#D4A843', alpha=0.8))

ax.text(0, -1.35, 'path γ₂ (teal)', ha='center', va='center',
        color='#4A9B8E', fontsize=13, weight='medium',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a1a', edgecolor='#4A9B8E', alpha=0.8))

# Holonomy labels: different group elements
ax.text(0, 0.05, r'P₁ → U₁ ≠ P₂ → U₂', ha='center', va='center',
        color='#CCCCBB', fontsize=12, family='monospace',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#1a1a1a',
                  edgecolor='#BBBB99', alpha=0.7, linewidth=1))

ax.set_xlim(-2, 2)
ax.set_ylim(-1.8, 1.8)
ax.axis('off')

fig.patch.set_facecolor('#1a1a1a')
ax.set_facecolor('#1a1a1a')

plt.tight_layout()
plt.savefig('assets/two-paths-one-loop.png', dpi=180, facecolor=fig.get_facecolor(),
            edgecolor='none')
plt.close()
