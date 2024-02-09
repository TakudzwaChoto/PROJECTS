import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
cmap = mpl.colormaps['viridis']
#x = np.linspace(0, 2 * np.pi, 200)
#y = np.sin(x)

#fig, ax = plt.subplots()
#ax.plot(x, y)
#plt.show()
###########################
#fig, ax = plt.subplots(figsize=(6, 1))
#fig.subplots_adjust(bottom=0.5)

#cmap = (mpl.colors.ListedColormap(['royalblue', 'cyan', 'yellow', 'orange'])
#        .with_extremes(over='red', under='blue'))

#bounds = [-1.0, -0.5, 0.0, 0.5, 1.0]
#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#fig.colorbar(
#    mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
#    cax=ax,
#    extend='both',
#    extendfrac='auto',
#    ticks=bounds,
#    spacing='uniform',
#    orientation='horizontal',
#    label='Custom extension lengths, some other units',
#)

#plt.show()
##########################
#fig, ax = plt.subplots(figsize=(6, 1))
#fig.subplots_adjust(bottom=0.5)

#cmap = (mpl.colors.ListedColormap(['royalblue', 'cyan', 'yellow', 'orange'])
#        .with_extremes(over='red', under='blue'))

#bounds = [-1.0, -0.5, 0.0, 0.5, 1.0]
#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#fig.colorbar(
#    mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
#    cax=ax,
#    extend='both',
#    extendfrac='auto',
#    ticks=bounds,
#    spacing='uniform',
#    orientation='horizontal',
#    label='Custom extension lengths, some other units',
#)

#plt.show()
#############################################

#fig, ax = plt.subplots(figsize=(6, 1))
#fig.subplots_adjust(bottom=0.5)

#cmap = (mpl.colors.ListedColormap(['red', 'green', 'blue', 'cyan'])
#        .with_extremes(over='0.25', under='0.75'))

#bounds = [1, 2, 4, 7, 8]
#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#fig.colorbar(
#    mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
#    cax=ax,
#    extend='both',
#    ticks=bounds,
#   spacing='proportional',
#    orientation='horizontal',
#    label='Discrete intervals, some other units',
#)
#plt.show()
######################################################
#import matplotlib.pyplot as plt
#import numpy as np

# Fixing random state for reproducibility
#np.random.seed(19680801)

#plt.subplot(211)
#plt.imshow(np.random.random((100, 100)))
#plt.subplot(212)
#plt.imshow(np.random.random((100, 100)))

#plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
#cax = plt.axes((0.85, 0.1, 0.075, 0.8))
#plt.colorbar(cax=cax)

#plt.show()
#############################################
#species = ('Adelie', 'Chinstrap', 'Gentoo')
#sex_counts = {
#    'Male': np.array([73, 34, 61]),
#    'Female': np.array([73, 34, 58]),
#}
#width = 0.6  # the width of the bars: can also be len(x) sequence


#fig, ax = plt.subplots()
#bottom = np.zeros(3)

#for sex, sex_count in sex_counts.items():
#    p = ax.bar(species, sex_count, width, label=sex, bottom=bottom)
#    bottom += sex_count

#    ax.bar_label(p, label_type='center')

#ax.set_title('Number of penguins by sex')
#ax.legend()

#plt.show()
################################################## Random Graphs
# Fixing random state for reproducibility
#np.random.seed(19680801)

# Example data
#people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
#y_pos = np.arange(len(people))
#performance = 3 + 10 * np.random.rand(len(people))
#error = np.random.rand(len(people))

#fig, ax = plt.subplots()

#hbars = ax.barh(y_pos, performance, xerr=error, align='center')
#ax.set_yticks(y_pos, labels=people)
#ax.invert_yaxis()  # labels read top-to-bottom
#ax.set_xlabel('Performance')
#ax.set_title('How fast do you want to go today?')

# Label with specially formatted floats
#ax.bar_label(hbars, fmt='%.2f')
#ax.set_xlim(right=15)  # adjust xlim to fit labels

