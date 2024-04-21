import numpy as np
import math

n = 50000000

x1 = np.random.rand(n)
y1 = np.random.rand(n)
x2 = np.random.rand(n)
y2 = np.random.rand(n)
r = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)/2
xc = (x1 + x2)/2
yc = (y1 + y2)/2
inside = (xc + r > 1) | (xc - r < 0) | (yc + r > 1) | (yc - r < 0) 
print(inside.mean())
print(1 - math.pi / 6)