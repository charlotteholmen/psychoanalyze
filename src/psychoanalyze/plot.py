import pandas as pd
from plotly import graph_objects as go


def all(trials: pd.DataFrame) -> dict[str, go.Figure]:
    return {
        "Psychometric function": go.Figure(),
        "Threshold vs Time": go.Figure(),
        "Strength-duration": go.Figure(),
        "Weber curves": go.Figure(),
    }
