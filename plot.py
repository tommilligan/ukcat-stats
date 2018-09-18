import logging

import bokeh.plotting as bk
from bokeh.models import Span
from bokeh.io import export_png, show, output_notebook
import numpy as np
from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.handlers = [ch]

SCORE = 3000
X_RANGE = (2000, 3200)


def is_notebook():
    """Return True is we are probably in a Jupyter notebook"""
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            # Jupyter notebook or qtconsole
            return True
    except NameError:
        pass
    # standard python, ipython, etc.
    return False


def sigmoid(x, x0, k):
    """General sigmoid curve equation for fitting"""
    y = 1 / (1 + np.exp(-k * (x - x0)))
    return y


# Input data - UKCAT scores vs deciles
# https://www.ukcat.ac.uk/ukcat-test/ukcat-results/test-statistics/
logger.info("Loading data")
x = [2220, 2340, 2420, 2490, 2550, 2610, 2680, 2760, 2870]
y = np.linspace(0.1, 0.9, 9)

# fit curve to sigmoid curve formula
logger.info("Fitting curves")
popt, pcov = curve_fit(sigmoid, x, y, bounds=((2000, 0.0001), (3000, 0.1)))


def sigmoid_fitted(x):
    return sigmoid(x, *popt)


# Create plot
logger.info("Creating plot")
p = bk.figure(x_range=X_RANGE, y_range=(0, 1), title="UKCAT Interim Results 2018")

# plot sigmoid
x_sigmoid = np.linspace(0, 4000, 1000)
y_sigmoid = sigmoid_fitted(x_sigmoid)
p.line(
    x_sigmoid,
    y_sigmoid,
    color="purple",
    legend="Sigmoid x0={:.0f} k={:.4f}".format(*popt),
)

# plot initial data points
p.circle(x, y, color="grey", legend="Deciles")

# Score!
# Calculate lines
vline = Span(location=SCORE, dimension="height", line_color="red", line_width=1)
percentile = sigmoid_fitted(SCORE)
hline = Span(
    location=percentile,
    dimension="width",
    line_color="red",
    line_width=1,
    line_dash="dashed",
)
p.renderers.extend([vline, hline])
# Add text
p.text([SCORE], [0], [""], text_baseline="bottom", text_align="right")
p.text(
    [X_RANGE[0]],
    [percentile],
    [" ~{0:.3f}%".format(percentile)],
    text_baseline="top",
    text_align="left",
)

# legend styling
p.legend.location = "center_left"
p.legend.background_fill_color = "white"
p.legend.background_fill_alpha = 0.7
p.legend.border_line_color = "grey"

# Run plot generation
logger.info("Generating output")
if is_notebook():
    output_notebook()
    show(p)
else:
    export_png(p)
