from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from clawpack.pyclaw import solution


dir = '_output'
files = glob(f'{dir}/fort.q*')
print(f"There are {len(files)} files in {dir}")

# %%
# Plot solution h(x, t)

frame = solution.Solution(len(files)-1, path=dir, file_format='ascii')

x  = frame.state.grid.x.centers
h  = frame.state.q[0]
s  = frame.state.aux[0]
g  = 9.81

h0 = 1
c0 = np.sqrt(g*h0)

# normal depth
hn = np.full_like(x, (10/50/np.sqrt(0.002))**(2/3))
hn[x < 10] = (10/50/np.sqrt(0.05))**(2/3)

print(f'depth at x = 1000 m: h = {h[-1]:.2f} m')

#true = qtrue(x,t)
fig, ax = plt.subplots(figsize=(5, 2.7), layout="tight")
line, = ax.plot(x, h+s, label=rf"$ t = {frame.t}$ s")
ax.fill_between(x, hn+s, s, alpha=0.1, label='normal depth')
ax.fill_between(x, s, s.min(), color="k")
ax.legend(loc='upper right')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$h(x, t)$')

# plt.show()

def update(i):
    frame = solution.Solution(i, path=dir, file_format='ascii')
    h  = frame.state.q[0]
    line.set_data(x, h+s)
    fig.canvas.draw()

anim = FuncAnimation(fig, update, frames=len(files), interval=500/len(files))
plt.show()
