import bokeh.plotting as bk
from bokeh.models import Span
from bokeh.io import export_png, show, output_notebook
import numpy as np
from scipy.interpolate import CubicSpline

SCORE = 3000
X_RANGE = (2000, 3200)

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            # Jupyter notebook or qtconsole
            return True   
    except NameError:
        pass
    # standard python, ipython, etc.
    return False

def map_average(iterable):
    l = list(iterable)
    for i, x in enumerate(iterable):
        try:
            yield (x + l[i + 1]) / 2
        except IndexError:
            return StopIteration

# code scores
x = [
    2220,
    2340,
    2420,
    2490,
    2550,
    2610,
    2680,
    2760,
    2870
]
# ukcat deciles
y = np.linspace(0.1, 0.9, 9)


print(hist)

# Create plot
p = bk.figure(x_range=X_RANGE, y_range=(0, 1), title="UKCAT Interim Results 2018")

# plot initial data points
p.circle(x, y, color='grey')

# Generate x points for a smooth curve
xvals=np.linspace(min(x), max(x), 100)

# bezier curve to fit points exactly
spl = CubicSpline(x, y) # First generate spline function
y_smooth = spl(xvals) # then evalute for your interpolated points
p.line(xvals, y_smooth, color='grey')

# gauss histogram
hist_areas = [0.1] * 8
edges = x
hist = np.array(list([area/(edges[i + 1] - edges[i]) for i, area in enumerate(hist_areas)]))
p.quad(top=(hist * 100), bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="lightgrey", line_color="grey")

# fit curve to s curve formula

# Score!
# Calculate lines
vline = Span(location=SCORE, dimension='height', line_color='red', line_width=1)
p.renderers.extend([vline])
# Add text
p.text([SCORE], [0], ["Score "], text_baseline="bottom", text_align="right")

if isnotebook():
    output_notebook()
    show(p)
else:
    export_png(p)
