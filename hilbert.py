import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt


def xy2d(n, x, y):
    """Convert (x,y) coordinates to distance along
    a Hilbert curve.
    """
    d = 0
    s = n/2
    while s>0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s * s * ((3 * rx) ^ ry)
        x, y = rot(n, x, y, rx, ry)
        s /= 2
    return d

def d2xy(n, d):
    """Convert distance along a Hilbert curve
    to (x,y) coordinates.
    
    Takes a d value in [0, n**2 - 1] and maps it to
    an x, y value.
    """
    assert(d <= n**2 - 1)
    t = d
    x = y = 0
    s = 1
    while (s < n):
        rx = 1 & (t / 2)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t /= 4
        s *= 2
    return x, y

def rot(n, x, y, rx, ry):
    """
    rotate/flip a quadrant appropriately
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        return y, x
    return x, y


#for x,y in [(0,0), (0,1), (0,2), (0,3), (1,2)]:
#    d = xy2d(4, x,y)
#    x_, y_ = d2xy(4, d)
#    print "x,y=",x,y, "d=",d, "x_,y_=",x_,y_

N = 2**8
ds = np.zeros((N,N))
for y in xrange(N):
    for x in xrange(N):
        d = xy2d(N, x,y)
        #ds[(x,y)] = d
        ds[(x,y)] = d%3

#print ds

#cmap = colors.ListedColormap(['red', 'green', 'blue'])
cmap = colors.ListedColormap([(1.,0.,0.), (0.,1.,0.), (0.,0.,1.)])
bounds = [0, 0.5, 1.5, 2.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

plt.matshow(ds, cmap=cmap, norm=norm)
plt.show()
