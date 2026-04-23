# =====================================================
#  VORTEX METRIC: f(r) = 1 - 2GM/c²r + γLp²/r²
#  + 3D spacetime plot (t, r, f)
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

G   = 6.674e-11
c   = 3.0e8
Lp  = 1.62e-35
M_sun = 1.99e30

def f_r(r, M, gamma=1.0):
    rs = 2 * G * M / c**2
    return 1 - rs/r + gamma * Lp**2 / r**2

fig = plt.figure(figsize=(14, 9))
fig.suptitle('Vortex Metric f(r) — Black Hole',
             fontsize=14, fontweight='bold')
plt.subplots_adjust(left=0.08, right=0.95,
                    bottom=0.22, top=0.91, wspace=0.35)

ax2 = fig.add_subplot(121)
ax3 = fig.add_subplot(122, projection='3d')

def render(val):
    M = 10 ** s_M.val * M_sun
    g = s_g.val
    rs = 2 * G * M / c**2
    r = np.linspace(1.01 * rs, 20 * rs, 500)

    ax2.clear()
    fr = f_r(r, M, g)
    ax2.plot(r/rs, fr, '#3266ad', lw=2, label='f(r) Vortex')
    ax2.axhline(0, color='black', lw=0.8)
    ax2.axvline(1, color='red', ls='--', alpha=0.7, label='r = r_s')
    ax2.set_xlabel('r / r_Schwarzschild')
    ax2.set_ylabel('f(r)')
    ax2.set_title('2D: Metric Function f(r)', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # 3D: f(r,t) — add a pseudo time axis
    ax3.clear()
    r_1d = np.linspace(1.05 * rs, 15 * rs, 60)
    t_1d = np.linspace(0, 1, 40)                # normalised time
    R, T = np.meshgrid(r_1d, t_1d)
    F = f_r(R, M, g)                            # stationary, no t dependence
    ax3.plot_surface(R/rs, T, F, cmap='viridis',
                     alpha=0.85, linewidth=0)
    ax3.set_xlabel('r / r_s')
    ax3.set_ylabel('t (normalised)')
    ax3.set_zlabel('f(r)')
    ax3.set_title('3D: f(r, t)', fontsize=11)
    fig.canvas.draw_idle()

ax_M = plt.axes([0.1, 0.1, 0.55, 0.03])
ax_g = plt.axes([0.1, 0.05, 0.55, 0.03])
s_M = Slider(ax_M, 'log₁₀(M/M☉)', -5, 10, valinit=0)
s_g = Slider(ax_g, 'γ (vortex coeff)', 0, 5, valinit=1)
s_M.on_changed(render)
s_g.on_changed(render)
render(None)
plt.show()