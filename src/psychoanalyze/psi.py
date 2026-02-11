import pandas as pd
import plotly.express as px
from plotly import graph_objects as go


def plot(points: pd.DataFrame) -> go.Figure:
    return px.scatter(
        points,
        x="magnitude",
        y="percent_correct",
    )