#plt.show()
####################################################### Broken Bar Charts
#import matplotlib.pyplot as plt

# Horizontal bar plot with gaps
#fig, ax = plt.subplots()
#ax.broken_barh([(110, 30), (150, 10)], (10, 9), facecolors='tab:blue')
#ax.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
#               facecolors=('tab:orange', 'tab:green', 'tab:red'))
#ax.set_ylim(5, 35)
#ax.set_xlim(0, 200)
#ax.set_xlabel('seconds since start')
#ax.set_yticks([15, 25], labels=['Bill', 'Jim'])     # Modify y-axis tick labels
#ax.grid(True)                                       # Make grid lines visible
#ax.annotate('race interrupted', (61, 25),
#            xytext=(0.8, 0.9), textcoords='axes fraction',
#            arrowprops=dict(facecolor='black', shrink=0.05),
#            fontsize=16,
#            horizontalalignment='right', verticalalignment='top')
#
#plt.show()
#####################################################  Cap Style Graphs

#import matplotlib.pyplot as plt

#from matplotlib._enums import CapStyle

#CapStyle.demo()
#plt.show()
##################################################### Categorical Plotting Graphs
import matplotlib.pyplot as plt

data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Categorical Plotting')
plt.show()

######################################################### 3D PLOTTING GRAPHS 
import matplotlib.pyplot as plt
import numpy as np

# set up the figure and axes
fig = plt.figure(figsize=(8, 3))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

# fake data
_x = np.arange(4)
_y = np.arange(5)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()

top = x + y
bottom = np.zeros_like(top)
width = depth = 1

ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
ax1.set_title('Shaded')

ax2.bar3d(x, y, bottom, width, depth, top, shade=False)
ax2.set_title('Not Shaded')

plt.show()
#############################################################3D wireframe plot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()

##############################################################3D voxel plot of the NumPy logo
import matplotlib.pyplot as plt
import numpy as np


def explode(data):
   size = np.array(data.shape)*2
   data_e = np.zeros(size - 1, dtype=data.dtype)
   data_e[::2, ::2, ::2] = data
   return data_e

# build up the numpy logo
n_voxels = np.zeros((4, 3, 4), dtype=bool)
n_voxels[0, 0, :] = True
n_voxels[-1, 0, :] = True
n_voxels[1, 0, 2] = True
n_voxels[2, 0, 1] = True
facecolors = np.where(n_voxels, '#FFD65DC0', '#7A88CCC0')
edgecolors = np.where(n_voxels, '#BFAB6E', '#7D84A6')
filled = np.ones(n_voxels.shape)

# upscale the above voxel image, leaving gaps
filled_2 = explode(filled)
fcolors_2 = explode(facecolors)
ecolors_2 = explode(edgecolors)

# Shrink the gaps
x, y, z = np.indices(np.array(filled_2.shape) + 1).astype(float) // 2
x[0::2, :, :] += 0.05
y[:, 0::2, :] += 0.05
z[:, :, 0::2] += 0.05
x[1::2, :, :] += 0.95
y[:, 1::2, :] += 0.95
z[:, :, 1::2] += 0.95

ax = plt.figure().add_subplot(projection='3d')
ax.voxels(x, y, z, filled_2, facecolors=fcolors_2, edgecolors=ecolors_2)
ax.set_aspect('equal')

plt.show()
#####################################################################3D voxel / volumetric plot with cylindrical coordinates
#import matplotlib.pyplot as plt
#import numpy as np

#import matplotlib.colors


#def midpoints(x):
#    sl = ()
 #   for i in range(x.ndim):
#        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
#        sl += np.index_exp[:]
#    return x

# prepare some coordinates, and attach rgb values to each
#r, theta, z = np.mgrid[0:1:11j, 0:np.pi*2:25j, -0.5:0.5:11j]
#x = r*np.cos(theta)
#y = r*np.sin(theta)

#rc, thetac, zc = midpoints(r), midpoints(theta), midpoints(z)

