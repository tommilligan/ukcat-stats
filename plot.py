import bokeh.plotting as bk
from bokeh.models import Span
from bokeh.io import export_png, show, output_notebook
import numpy as np
from scipy.optimize import curve_fit

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
        
def sigmoid(x, x0, k):
     y = 1 / (1 + np.exp(-k*(x-x0)))
     return y

# Input data - UKCAT scores vs deciles
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
y = np.linspace(0.1, 0.9, 9)

# fit curve to sigmoid curve formula
popt, pcov = curve_fit(sigmoid, x, y, method="dogbox", bounds=((2000, 0.0001), (3000, 0.1)))

# Create plot
p = bk.figure(x_range=X_RANGE, y_range=(0, 1), title="UKCAT Interim Results 2018")

# plot sigmoid
x_sigmoid = np.linspace(0, 4000, 1000)
y_sigmoid = sigmoid(x_sigmoid, *popt)
p.line(x_sigmoid, y_sigmoid, color='purple', legend="Sigmoid x0={:.0f} k={:.4f}".format(*popt))

# plot initial data points
p.circle(x, y, color='grey', legend="Deciles")

# Score!
# Calculate lines
vline = Span(location=SCORE, dimension='height', line_color='red', line_width=1)
percentile = sigmoid(SCORE, *popt)
hline = Span(location=percentile, dimension='width', line_color='red', line_width=1, line_dash='dashed')
p.renderers.extend([vline, hline])
# Add text
p.text([SCORE], [0], [""], text_baseline="bottom", text_align="right")
p.text([X_RANGE[0]], [percentile], [" ~{0:.3f}%".format(percentile)], text_baseline="top", text_align="left")

# legend styling
p.legend.location = "center_left"
p.legend.background_fill_color = "white"
p.legend.background_fill_alpha = 0.7
p.legend.border_line_color = 'grey'

if isnotebook():
    output_notebook()
    show(p)
else:
    export_png(p)
