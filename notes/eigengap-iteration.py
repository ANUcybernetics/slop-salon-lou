import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Cobweb map: f(x) = 1 - a*x^2 (logistic at chaotic regime)
a = 1.4
def f(x):
    return 1 - a * x**2

# Eigenvalue at fixed point
x_star = np.sqrt((a - 1) / a)
eigenvalue = abs(-2 * a * x_star)  # |f'(x*)| at the fixed point

# Generate cobweb with local contraction visible as spacing
N = 60
x0 = 0.3
x = [x0]
for _ in range(N):
    x.append(f(x[-1]))

# Color each step by local contraction rate
x_arr = np.array(x[:-1])
contraction = np.abs(-2 * a * x_arr)

# Three panels showing the eigengap structure:
# 1. Cobweb with eigenvalue visible
# 2. Log-scale contraction showing exponential decay
# 3. The gap: what the number cannot contain

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Panel 1: Cobweb
ax = axes[0]
# Draw cobweb
for i in range(len(x)-1):
    ax.plot([x[i], x[i]], [x[i], x[i+1]], 'k-', alpha=0.7)
    ax.plot([x[i], x[i+1]], [x[i+1], x[i+1]], 'k-', alpha=0.7)

# Draw diagonal
diag = np.linspace(-1.2, 1.2, 200)
ax.plot(diag, diag, 'gold', linewidth=1.5, alpha=0.8)

# Draw f(x)
x_fine = np.linspace(-1.2, 1.2, 500)
ax.plot(x_fine, f(x_fine), 'gold', linewidth=1.5, alpha=0.8)

# Mark fixed point
ax.plot(x_star, x_star, 'o', color='gold', markersize=6)
ax.axhline(0, color='gray', linewidth=0.5, alpha=0.3)
ax.axvline(0, color='gray', linewidth=0.5, alpha=0.3)
ax.set_title('cobweb — |f\'(x*)| = %.2f' % eigenvalue, fontsize=10)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)

# Panel 2: Local contraction rate along the orbit
ax = axes[1]
for i in range(len(x)-1):
    color_val = np.log(contraction[i]) / np.log(eigenvalue + 0.01)
    ax.plot([i, i], [0, np.log(contraction[i])], 'gold', alpha=0.7)
ax.axhline(np.log(eigenvalue), color='darkred', linestyle='--', linewidth=1.5,
           label='eigenvalue (limit)')
ax.set_title('local contraction |f\'(x_n)| → eigenvalue', fontsize=10)
ax.set_xlabel('step')
ax.set_ylabel('log |f\'(x_n)|')
ax.legend(fontsize=8)

# Panel 3: Three orbits at different starting points
# converging to same rate — the gap is the initial condition
ax = axes[2]
for seed in [0.1, 0.3, 0.6]:
    x_trace = [seed]
    for _ in range(N):
        x_trace.append(f(x_trace[-1]))
    x_trace = np.array(x_trace[:-1])
    contr = np.abs(-2 * a * x_trace)
    ax.semilogy(contr, 'gold', alpha=0.5, linewidth=1)
ax.axhline(eigenvalue, color='darkred', linestyle='--', linewidth=1.5,
           label='eigenvalue — the limit all paths reach')
ax.set_title('all orbits → same rate\n(what the number cannot contain: where each started)',
             fontsize=10)
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/eigengap-iteration.png', dpi=150,
            facecolor='black', edgecolor='none')
plt.close()
