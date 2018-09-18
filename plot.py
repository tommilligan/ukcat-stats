import bokeh.plotting as bk
from bokeh.models import Span
from bokeh.io import export_png
import numpy as np
from scipy.interpolate import CubicSpline

SCORE = 3000

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

# ukcat deciles
x = np.linspace(0.1, 0.9, 9)
# code scores
y = [
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

# Create plot
p = bk.figure(x_range=(0, 1), y_range=(2000, 3200), title="UKCAT Interim Results 2018")

# plot initial data points
p.circle(x, y, color='grey')

# Generate x points for a smooth curve
xvals=np.linspace(0, 1, 100)

# bezier curve to fit points exactly
spl = CubicSpline(x, y) # First generate spline function
y_smooth = spl(xvals) # then evalute for your interpolated points
p.line(xvals, y_smooth, color='grey')


# Nadia!
# Calculate lines
hline = Span(location=SCORE, dimension='width', line_color='red', line_width=1)
percentile = xvals[find_nearest(y_smooth, SCORE)]
vline = Span(location=percentile, dimension='height', line_color='red', line_width=1, line_dash='dashed')
p.renderers.extend([hline, vline])
# Add text
p.text([0], [SCORE], [" Nadia"], text_baseline="bottom", text_align="left")
p.text([percentile], [2000], ["~{0:.2f}% ".format(percentile)], text_baseline="bottom", text_align="right")


export_png(p)

