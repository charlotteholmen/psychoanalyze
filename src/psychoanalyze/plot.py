import pandas as pd
import xarray as xr
from plotly import graph_objects as go


def all(trials: pd.DataFrame | xr.Dataset) -> dict[str, go.Figure]:
    if isinstance(trials, xr.Dataset):
        trials = trials.to_dataframe().reset_index()
    return {
        "Psychometric function": go.Figure(),
        "Threshold vs Time": go.Figure(),
        "Strength-duration": go.Figure(),
        "Weber curves": go.Figure(),
    }
