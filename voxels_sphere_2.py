"""
=======================================================
3D voxel / volumetric plot with cylindrical coordinates
=======================================================

Demonstrates using the *x*, *y*, *z* parameters of `.Axes3D.voxels`.
"""

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors


def midpoints(x):
    sl = ()
    for i in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return x

# prepare some coordinates, and attach rgb values to each
if 0:
    r, theta, z = np.mgrid[0:1:11j, 0:np.pi*2:25j, -0.5:0.5:11j]
    x = r*np.cos(theta)
    y = r*np.sin(theta)
else:
    x = np.linspace(-1., 1., 7)
    y = np.linspace(-1., 1., 6)
    z = np.linspace(-1., 1., 5)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    print(f"{R.shape=}")

if 0:
    rc, thetac, zc = midpoints(r), midpoints(theta), midpoints(z)
else:
    Xc, Yc, Zc = X, Y, Z

if 0:
    # define a wobbly torus about [0.7, *, 0]
    #sphere = (rc - 0.7)**2 + (zc + 0.2*np.cos(thetac*2))**2 < 0.2**2
    rc_range = np.logical_and( 0.5 <= rc , rc  <= 0.7)
    zc_range = np.logical_or ( zc  < -0.3, 0.3 <  zc )
    sphere   = np.logical_and(rc_range, zc_range)

sphere = R < 1.0

# combine the color components
if 0:
    hsv = np.zeros(sphere.shape + (3,))
    hsv[..., 0] = thetac / (np.pi*2)
    hsv[..., 1] = rc
    hsv[..., 2] = zc + 0.5
else:
    hsv = np.zeros(sphere.shape + (3,))
    hsv[..., 0] = 0.5 * (X + 1.0)
    hsv[..., 1] = 0.5 * (Y + 1.0)
    hsv[..., 2] = 0.5 * (Z + 1.0)
colors = matplotlib.colors.hsv_to_rgb(hsv)

# and plot everything
ax = plt.figure().add_subplot(projection='3d')
if 0:
    ax.voxels(x, y, z, sphere,
              facecolors=colors,
              edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
              linewidth=0.5)
else:
    print(f"{X.shape=}, {Y.shape=}, {Z.shape=}, {sphere.shape=}, {colors.shape=}")
    ax.voxels(X, Y, Z, R < 1.0) #,
              #facecolors=colors,
              #edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
              #linewidth=0.5)

plt.show()

