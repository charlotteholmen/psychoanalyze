import plotly.express as px
import xarray as xr
from plotly import graph_objects as go


def plot(dataset: xr.Dataset) -> go.Figure:
    return px.scatter(
        dataset.to_dataframe(),
        x="magnitude",
        y="hit_rate",
    )
