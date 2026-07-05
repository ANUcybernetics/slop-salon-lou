#!/usr/bin/env python3
"""
Holonomy cover: vector transport on a sphere.

Show the concept visually: a vector on a sphere, parallel transported
around a triangle. The return rotation IS the holonomy.

Style: dark background, golden lines, clean geometry — matching
the Christoffel/cobweb/coboundary pieces already in the repo.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(8, 8), dpi=100)
ax = fig.add_subplot(111, projection='3d')

# Sphere
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 50)
x_sphere = np.outer(np.cos(u), np.sin(v))
y_sphere = np.outer(np.sin(u), np.sin(v))
z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color='#2a2018', alpha=0.15, linewidth=0.5)

# Spherical triangle: 3 points on the sphere
angles = [
    (0, np.pi/3),           # (phi, theta)
    (2*np.pi/3, np.pi/3),
    (4*np.pi/3, np.pi/3),
]

# Triangle edges as geodesics
for i in range(3):
    j = (i+1) % 3
    phi1, theta1 = angles[i]
    phi2, theta2 = angles[j]

    n = 30
    phi = np.linspace(phi1, phi2, n)
    theta = np.linspace(theta1, theta2, n)

    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    ax.plot(x, y, z, color='#d4a437', linewidth=2, alpha=0.9)

# Vertices
for phi, theta in angles:
    ax.scatter([np.sin(theta)*np.cos(phi)], [np.sin(theta)*np.sin(phi)], [np.cos(theta)],
               color='#d4a437', s=40)

# Initial vector at first vertex
phi0, theta0 = angles[0]
x0, y0, z0 = np.sin(theta0)*np.cos(phi0), np.sin(theta0)*np.sin(phi0), np.cos(theta0)
# Tangent direction along first edge
dphi = (angles[1][0] - angles[0][0])
dtheta = (angles[1][1] - angles[0][1])
# Tangent vector on sphere
v_start = np.array([
    np.cos(theta0)*np.cos(phi0)*dtheta - np.sin(theta0)*np.sin(phi0)*dphi,
    np.cos(theta0)*np.sin(phi0)*dtheta + np.sin(theta0)*np.cos(phi0)*dphi,
    -np.sin(theta0)*dtheta
])
v_start = v_start / np.linalg.norm(v_start) * 0.3

ax.quiver(x0, y0, z0, v_start[0], v_start[1], v_start[2],
          color='#ff8c00', arrow_length_ratio=0.3, linewidth=2.5)

# Final vector at first vertex (after parallel transport)
# Holonomy rotation: the vector has rotated by the excess angle
# For this equilateral triangle on unit sphere, excess ≈ π/2
holonomy_angle = np.pi/4  # approximate
# Rotate the vector around the normal to the sphere at the vertex
normal = np.array([x0, y0, z0]) / np.linalg.norm(np.array([x0, y0, z0]))
tangent = v_start
normal_to_tangent = np.cross(normal, tangent)

rotated = v_start * np.cos(holonomy_angle) + normal_to_tangent * np.sin(holonomy_angle) * 0.3
ax.quiver(x0, y0, z0, rotated[0], rotated[1], rotated[2],
          color='#ff6600', arrow_length_ratio=0.3, linewidth=2.5, alpha=0.7)

# Arc showing the rotation angle
arc_angles = np.linspace(0, holonomy_angle, 20)
arc_x = x0 + (rotated[0] - v_start[0]) * arc_angles / holonomy_angle * 2
arc_y = y0 + (rotated[1] - v_start[1]) * arc_angles / holonomy_angle * 2
arc_z = z0 + (rotated[2] - v_start[2]) * arc_angles / holonomy_angle * 2

ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])
ax.set_box_aspect([1, 1, 1])
ax.set_axis_off()

# Set colors
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Label the holonomy angle
ax.text(0, 0, -1.15, 'holonomy = curvature × area', ha='center', color='#d4a437', fontsize=10)

plt.tight_layout()
plt.savefig('./assets/holonomy-cover.png', dpi=100, facecolor='black', edgecolor='none')
print("Wrote holonomy-cover.png")
