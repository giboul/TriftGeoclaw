from scipy.interpolate import interp1d
import numpy as np

xlower = 0
xupper = 3000.

slope1 = 0.05
slope2 = 0.002
slope3 = 0.
mx     = 1000 + 1
x_A    = 10
x_B    = 1000.
z_A    = 0-slope1*x_A
z_B    = z_A -(x_B-x_A)*slope2

x = np.linspace(xlower, xupper, num=mx, endpoint=True)
z = interp1d((xlower, x_A, x_B, xupper), (0, z_A, z_B, z_B))(x)

if False:
    from matplotlib import pyplot as plt
    plt.fill_between(x, z, z.min()-1)
    plt.show()

np.savetxt(fname="topography.data",
           X=np.vstack((x, z)).T,
           header=f"{mx} # number of points",
           comments="")
