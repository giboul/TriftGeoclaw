"""
Script for generating the topography file and the extents.

Currently
---------
    `gdaltranslate` crops, coarsens and the converts the file to `bathymetry.xyz`
    `plot` helps to analyse both created files
    `make_qinit` as well as `qinit` are in progress
"""
from pathlib import Path
from shutil import rmtree
from osgeo.gdal import Open, Translate, Warp

import numpy as np
from clawpack.geoclaw.topotools import Topography

from matplotlib import pyplot as plt


scale = 1e3

sea_level = 1767/scale
# For setrun.py
cxstart = 2669850./scale
cxstop = 2670894./scale
cystart = 1170285./scale
cystop = 1171950./scale

xstart = 2669700./scale
xstop = 2671000./scale
ystart = 1170100./scale
ystop = 1172100./scale

if (
    cxstart <= xstart or
    cxstop >= xstop or
    cystart <= ystart or
    cystop >= ystop
):
    raise ValueError(
        "The cropping box (topo file) is not fully "
        "contained by the computation box (grid bounds)"
    )
# Normalize domain for computations
cxstart = cxstart - xstart
cxstop  = cxstop  - xstart 
cystart = cystart - ystart
cystop  = cystop  - ystart

# for k, v in dict(cxstart=cxstart, cxstop=cxstop, cystart=cystart, cystop=cystop).items():
#     print(f"{k} = {v}")


def gdaltranslate() -> None:

    xRes = yRes = 10
    # Temporary directory
    ifile = Path("..") / "swissALTI3D_merged.tif"
    tempdir = Path("_temp")
    tempdir.mkdir(exist_ok=True)

    ulx, uly, lrx, lry = map(lambda x: x*scale, (xstart, ystop, xstop, ystart))

    data = Open(str(ifile))
    print(f"\tINFO: Cropping {ifile} to {tempdir / 'b1.tif'}")
    data = Translate(str(tempdir / "b1.tif"), data, projWin=(ulx, uly, lrx, lry))
    print(f"\tINFO: Downsampling {tempdir / 'b1.tif'} to {xRes=} {yRes=}")
    data = Warp(str(tempdir / 'b2.tif'), data, xRes=xRes, yRes=yRes)

    print(f"\tINFO: Converting {tempdir / 'b2.tif'} to bathymetry.xyz")
    Translate(f"bathymetry.xyz", data, format="xyz")

    print(f"\tINFO: Rescaling bathymetry.xyz to computable values")
    x, y, z = np.loadtxt("bathymetry.xyz").T/scale
    print(f"\tINFO: Stripping lake level to altitude 0 (bathymetry.xyz)")
    x = x - xstart
    y = y - ystart
    z = z - sea_level
    np.savetxt(f"bathymetry.xyz", np.vstack((x, y, z)).T)

    # Adding dam
    # dam = ((x >= 2.6700500) & (x <= 2.6705) &
    #        (y >= 1.1717714) & (y <= 1.1719301))
    # z[dam] += 115  # m (hauteur du barrage)

    # print(f"\tINFO: Converting {tempdir / 'b2.tif'} to bathymetry.asc")
    # Translate(f"bathymetry.asc", data, format="AAIGrid")  # Not in the right format

    rmtree(tempdir)


def plot(asc=False, h0=False) -> None:

    print(f"\tINFO: plotting bathymetry and approximate computational domain")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if asc is True:
        nx, ny, x0, y0, cs = np.loadtxt("bathymetry.asc", max_rows=5, usecols=1)
        nx, ny = int(nx), int(ny)
        x = np.linspace(x0, x0 + nx*cs, num=nx)
        y = np.linspace(y0, y0 + ny*cs, num=ny)
        z = np.loadtxt("bathymetry.asc", skiprows=5)
        x, y = np.meshgrid(x, y)
    else:
        x, y, z = np.loadtxt("bathymetry.xyz").T

    ax.plot_trisurf(x, y, z, color='gray', alpha=0.7, label="Bathymetry")

    if h0 is True:
        xw, yw, zw = np.loadtxt("qinit.xyz").T
        above = zw >= z
        # above = 0 >= z
        if above.sum() >= 3:
            ax.plot_trisurf(x[above], y[above], np.full_like(above, 0), label="q0")

    # Plot approximate computational domain limits
    walls_kwargs = dict(facecolor='red', alpha=.2)
    Xc, Zc = np.meshgrid((cxstart, cxstop), (z.min(), z.max()))
    Yc = np.full_like(Xc, cystart)
    ax.plot_surface(Xc, Yc, Zc, **walls_kwargs, label="Computational bounds")

    Xc, Zc = np.meshgrid((cxstart, cxstop), (z.min(), z.max()))
    Yc = np.full_like(Xc, cystop)
    ax.plot_surface(Xc, Yc, Zc, **walls_kwargs)

    Yc, Zc = np.meshgrid((cystart, cystop), (z.min(), z.max()))
    Xc = np.full_like(Xc, cxstart)
    ax.plot_surface(Xc, Yc, Zc, **walls_kwargs)

    Yc, Zc = np.meshgrid((cystart, cystop), (z.min(), z.max()))
    Xc = np.full_like(Xc, cxstop)
    ax.plot_surface(Xc, Yc, Zc, **walls_kwargs)

    ax.set_aspect("equal")
    ax.legend(loc="upper left")
    if True:
        file = "Topography.png"
        print(f"\tINFO: Saving {file}...", end=" ")
        fig.savefig(file, bbox_inches='tight')
        print("Done.")
    else:
        plt.show()


def make_qinit():
    """
    Create qinit data file
    """
    x, y, z = np.loadtxt("bathymetry.xyz").T
    # print(f"{x.min(), x.max() = }")
    # print(f"{y.min(), y.max() = }")
    nxpoints = np.unique(x).size
    nypoints = np.unique(y).size
    xlower = x.min()
    xupper = x.max()
    ylower = y.min()
    yupper = y.max()
    outfile = "qinit.xyz"

    topography = Topography(topo_func=qinit)
    topography.x = np.linspace(xlower,xupper,nxpoints)
    topography.y = np.linspace(ylower,yupper,nypoints)
    topography.write(outfile, topo_type=1)


def qinit(x, y):
    """"""
    q = np.zeros_like(x+y, dtype=np.float16)
    # q[(np.abs(x-cxstart) <= 1e-3) & (np.abs(y-1.1714) <= 1e-3)] = 100
    xm = cxstart  # (xstart+xstop)/2
    ym = 1171400./scale-ystart  # (ystart+ystop)/2
    # q += sea_level
    domain = (x-xm)**2+(y-ym)**2 <= (0.05)**2
    q[domain] += 1/scale
    # print(q.min(), q.max())
    return q


if __name__ == "__main__":
    print(f"INFO: running {__file__}")
    gdaltranslate()
    make_qinit()
    plot(h0=True)
