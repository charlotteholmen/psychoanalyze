"""PsychoAnalyze dashboard as a marimo notebook.

Interactive data simulation & analysis for psychophysics.
Replaces the former Dash dashboard (removed).
"""

import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full", app_title="PsychoAnalyze")


@app.cell
def _():
    import plotly.express as px

    return (px,)


@app.cell
def _(px):
    px.scatter(y="percent_correct")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
