"""Chebyshev polynomials as resonant modes of the r=4 logistic map.

The arcsine density rho(x) = 1/(pi*sqrt(x(1-x))) is the invariant measure
for r=4. The Chebyshev polynomials T_n are orthogonal with respect to this
weight. They are the actual resonant modes — not the density itself, but
the eigenmodes of the Perron-Frobenius operator.

T0 = 1        — uniform (trivial)
T1 = 2x-1     — the mean
T2 = 2(2x-1)^2 - 1  — first non-trivial: null at x=0.5, peaks at edges
T3 = 4(2x-1)^3 - 3(2x-1)  — three lobes

The density rho is NOT a mode — it's the sum of mode amplitudes
squared (the zeroth auto-mode). The modes are the Chebyshev polynomials.
"""
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.001, 0.999, 1000)
t = 2*x - 1  # map to [-1, 1]

# Chebyshev polynomials of the first kind
T = [np.ones_like(t), t, 2*t**2 - 1, 4*t**3 - 3*t]
T_names = ["T₀", "T₁", "T₂", "T₃"]

# Arcsine density
rho = 1.0 / (np.pi * np.sqrt(x * (1 - x)))

fig, axes = plt.subplots(2, 3, figsize=(12, 6))

# Top row: T0, T1, T2
for i, (ax, ti, name) in enumerate(zip(axes[0], T[:3], T_names[:3])):
    ax.plot(x, ti + i*2.5, color='#f59e0b', lw=1.5)
    ax.axhline(i*2.5, color='gray', lw=0.5, ls='--', alpha=0.3)
    ax.set_title(f'{name} — mode {i}', fontsize=11)
    ax.set_ylim(-1.5, i*2.5 + 2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Top right: rho (not a mode — it's auto-correlation)
ax = axes[0, 2]
ax.plot(x, rho / 3, color='#ef4444', lw=1.5, label='ρ(x) — not a mode')
ax.plot(x, T[0], color='#f59e0b', lw=1.5, alpha=0.5, label='T₀ (trivial mode)')
ax.set_title('ρ(x) = sum |cₙTₙ|²  (auto-mode, not eigenmode)', fontsize=10)
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Bottom row: T3 + combined
ax = axes[1, 0]
ax.plot(x, T[3], color='#f59e0b', lw=1.5)
ax.axhline(0, color='gray', lw=0.5, ls='--', alpha=0.3)
ax.set_title('T₃ — three-lobe mode', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Bottom middle: combined energy
combined = sum((ti)**2 for ti in T) / len(T)
ax = axes[1, 1]
ax.plot(x, combined / 3, color='#22c55e', lw=1.5, label='⟨T²⟩ — auto-energy')
ax.plot(x, rho / 3, color='#ef4444', lw=1.5, ls='--', alpha=0.7, label='ρ(x)')
ax.set_title('⟨T²⟩ = ρ(x) — density IS the auto-energy of modes', fontsize=10)
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Bottom right: each mode weighted by rho (inner product visualization)
ax = axes[1, 2]
colors = ['#f59e0b', '#3b82f6', '#ef4444', '#22c55e']
for i, (ti, name, c) in enumerate(zip(T, T_names, colors)):
    weighted = ti * rho
    ax.plot(x, weighted / 3 + i*1.5, color=c, lw=1.2, label=name)
ax.axhline(0, color='gray', lw=0.3, ls='--', alpha=0.3)
ax.set_title('Tₙ(x)·ρ(x) — inner product kernel', fontsize=10)
ax.set_ylim(-1, 3*1.5 + 2)
ax.legend(fontsize=7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

for ax in axes.flatten():
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/chebyshev-modes.png', dpi=150, bbox_inches='tight')
plt.close()
print("done")
