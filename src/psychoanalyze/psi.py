import pandas as pd
import plotly.express as px
from plotly import graph_objects as go


def plot() -> go.Figure:
    return px.scatter(
        pd.DataFrame({"percent_correct": []}),
        y="percent_correct",
    )
