import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

# Generate random points
points = np.random.rand(10, 2)

# Perform Delaunay triangulation
tri = Delaunay(points)

# Plot the points and triangles
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'ro')
plt.show()