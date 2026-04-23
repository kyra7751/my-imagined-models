# =====================================================
#  VORTEX THEORY — Interactive 2D + 3D plot
#  Formula: V_x = m * c^4 * L_p / r^2
#  Install first: pip install numpy matplotlib
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, RadioButtons

# ── Physical constants ───────────────────────────────
c   = 3.0e8      # speed of light (m/s)
Lp  = 1.62e-35   # Planck length (m)
m_e = 9.11e-31   # electron mass (kg)
G   = 6.674e-11  # gravitational constant

# ── Vortex formula ─────────────────────────────────
def V_x(r, m=m_e):
    """Core formula: V_x = m * c^4 * L_p / r^2"""
    return m * c**4 * Lp / r**2

# ── Setup figure ──────────────────────────────────
fig = plt.figure(figsize=(14, 9))
fig.suptitle('Vortex Theory — V_x = m·c⁴·Lp / r²',
             fontsize=14, fontweight='bold', y=0.97)
plt.subplots_adjust(left=0.08, right=0.95,
                    bottom=0.18, top=0.91, wspace=0.35)

gs = gridspec.GridSpec(1, 2, figure=fig)
ax2 = fig.add_subplot(gs[0, 0])           # 2D
ax3 = fig.add_subplot(gs[0, 1],
          projection='3d')                # 3D

# ── Initial data ─────────────────────────────────────
r_min, r_max = 1e-15, 1e-10
r = np.logspace(np.log10(r_min), np.log10(r_max), 500)

def plot_2d(ax, r, m, log_y=True):
    ax.clear()
    Vx = V_x(r, m)
    ax.plot(r, Vx, color='#3266ad', linewidth=2)
    ax.set_xlabel('r (m)')
    ax.set_ylabel('V_x (Vx)')
    ax.set_title('2D Plot: V_x vs r', fontsize=11)
    ax.set_xscale('log')
    if log_y:
        ax.set_yscale('log')
    ax.axvline(x=Lp, color='red', ls='--',
               alpha=0.6, label='r = L_p')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

def plot_3d(ax, r, m):
    ax.clear()
    # Create mesh r, θ → x, y, z
    r_1d  = np.logspace(np.log10(1e-15),
                         np.log10(1e-10), 60)
    theta = np.linspace(0, 2*np.pi, 60)
    R, TH = np.meshgrid(r_1d, theta)
    X = R * np.cos(TH)
    Y = R * np.sin(TH)
    Z = np.log10(V_x(R, m) + 1e-100)   # log to make it visible
    ax.plot_surface(X, Y, Z, cmap='plasma',
                    alpha=0.85, linewidth=0)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('log₁₀(V_x)')
    ax.set_title('3D Plot: Vortex Well', fontsize=11)

# ── Mass slider ──────────────────────────────────
ax_mass = plt.axes([0.12, 0.07, 0.55, 0.03])
s_mass = Slider(ax_mass, 'log₁₀(m/kg)',
                -35, -20, valinit=np.log10(m_e))

ax_radio = plt.axes([0.72, 0.02, 0.22, 0.12])
radio = RadioButtons(ax_radio,
        ('log-log', 'lin-log'), active=0)

def update(val):
    m_val = 10 ** s_mass.val
    log_y = (radio.value_selected == 'log-log')
    plot_2d(ax2, r, m_val, log_y)
    plot_3d(ax3, r, m_val)
    fig.canvas.draw_idle()

s_mass.on_changed(update)
radio.on_clicked(update)

plot_2d(ax2, r, m_e)
plot_3d(ax3, r, m_e)
plt.show()