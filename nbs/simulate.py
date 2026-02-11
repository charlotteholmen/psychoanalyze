"""PsychoAnalyze dashboard as a marimo notebook.

Interactive data simulation & analysis for psychophysics.
Replaces the former Dash dashboard (removed).
"""

import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full", app_title="PsychoAnalyze")


@app.cell
def _():
    import psychoanalyze as ps
    import pandas as pd

    return pd, ps


@app.cell
def _(pd, ps):
    ps.psi.plot(points=pd.DataFrame({
        "magnitude": [0.1, 0.2, 0.3],
        "hit_rate": [0.1, 0.5, 0.7],
        "n_trials": [100, 100, 100]
    }))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