# define a wobbly torus about [0.7, *, 0]
#sphere = (rc - 0.7)**2 + (zc + 0.2*np.cos(thetac*2))**2 < 0.2**2

# combine the color components
#hsv = np.zeros(sphere.shape + (3,))
#hsv[..., 0] = thetac / (np.pi*2)
#hsv[..., 1] = rc
#hsv[..., 2] = zc + 0.5
#colors = matplotlib.colors.hsv_to_rgb(hsv)

# and plot everything
#ax = plt.figure().add_subplot(projection='3d')
#ax.voxels(x, y, z, sphere,
#          facecolors=colors,
#          edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
#          linewidth=0.5)

#plt.show()
################################################################ Logit Demo Graphs

#import math

#import matplotlib.pyplot as plt
#import numpy as np

#xmax = 10
#x = np.linspace(-xmax, xmax, 10000)
#cdf_norm = [math.erf(w / np.sqrt(2)) / 2 + 1 / 2 for w in x]
#cdf_laplacian = np.where(x < 0, 1 / 2 * np.exp(x), 1 - 1 / 2 * np.exp(-x))
#cdf_cauchy = np.arctan(x) / np.pi + 1 / 2

#fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(6.4, 8.5))

# Common part, for the example, we will do the same plots on all graphs
#for i in range(3):
#    for j in range(2):
#        axs[i, j].plot(x, cdf_norm, label=r"$\mathcal{N}$")
#        axs[i, j].plot(x, cdf_laplacian, label=r"$\mathcal{L}$")
#        axs[i, j].plot(x, cdf_cauchy, label="Cauchy")
#        axs[i, j].legend()
#        axs[i, j].grid()

# First line, logitscale, with standard notation
#axs[0, 0].set(title="logit scale")
#axs[0, 0].set_yscale("logit")
#axs[0, 0].set_ylim(1e-5, 1 - 1e-5)

#axs[0, 1].set(title="logit scale")
#axs[0, 1].set_yscale("logit")
#axs[0, 1].set_xlim(0, xmax)
#axs[0, 1].set_ylim(0.8, 1 - 5e-3)

# Second line, logitscale, with survival notation (with `use_overline`), and
# other format display 1/2
#axs[1, 0].set(title="logit scale")
#axs[1, 0].set_yscale("logit", one_half="1/2", use_overline=True)
#axs[1, 0].set_ylim(1e-5, 1 - 1e-5)

#axs[1, 1].set(title="logit scale")
#axs[1, 1].set_yscale("logit", one_half="1/2", use_overline=True)
#axs[1, 1].set_xlim(0, xmax)
#axs[1, 1].set_ylim(0.8, 1 - 5e-3)

# Third line, linear scale
#axs[2, 0].set(title="linear scale")
#axs[2, 0].set_ylim(0, 1)

#axs[2, 1].set(title="linear scale")
#axs[2, 1].set_xlim(0, xmax)
#axs[2, 1].set_ylim(0.8, 1)

#fig.tight_layout()
#plt.show()
###################################################################### 3Mmh Donuts!!!
#import matplotlib.pyplot as plt
#import numpy as np

#import matplotlib.patches as mpatches
#import matplotlib.path as mpath


#def wise(v):
#    if v == 1:
#        return "CCW"
#    else:
#        return "CW"


#def make_circle(r):
#   t = np.arange(0, np.pi * 2.0, 0.01)
#    t = t.reshape((len(t), 1))
#    x = r * np.cos(t)
#    y = r * np.sin(t)
#    return np.hstack((x, y))

#Path = mpath.Path

#fig, ax = plt.subplots()

#inside_vertices = make_circle(0.5)
#outside_vertices = make_circle(1.0)
#codes = np.ones(
#    len(inside_vertices), dtype=mpath.Path.code_type) * mpath.Path.LINETO
#codes[0] = mpath.Path.MOVETO

#for i, (inside, outside) in enumerate(((1, 1), (1, -1), (-1, 1), (-1, -1))):
    # Concatenate the inside and outside subpaths together, changing their
    # order as needed
