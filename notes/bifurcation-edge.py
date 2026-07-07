"""Generate a bifurcation diagram for the logistic map, then render as edge-map."""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Logistic map: x_{n+1} = r * x_n * (1 - x_n)
r_min, r_max = 2.5, 4.0
r_steps = 1000
x0 = 0.5
transient = 1000
plot_steps = 200

r = np.linspace(r_min, r_max, r_steps)
x = x0 * np.ones(r_steps)

xs = []
rs = []

for i in range(r_steps):
    for _ in range(transient):
        x[i] = r[i] * x[i] * (1 - x[i])
    for _ in range(plot_steps):
        x[i] = r[i] * x[i] * (1 - x[i])
        rs.append(r[i])
        xs.append(x[i])

rs = np.array(rs)
xs = np.array(xs)

fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
ax.scatter(rs, xs, s=0.15, color='black', alpha=0.5)
ax.set_xlim(r_min, r_max)
ax.set_ylim(0, 1)
ax.set_xlabel('r')
ax.set_ylabel('x')
ax.set_title('Logistic Map Bifurcation Diagram')
ax.axis('off')
fig.savefig('/tmp/bifurcation_full.png', bbox_inches='tight', pad_inches=0, dpi=100)
plt.close()

# Extract edges via simple Sobel
from PIL import ImageFilter
img = Image.open('/tmp/bifurcation_full.png').convert('L')
edges = img.filter(ImageFilter.FIND_EDGES)
edges.save('/tmp/bifurcation_edges.png')

# Also: time-series waveform (r=3.8, periodic/chaotic)
r_val = 3.8
x = 0.5
timeseries_x = []
for i in range(200):
    x = r_val * x * (1 - x)
    timeseries_x.append(x)

plt.figure(figsize=(10, 3), dpi=100)
plt.plot(timeseries_x, color='black', linewidth=0.5)
plt.xlim(0, 200)
plt.ylim(0, 1)
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig('/tmp/timeseries_full.png', bbox_inches='tight', pad_inches=0)
plt.close()

ts_img = Image.open('/tmp/timeseries_full.png').convert('L')
ts_edges = ts_img.filter(ImageFilter.FIND_EDGES)
ts_edges.save('/tmp/timeseries_edges.png')

print("Done: bifurcation edges, time-series edges, and full renders saved")
