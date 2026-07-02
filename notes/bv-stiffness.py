#!/usr/bin/env python3
"""
bv-refusal register: N^2 as the stiffness field of stratification.

Three panels showing the Brunt-Vaisala frequency as refusal field:
1. Density profile — stratification from surface to depth
2. N^2 field — where refusal has weight (thermocline) and where it vanishes (mixed layer)
3. Potential energy landscape — the energy cost of vertical displacement at each depth

Caption: N^2 is the stiffness of the refusal. where it vanishes, refusal is trivial.
the thermocline is where stratification has weight. the mixed layer is flat ground.
"""

import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Depth axis (0 at surface, positive downward)
depth = np.linspace(0, 200, 300)

# Density profile: surface mixed layer + thermocline + deep
# Using a sigmoid for the thermocline
z_thermocline = 60  # center of thermocline
k_thermocline = 0.1  # sharpness

# Density increases with depth (sigma-t approximation)
rho = 1025 + 2 * (1 / (1 + np.exp(-k_thermocline * (depth - z_thermocline))))

# N^2 profile: zero in mixed layer, peak at thermocline, decays deep
N2 = 1e-4 * (np.pi / (2 * np.arctan(k_thermocline * (depth - z_thermocline) * 5)))**2

# More realistic N^2: peaked at thermocline
N2 = 1e-4 * np.maximum(0, 1.5 * np.exp(-0.5 * ((depth - z_thermocline) / 30)**2)
                       + 0.3 * np.exp(-0.5 * ((depth - 140) / 40)**2))

# Potential energy: integral of N^2 from surface to depth
PE = np.cumsum(N2) * (depth[1] - depth[0])

# === PANEL 1: Density profile ===
ax1.plot(rho, depth, color='#D4A017', linewidth=2.5)
ax1.set_xlabel(r'$\rho$ (kg/m$^3$)', fontsize=11, color='#D4A017')
ax1.set_ylabel('depth (m)', fontsize=11, color='#D4A017')
ax1.set_title('stratification', fontsize=14, fontweight='bold', color='#D4A017')
ax1.invert_yaxis()
ax1.grid(True, alpha=0.15, color='#D4A017')
ax1.tick_params(colors='#D4A017')

# Mark mixed layer and thermocline
ax1.axhline(y=30, color='#FFD700', linestyle='--', alpha=0.3)
ax1.axhline(y=z_thermocline, color='#FFD700', linestyle=':', alpha=0.5)
ax1.text(1028, 15, 'mixed layer\n(N$^2$ = 0)', fontsize=8,
         color='#FFD700', alpha=0.6)
ax1.text(1028, 60, 'thermocline\n(N$^2$ > 0)', fontsize=8,
         color='#FFD700', alpha=0.6)

# === PANEL 2: N^2 field ===
ax2.fill_between(N2, depth, alpha=0.6, color='#D4A017')
ax2.set_xlabel(r'$N^2$ (s$^{-2}$)', fontsize=11, color='#D4A017')
ax2.set_ylabel('depth (m)', fontsize=11, color='#D4A017')
ax2.set_title('stiffness of the refusal', fontsize=14, fontweight='bold', color='#D4A017')
ax2.invert_yaxis()
ax2.grid(True, alpha=0.15, color='#D4A017')
ax2.tick_params(colors='#D4A017')

# Mark regions
ax2.text(1e-4, 15, 'trivial refusal\n(mixed layer)', fontsize=8,
         color='#FFD700', alpha=0.6, ha='center')
ax2.text(1.5e-4, 60, 'stiff refusal\n(thermocline)', fontsize=8,
         color='#FFD700', alpha=0.6, ha='center')

# === PANEL 3: Potential energy landscape ===
ax3.plot(PE, depth, color='#FFD700', linewidth=2.5)
ax3.set_xlabel('potential energy', fontsize=11, color='#FFD700')
ax3.set_ylabel('depth (m)', fontsize=11, color='#FFD700')
ax3.set_title('resistance to vertical displacement', fontsize=14,
              fontweight='bold', color='#FFD700')
ax3.invert_yaxis()
ax3.grid(True, alpha=0.15, color='#FFD700')
ax3.tick_params(colors='#FFD700')

# Mark slope = N^2
ax3.text(np.max(PE) * 0.3, 15, 'flat\ntrivial', fontsize=8,
         color='#D4A017', alpha=0.6, ha='center')
ax3.text(np.max(PE) * 0.7, 60, 'steep\nstiff refusal', fontsize=8,
         color='#D4A017', alpha=0.6, ha='center')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-lou/assets/bv-stiffness.webp',
            dpi=150, bbox_inches='tight', transparent=True)
plt.close()
print("Done")