#   vertices = np.concatenate((outside_vertices[::outside],
#                               inside_vertices[::inside]))
    # Shift the path
#   vertices[:, 0] += i * 2.5
    # The codes will be all "LINETO" commands, except for "MOVETO"s at the
    # beginning of each subpath
#    all_codes = np.concatenate((codes, codes))
    # Create the Path object
#    path = mpath.Path(vertices, all_codes)
    # Add plot it
#   patch = mpatches.PathPatch(path, facecolor='#885500', edgecolor='black')
#    ax.add_patch(patch)

#    ax.annotate(f"Outside {wise(outside)},\nInside {wise(inside)}",
#                (i * 2.5, -1.5), va="top", ha="center")

#ax.set_xlim(-2, 10)
#ax.set_ylim(-3, 2)
#ax.set_title('Mmm, donuts!')
#ax.set_aspect(1.0)
#plt.show()


###################################################################### Animated histogram
#import matplotlib.pyplot as plt
#import numpy as np

#import matplotlib.animation as animation

# Fixing random state for reproducibility
#np.random.seed(19680801)
# Fixing bin edges
#HIST_BINS = np.linspace(-4, 4, 100)

# histogram our data with numpy
#data = np.random.randn(1000)
#n, _ = np.histogram(data, HIST_BINS)

#def prepare_animation(bar_container):

#     def animate(frame_number):
        # simulate new data coming in
#        data = np.random.randn(1000)
#        n, _ = np.histogram(data, HIST_BINS)
#        for count, rect in zip(n, bar_container.patches):
#            rect.set_height(count)
#       return bar_container.patches
#    return animate


# Output generated via `matplotlib.animation.Animation.to_jshtml`.

#fig, ax = plt.subplots()
#_, _, bar_container = ax.hist(data, HIST_BINS, lw=1,
#                              ec="yellow", fc="green", alpha=0.5)
#ax.set_ylim(top=55)  # set safe limit to ensure that all data is visible.

#ani = animation.FuncAnimation(fig, prepare_animation(bar_container), 50,
#                              repeat=False, blit=True)
#plt.show()
######################################################################## Geographic Projections
import matplotlib.pyplot as plt

plt.figure()
plt.subplot(projection="aitoff")
plt.title("Aitoff")
plt.grid(True)
plt.show()

plt.figure()
plt.subplot(projection="hammer")
plt.title("Hammer")
plt.grid(True)
plt.show()

plt.figure()
plt.subplot(projection="lambert")
plt.title("Lambert")
plt.grid(True)
plt.show()

plt.figure()
plt.subplot(projection="mollweide")
plt.title("Mollweide")
plt.grid(True)

plt.show()
##################################################################### BboxImage Demo
#import matplotlib.pyplot as plt
#import numpy as np

#from matplotlib.image import BboxImage
#from matplotlib.transforms import Bbox, TransformedBbox

#fig, (ax1, ax2) = plt.subplots(ncols=2)

# ----------------------------
# Create a BboxImage with Text
# ----------------------------
#txt = ax1.text(0.5, 0.5, "test", size=30, ha="center", color="w")
#ax1.add_artist(
#    BboxImage(txt.get_window_extent, data=np.arange(256).reshape((1, -1))))

# ------------------------------------
# Create a BboxImage for each colormap
# ------------------------------------
# List of all colormaps; skip reversed colormaps.
#cmap_names = sorted(m for m in plt.colormaps if not m.endswith("_r"))

#ncol = 2
#nrow = len(cmap_names) // ncol + 1

#xpad_fraction = 0.3
#dx = 1 / (ncol + xpad_fraction * (ncol - 1))

#ypad_fraction = 0.3
#dy = 1 / (nrow + ypad_fraction * (nrow - 1))

#for i, cmap_name in enumerate(cmap_names):
 #   ix, iy = divmod(i, nrow)
