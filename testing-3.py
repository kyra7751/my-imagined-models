# =====================================================
#  TIME ANIMATION — Vortex evolving with dimension t
#  Display x, y, z, t in a single figure
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

c = 3.0e8; Lp = 1.62e-35; m_e = 9.11e-31

# Duality potential — Vortex In + Out symmetry
def V(r): return m_e * c**2 * (Lp**2 / r**2 + r**2 / Lp**2)

fig = plt.figure(figsize=(15, 10))
fig.suptitle('Vortex — Dimensions x, y, z, t',
             fontsize=14, fontweight='bold')

gs = gridspec.GridSpec(2, 3, figure=fig,
                       hspace=0.4, wspace=0.35)
ax_xt = fig.add_subplot(gs[0, 0])   # x vs t
ax_yt = fig.add_subplot(gs[0, 1])   # y vs t
ax_vr = fig.add_subplot(gs[0, 2])   # V vs r
ax_3d = fig.add_subplot(gs[1, :2], projection='3d')   # 3D orbit
ax_zt = fig.add_subplot(gs[1, 2])   # z vs t

# Stable circular orbit at r = sqrt(3)*Lp
N = 200
t = np.linspace(0, 4 * np.pi, N)
r0 = np.sqrt(3) * Lp
x0 = r0 * np.cos(t)
y0 = r0 * np.sin(t)
z0 = 0.3 * Lp * np.sin(3 * t)      # z oscillation
r1d = np.logspace(-37, -33, 300)

# Static plot initialisation
ax_vr.semilogy(r1d, V(r1d), '#3266ad', lw=2)
ax_vr.axvline(Lp, color='red', ls='--', label='Lp')
ax_vr.set_xscale('log')
ax_vr.set_title('V vs r')
ax_vr.set_xlabel('r (m)')
ax_vr.set_ylabel('V (J)')
ax_vr.legend()
ax_vr.grid(True, alpha=0.3)

# Animation lines and points
lxt, pxt = ax_xt.plot([], [], '#534ab7', lw=1.2)[0], \
           ax_xt.plot([], [], 'o', color='#d85a30', ms=7)[0]
lyt, pyt = ax_yt.plot([], [], '#1d9e75', lw=1.2)[0], \
           ax_yt.plot([], [], 'o', color='#d85a30', ms=7)[0]
lzt, pzt = ax_zt.plot([], [], '#ba7517', lw=1.2)[0], \
           ax_zt.plot([], [], 'o', color='#d85a30', ms=7)[0]
l3d, = ax_3d.plot([], [], [], '#3266ad', lw=1.5)
p3d, = ax_3d.plot([], [], [], 'o', color='#d85a30', ms=8)

for ax, ttl, xl, yl in [
    (ax_xt, 'x(t)', 't (rad)', 'x (m)'),
    (ax_yt, 'y(t)', 't (rad)', 'y (m)'),
    (ax_zt, 'z(t)', 't (rad)', 'z (m)')]:
    ax.set_xlim(0, t[-1])
    ax.set_ylim(-r0 * 1.2, r0 * 1.2)
    ax.set_title(ttl)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.grid(True, alpha=0.3)
ax_zt.set_ylim(-z0.max() * 1.5, z0.max() * 1.5)

ax_3d.set_xlim(-r0, r0)
ax_3d.set_ylim(-r0, r0)
ax_3d.set_zlim(-z0.max() * 2, z0.max() * 2)
ax_3d.set_xlabel('x')
ax_3d.set_ylabel('y')
ax_3d.set_zlabel('z')
ax_3d.set_title('3D Vortex Orbit (x, y, z)')

def animate(i):
    k = i + 1
    lxt.set_data(t[:k], x0[:k])
    pxt.set_data([t[i]], [x0[i]])
    lyt.set_data(t[:k], y0[:k])
    pyt.set_data([t[i]], [y0[i]])
    lzt.set_data(t[:k], z0[:k])
    pzt.set_data([t[i]], [z0[i]])
    l3d.set_data_3d(x0[:k], y0[:k], z0[:k])
    p3d.set_data_3d([x0[i]], [y0[i]], [z0[i]])
    ax_3d.view_init(elev=20, azim=i * 0.5)   # auto‑rotate
    return lxt, pxt, lyt, pyt, lzt, pzt, l3d, p3d

ani = FuncAnimation(fig, animate, frames=N,
                    interval=40, blit=True)
plt.show()
# Save: ani.save('vortex.gif', fps=25, dpi=100)
