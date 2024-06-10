from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from clawpack.pyclaw import solution


dir = '_output'
files = glob(f'{dir}/fort.q*')
print(f"There are {len(files)} files in {dir}")

# %%

# Get first frame
frame = solution.Solution(0, path=dir, file_format='ascii')
# Get bed arrays
x = frame.state.grid.x.centers
s = frame.state.aux[0]

# Compute normal depth (Chézy)
hn = np.full_like(x, (10/50/np.sqrt(0.002))**(2/3))
hn[x < 10] = (10/50/np.sqrt(0.05))**(2/3)

# Initialize figure
fig, ax = plt.subplots(figsize=(5, 2.7), layout="tight")
ax.fill_between(x, hn+s, s, alpha=0.1, label='normal depth')
ax.fill_between(x, s, s.min(), color="k")
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$h(x, t)$')

# Initialize water line to plot and animate
line, = ax.plot(x, frame.state.q[0]+s)
# Function for water line udpating
def update(i):
    frame = solution.Solution(i, path=dir, file_format='ascii')
    h  = frame.state.q[0]
    line.set_data(x, h+s)
    line.set_label(rf"$ t = {frame.t}$ s")
    ax.legend(loc='upper right')
    fig.canvas.draw()
# Animate
anim = FuncAnimation(fig, update, frames=len(files), interval=500/len(files))
# anim.save("movie.gif", fps=len(files)/5)
plt.show()