#    bbox0 = Bbox.from_bounds(ix*dx*(1+xpad_fraction),
#                             1 - iy*dy*(1+ypad_fraction) - dy,
#                             dx, dy)
#    bbox = TransformedBbox(bbox0, ax2.transAxes)
#    ax2.add_artist(
#        BboxImage(bbox, cmap=cmap_name, data=np.arange(256).reshape((1, -1))))

#plt.show()
####################################################################### Bar Code
#import matplotlib.pyplot as plt
#import numpy as np

#code = np.array([
#    1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1,
#    0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0,
#    1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1,
#    1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1])

#pixel_per_bar = 4
#dpi = 100

#fig = plt.figure(figsize=(len(code) * pixel_per_bar / dpi, 2), dpi=dpi)
#ax = fig.add_axes([0, 0, 1, 1])  # span the whole figure
#ax.set_axis_off()
#ax.imshow(code.reshape(1, -1), cmap='binary', aspect='auto',
#          interpolation='nearest')
#plt.show()

########################################################## Contourf Hatching
#import matplotlib.pyplot as plt
#import numpy as np

# invent some numbers, turning the x and y arrays into simple
# 2d arrays, which make combining them together easier.
#x = np.linspace(-3, 5, 150).reshape(1, -1)
#y = np.linspace(-3, 5, 120).reshape(-1, 1)
#z = np.cos(x) + np.sin(y)

# we no longer need x and y to be 2 dimensional, so flatten them.
#x, y = x.flatten(), y.flatten()
#fig1, ax1 = plt.subplots()
#cs = ax1.contourf(x, y, z, hatches=['-', '/', '\\', '//'],
#                  cmap='gray', extend='both', alpha=0.5)
#fig1.colorbar(cs)
#plt.show()

############################################################# Creating a timeline with lines, dates, and text
#from datetime import datetime

#import matplotlib.pyplot as plt
#import numpy as np

#import matplotlib.dates as mdates

#try:
    ## Try to fetch a list of Matplotlib releases and their dates
    ## from https://api.github.com/repos/matplotlib/matplotlib/releases

#    import json
#    import urllib.request

#    url = 'https://api.github.com/repos/matplotlib/matplotlib/releases'
#   url += '?per_page=100'
#    data = json.loads(urllib.request.urlopen(url, timeout=1).read().decode())

#    dates = []
#    names = []
#    for item in data:
#        if 'rc' not in item['tag_name'] and 'b' not in item['tag_name']:
#            dates.append(item['published_at'].split("T")[0])
#            names.append(item['tag_name'])
#    # Convert date strings (e.g. 2014-10-18) to datetime
#   dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

#except Exception:
    # In case the above fails, e.g. because of missing internet connection
    # use the following lists as fallback.
    # 
    #names = ['v2.2.4', 'v3.0.3', 'v3.0.2', 'v3.0.1', 'v3.0.0', 'v2.2.3',
#             'v2.2.2', 'v2.2.1', 'v2.2.0', 'v2.1.2', 'v2.1.1', 'v2.1.0',
#             'v2.0.2', 'v2.0.1', 'v2.0.0', 'v1.5.3', 'v1.5.2', 'v1.5.1',
#             'v1.5.0', 'v1.4.3', 'v1.4.2', 'v1.4.1', 'v1.4.0']

#    dates = ['2019-02-26', '2019-02-26', '2018-11-10', '2018-11-10',
#             '2018-09-18', '2018-08-10', '2018-03-17', '2018-03-16',
#             '2018-03-06', '2018-01-18', '2017-12-10', '2017-10-07',
#             '2017-05-10', '2017-05-02', '2017-01-17', '2016-09-09',
#             '2016-07-03', '2016-01-10', '2015-10-29', '2015-02-16',
#             '2014-10-26', '2014-10-18', '2014-08-26']

    # Convert date strings (e.g. 2014-10-18) to datetime
#    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]


    # Choose some nice levels
#levels = np.tile([-5, 5, -3, 3, -1, 1],
#                 int(np.ceil(len(dates)/6)))[:len(dates)]

# Create figure and plot a stem plot with the date
#fig, ax = plt.subplots(figsize=(8.8, 4), layout="constrained")
#ax.set(title="Matplotlib release dates")

#ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
#ax.plot(dates, np.zeros_like(dates), "-o",
#        color="k", markerfacecolor="w")  # Baseline and markers on it.

# annotate lines
#for d, l, r in zip(dates, levels, names):
#    ax.annotate(r, xy=(d, l),
#                xytext=(-3, np.sign(l)*3), textcoords="offset points",
#                horizontalalignment="right",
#                verticalalignment="bottom" if l > 0 else "top")

# format x-axis with 4-month intervals
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
#plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y-axis and spines
#ax.yaxis.set_visible(False)
#ax.spines[["left", "top", "right"]].set_visible(False)

#ax.margins(y=0.1)
#plt.show()
#############################################################Colormap normalizations SymLogNorm
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors


def rbf(x, y):
    return 1.0 / (1 + 5 * ((x ** 2) + (y ** 2)))

N = 200
gain = 8
X, Y = np.mgrid[-3:3:complex(0, N), -2:2:complex(0, N)]
Z1 = rbf(X + 0.5, Y + 0.5)
Z2 = rbf(X - 0.5, Y - 0.5)
Z = gain * Z1 - Z2

shadeopts = {'cmap': 'PRGn', 'shading': 'gouraud'}
colormap = 'PRGn'
lnrwidth = 0.5

fig, ax = plt.subplots(2, 1, sharex=True, sharey=True)

pcm = ax[0].pcolormesh(X, Y, Z,
                       norm=colors.SymLogNorm(linthresh=lnrwidth, linscale=1,
                                              vmin=-gain, vmax=gain, base=10),
                       **shadeopts)
fig.colorbar(pcm, ax=ax[0], extend='both')
ax[0].text(-2.5, 1.5, 'symlog')

pcm = ax[1].pcolormesh(X, Y, Z, vmin=-gain, vmax=gain,
                       **shadeopts)
fig.colorbar(pcm, ax=ax[1], extend='both')
ax[1].text(-2.5, 1.5, 'linear')
plt.show()
################################################################## Hexagonal binned plot
#import matplotlib.pyplot as plt
#import numpy as np

# Fixing random state for reproducibility
#np.random.seed(19680801)

#n = 100_000
#x = np.random.standard_normal(n)
#y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
#xlim = x.min(), x.max()
#ylim = y.min(), y.max()

#fig, (ax0, ax1) = plt.subplots(ncols=2, sharey=True, figsize=(9, 4))

#hb = ax0.hexbin(x, y, gridsize=50, cmap='inferno')
#ax0.set(xlim=xlim, ylim=ylim)
#ax0.set_title("Hexagon binning")
#cb = fig.colorbar(hb, ax=ax0, label='counts')

#hb = ax1.hexbin(x, y, gridsize=50, bins='log', cmap='inferno')
#ax1.set(xlim=xlim, ylim=ylim)
#ax1.set_title("With a log color scale")
#cb = fig.colorbar(hb, ax=ax1, label='log10(N)')

#plt.show()
######################################################### Hexagonal binned plot
#import matplotlib.pyplot as plt
#import numpy as np

# Fixing random state for reproducibility
#np.random.seed(19680801)

#n = 100_000
#x = np.random.standard_normal(n)
#y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
#xlim = x.min(), x.max()
#ylim = y.min(), y.max()

#fig, (ax0, ax1) = plt.subplots(ncols=2, sharey=True, figsize=(9, 4))

#hb = ax0.hexbin(x, y, gridsize=50, cmap='inferno')
#ax0.set(xlim=xlim, ylim=ylim)
#ax0.set_title("Hexagon binning")
#cb = fig.colorbar(hb, ax=ax0, label='counts')

#hb = ax1.hexbin(x, y, gridsize=50, bins='log', cmap='inferno')
#ax1.set(xlim=xlim, ylim=ylim)
#ax1.set_title("With a log color scale")
#cb = fig.colorbar(hb, ax=ax1, label='log10(N)')

#plt.show()
##########################################################################
