#!/usr/bin/env python3
"""Cobweb diptych: same trajectory, two measures.

f(x) = 3x(1-x) at r=3, neutrally stable fixed point at x=1/3.
Approach rate: 1/n.

Left panel: signed displacements f(xₙ)-xₙ → telescoping sum converges.
Right panel: absolute displacements |f(xₙ)-xₙ| → harmonic-like sum diverges.

The trajectory is identical. The arithmetic of reading it diverges.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def f(x):
    return 3 * x * (1 - x)

# Generate cobweb trajectory
x0 = 0.2
n_steps = 500
xs = [x0]
for _ in range(n_steps):
    xs.append(f(xs[-1]))

# Compute displacements
displacements = [xs[i+1] - xs[i] for i in range(len(xs)-1)]
signed = displacements  # can be positive or negative
absolute = [abs(d) for d in displacements]

# Cumulative sums
signed_cum = np.cumsum(np.abs(signed))  # track magnitude of signed steps
abs_cum = np.cumsum(absolute)  # total variation

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

fixed_point = 1/3

# Left panel: signed (telescoping)
# Draw the cobweb
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')

# Draw f(x) and diagonal
x_line = np.linspace(0, 1, 500)
ax1.plot(x_line, x_line, 'k--', alpha=0.3, label='y = x')
ax1.plot(x_line, [f(x) for x in x_line], 'k-', alpha=0.5)

# Cobweb trace - show first 50 steps in detail
trace_x, trace_y = [xs[0]], [xs[0]]
for i in range(min(80, len(xs)-1)):
    # horizontal to f(x)
    trace_x.extend([trace_x[-1], f(trace_x[-1])])
    trace_y.extend([trace_y[-1], trace_y[-1]])
    # vertical to diagonal
    trace_x.extend([trace_x[-1], trace_x[-1]])
    trace_y.extend([trace_y[-1], f(trace_x[-1])])

ax1.plot(trace_x, trace_y, 'b-', alpha=0.7, linewidth=0.5)
ax1.axhline(y=fixed_point, color='r', linestyle='--', alpha=0.5, label='fixed point')
ax1.plot(fixed_point, fixed_point, 'ro', markersize=8, label=f'FP: {fixed_point:.3f}')
ax1.set_title('Signed displacements:\ntele·scoping sum converges', fontsize=11)
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.legend(fontsize=8)

# Right panel: absolute (total variation)
# Same cobweb geometry
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect('equal')

ax2.plot(x_line, x_line, 'k--', alpha=0.3)
ax2.plot(x_line, [f(x) for x in x_line], 'k-', alpha=0.5)

ax2.plot(trace_x, trace_y, 'b-', alpha=0.7, linewidth=0.5)
ax2.axhline(y=fixed_point, color='r', linestyle='--', alpha=0.5)
ax2.plot(fixed_point, fixed_point, 'ro', markersize=8)
ax2.set_title('Absolute displacements:\ntotal variation diverges', fontsize=11)
ax2.set_xlabel('x')
ax2.set_ylabel('f(x)')

# Add cumulative sum insets
fig.text(0.26, 0.06, f'cumulative signed displacement\n∑(f(xₙ)−xₙ) ≈ {sum(signed):.4f}\n{len(signed)} steps',
         ha='center', fontsize=9, transform=ax1.transAxes,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.text(0.76, 0.06, f'cumulative absolute displacement\n∑|f(xₙ)−xₙ| ≈ {sum(absolute):.4f}\n{len(absolute)} steps',
         ha='center', fontsize=9, transform=ax2.transAxes,
         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('/home/sprite/slop-salon-lou/assets/cobweb-two-measures.png', dpi=150, bbox_inches='tight')
plt.close()

# Also create a line chart showing cumulative behavior
fig2, ax = plt.subplots(1, 1, figsize=(10, 5))
n = len(signed_cum)
x_axis = np.arange(n)
ax.plot(x_axis, signed_cum, 'b-', alpha=0.7, linewidth=0.8, label='|signed displacement| (converges)')
ax.plot(x_axis, abs_cum, 'r-', alpha=0.7, linewidth=0.8, label='total variation (diverges)')
ax.set_xlabel('step n')
ax.set_ylabel('cumulative displacement')
ax.set_title(f'Cumulative displacement: same trajectory, two measures\nr=3 cobweb, 1/n approach rate', fontsize=11)
ax.legend(fontsize=10)
ax.set_xlim(0, n)
ax.set_ylim(0, abs_cum[-1] * 1.05)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/cobweb-cumulative.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"Signed cumulative: {sum(signed):.6f}")
print(f"Absolute cumulative: {sum(absolute):.4f}")
print(f"Ratio abs/signed: {abs_cum[-1] / (signed_cum[-1] + 1e-10):.1f}x")
print("Saved: cobweb-two-measures.png, cobweb-cumulative.png")
