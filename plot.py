import datetime
import logging

import bokeh.plotting as bk
from bokeh.models import Span
from bokeh.io import export_png, show, output_notebook
import numpy as np
from scipy.optimize import curve_fit
import structlog

# Logging with structlog
def timestamper(_, __, event_dict):
    event_dict["time"] = datetime.datetime.now().isoformat()
    return event_dict


structlog.configure(processors=[timestamper, structlog.processors.JSONRenderer()])
logger = structlog.get_logger(__name__)


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
logger.info("Loading data")
datasets = {
    "2018_interim": {
        "color": "lightgreen",
        "data": [2220, 2340, 2420, 2490, 2550, 2610, 2680, 2760, 2870],
        "description": "2018 Interim",
        "offset": 160,
    },
    "2017_final": {
        "color": "blue",
        "data": [2230, 2340, 2420, 2480, 2540, 2600, 2670, 2750, 2860],
        "description": "2017 Final",
        "offset": 0,
    },
    "2017_interim": {
        "color": "lightblue",
        "data": [2280, 2400, 2480, 2540, 2600, 2660, 2730, 2800, 2920],
        "description": "2017 Interim",
        "offset": 0,
    },
}
y = np.linspace(0.1, 0.9, 9)

# Create plot
logger.info("Creating plot")
p = bk.figure(x_range=X_RANGE, y_range=(0, 1), title="UKCAT Interim Results 2018")

# Score!
# Calculate lines
vline = Span(location=SCORE, dimension="height", line_color="red", line_width=1)
p.renderers.append(vline)


def plot_sigmoid(x):
    logger.info("Plotting series")

    # plot sigmoid
    x_sigmoid = np.linspace(0, 4000, 1000)
    f = lambda a: sigmoid(a, *x["sigmoid_popt"])
    y_sigmoid = f(x_sigmoid)
    p.line(
        x_sigmoid,
        y_sigmoid,
        color=x["color"],
        legend="Sigmoid x0={:.0f} k={:.4f}".format(*x["sigmoid_popt"]),
    )

    percentile = f(SCORE)
    hline = Span(
        location=percentile,
        dimension="width",
        line_color=x["color"],
        line_width=1,
        line_dash="dashed",
    )
    p.renderers.append(hline)

    # Add text
    p.text(
        [X_RANGE[0] + x["offset"]],
        [percentile],
        [" ~{0:.3f}%".format(percentile)],
        text_baseline="top",
        text_align="left",
        text_font_size="10px",
    )


for x in datasets.values():
    # fit curve to sigmoid curve formula
    logger.info("Fitting curves")
    popt, pcov = curve_fit(sigmoid, x["data"], y, bounds=((2000, 0.0001), (3000, 0.1)))
    x["sigmoid_popt"] = popt

    plot_sigmoid(x)

    # plot initial data points
    p.circle(x["data"], y, color=x["color"], legend=x["description"])


# Calculate this year's final results based on the interim
x0_diff = (
    datasets["2017_final"]["sigmoid_popt"][0]
    - datasets["2017_interim"]["sigmoid_popt"][0]
)
popt = list(datasets["2018_interim"]["sigmoid_popt"])
popt[0] = popt[0] + x0_diff
dataset = {
    "sigmoid_popt": popt,
    "color": "green",
    "offset": 160,
    "description": "2018 Final (predicted)",
}
plot_sigmoid(dataset)


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


logger.info("Complete")
