# ukcat-stats

Quick statistical anaysis of UKCAT scores to directly convert scores to percentiles.

Scores were plotted against deciles and fitted to a Sigmoid curve.

## Use

The `plot.py` script generates a static image when run locally.

It generates an interactive bokeh plot when run in a Jupyter notebook.

```
# You will need PhantomJS avaiable globally for static bokeh output
yarn global add phantomjs-prebuilt

pip install -r requirements.txt
python plot.py
```

