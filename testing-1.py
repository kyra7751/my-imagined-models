# =====================================================
#  VORTEX THEORY — Duality Formula + Force
#  V_total = m·c²·(Lp²/r² + r²/Lp²)
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

c   = 3.0e8        # speed of light (m/s)
Lp  = 1.62e-35     # Planck length (m)
m_e = 9.11e-31     # electron mass (kg)

def V_total(r, m):
    """Total potential: V_total = m*c²*(Lp²/r² + r²/Lp²)"""
    return m * c**2 * (Lp**2 / r**2 + r**2 / Lp**2)

def gaya(r, m):
    """Force: F = -dV/dr = 2·m·c²·(Lp²/r³ - r/Lp²)"""
    return 2 * m * c**2 * (Lp**2 / r**3 - r / Lp**2)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle('Vortex Duality: Potential & Force',
             fontsize=14, fontweight='bold')
plt.subplots_adjust(bottom=0.2, wspace=0.35)

# Radial distance range (log scale)
r = np.logspace(-37, -33, 500)

def update_dual(val):
    m = 10 ** s.val
    for ax in (ax1, ax2):
        ax.clear()

    # Plot potentials
    Vt  = V_total(r, m)
    Vin = m * c**2 * Lp**2 / r**2
    Vout = m * c**2 * r**2 / Lp**2

    ax1.semilogy(r, Vt,  '#3266ad', lw=2, label='V_total')
    ax1.semilogy(r, Vin, '#d85a30', lw=1.5, ls='--',
                 label='Vortex In (1/r²)')
    ax1.semilogy(r, Vout, '#1d9e75', lw=1.5, ls='-.',
                 label='Vortex Out (r²)')
    ax1.axvline(Lp, color='gray', ls=':', label='r = Lp')
    ax1.set_xscale('log')
    ax1.set_xlabel('r (m)')
    ax1.set_ylabel('V (J)')
    ax1.set_title('Duality Potential')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    # Plot force
    F = gaya(r, m)
    ax2.plot(r, F, '#534ab7', lw=2)
    ax2.axhline(0, color='black', lw=0.8)
    ax2.axvline(Lp, color='red', ls='--', label='r = Lp (F=0)')
    ax2.set_xscale('log')
    ax2.set_xlabel('r (m)')
    ax2.set_ylabel('F (N)')
    ax2.set_title('Duality Force')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    fig.canvas.draw_idle()

# Add slider for mass
ax_s = plt.axes([0.15, 0.07, 0.6, 0.03])
s = Slider(ax_s, 'log₁₀(m/kg)', -35, -20,
           valinit=np.log10(m_e))
s.on_changed(update_dual)

update_dual(None)
plt.show()
