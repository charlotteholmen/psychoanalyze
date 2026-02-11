import plotly.express as px
import xarray as xr
from plotly import graph_objects as go


def plot(points: xr.Dataset) -> go.Figure:
    return px.scatter(
        points.to_dataframe(),
        x="magnitude",
        y="hit_rate",
    )
