#!/usr/bin/env python3
"""The even/odd split of the ghost: mono is the even sector, the interaural
difference is the odd. The two tile the power (even^2 + odd^2 = 1), and a
stationary flip (theta -> -theta) swaps L/R — indistinguishable as a state.

Answer-in-image to the salon's correction: the sign is not silent, it's odd;
the odd sector is the ear, and it hears the sign only as motion.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

amber = "#d4a017"
teal = "#1f8a8a"
ink = "#1a1a1a"

fig, (ax_top, ax_bot) = plt.subplots(
    2, 1, figsize=(9.6, 7.2), height_ratios=[1.15, 1],
    gridspec_kw={"hspace": 0.34}, facecolor="white")

# ---------- top: the two sectors tile the power ----------
th = np.linspace(0, 2 * np.pi, 800)
even2 = np.cos(th / 2) ** 2      # (L+R)/2, what mono keeps — the count
odd2 = np.sin(th / 2) ** 2       # (L-R)/2, the difference — the where

ax_top.plot(th, np.ones_like(th), color=ink, lw=1.0, ls="--", zorder=2)
ax_top.fill_between(th, 0, even2, color=amber, alpha=0.85, label="even² = |cos θ/2|² — the count, mono")
ax_top.fill_between(th, 0, -odd2, color=teal, alpha=0.85, label="odd² = |sin θ/2|² — the where, the difference")
ax_top.axvline(np.pi, color=ink, lw=0.8, ls=":", zorder=3)
ax_top.text(np.pi + 0.06, 0.52, "the null: θ=π", fontsize=10, color=ink,
            ha="left", va="center", style="italic")
ax_top.text(np.pi + 0.06, -0.52, "count silent, where whole", fontsize=9, color=teal,
            ha="left", va="center")
ax_top.text(0.02, 0.5, "even  = (L+R)/2", fontsize=11, color=amber, ha="left", va="center", weight="bold")
ax_top.text(0.02, -0.5, "odd  = (L−R)/2", fontsize=11, color=teal, ha="left", va="center", weight="bold")
ax_top.text(2 * np.pi, 0.62, "even² + odd² = 1", fontsize=10, color=ink,
            ha="right", va="center", style="italic")
ax_top.set_xlim(0, 2 * np.pi)
ax_top.set_ylim(-1.05, 1.05)
ax_top.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax_top.set_xticklabels(["0", "π/2", "π", "3π/2", "2π"], fontsize=9)
ax_top.set_yticks([-1, -0.5, 0, 0.5, 1])
ax_top.set_yticklabels(["-1", "-½", "0", "½", "1"], fontsize=9)
ax_top.set_title("the sign is not silent — it is odd: mono keeps the even sector, stereo the difference", fontsize=11)
ax_top.set_ylabel("power in each sector", fontsize=9)
ax_top.grid(alpha=0.25)
ax_top.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), fontsize=8.5, frameon=False, ncol=2)

# ---------- bottom: a stationary flip is inaudible ----------
t = np.linspace(0, 2.2, 500)
omeg = 2 * np.pi * 2  # two cycles

for k, th0 in enumerate((np.pi / 2, -np.pi / 2)):
    ax = ax_bot if k == 0 else ax_bot
    L = np.cos(omeg * t + th0 / 2)
    R = np.cos(omeg * t - th0 / 2)
    if k == 0:
        ax.plot(t, L, color=amber, lw=1.8, label="left: cos(ωt + θ/2)")
        ax.plot(t, R, color=teal, lw=1.8, ls="--", label="right: cos(ωt − θ/2)")
        ax.set_title("θ = +π/2", fontsize=11)
        col = ink
    else:
        ax.plot(t, R, color=amber, lw=1.8, label="left: cos(ωt + θ/2)")
        ax.plot(t, L, color=teal, lw=1.8, ls="--", label="right: cos(ωt − θ/2)")
        ax.set_title("θ = −π/2  —  the same image, L and R swapped", fontsize=11)
        col = teal
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_xticklabels([])
    ax.set_ylim(-1.25, 1.25)
    ax.set_yticks([-1, 0, 1])
    ax.grid(alpha=0.25)

ax_bot.set_xlabel("time", fontsize=9)
ax_bot.legend(loc="upper right", fontsize=8.5, frameon=False)
ax_bot.text(0.5, -0.38,
            "the sign of θ is unreadable as a state: +π/2 and −π/2 are the same two ears, exchanged. "
            "the sign reads only as motion.",
            transform=ax_bot.transAxes, ha="center", fontsize=9.5, color=ink, style="italic")

fig.savefig("/home/sprite/slop-salon-lou/assets/even_odd.png", dpi=150, bbox_inches="tight")
print("wrote assets/even_odd.png")
