
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create meshgrids
n = 16 # n=16: 16807/35937 ie (33, 33, 33) Voxels size:0.200, Sphere radius: 3.300
#n =  8  # n= 8: 2312/4913 ie (17, 17, 17) Voxels size:0.200, Sphere radius: 1.700
#n =  4 # n= 4: 363/729 ie (9, 9, 9) Voxels size:0.200, Sphere radius: 0.900
#n =  2 # n= 2: 77/125 ie (5, 5, 5) Voxels size:0.200, Sphere radius: 0.500

nV = 2*n + 1 # nb of voxels per axe
d = 0.2  # dim of voxel
hd = d / 2
dMin = -(n+0.5) * d
Rmax = d * n + hd # max sphere radius
val0s = [dMin+ d*i for i in range(nV+1)]

# for voxels origins
x0 = np.array(val0s, dtype=np.float32)
y0 = np.array(val0s, dtype=np.float32)
z0 = np.array(val0s, dtype=np.float32) 
print(f"{d=:5.3f}, {x0.shape=}: {x0=}")
X0, Y0, Z0 = np.meshgrid(x0, y0, z0, indexing='ij')
print(f"{X0.shape=}: {X0[0,0,0]=}")

# for voxels Center
xc = x0[:-1] + hd
yc = y0[:-1] + hd
zc = z0[:-1] + hd
print(f"{xc.shape=}: {xc[0]=}")
Xc, Yc, Zc = np.meshgrid(xc, yc, zc, indexing='ij')
print(f"{Xc.shape=}: {Xc[0,0,0]=}")

R = np.sqrt(Xc**2 + Yc**2 + Zc**2)
print(f"{R.shape=}")

axes = list(R.shape)

# Create Data
if 1: data = R <= Rmax # voxels of the sphere
else: data = np.ones(axes, dtype=np.bool) # all cube

xyzPos = np.logical_and( np.logical_and(Xc > 0.0, Yc < 0.0), Zc > 0.0)
data = np.logical_and(data, np.logical_not(xyzPos)) 
nx, ny, nz = data.shape
nVoxels = nx * ny * nz
nVoxelsInVol = data.sum()

title = f"{n=:2d}: {nVoxelsInVol}/{nVoxels} ie {data.shape} Voxels size:{d:.3f}, Sphere radius:{Rmax:6.3f}"
print(f"{title=}")

alpha = 0.8 # Control Transparency
# Colours of voxels
Colors = (  (1, 0, 0, alpha),  # red
            (0, 1, 0, alpha),  # green
            (0, 0, 1, alpha),  # blue
            (1, 1, 0, alpha),  # yellow
            (1, 1, 1, alpha),  # grey
         )
         
nColors = len(Colors)
Colors = np.array(Colors, dtype=np.float32)
colorsShape = list(R.shape) + [4] # 4 = len(rgba)
colors = np.zeros(colorsShape, dtype=np.float32) 
#for i in range(colorsShape[0]): colors[i] = Colors[i%nColors]# axeX

Ridx = (R/d).astype(np.uint16) % nColors
print(f"{Ridx.shape=} {Ridx.dtype}")
print(Ridx)

print(f"{Ridx.shape=} {Ridx.dtype}:{Ridx}")
colors = Colors[Ridx]  
print(f"{colors.shape=}")

# Plot figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.voxels(X0, Y0, Z0, data, facecolors=colors, linewidth=0.2, edgecolors='k')
ax.set_title(title)
ax.axis("equal")

plt.show()

